#!/usr/bin/env python3
import typer
from dotenv import load_dotenv
from rich.progress import Progress, SpinnerColumn, TextColumn

from agent import agent
from utils import console, get_commits, prompt_if_none, write_markdown

load_dotenv()


def main(
    repo_path: str = typer.Option(
        None, "--repo-path", help="Path to the git repository"
    ),
    base_branch: str = typer.Option(None, "--base-branch", help="Base branch name"),
    compare_branch: str = typer.Option(
        None, "--compare-branch", help="Compare branch name"
    ),
):
    repo_path = prompt_if_none(repo_path, "REPO PATH")
    base_branch = prompt_if_none(base_branch, "BASE BRANCH")
    compare_branch = prompt_if_none(compare_branch, "COMPARE BRANCH")

    console.print(
        f"[cyan]Getting commits from [bold]{base_branch}[/bold] → [bold]{compare_branch}[/bold] in [bold]{repo_path}[/bold] …[/cyan]"
    )

    commit_list = get_commits(repo_path, base_branch, compare_branch)
    if not commit_list:
        console.print("[yellow]No commits found between those branches.[/yellow]")
        raise typer.Exit()

    console.print(
        f"[magenta]Found [bold]{len(commit_list)}[/bold] commits. Sending to AI for human-friendly summarisation…[/magenta]"
    )

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
    ) as progress:
        task = progress.add_task("Summarising commits…", total=None)
        result = agent.run_sync("Summarise the commits", deps=commit_list)
        progress.update(task, description="Done")

    console.print("\n[bold underline]### Release note summary ###[/bold underline]\n")
    for out in result.output:
        short_sha = out.sha[:7]
        console.print(
            f"[white]- [/white][bold]{short_sha}[/bold] [dim]({out.category})[/dim]: {out.human_summary}"
        )

    # Write markdown
    md_filename = f"release_notes_{base_branch}_to_{compare_branch}.md"
    write_markdown(result.output, base_branch, compare_branch, repo_path, md_filename)


if __name__ == "__main__":
    typer.run(main)
