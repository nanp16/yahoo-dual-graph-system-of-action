#!/usr/bin/env python3
"""
Main Entrypoint: Yahoo Seller Multi-Agent System
Orchestrates specialized subagents across Cloud Spanner Graph and BigQuery Graph.
"""

from datetime import datetime, timezone
import uuid
from agents.supervisor_agent import YahooSellerSupervisorAgent

def main():
    supervisor = YahooSellerSupervisorAgent(project_id="nandemo-377912")

    brief_data = {
        "BriefId": f"BRIEF-2026-{uuid.uuid4().hex[:6].upper()}",
        "AdvertiserId": "ADV-2",
        "TargetDescription": "Target Tech & AI Enthusiasts with $60,000 budget under Brand Safety & Financial Compliance rules",
        "BudgetUSD": 60000.0,
        "RequiredCompliance": "Tier-1 Brand Safety (GARM) + High-Net-Worth Accreditation Compliance",
        "SubmittedAt": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
    }

    supervisor.execute_campaign_workflow(brief_data)

if __name__ == "__main__":
    main()
