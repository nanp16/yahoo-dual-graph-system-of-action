-- 1. Advertisers
INSERT INTO Advertisers (AdvertiserId, Name, Industry, Tier) VALUES
  ('ADV-1', 'Acme Financial Corp', 'Finance', 'Enterprise'),
  ('ADV-2', 'Apex AI Technologies', 'Technology', 'Strategic'),
  ('ADV-3', 'GreenLife Eco Retail', 'Retail', 'Standard');

-- 2. Audiences
INSERT INTO Audiences (AudienceId, Name, Category, EstimatedReach, Region) VALUES
  ('AUD-1', 'Tech & AI Enthusiasts', 'Technology', 12500000, 'GLOBAL'),
  ('AUD-2', 'High-Net-Worth Investors', 'Finance', 3200000, 'US'),
  ('AUD-3', 'EU Privacy-Strict Consumers', 'Retail', 8400000, 'EU'),
  ('AUD-4', 'Global Mobile Gamers', 'Entertainment', 25000000, 'GLOBAL');

-- 3. Policies
INSERT INTO Policies (PolicyId, Name, PolicyType, ThresholdRule, IsActive, Version) VALUES
  ('POL-1', 'GDPR EU Explicit Consent', 'PRIVACY', 'User must have opt-in consent for targeted ad delivery in EU', true, 'v2.1'),
  ('POL-2', 'Tier-1 Brand Safety Verification', 'BRAND_SAFETY', 'Placement must pass GARM brand safety verification', true, 'v1.4'),
  ('POL-3', 'Minimum Budget Threshold $10k', 'BUDGET_THRESHOLD', 'Campaign allocation must exceed $10,000 for premium placements', true, 'v1.0'),
  ('POL-4', 'Regulatory Investment Risk Notice', 'REGULATORY', 'Must display statutory financial investment risk warning', true, 'v3.0');

-- 4. AdProducts
INSERT INTO AdProducts (ProductId, Name, Channel, AvailableImpressions, FloorPriceCPM, Category) VALUES
  ('PRD-1', 'Yahoo Finance Premium Hero Banner', 'Display Web', 45000000, 18.50, 'Finance'),
  ('PRD-2', 'Yahoo Tech AI & Gadgets Spotlight', 'Newsletter & App', 12000000, 24.00, 'Technology'),
  ('PRD-3', 'Yahoo Sports Live Match Interstitial', 'Mobile Video', 35000000, 12.00, 'Sports'),
  ('PRD-4', 'Global In-Stream Native Video Feed', 'Cross-Platform Feed', 80000000, 8.50, 'General');

-- 5. ProductAudiences (REACHES)
INSERT INTO ProductAudiences (ProductAudienceId, ProductId, AudienceId, AffinityScore) VALUES
  ('PA-1', 'PRD-1', 'AUD-2', 0.95),
  ('PA-2', 'PRD-1', 'AUD-1', 0.70),
  ('PA-3', 'PRD-2', 'AUD-1', 0.98),
  ('PA-4', 'PRD-2', 'AUD-2', 0.65),
  ('PA-5', 'PRD-3', 'AUD-4', 0.92),
  ('PA-6', 'PRD-4', 'AUD-1', 0.75),
  ('PA-7', 'PRD-4', 'AUD-3', 0.80),
  ('PA-8', 'PRD-4', 'AUD-4', 0.85);

-- 6. ProductPolicies (GOVERNED_BY)
INSERT INTO ProductPolicies (ProductPolicyId, ProductId, PolicyId, EnforcementLevel) VALUES
  ('PP-1', 'PRD-1', 'POL-2', 'STRICT'),
  ('PP-2', 'PRD-1', 'POL-3', 'MANDATORY'),
  ('PP-3', 'PRD-1', 'POL-4', 'STRICT'),
  ('PP-4', 'PRD-2', 'POL-2', 'STRICT'),
  ('PP-5', 'PRD-2', 'POL-3', 'MANDATORY'),
  ('PP-6', 'PRD-3', 'POL-2', 'STANDARD'),
  ('PP-7', 'PRD-4', 'POL-1', 'STRICT'),
  ('PP-8', 'PRD-4', 'POL-2', 'STANDARD');

-- 7. AudiencePolicies (REQUIRES_POLICY)
INSERT INTO AudiencePolicies (AudiencePolicyId, AudienceId, PolicyId, ConsentRequirement) VALUES
  ('AP-1', 'AUD-3', 'POL-1', 'GDPR_EXPLICIT_OPT_IN'),
  ('AP-2', 'AUD-2', 'POL-4', 'INVESTOR_ACCREDITATION_NOTICE');
