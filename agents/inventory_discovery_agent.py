from google.cloud import spanner

class InventoryDiscoveryAgent:
    """
    Inventory Discovery Specialist Agent:
    Uses native Google Cloud Spanner SDK with gRPC connection pooling
    to traverse Spanner Knowledge Graph in milliseconds.
    """
    def __init__(self, project_id="nandemo-377912", instance_id="demo-spanner", database_id="spanner"):
        self.project_id = project_id
        self.instance_id = instance_id
        self.database_id = database_id
        self.client = spanner.Client(project=self.project_id)
        self.instance = self.client.instance(self.instance_id)
        self.database = self.instance.database(self.database_id)

    def discover_matching_inventory(self, target_keywords=None):
        """
        Executes real-time ISO GQL graph traversal on Spanner Graph via native gRPC.
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
        with self.database.snapshot() as snapshot:
            results = snapshot.execute_sql(gql_query)
            rows = []
            for row in results:
                rows.append({
                    "ProductId": row[0],
                    "ProductName": row[1],
                    "CPM": row[2],
                    "AvailableImpressions": row[3],
                    "AudienceId": row[4],
                    "AudienceName": row[5],
                    "AffinityScore": row[6],
                    "PolicyId": row[7],
                    "PolicyName": row[8],
                    "EnforcementLevel": row[9]
                })
            return rows
