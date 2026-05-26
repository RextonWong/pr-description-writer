import asyncio
import subprocess
import os
import sys

from claude_agent_sdk import query, ClaudeAgentOptions
from claude_agent_sdk.types import AssistantMessage, ResultMessage


def get_git_diff() -> str:
    candidates = [
        ["git", "diff", "main"],       # commits ahead of main
        ["git", "diff", "--cached"],   # staged changes
        ["git", "diff", "HEAD"],       # unstaged changes vs last commit
    ]
    for cmd in candidates:
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.stdout.strip():
            return result.stdout.strip()
    return ""


async def main() -> None:
    diff = get_git_diff()

    if not diff:
        print("No changes detected against main (or HEAD).")
        sys.exit(0)

    options = ClaudeAgentOptions(
        allowed_tools=["Bash"],
        system_prompt=(
            "You are a senior software engineer writing pull request documentation. "
            "Be concise, professional, and precise. Focus on what changed and why."
        ),
        model="claude-sonnet-4-6",
        permission_mode="bypassPermissions",
        cwd=os.getcwd(),
    )

    prompt = f"""Write a professional GitHub pull request title and description based on the git diff below.

Format your response exactly like this:

**Title:** <a short, imperative PR title under 72 characters>

**Description:**
## Summary
<1-3 bullet points summarising what changed>

## Key Changes
<bullet points listing the most important code changes>

## Notes
<any relevant testing notes, caveats, or follow-ups — omit this section if there are none>

Git diff:
```diff
{diff}
```"""

    print("Generating PR title and description...\n")

    async for message in query(prompt=prompt, options=options):
        if isinstance(message, AssistantMessage):
            for block in message.content:
                if hasattr(block, "text"):
                    print(block.text, end="", flush=True)

    print()  # final newline


if __name__ == "__main__":
    asyncio.run(main())
