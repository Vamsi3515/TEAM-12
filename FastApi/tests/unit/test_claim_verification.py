import pytest
from app.models.authenticity import ResumeData, EvidenceItem, AuthenticityExtendedInput
from app.core.Agents.authenticity_agent import analyze_authenticity

@pytest.mark.asyncio
async def test_claim_extraction_and_verification_basic():
    resume = ResumeData(
        skills=["Python", "React"],
        projects=[{"name": "react-dashboard"}],
        certifications=["AWS Solutions Architect"]
    )
    evidences = [
        EvidenceItem(type="github_repo", url="https://github.com/user/react-dashboard", title="react-dashboard", metadata={"stars": 10, "commits": 25, "readme_quality": "good"}),
        EvidenceItem(type="certificate", url="https://example.com/cert/aws", title="AWS Solutions Architect", metadata={"issuer_verified": True}),
        EvidenceItem(type="github_profile", url="https://github.com/user", title="user")
    ]
    input_data = AuthenticityExtendedInput(resume=resume, evidences=evidences)
    output = await analyze_authenticity(input_data)
    assert len(output.extracted_claims) >= 3
    assert len(output.claim_verifications) >= 3
    statuses = {cv.status for cv in output.claim_verifications}
    assert any(s in ["Verified", "Partially Verified"] for s in statuses)
