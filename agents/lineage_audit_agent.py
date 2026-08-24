import subprocess
import json
import uuid

class LineageAuditAgent:
    """
    Decision Lineage & Audit Specialist Agent:
    Captures operational spans into BigQuery Context Graph (DecisionTraceGraph)
    and executes regulator-grade ISO GQL queries for complete explainability.
    """
    def __init__(self, project_id="nandemo-377912", dataset_id="yahoo_context_graph"):
        self.project_id = project_id
        self.dataset_id = dataset_id

    def commit_decision_trace(self, brief, decision, candidates_with_evals):
        """
        Commits Brief, Decision, Candidates, Evaluated Policies, and Edges to BigQuery Graph.
        """
        statements = []

        # 1. Brief Node
        statements.append(f"""
        INSERT INTO `{self.project_id}.{self.dataset_id}.CampaignBriefs`
        VALUES ('{brief["BriefId"]}', '{brief["AdvertiserId"]}', '{brief["TargetDescription"]}', 
                {brief["BudgetUSD"]}, '{brief["RequiredCompliance"]}', TIMESTAMP('{brief["SubmittedAt"]}'));
        """)

        # 2. Decision Node
        statements.append(f"""
        INSERT INTO `{self.project_id}.{self.dataset_id}.AgentDecisions`
        VALUES ('{decision["DecisionId"]}', '{brief["BriefId"]}', '{decision["PackageId"]}', 
                '{decision["Rationale"]}', '{decision["AgentName"]}', TIMESTAMP('{decision["Timestamp"]}'));
        """)

        # 3. Candidate Nodes, Policy Evaluations, and Edges
        edge_b2d = f"E-{uuid.uuid4().hex[:6]}"
        statements.append(f"INSERT INTO `{self.project_id}.{self.dataset_id}.BriefToDecisions` VALUES ('{edge_b2d}', '{brief['BriefId']}', '{decision['DecisionId']}');")

        for item in candidates_with_evals:
            cand = item["candidate"]
            evals = item["evaluations"]
            status = item["status"]
            cand_id = f"CAND-{uuid.uuid4().hex[:4].upper()}"

            statements.append(f"""
            INSERT INTO `{self.project_id}.{self.dataset_id}.CandidatePackages`
            VALUES ('{cand_id}', '{decision["DecisionId"]}', '{cand["ProductId"]}', '{cand["ProductName"]}', 
                    '{cand["AudienceId"]}', '{cand["AudienceName"]}', {cand["PredictedCPM"]}, 
                    {cand["AllocatedBudget"]}, {cand["EstimatedImpressions"]}, '{status}');
            """)

            edge_d2c = f"E-{uuid.uuid4().hex[:6]}"
            statements.append(f"INSERT INTO `{self.project_id}.{self.dataset_id}.DecisionToCandidates` VALUES ('{edge_d2c}', '{decision['DecisionId']}', '{cand_id}');")

            for ev in evals:
                ev_id = f"EV-{uuid.uuid4().hex[:4].upper()}"
                statements.append(f"""
                INSERT INTO `{self.project_id}.{self.dataset_id}.EvaluatedPolicies`
                VALUES ('{ev_id}', '{cand_id}', '{ev["PolicyId"]}', '{ev["PolicyName"]}', 
                        '{ev["EnforcementLevel"]}', '{ev["ComplianceStatus"]}', '{ev["AuditEvidence"]}');
                """)
                edge_c2e = f"E-{uuid.uuid4().hex[:6]}"
                statements.append(f"INSERT INTO `{self.project_id}.{self.dataset_id}.CandidateToEvaluations` VALUES ('{edge_c2e}', '{cand_id}', '{ev_id}');")

        full_dml = "\n".join(statements)
        cmd = [
            "bq", "query", "--use_legacy_sql=false",
            f"--project_id={self.project_id}",
            "--location=US",
            "--format=prettyjson",
            full_dml
        ]
        res = subprocess.run(cmd, capture_output=True, text=True)
        if res.returncode != 0:
            raise RuntimeError(f"LineageAuditAgent error writing to BigQuery Graph: {res.stderr}")

    def run_regulator_audit_query(self, brief_id):
        """
        Runs an ISO GQL graph traversal on BigQuery Context Graph to answer audit inquiries.
        """
        gql = f"""
        GRAPH `{self.project_id}.{self.dataset_id}.DecisionTraceGraph`
        MATCH (b:CampaignBriefs)-[:PRODUCED_DECISION]->(d:AgentDecisions)-[:EVALUATED_CANDIDATE]->(c:CandidatePackages)-[:GOVERNED_BY]->(p:EvaluatedPolicies)
        WHERE b.BriefId = '{brief_id}'
        RETURN
          b.BriefId AS BriefId,
          d.AgentName AS AgentName,
          c.ProductName AS ProductName,
          c.SelectionStatus AS Status,
          c.AllocatedBudget AS Budget,
          p.PolicyName AS Policy,
          p.ComplianceStatus AS Compliance,
          p.AuditEvidence AS AuditEvidence
        ORDER BY Status DESC, Budget DESC;
        """
        cmd = [
            "bq", "query", "--use_legacy_sql=false",
            f"--project_id={self.project_id}",
            "--location=US",
            "--format=prettyjson",
            gql
        ]
        res = subprocess.run(cmd, capture_output=True, text=True)
        if res.returncode != 0:
            raise RuntimeError(f"LineageAuditAgent error executing BigQuery GQL: {res.stderr}")
        
        return json.loads(res.stdout) if res.stdout.strip() else []
