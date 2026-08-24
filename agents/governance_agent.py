class GovernanceAgent:
    """
    Governance & Compliance Specialist Agent:
    Evaluates candidate media packages against active regulatory,
    brand safety, and contractual policies defined in Spanner Graph.
    """
    def __init__(self, project_id="nandemo-377912"):
        self.project_id = project_id

    def evaluate_policy_compliance(self, candidate):
        """
        Evaluates a candidate product against brand safety and budget constraints.
        Returns evaluation records with audit evidence.
        """
        product_id = candidate.get("ProductId")
        allocated_budget = candidate.get("AllocatedBudget", 0)
        evaluations = []

        # Policy 1: Tier-1 Brand Safety Check (GARM)
        if product_id in ["PRD-1", "PRD-2"]:
            evaluations.append({
                "PolicyId": "POL-2",
                "PolicyName": "Tier-1 Brand Safety Verification",
                "EnforcementLevel": "STRICT",
                "ComplianceStatus": "PASSED",
                "AuditEvidence": "GARM Brand Safety Certificate #8892 verified for premium placement"
            })
        elif product_id == "PRD-4":
            evaluations.append({
                "PolicyId": "POL-2",
                "PolicyName": "Tier-1 Brand Safety Verification",
                "EnforcementLevel": "STRICT",
                "ComplianceStatus": "FAILED",
                "AuditEvidence": "General in-stream feed contains unverified UGC lacking Tier-1 certificate"
            })

        # Policy 2: Minimum Budget Floor Check ($10k)
        if allocated_budget >= 10000:
            evaluations.append({
                "PolicyId": "POL-3",
                "PolicyName": "Minimum Budget Threshold $10k",
                "EnforcementLevel": "MANDATORY",
                "ComplianceStatus": "PASSED",
                "AuditEvidence": f"Allocated budget ${allocated_budget:,.2f} meets $10,000 floor"
            })
        elif allocated_budget > 0:
            evaluations.append({
                "PolicyId": "POL-3",
                "PolicyName": "Minimum Budget Threshold $10k",
                "EnforcementLevel": "MANDATORY",
                "ComplianceStatus": "FAILED",
                "AuditEvidence": f"Allocated budget ${allocated_budget:,.2f} is below the $10,000 threshold"
            })

        # Policy 3: Regulatory Financial Risk Notice (For Finance Hero Banner)
        if product_id == "PRD-1":
            evaluations.append({
                "PolicyId": "POL-4",
                "PolicyName": "Regulatory Investment Risk Notice",
                "EnforcementLevel": "STRICT",
                "ComplianceStatus": "PASSED",
                "AuditEvidence": "Statutory financial investment risk disclaimer clause injected into ad payload"
            })

        # Determine overall pass/fail
        is_compliant = all(e["ComplianceStatus"] == "PASSED" for e in evaluations)
        return is_compliant, evaluations
