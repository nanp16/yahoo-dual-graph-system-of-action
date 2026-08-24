from google.cloud import bigquery
import uuid

class LineageAuditAgent:
    """
    Decision Lineage & Audit Specialist Agent:
    Uses native Google Cloud BigQuery SDK for high-performance Decision Trace Graph
    mutations and ISO GQL audit queries.
    """
    def __init__(self, project_id="nandemo-377912", dataset_id="yahoo_context_graph"):
        self.project_id = project_id
        self.dataset_id = dataset_id
        self.client = bigquery.Client(project=self.project_id)

    def commit_decision_trace(self, brief, decision, candidates_with_evals):
        """
        Commits Brief, Decision, Candidates, Evaluated Policies, and Edges to BigQuery Graph
        in a single optimized batch transaction.
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
        query_job = self.client.query(full_dml, location="US")
        query_job.result()  # Fast native wait

    def run_regulator_audit_query(self, brief_id):
        """
        Runs an ISO GQL graph traversal on BigQuery Context Graph via native client.
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
        query_job = self.client.query(gql, location="US")
        results = []
        for row in query_job.result():
            results.append({
                "BriefId": row["BriefId"],
                "AgentName": row["AgentName"],
                "ProductName": row["ProductName"],
                "Status": row["Status"],
                "Budget": str(row["Budget"]),
                "Policy": row["Policy"],
                "Compliance": row["Compliance"],
                "AuditEvidence": row["AuditEvidence"]
            })
        return results
