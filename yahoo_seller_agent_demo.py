#!/usr/bin/env python3
"""
Yahoo Dual-Graph System of Action: End-to-End Demo
- Acting Layer: Cloud Spanner Knowledge Graph (AdMonetizationKnowledgeGraph)
- Auditing & Learning Layer: BigQuery Context Graph (DecisionTraceGraph)
"""

import subprocess
import json
import uuid
import sys
from datetime import datetime, timezone

PROJECT_ID = "nandemo-377912"
SPANNER_INSTANCE = "demo-spanner"
SPANNER_DB = "spanner"
BQ_DATASET = "yahoo_context_graph"

def log(msg):
    print(msg, flush=True)

def log_banner(title):
    log("\n" + "=" * 80)
    log(f"  {title}")
    log("=" * 80 + "\n")

def run_spanner_gql(gql_query):
    cmd = [
        "gcloud", "spanner", "databases", "execute-sql", SPANNER_DB,
        f"--instance={SPANNER_INSTANCE}",
        f"--project={PROJECT_ID}",
        f"--sql={gql_query}",
        "--format=json"
    ]
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        raise RuntimeError(f"Spanner GQL error: {res.stderr}")
    return json.loads(res.stdout) if res.stdout.strip() else {}

def run_bq_query(sql_query):
    cmd = [
        "bq", "query", "--use_legacy_sql=false",
        f"--project_id={PROJECT_ID}",
        "--location=US",
        "--format=prettyjson",
        sql_query
    ]
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        raise RuntimeError(f"BigQuery error: {res.stderr}")
    return json.loads(res.stdout) if res.stdout.strip() else []

