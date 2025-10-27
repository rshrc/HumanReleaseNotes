from pydantic_ai import Agent, RunContext

from .schema import CommitData, SummaryOutput

MODEL_ID = "google-gla:gemini-2.5-pro"

agent = Agent(
    MODEL_ID,
    deps_type=list[CommitData],
    output_type=list[SummaryOutput],
    instructions=(
        "You are a technical writer summarising software changes for QA and non-technical stakeholders. "
        "Given a list of commits (author, date, message), output for each commit: "
        "- category (choose from feature, bugfix, refactor, other) "
        "- a clear, human-friendly summary of what changed and why it matters."
    ),
)
