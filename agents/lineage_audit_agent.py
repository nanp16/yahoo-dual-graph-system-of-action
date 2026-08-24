from google.cloud import bigquery
import uuid

class LineageAuditAgent:
    """
    Decision Lineage & Audit Specialist Agent:
    Uses BigQuery Streaming Ingestion (insert_rows_json) for sub-second writes.
    """
    def __init__(self, project_id="nandemo-377912", dataset_id="yahoo_context_graph"):
        self.project_id = project_id
        self.dataset_id = dataset_id
        self.client = bigquery.Client(project=self.project_id)

    def commit_decision_trace(self, brief, decision, candidates_with_evals):
        """
        Fast Streaming Ingestion into BigQuery Graph tables (<150ms).
        """
        # 1. Brief Node
        brief_rows = [{
            "BriefId": brief["BriefId"],
            "AdvertiserId": brief["AdvertiserId"],
            "TargetAudienceDescription": brief["TargetDescription"],
            "BudgetUSD": float(brief["BudgetUSD"]),
            "RequiredCompliance": brief["RequiredCompliance"],
            "SubmittedAt": brief["SubmittedAt"]
        }]
        self.client.insert_rows_json(f"{self.project_id}.{self.dataset_id}.CampaignBriefs", brief_rows)

        # 2. Decision Node
        decision_rows = [{
            "DecisionId": decision["DecisionId"],
            "BriefId": brief["BriefId"],
            "SelectedPackageId": decision["PackageId"],
            "ExecutiveRationale": decision["Rationale"],
            "AgentName": decision["AgentName"],
            "DecisionTimestamp": decision["Timestamp"]
        }]
        self.client.insert_rows_json(f"{self.project_id}.{self.dataset_id}.AgentDecisions", decision_rows)

        # 3. Edge: Brief -> Decision
        edge_b2d = [{
            "EdgeId": f"E-{uuid.uuid4().hex[:6]}",
            "BriefId": brief["BriefId"],
            "DecisionId": decision["DecisionId"]
        }]
        self.client.insert_rows_json(f"{self.project_id}.{self.dataset_id}.BriefToDecisions", edge_b2d)

        # 4. Candidates, Evaluations, and Edges
        candidate_rows = []
        d2c_edges = []
        eval_rows = []
        c2e_edges = []

        for item in candidates_with_evals:
            cand = item["candidate"]
            evals = item["evaluations"]
            status = item["status"]
            cand_id = f"CAND-{uuid.uuid4().hex[:4].upper()}"

            candidate_rows.append({
                "CandidateId": cand_id,
                "DecisionId": decision["DecisionId"],
                "ProductId": cand["ProductId"],
                "ProductName": cand["ProductName"],
                "AudienceId": cand["AudienceId"],
                "AudienceName": cand["AudienceName"],
                "PredictedCPM": float(cand["PredictedCPM"]),
                "AllocatedBudget": float(cand["AllocatedBudget"]),
                "EstimatedImpressions": int(cand["EstimatedImpressions"]),
                "SelectionStatus": status
            })

            d2c_edges.append({
                "EdgeId": f"E-{uuid.uuid4().hex[:6]}",
                "DecisionId": decision["DecisionId"],
                "CandidateId": cand_id
            })

            for ev in evals:
                ev_id = f"EV-{uuid.uuid4().hex[:4].upper()}"
                eval_rows.append({
                    "EvaluationId": ev_id,
                    "CandidateId": cand_id,
                    "PolicyId": ev["PolicyId"],
                    "PolicyName": ev["PolicyName"],
                    "EnforcementLevel": ev["EnforcementLevel"],
                    "ComplianceStatus": ev["ComplianceStatus"],
                    "AuditEvidence": ev["AuditEvidence"]
                })

                c2e_edges.append({
                    "EdgeId": f"E-{uuid.uuid4().hex[:6]}",
                    "CandidateId": cand_id,
                    "EvaluationId": ev_id
                })

        self.client.insert_rows_json(f"{self.project_id}.{self.dataset_id}.CandidatePackages", candidate_rows)
        self.client.insert_rows_json(f"{self.project_id}.{self.dataset_id}.DecisionToCandidates", d2c_edges)
        self.client.insert_rows_json(f"{self.project_id}.{self.dataset_id}.EvaluatedPolicies", eval_rows)
        self.client.insert_rows_json(f"{self.project_id}.{self.dataset_id}.CandidateToEvaluations", c2e_edges)

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
