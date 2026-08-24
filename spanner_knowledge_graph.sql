CREATE TABLE AdProducts (
  ProductId STRING(36) NOT NULL,
  Name STRING(128) NOT NULL,
  Channel STRING(64) NOT NULL,
  AvailableImpressions INT64 NOT NULL,
  FloorPriceCPM FLOAT64 NOT NULL,
  Category STRING(64) NOT NULL,
) PRIMARY KEY(ProductId);

CREATE TABLE Audiences (
  AudienceId STRING(36) NOT NULL,
  Name STRING(128) NOT NULL,
  Category STRING(64) NOT NULL,
  EstimatedReach INT64 NOT NULL,
  Region STRING(32) NOT NULL,
) PRIMARY KEY(AudienceId);

CREATE TABLE Policies (
  PolicyId STRING(36) NOT NULL,
  Name STRING(128) NOT NULL,
  PolicyType STRING(64) NOT NULL,
  ThresholdRule STRING(MAX),
  IsActive BOOL NOT NULL,
  Version STRING(16) NOT NULL,
) PRIMARY KEY(PolicyId);

CREATE TABLE Advertisers (
  AdvertiserId STRING(36) NOT NULL,
  Name STRING(128) NOT NULL,
  Industry STRING(64) NOT NULL,
  Tier STRING(32) NOT NULL,
) PRIMARY KEY(AdvertiserId);

CREATE TABLE ProductAudiences (
  ProductAudienceId STRING(36) NOT NULL,
  ProductId STRING(36) NOT NULL,
  AudienceId STRING(36) NOT NULL,
  AffinityScore FLOAT64 NOT NULL,
) PRIMARY KEY(ProductAudienceId);

CREATE TABLE ProductPolicies (
  ProductPolicyId STRING(36) NOT NULL,
  ProductId STRING(36) NOT NULL,
  PolicyId STRING(36) NOT NULL,
  EnforcementLevel STRING(32) NOT NULL,
) PRIMARY KEY(ProductPolicyId);

CREATE TABLE AudiencePolicies (
  AudiencePolicyId STRING(36) NOT NULL,
  AudienceId STRING(36) NOT NULL,
  PolicyId STRING(36) NOT NULL,
  ConsentRequirement STRING(64) NOT NULL,
) PRIMARY KEY(AudiencePolicyId);

CREATE OR REPLACE PROPERTY GRAPH AdMonetizationKnowledgeGraph
  NODE TABLES(
    AdProducts
      KEY(ProductId)
      LABEL AdProducts PROPERTIES(
        ProductId,
        Name,
        Channel,
        AvailableImpressions,
        FloorPriceCPM,
        Category),
    Audiences
      KEY(AudienceId)
      LABEL Audiences PROPERTIES(
        AudienceId,
        Name,
        Category,
        EstimatedReach,
        Region),
    Policies
      KEY(PolicyId)
      LABEL Policies PROPERTIES(
        PolicyId,
        Name,
        PolicyType,
        ThresholdRule,
        IsActive,
        Version),
    Advertisers
      KEY(AdvertiserId)
      LABEL Advertisers PROPERTIES(
        AdvertiserId,
        Name,
        Industry,
        Tier)
  )
  EDGE TABLES(
    ProductAudiences
      KEY(ProductAudienceId)
      SOURCE KEY(ProductId) REFERENCES AdProducts(ProductId)
      DESTINATION KEY(AudienceId) REFERENCES Audiences(AudienceId)
      LABEL REACHES PROPERTIES(
        ProductAudienceId,
        ProductId,
        AudienceId,
        AffinityScore),
    ProductPolicies
      KEY(ProductPolicyId)
      SOURCE KEY(ProductId) REFERENCES AdProducts(ProductId)
      DESTINATION KEY(PolicyId) REFERENCES Policies(PolicyId)
      LABEL GOVERNED_BY PROPERTIES(
        ProductPolicyId,
        ProductId,
        PolicyId,
        EnforcementLevel),
    AudiencePolicies
      KEY(AudiencePolicyId)
      SOURCE KEY(AudienceId) REFERENCES Audiences(AudienceId)
      DESTINATION KEY(PolicyId) REFERENCES Policies(PolicyId)
      LABEL REQUIRES_POLICY PROPERTIES(
        AudiencePolicyId,
        AudienceId,
        PolicyId,
        ConsentRequirement)
  );
