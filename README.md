# 🚀 Google Cloud Agentic Dual-Graph System of Action
### *A Production Blueprint Inspired by Yahoo Seller Agent & Google Cloud*

[![Google Cloud Spanner Graph](https://img.shields.io/badge/Google%20Cloud-Spanner%20Graph-4285F4?logo=googlecloud&logoColor=white)](https://cloud.google.com/spanner)
[![Google Cloud BigQuery Graph](https://img.shields.io/badge/Google%20Cloud-BigQuery%20Graph-669DF6?logo=googlecloud&logoColor=white)](https://cloud.google.com/bigquery)
[![ISO GQL](https://img.shields.io/badge/Query%20Language-ISO%20GQL-34A853)](https://www.iso.org/standard/76388.html)
[![Agent Protocol](https://img.shields.io/badge/Protocol-AdCP%20%2F%20A2A-EA4335)](#)

---

## 📖 Overview

As enterprises transition from **Systems of Intelligence** (reactive chatbots/copilots) to **Systems of Action** (autonomous agents executing real transactions with budgets), traditional LLM approaches face two critical risks:
1. **Factual Grounding Risk (Hallucination):** Agents acting without deterministic awareness of active contracts, inventory, and legal constraints make costly errors.
2. **The "Black Box" Audit Risk:** Regulators, auditors, and enterprise clients demand instant, verifiable answers for *why* specific decisions were made.

This repository provides an end-to-end, runnable implementation of the **Dual-Graph Agentic Blueprint** pioneered by **Yahoo and Google Cloud**:
* **Graph 1: The Knowledge Graph (Acting Layer in Cloud Spanner Graph):** Grounds autonomous agents in real-time operational truth with sub-millisecond graph traversals. Policies are modeled as first-class, versioned graph edges (`GOVERNED_BY`, `REQUIRES_POLICY`).
* **Graph 2: The Context Graph (Auditing & Learning Layer in BigQuery Graph):** Captures every decision span, candidate package, rejected alternative, and policy evaluation into a queryable decision lineage graph for regulator-grade explainability.

---

## 🏛️ Architecture

```
                                  YAHOO SELLER AGENT PLATFORM
                               (ADK + Multi-Agent Orchestration)
                                               │
                 ┌─────────────────────────────┴─────────────────────────────┐
                 ▼                                                           ▼
     ┌───────────────────────────────┐                           ┌───────────────────────────────┐
     │    SPANNER GRAPH (ACTING)     │                           │   BIGQUERY GRAPH (LEARNING)   │
     │     "The Knowledge Graph"     │                           │      "The Context Graph"      │
     ├───────────────────────────────┤                           ├───────────────────────────────┤
     │ • Real-time Operational Truth │                           │ • Decision Lineage & Memory   │
     │ • Sub-millisecond latency     │                           │ • Immutable Audit Ledger      │
     │ • Inventory, Pricing, Rules   │                           │ • BigQuery Agent Analytics    │
     │ • Policies as Versioned Edges │                           │ • Closed-Loop ML Training     │
     └───────────────────────────────┘                           └───────────────────────────────┘
```

---

## 📁 Repository Structure

```
├── spanner_knowledge_graph.sql      # DDL defining Spanner Property Graph (AdMonetizationKnowledgeGraph)
├── insert_spanner.sql               # Seed data for Ad Products, Audiences, Policies, and Edges
├── bigquery_context_graph.sql       # DDL defining BigQuery Property Graph (DecisionTraceGraph)
├── yahoo_seller_agent_demo.py       # Autonomous Agent execution runner & live audit GQL queries
├── populate_spanner.py              # Python SDK hydration utility
├── .gitignore                       # Git ignore rules
└── README.md                        # Complete documentation & architecture guide
```

---

## 🚀 Getting Started

### Prerequisites
* Google Cloud SDK (`gcloud` CLI & `bq` CLI) authenticated to your project.
* A Cloud Spanner instance with an active database.
* BigQuery dataset enabled for Property Graphs.

### 1. Deploy Spanner Knowledge Graph (The Acting Layer)
Apply the DDL and seed the operational graph:
```bash
gcloud spanner databases ddl update <YOUR_DATABASE> \
  --instance=<YOUR_INSTANCE> \
  --ddl-file=spanner_knowledge_graph.sql

gcloud spanner databases execute-sql <YOUR_DATABASE> \
  --instance=<YOUR_INSTANCE> \
  --sql="$(cat insert_spanner.sql)"
```

### 2. Deploy BigQuery Context Graph (The Auditing Layer)
Deploy the BigQuery schema and Property Graph:
```bash
bq query --use_legacy_sql=false < bigquery_context_graph.sql
```

### 3. Run the Autonomous Multi-Agent Loop
Execute the Python runner to simulate an incoming campaign brief, real-time Spanner GQL evaluation, BigQuery lineage logging, and regulator audit traversal:
```bash
python3 yahoo_seller_agent_demo.py
```

---

## 🔍 Sample Graph Queries (ISO GQL)

### 1. Spanner Knowledge Graph Traversal (Acting)
Traverse eligible ad products, target audiences, and legal governing policies in a single query:
```sql
GRAPH AdMonetizationKnowledgeGraph
MATCH (p:AdProducts)-[r:REACHES]->(a:Audiences)
OPTIONAL MATCH (p)-[gp:GOVERNED_BY]->(pol:Policies)
RETURN 
  p.Name AS ProductName, 
  p.FloorPriceCPM AS FloorPriceCPM, 
  a.Name AS AudienceName, 
  r.AffinityScore AS AffinityScore, 
  pol.Name AS PolicyName, 
  gp.EnforcementLevel AS EnforcementLevel;
```

### 2. BigQuery Context Graph Traversal (Regulator Audit)
Trace the full provenance of why a candidate was selected or rejected for a campaign brief:
```sql
GRAPH `your_project.yahoo_context_graph.DecisionTraceGraph`
MATCH (b:CampaignBriefs)-[:PRODUCED_DECISION]->(d:AgentDecisions)-[:EVALUATED_CANDIDATE]->(c:CandidatePackages)-[:GOVERNED_BY]->(p:EvaluatedPolicies)
WHERE b.BriefId = 'BRIEF-2026-82DEC5'
RETURN
  c.ProductName AS ProductName,
  c.SelectionStatus AS Status,
  c.AllocatedBudget AS Budget,
  p.PolicyName AS Policy,
  p.ComplianceStatus AS Compliance,
  p.AuditEvidence AS AuditEvidence
ORDER BY Status DESC, Budget DESC;
```

---

## 📚 References & Case Studies
* [Google Cloud Blog: Graph technologies underpin Yahoo’s system of action](https://cloud.google.com/blog/products/databases/graph-technologies-underpin-yahoo-system-of-action?e=48754805)
* [Google Cloud Spanner Graph Documentation](https://cloud.google.com/spanner/docs/graph-overview)
* [Google Cloud BigQuery Graph Documentation](https://cloud.google.com/bigquery/docs/graph-overview)
