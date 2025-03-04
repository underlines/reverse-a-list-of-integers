# Reverse a list of integers

My take and random explorations on the "Reverse the list of integers" game by Alexandre Muñiz

- Found on: https://mathstodon.xyz/@two_star/112242224494626411
- With additional discussions on: https://news.ycombinator.com/item?id=40010066

## Important

Much of the code and the theory is derrived from collaborating with an LLM.
I'm sure there are major flaws for which I take no responsibility.

## Repository

- **game.html**
    Single static HTML/JS implementation of the game how I understand it
- **graph_representation.py**
    Simple graph plotting logic of a completed game, using a simple string syntax 0: [a, b, c]...
- **solver.py**
    Various methods to try finding game solutions, none of which are particularily good :)
- **theory/theorie deutsch.md & theory english.md**
    Topics such as Computational complexity, NP-Hardness, Graphs and more combined from LLM sessions

### Running

I suggest using [uv](https://github.com/astral-sh/uv) (the future of python project management ;)

1. Install uv
    - On macOS and Linux: `curl -LsSf https://astral.sh/uv/install.sh | sh`
    - On Windows: `powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"`

2. Run a single script
    ```bash
    uv run solver.py
    ```

3. Create a new script
    ```bash
    uv add --script example.py
    ```

Learn more about uv:
- Run single scripts: https://docs.astral.sh/uv/guides/scripts/
- Run entire projects: https://docs.astral.sh/uv/guides/projects/