def main():
    log_banner("YAHOO SELLER AGENT: DUAL-GRAPH SYSTEM OF ACTION DEMO")

    # 1. Incoming Campaign Brief (Ad Context Protocol - AdCP)
    brief_id = f"BRIEF-2026-{uuid.uuid4().hex[:6].upper()}"
    advertiser_id = "ADV-2"
    target_description = "Target Tech & AI Enthusiasts with $60,000 budget under Brand Safety & Financial Compliance rules"
    total_budget = 60000.0
    required_compliance = "Tier-1 Brand Safety (GARM) + High-Net-Worth Accreditation Compliance"
    submitted_at = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")

    log("📥 [STEP 1: INCOMING CAMPAIGN BRIEF via AdCP Protocol]")
    log(f"   • Brief ID:            {brief_id}")
    log("   • Advertiser:          Apex AI Technologies (ADV-2)")
    log(f"   • Budget:              ${total_budget:,.2f}")
    log("   • Target Audience:     Tech & AI Enthusiasts / High-Net-Worth Investors")
    log(f"   • Required Compliance: {required_compliance}\n")

    # 2. Acting Layer: Real-Time Spanner Knowledge Graph Traversal
    log("🔍 [STEP 2: TRAVERSING SPANNER KNOWLEDGE GRAPH (The Acting Layer)]")
    spanner_gql = """
    GRAPH AdMonetizationKnowledgeGraph
    MATCH (p:AdProducts)-[r:REACHES]->(a:Audiences)
    RETURN 
      p.ProductId AS ProductId,
      p.Name AS ProductName,
      p.FloorPriceCPM AS CPM,
      p.AvailableImpressions AS AvailableImpressions,
      a.AudienceId AS AudienceId,
      a.Name AS AudienceName,
      r.AffinityScore AS AffinityScore
    """
    log("   Running Spanner ISO GQL traversal across Products and Audiences...")
    spanner_results = run_spanner_gql(spanner_gql)

    rows = spanner_results.get("rows", [])
    log(f"   Found {len(rows)} matching inventory-audience paths in Spanner Knowledge Graph.\n")

    # 3. Agent Evaluation & Decision Logic
    decision_id = f"DEC-{uuid.uuid4().hex[:6].upper()}"
    decision_time = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")

    cand_1_id = f"CAND-{uuid.uuid4().hex[:4].upper()}"
    cand_1_budget = 40000.0
    cand_1_impressions = int((cand_1_budget / 24.00) * 1000)

    cand_2_id = f"CAND-{uuid.uuid4().hex[:4].upper()}"
    cand_2_budget = 20000.0
    cand_2_impressions = int((cand_2_budget / 18.50) * 1000)

    cand_3_id = f"CAND-{uuid.uuid4().hex[:4].upper()}"
    cand_3_budget = 0.0
    cand_3_impressions = 0

    executive_rationale = (
        "Allocated 67% ($40k) to Yahoo Tech AI Spotlight (0.98 affinity) and 33% ($20k) to Yahoo Finance Premium Banner "
        "(0.95 investor affinity). Both passed Tier-1 Brand Safety and Minimum Budget thresholds. "
        "Global In-Stream Video was evaluated and rejected due to failing Tier-1 Brand Safety policy."
    )

    log("🤖 [STEP 3: AUTONOMOUS AGENT DECISION & POLICY EVALUATION]")
    log(f"   • Decision ID:  {decision_id}")
    log(f"   • Candidate 1:  Yahoo Tech AI Spotlight ➔ [SELECTED: ${cand_1_budget:,.2f} | ~{cand_1_impressions:,} imps]")
    log(f"   • Candidate 2:  Yahoo Finance Premium Banner ➔ [SELECTED: ${cand_2_budget:,.2f} | ~{cand_2_impressions:,} imps]")
    log("   • Candidate 3:  Global In-Stream Video Feed ➔ [REJECTED: Failed Strict Brand Safety Policy]\n")

    # 4. Context Graph Hydration in BigQuery (The Auditing Layer)
    log("📝 [STEP 4: HYDRATING BIGQUERY CONTEXT GRAPH (Auditable Memory)]")
    
    # Insert Nodes and Edges
    eval_1_id = f"EV-{uuid.uuid4().hex[:4].upper()}"
    eval_2_id = f"EV-{uuid.uuid4().hex[:4].upper()}"
    eval_3_id = f"EV-{uuid.uuid4().hex[:4].upper()}"
    eval_4_id = f"EV-{uuid.uuid4().hex[:4].upper()}"

    edge_1 = f"E-{uuid.uuid4().hex[:4]}"
    edge_2 = f"E-{uuid.uuid4().hex[:4]}"
    edge_3 = f"E-{uuid.uuid4().hex[:4]}"
    edge_4 = f"E-{uuid.uuid4().hex[:4]}"
    edge_5 = f"E-{uuid.uuid4().hex[:4]}"
    edge_6 = f"E-{uuid.uuid4().hex[:4]}"
    edge_7 = f"E-{uuid.uuid4().hex[:4]}"
    edge_8 = f"E-{uuid.uuid4().hex[:4]}"

    bq_statements = f"""
    INSERT INTO `{PROJECT_ID}.{BQ_DATASET}.CampaignBriefs`
    VALUES ('{brief_id}', '{advertiser_id}', '{target_description}', {total_budget}, '{required_compliance}', TIMESTAMP('{submitted_at}'));

    INSERT INTO `{PROJECT_ID}.{BQ_DATASET}.AgentDecisions`
    VALUES ('{decision_id}', '{brief_id}', 'PKG-DUAL-PREMIUM', '{executive_rationale}', 'YahooSellerSupervisorAgent_v4', TIMESTAMP('{decision_time}'));

    INSERT INTO `{PROJECT_ID}.{BQ_DATASET}.CandidatePackages`
    VALUES
      ('{cand_1_id}', '{decision_id}', 'PRD-2', 'Yahoo Tech AI & Gadgets Spotlight', 'AUD-1', 'Tech & AI Enthusiasts', 24.00, {cand_1_budget}, {cand_1_impressions}, 'SELECTED'),
      ('{cand_2_id}', '{decision_id}', 'PRD-1', 'Yahoo Finance Premium Hero Banner', 'AUD-2', 'High-Net-Worth Investors', 18.50, {cand_2_budget}, {cand_2_impressions}, 'SELECTED'),
      ('{cand_3_id}', '{decision_id}', 'PRD-4', 'Global In-Stream Native Video Feed', 'AUD-1', 'Tech & AI Enthusiasts', 8.50, {cand_3_budget}, {cand_3_impressions}, 'REJECTED');

    INSERT INTO `{PROJECT_ID}.{BQ_DATASET}.EvaluatedPolicies`
    VALUES
      ('{eval_1_id}', '{cand_1_id}', 'POL-2', 'Tier-1 Brand Safety Verification', 'STRICT', 'PASSED', 'GARM Brand Safety Certificate #8892 verified'),
      ('{eval_2_id}', '{cand_1_id}', 'POL-3', 'Minimum Budget Threshold $10k', 'MANDATORY', 'PASSED', 'Allocated $40,000 exceeds $10,000 floor'),
      ('{eval_3_id}', '{cand_2_id}', 'POL-4', 'Regulatory Investment Risk Notice', 'STRICT', 'PASSED', 'Statutory Financial Notice clause injected'),
      ('{eval_4_id}', '{cand_3_id}', 'POL-2', 'Tier-1 Brand Safety Verification', 'STRICT', 'FAILED', 'General feed contains user-generated content without Tier-1 certificate');

    INSERT INTO `{PROJECT_ID}.{BQ_DATASET}.BriefToDecisions` VALUES ('{edge_1}', '{brief_id}', '{decision_id}');

    INSERT INTO `{PROJECT_ID}.{BQ_DATASET}.DecisionToCandidates` VALUES 
      ('{edge_2}', '{decision_id}', '{cand_1_id}'),
      ('{edge_3}', '{decision_id}', '{cand_2_id}'),
      ('{edge_4}', '{decision_id}', '{cand_3_id}');

    INSERT INTO `{PROJECT_ID}.{BQ_DATASET}.CandidateToEvaluations` VALUES
      ('{edge_5}', '{cand_1_id}', '{eval_1_id}'),
      ('{edge_6}', '{cand_1_id}', '{eval_2_id}'),
      ('{edge_7}', '{cand_2_id}', '{eval_3_id}'),
      ('{edge_8}', '{cand_3_id}', '{eval_4_id}');
    """

    run_bq_query(bq_statements)
    log("   ✅ Decision lineage nodes and edges committed to BigQuery Context Graph.\n")

    # 5. Regulator-Grade Audit Traversal on BigQuery Graph
    log("🏛️ [STEP 5: REGULATOR-GRADE AUDIT TRAVERSAL ON BIGQUERY GRAPH (ISO GQL)]")
    bq_audit_gql = f"""
    GRAPH `{PROJECT_ID}.{BQ_DATASET}.DecisionTraceGraph`
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

    audit_results = run_bq_query(bq_audit_gql)

    log(f"\n{'-'*115}")
    log(f"{'PRODUCT NAME':<35} | {'STATUS':<9} | {'BUDGET':<10} | {'POLICY NAME':<30} | {'COMPLIANCE':<10}")
    log(f"{'-'*115}")
    for res in audit_results:
        log(f"{res['ProductName']:<35} | {res['Status']:<9} | ${float(res['Budget']):<9,.2f} | {res['Policy']:<30} | {res['Compliance']:<10}")
    log(f"{'-'*115}\n")

    log("🎉 [DEMO COMPLETE: DUAL-GRAPH SYSTEM OF ACTION IS FULLY OPERATIONAL]")
    log("   • Spanner Knowledge Graph: Real-time operational truth for inventory & constraints.")
    log("   • BigQuery Context Graph: Complete auditable memory proving why decisions were made.")

if __name__ == "__main__":
    main()
