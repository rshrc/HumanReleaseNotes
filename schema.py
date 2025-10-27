from pydantic import BaseModel, Field


class CommitData(BaseModel):
    author: str = Field(..., description="Author name")
    date: str = Field(..., description="Commit date/time")
    message: str = Field(..., description="Commit message")


class SummaryOutput(BaseModel):
    sha: str = Field(..., description="Commit hash")
    category: str = Field(
        ..., description="Change category (feature/bugfix/refactor/other)"
    )
    human_summary: str = Field(..., description="Human-friendly summary")
