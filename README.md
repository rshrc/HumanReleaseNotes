# HumaniseReleaseNotes

## Overview  
This tool helps teams convert technical commit history between two Git branches into human-friendly release notes suitable for QA and non-technical stakeholders. It automates:  
- fetching commits between two branches  
- sending them to an LLM agent (via Pydantic AI) for summarisation  
- producing a formatted Markdown release notes file  

## Features  
- Prompts for repository path, base branch and compare branch (or accepts them via CLI options)  
- Validates branches and fetches the commit list  
- Categorises each commit (feature, bugfix, refactor, other) and summarises it  
- Outputs to console and writes a Markdown file (`release_notes_<base>_to_<compare>.md`)  
- Simple CLI-tool style: no large dependencies beyond GitPython, Typer, Pydantic AI  

## Getting Started  

### Prerequisites  
- Python 3.10 or later  
- Git installed and accessible via command line  
- An LLM provider API key configured (for example: `GOOGLE_API_KEY` for Google Generative Language API)  
- Virtual environment is recommended  

### Installation  
1. Clone this repository:  
   ```bash
   git clone <your-repo-url>   
   cd <your-repo-folder> ```


2. Set up virtual environment and install dependencies:

   ```bash
   python3 -m venv venv  
   source venv/bin/activate  
   pip install gitpython typer python-dotenv pydantic-ai  
   ```

3. Create a `.env` file at the project root with your API key, for example:

   ```
   GOOGLE_API_KEY=your_api_key_here  
   ```

## Usage

Run the script:

```bash
python main.py  
```

You will be prompted (if not provided via flags) for:

* **REPO PATH**: local file system path to the Git repository
* **BASE BRANCH**: the branch you are comparing *from*
* **COMPARE BRANCH**: the branch you are comparing *to*

Alternatively you can supply them via CLI options:

```bash
python main.py --repo-path /path/to/repo --base-branch dev --compare-branch release  
```

On successful execution you will see:

* A console summary of the commits and categorised summaries
* A Markdown file generated, e.g. `release_notes_dev_to_release.md`, in the working directory

## Output Details

The Markdown file will start with a heading and metadata, followed by a bullet list where each item has:

* The first 7 characters of the commit SHA
* The change category (feature, bugfix, refactor, other)
* A human-friendly summary describing what changed and why it matters

Example snippet:

```
- **a1b2c3d** (feature): Introduced a new user authentication module enabling secure login for users and improving overall system security.
```

## Customisation & Extension Ideas

* Add support for summarising file diffs (files changed + lines added/removed)
* Chunk large commit sets to respect LLM token limits
* Add flags for plain mode (no colour output) or verbose mode
* Group output in Markdown into sections by category (features / bug-fixes / refactors / others)
* Save output to custom path or format (e.g., CSV)
* Integrate with CI/CD to auto-generate release notes on each merge

## Troubleshooting

* If you encounter errors such as `fatal: bad revision '<base>..<compare>'`, ensure both branch names exist locally or remote (`origin/<branch>`).
* If the LLM agent fails, verify your environment API key is set and correct.
