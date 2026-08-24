-- 1. Create dataset if not exists
CREATE SCHEMA IF NOT EXISTS `nandemo-377912.yahoo_context_graph`
OPTIONS (location = 'US');

-- 2. Nodes: CampaignBriefs
CREATE OR REPLACE TABLE `nandemo-377912.yahoo_context_graph.CampaignBriefs` (
  BriefId STRING NOT NULL,
  AdvertiserId STRING NOT NULL,
  TargetAudienceDescription STRING NOT NULL,
  BudgetUSD FLOAT64 NOT NULL,
  RequiredCompliance STRING NOT NULL,
  SubmittedAt TIMESTAMP NOT NULL
);

-- 3. Nodes: AgentDecisions
CREATE OR REPLACE TABLE `nandemo-377912.yahoo_context_graph.AgentDecisions` (
  DecisionId STRING NOT NULL,
  BriefId STRING NOT NULL,
  SelectedPackageId STRING NOT NULL,
  ExecutiveRationale STRING NOT NULL,
  AgentName STRING NOT NULL,
  DecisionTimestamp TIMESTAMP NOT NULL
);

-- 4. Nodes: CandidatePackages
CREATE OR REPLACE TABLE `nandemo-377912.yahoo_context_graph.CandidatePackages` (
  CandidateId STRING NOT NULL,
  DecisionId STRING NOT NULL,
  ProductId STRING NOT NULL,
  ProductName STRING NOT NULL,
  AudienceId STRING NOT NULL,
  AudienceName STRING NOT NULL,
  PredictedCPM FLOAT64 NOT NULL,
  AllocatedBudget FLOAT64 NOT NULL,
  EstimatedImpressions INT64 NOT NULL,
  SelectionStatus STRING NOT NULL -- 'SELECTED', 'REJECTED'
);

-- 5. Nodes: EvaluatedPolicies
CREATE OR REPLACE TABLE `nandemo-377912.yahoo_context_graph.EvaluatedPolicies` (
  EvaluationId STRING NOT NULL,
  CandidateId STRING NOT NULL,
  PolicyId STRING NOT NULL,
  PolicyName STRING NOT NULL,
  EnforcementLevel STRING NOT NULL,
  ComplianceStatus STRING NOT NULL, -- 'PASSED', 'FAILED'
  AuditEvidence STRING NOT NULL
);

-- 6. Edges: BriefToDecisions (PRODUCED_DECISION)
CREATE OR REPLACE TABLE `nandemo-377912.yahoo_context_graph.BriefToDecisions` (
  EdgeId STRING NOT NULL,
  BriefId STRING NOT NULL,
  DecisionId STRING NOT NULL
);

-- 7. Edges: DecisionToCandidates (EVALUATED_CANDIDATE)
CREATE OR REPLACE TABLE `nandemo-377912.yahoo_context_graph.DecisionToCandidates` (
  EdgeId STRING NOT NULL,
  DecisionId STRING NOT NULL,
  CandidateId STRING NOT NULL
);

-- 8. Edges: CandidateToEvaluations (GOVERNED_BY)
CREATE OR REPLACE TABLE `nandemo-377912.yahoo_context_graph.CandidateToEvaluations` (
  EdgeId STRING NOT NULL,
  CandidateId STRING NOT NULL,
  EvaluationId STRING NOT NULL
);

-- 9. BigQuery Property Graph Definition
CREATE OR REPLACE PROPERTY GRAPH `nandemo-377912.yahoo_context_graph.DecisionTraceGraph`
  NODE TABLES(
    `nandemo-377912.yahoo_context_graph.CampaignBriefs`
      KEY(BriefId)
      LABEL CampaignBriefs PROPERTIES (BriefId, AdvertiserId, TargetAudienceDescription, BudgetUSD, RequiredCompliance, SubmittedAt),
    `nandemo-377912.yahoo_context_graph.AgentDecisions`
      KEY(DecisionId)
      LABEL AgentDecisions PROPERTIES (DecisionId, BriefId, SelectedPackageId, ExecutiveRationale, AgentName, DecisionTimestamp),
    `nandemo-377912.yahoo_context_graph.CandidatePackages`
      KEY(CandidateId)
      LABEL CandidatePackages PROPERTIES (CandidateId, DecisionId, ProductId, ProductName, AudienceId, AudienceName, PredictedCPM, AllocatedBudget, EstimatedImpressions, SelectionStatus),
    `nandemo-377912.yahoo_context_graph.EvaluatedPolicies`
      KEY(EvaluationId)
      LABEL EvaluatedPolicies PROPERTIES (EvaluationId, CandidateId, PolicyId, PolicyName, EnforcementLevel, ComplianceStatus, AuditEvidence)
  )
  EDGE TABLES(
    `nandemo-377912.yahoo_context_graph.BriefToDecisions`
      KEY(EdgeId)
      SOURCE KEY(BriefId) REFERENCES `nandemo-377912.yahoo_context_graph.CampaignBriefs`(BriefId)
      DESTINATION KEY(DecisionId) REFERENCES `nandemo-377912.yahoo_context_graph.AgentDecisions`(DecisionId)
      LABEL PRODUCED_DECISION,
    `nandemo-377912.yahoo_context_graph.DecisionToCandidates`
      KEY(EdgeId)
      SOURCE KEY(DecisionId) REFERENCES `nandemo-377912.yahoo_context_graph.AgentDecisions`(DecisionId)
      DESTINATION KEY(CandidateId) REFERENCES `nandemo-377912.yahoo_context_graph.CandidatePackages`(CandidateId)
      LABEL EVALUATED_CANDIDATE,
    `nandemo-377912.yahoo_context_graph.CandidateToEvaluations`
      KEY(EdgeId)
      SOURCE KEY(CandidateId) REFERENCES `nandemo-377912.yahoo_context_graph.CandidatePackages`(CandidateId)
      DESTINATION KEY(EvaluationId) REFERENCES `nandemo-377912.yahoo_context_graph.EvaluatedPolicies`(EvaluationId)
      LABEL GOVERNED_BY
  );
