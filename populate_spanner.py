from google.cloud import spanner
import datetime

def populate_spanner_knowledge_graph(project_id="nandemo-377912", instance_id="demo-spanner", database_id="spanner"):
    spanner_client = spanner.Client(project=project_id)
    instance = spanner_client.instance(instance_id)
    database = instance.database(database_id)

    def insert_data(transaction):
        # 1. Advertisers
        advertisers = [
            ("ADV-1", "Acme Financial Corp", "Finance", "Enterprise"),
            ("ADV-2", "Apex AI Technologies", "Technology", "Strategic"),
            ("ADV-3", "GreenLife Eco Retail", "Retail", "Standard"),
        ]
        transaction.insert_or_update(
            "Advertisers",
            columns=["AdvertiserId", "Name", "Industry", "Tier"],
            values=advertisers
        )

        # 2. Audiences
        audiences = [
            ("AUD-1", "Tech & AI Enthusiasts", "Technology", 12500000, "GLOBAL"),
            ("AUD-2", "High-Net-Worth Investors", "Finance", 3200000, "US"),
            ("AUD-3", "EU Privacy-Strict Consumers", "Retail", 8400000, "EU"),
            ("AUD-4", "Global Mobile Gamers", "Entertainment", 25000000, "GLOBAL"),
        ]
        transaction.insert_or_update(
            "Audiences",
            columns=["AudienceId", "Name", "Category", "EstimatedReach", "Region"],
            values=audiences
        )

        # 3. Policies
        policies = [
            ("POL-1", "GDPR EU Explicit Consent", "PRIVACY", "User must have opt-in consent for targeted ad delivery in EU", True, "v2.1"),
            ("POL-2", "Tier-1 Brand Safety Verification", "BRAND_SAFETY", "Placement must pass GARM brand safety verification", True, "v1.4"),
            ("POL-3", "Minimum Budget Threshold $10k", "BUDGET_THRESHOLD", "Campaign allocation must exceed $10,000 for premium placements", True, "v1.0"),
            ("POL-4", "Regulatory Investment Risk Notice", "REGULATORY", "Must display statutory financial investment risk warning", True, "v3.0"),
        ]
        transaction.insert_or_update(
            "Policies",
            columns=["PolicyId", "Name", "PolicyType", "ThresholdRule", "IsActive", "Version"],
            values=policies
        )

        # 4. AdProducts (Inventory)
        ad_products = [
            ("PRD-1", "Yahoo Finance Premium Hero Banner", "Display Web", 45000000, 18.50, "Finance"),
            ("PRD-2", "Yahoo Tech AI & Gadgets Spotlight", "Newsletter & App", 12000000, 24.00, "Technology"),
            ("PRD-3", "Yahoo Sports Live Match Interstitial", "Mobile Video", 35000000, 12.00, "Sports"),
            ("PRD-4", "Global In-Stream Native Video Feed", "Cross-Platform Feed", 80000000, 8.50, "General"),
        ]
        transaction.insert_or_update(
            "AdProducts",
            columns=["ProductId", "Name", "Channel", "AvailableImpressions", "FloorPriceCPM", "Category"],
            values=ad_products
        )

        # 5. ProductAudiences Edges (REACHES)
        product_audiences = [
            ("PA-1", "PRD-1", "AUD-2", 0.95),
            ("PA-2", "PRD-1", "AUD-1", 0.70),
            ("PA-3", "PRD-2", "AUD-1", 0.98),
            ("PA-4", "PRD-2", "AUD-2", 0.65),
            ("PA-5", "PRD-3", "AUD-4", 0.92),
            ("PA-6", "PRD-4", "AUD-1", 0.75),
            ("PA-7", "PRD-4", "AUD-3", 0.80),
            ("PA-8", "PRD-4", "AUD-4", 0.85),
        ]
        transaction.insert_or_update(
            "ProductAudiences",
            columns=["ProductAudienceId", "ProductId", "AudienceId", "AffinityScore"],
            values=product_audiences
        )

        # 6. ProductPolicies Edges (GOVERNED_BY)
        product_policies = [
            ("PP-1", "PRD-1", "POL-2", "STRICT"),
            ("PP-2", "PRD-1", "POL-3", "MANDATORY"),
            ("PP-3", "PRD-1", "POL-4", "STRICT"),
            ("PP-4", "PRD-2", "POL-2", "STRICT"),
            ("PP-5", "PRD-2", "POL-3", "MANDATORY"),
            ("PP-6", "PRD-3", "POL-2", "STANDARD"),
            ("PP-7", "PRD-4", "POL-1", "STRICT"),
            ("PP-8", "PRD-4", "POL-2", "STANDARD"),
        ]
        transaction.insert_or_update(
            "ProductPolicies",
            columns=["ProductPolicyId", "ProductId", "PolicyId", "EnforcementLevel"],
            values=product_policies
        )

        # 7. AudiencePolicies Edges (REQUIRES_POLICY)
        audience_policies = [
            ("AP-1", "AUD-3", "POL-1", "GDPR_EXPLICIT_OPT_IN"),
            ("AP-2", "AUD-2", "POL-4", "INVESTOR_ACCREDITATION_NOTICE"),
        ]
        transaction.insert_or_update(
            "AudiencePolicies",
            columns=["AudiencePolicyId", "AudienceId", "PolicyId", "ConsentRequirement"],
            values=audience_policies
        )

    database.run_in_transaction(insert_data)
    print("Successfully hydrated Spanner AdMonetizationKnowledgeGraph with operational data!")

if __name__ == "__main__":
    populate_spanner_knowledge_graph()
