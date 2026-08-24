import subprocess
import json

class InventoryDiscoveryAgent:
    """
    Inventory Discovery Specialist Agent:
    Traverses Cloud Spanner Knowledge Graph (AdMonetizationKnowledgeGraph)
    to discover active ad products, target audiences, and governing policies in real-time.
    """
    def __init__(self, project_id="nandemo-377912", instance_id="demo-spanner", database_id="spanner"):
        self.project_id = project_id
        self.instance_id = instance_id
        self.database_id = database_id

    def discover_matching_inventory(self, target_keywords=None):
        """
        Executes real-time ISO GQL graph traversal on Spanner Graph.
        """
        gql_query = """
        GRAPH AdMonetizationKnowledgeGraph
        MATCH (p:AdProducts)-[r:REACHES]->(a:Audiences)
        OPTIONAL MATCH (p)-[gp:GOVERNED_BY]->(pol:Policies)
        RETURN 
          p.ProductId AS ProductId,
          p.Name AS ProductName,
          p.FloorPriceCPM AS CPM,
          p.AvailableImpressions AS AvailableImpressions,
          a.AudienceId AS AudienceId,
          a.Name AS AudienceName,
          r.AffinityScore AS AffinityScore,
          pol.PolicyId AS PolicyId,
          pol.Name AS PolicyName,
          gp.EnforcementLevel AS EnforcementLevel
        """
        cmd = [
            "gcloud", "spanner", "databases", "execute-sql", self.database_id,
            f"--instance={self.instance_id}",
            f"--project={self.project_id}",
            f"--sql={gql_query}",
            "--format=json"
        ]
        res = subprocess.run(cmd, capture_output=True, text=True)
        if res.returncode != 0:
            raise RuntimeError(f"InventoryDiscoveryAgent error querying Spanner Graph: {res.stderr}")
        
        data = json.loads(res.stdout) if res.stdout.strip() else {}
        return data.get("rows", [])
