from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import Optional
from datetime import datetime, timezone
import uuid
import os

from agents.supervisor_agent import YahooSellerSupervisorAgent
from agents.lineage_audit_agent import LineageAuditAgent

app = FastAPI(
    title="Yahoo Seller Agent - Dual-Graph System of Action API",
    description="Autonomous Media Buying & Regulator-Grade Auditing over Cloud Spanner Graph & BigQuery Graph",
    version="1.0.0"
)

supervisor = YahooSellerSupervisorAgent(project_id="nandemo-377912")
audit_agent = LineageAuditAgent(project_id="nandemo-377912")

class CampaignBriefRequest(BaseModel):
    advertiser_id: str = "ADV-2"
    target_description: str = "Target Tech & AI Enthusiasts with $60,000 budget under Brand Safety rules"
    budget_usd: float = 60000.0
    required_compliance: str = "Tier-1 Brand Safety (GARM) + High-Net-Worth Accreditation Compliance"

@app.get("/")
def get_ui():
    index_path = os.path.join(os.path.dirname(__file__), "static", "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return {
        "status": "HEALTHY",
        "service": "Yahoo Seller Multi-Agent Platform",
        "acting_layer": "Cloud Spanner Graph (AdMonetizationKnowledgeGraph)",
        "auditing_layer": "BigQuery Graph (DecisionTraceGraph)"
    }

@app.post("/api/v1/campaigns/execute")
def execute_campaign(request: CampaignBriefRequest):
    """
    Submits a campaign brief. Autonomous agents traverse Spanner Knowledge Graph,
    score candidates, enforce brand safety, and write decision trace to BigQuery.
    """
    try:
        brief_id = f"BRIEF-2026-{uuid.uuid4().hex[:6].upper()}"
        brief_data = {
            "BriefId": brief_id,
            "AdvertiserId": request.advertiser_id,
            "TargetDescription": request.target_description,
            "BudgetUSD": request.budget_usd,
            "RequiredCompliance": request.required_compliance,
            "SubmittedAt": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
        }

        decision, audit_results = supervisor.execute_campaign_workflow(brief_data)

        return {
            "status": "COMPLETED",
            "brief_id": brief_id,
            "decision": decision,
            "audit_lineage": audit_results
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/v1/campaigns/{brief_id}/audit")
def audit_campaign(brief_id: str):
    """
    Runs a live ISO GQL audit traversal on BigQuery Graph to explain why decisions were made.
    """
    try:
        results = audit_agent.run_regulator_audit_query(brief_id)
        if not results:
            raise HTTPException(status_code=404, detail=f"No decision trace found for brief {brief_id}")
        return {
            "brief_id": brief_id,
            "graph_engine": "BigQuery Property Graph (DecisionTraceGraph)",
            "query_language": "ISO GQL",
            "decision_lineage": results
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
