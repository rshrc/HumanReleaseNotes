import os

import git
from rich.console import Console

console = Console()
import typer

from schema import CommitData, SummaryOutput


def prompt_if_none(value: str, prompt_text: str) -> str:
    if value:
        return value
    return console.input(f"[bold cyan]{prompt_text}[/bold cyan] : ")


def get_commits(repo_path: str, base: str, compare: str) -> list[CommitData]:
    try:
        repo = git.Repo(repo_path)
    except git.exc.InvalidGitRepositoryError:
        console.print(
            f"[bold red]Error:[/bold red] '{repo_path}' is not a valid git repository."
        )
        raise typer.Exit(code=1)

    # fetch to ensure remote refs are up-to-date
    try:
        repo.git.fetch()
    except Exception:
        pass  # ignore fetch failures

    refs = [str(r) for r in repo.refs]
    if base not in refs and f"origin/{base}" not in refs:
        console.print(
            f"[bold red]Error:[/bold red] base branch '{base}' not found in refs."
        )
        raise typer.Exit(code=1)
    if compare not in refs and f"origin/{compare}" not in refs:
        console.print(
            f"[bold red]Error:[/bold red] compare branch '{compare}' not found in refs."
        )
        raise typer.Exit(code=1)

    try:
        commits = list(repo.iter_commits(f"{base}..{compare}"))
    except git.GitCommandError as e:
        console.print(f"[bold red]Error running git command:[/bold red] {e}")
        raise typer.Exit(code=1)

    return [
        CommitData(
            sha=c.hexsha,
            author=c.author.name,
            date=str(c.committed_datetime),
            message=c.message.strip(),
        )
        for c in commits
    ]


def write_markdown(
    output_list: list[SummaryOutput], base: str, compare: str, repo: str, md_file: str
):
    with open(md_file, "w") as f:
        f.write(f"# Release Notes: {repo} — {base} → {compare}\n\n")
        f.write(f"Generated: {os.getcwd()}\n\n")
        for out in output_list:
            short_sha = out.sha[:7]
            f.write(f"- **{short_sha}** ({out.category}): {out.human_summary}\n")
    console.print(f"[green]✅ Markdown output saved to:[/green] [bold]{md_file}[/bold]")
