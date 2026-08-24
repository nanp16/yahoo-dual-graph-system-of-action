import uuid
from datetime import datetime, timezone
from agents.inventory_discovery_agent import InventoryDiscoveryAgent
from agents.pricing_forecast_agent import PricingForecastAgent
from agents.governance_agent import GovernanceAgent
from agents.lineage_audit_agent import LineageAuditAgent

class YahooSellerSupervisorAgent:
    """
    Planning Supervisor Agent:
    Orchestrates specialized subagents (Inventory Discovery, Pricing & Forecast,
    Governance, and Lineage Audit) to execute campaigns across Spanner and BigQuery graphs.
    """
    def __init__(self, project_id="nandemo-377912"):
        self.project_id = project_id
        self.inventory_agent = InventoryDiscoveryAgent(project_id=project_id)
        self.pricing_agent = PricingForecastAgent()
        self.governance_agent = GovernanceAgent(project_id=project_id)
        self.audit_agent = LineageAuditAgent(project_id=project_id)

    def execute_campaign_workflow(self, brief_data):
        print("\n" + "=" * 85)
        print("  YAHOO SELLER SUPERVISOR AGENT: MULTI-AGENT EXECUTION LOOP")
        print("=" * 85 + "\n")

        # Step 1: Ingest Brief
        brief_id = brief_data.get("BriefId", f"BRIEF-2026-{uuid.uuid4().hex[:6].upper()}")
        print(f"📥 [SUPERVISOR] Processing Campaign Brief: {brief_id}")
        print(f"   • Advertiser: {brief_data['AdvertiserId']} | Budget: ${brief_data['BudgetUSD']:,.2f}")
        print(f"   • Constraints: {brief_data['RequiredCompliance']}\n")

        # Step 2: Delegate to Inventory Discovery Agent (Spanner Graph)
        print("🔍 [SUPERVISOR ➔ INVENTORY DISCOVERY AGENT] Traversing Spanner Knowledge Graph...")
        inventory_rows = self.inventory_agent.discover_matching_inventory()
        print(f"   • Inventory Discovery Agent returned {len(inventory_rows)} candidate inventory paths from Spanner.\n")

        # Step 3: Delegate to Pricing & Forecasting Agent
        print("💰 [SUPERVISOR ➔ PRICING & FORECASTING AGENT] Generating optimal candidate packages...")
        candidate_packages = self.pricing_agent.generate_candidate_packages(inventory_rows, brief_data['BudgetUSD'])
        print(f"   • Generated {len(candidate_packages)} candidate packages.\n")

        # Step 4: Delegate to Governance & Compliance Agent
        print("⚖️  [SUPERVISOR ➔ GOVERNANCE AGENT] Auditing policy constraints on candidate packages...")
        candidates_with_evals = []
        for cand in candidate_packages:
            is_compliant, evals = self.governance_agent.evaluate_policy_compliance(cand)
            status = "SELECTED" if is_compliant and cand["AllocatedBudget"] > 0 else "REJECTED"
            candidates_with_evals.append({
                "candidate": cand,
                "evaluations": evals,
                "status": status
            })
            print(f"   • Candidate '{cand['ProductName']}': {status} ({len(evals)} policies evaluated)")

        # Step 5: Final Decision Synthesis
        decision = {
            "DecisionId": f"DEC-{uuid.uuid4().hex[:6].upper()}",
            "PackageId": "PKG-DUAL-PREMIUM",
            "Rationale": "Allocated budget to highest affinity placements with verified Tier-1 Brand Safety & Regulatory compliance.",
            "AgentName": "YahooSellerSupervisorAgent_v4",
            "Timestamp": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
        }
        print(f"\n🤖 [SUPERVISOR] Final Decision Synthesized: {decision['DecisionId']}\n")

        # Step 6: Delegate to Lineage Audit Agent (BigQuery Graph)
        print("📝 [SUPERVISOR ➔ LINEAGE AUDIT AGENT] Writing Decision Trace Graph to BigQuery...")
        self.audit_agent.commit_decision_trace(brief_data, decision, candidates_with_evals)
        print("   • Successfully committed typed Decision Lineage to BigQuery Context Graph.\n")

        # Step 7: Execute Regulator Audit Query via ISO GQL
        print("🏛️ [LINEAGE AUDIT AGENT] Running Regulator-Grade Audit Traversal (ISO GQL on BigQuery)...")
        audit_results = self.audit_agent.run_regulator_audit_query(brief_id)

        print(f"\n{'-'*115}")
        print(f"{'PRODUCT NAME':<35} | {'STATUS':<9} | {'BUDGET':<10} | {'POLICY NAME':<30} | {'COMPLIANCE':<10}")
        print(f"{'-'*115}")
        for res in audit_results:
            print(f"{res['ProductName']:<35} | {res['Status']:<9} | ${float(res['Budget']):<9,.2f} | {res['Policy']:<30} | {res['Compliance']:<10}")
        print(f"{'-'*115}\n")

        return decision, audit_results
