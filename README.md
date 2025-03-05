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

I suggest using [uv](https://github.com/astral-sh/uv) (the future of python package and project management ;)

1. Install uv
    - On macOS and Linux: `curl -LsSf https://astral.sh/uv/install.sh | sh`
    - On Windows: `powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"`

2. Set up .venv python version and install dependencies
    - This project already locked python version, but if you want to switch, run: `uv venv --python 3.13`
    - `uv sync` installs defined python version (defined by above comment which created the `.python-version` file)

3. Select the interpreter and load it as default when opening new terminals in VS Code
    - In VS Code select `.venv\Scripts\python.exe` as the interpreter (CTRL+SHIFT+P > 'Python: Select Interpreter')
    - Additionally add `.vscode/settings.json` to always activate the .venv when opening a new terminal window in VS Code:
    ```json
    {
        "python.defaultInterpreterPath": "${workspaceFolder}/.venv/bin/python",
        "terminal.integrated.env.linux": {
            "VIRTUAL_ENV": "${workspaceFolder}/.venv",
            "PATH": "${workspaceFolder}/.venv/bin:${env:PATH}"
        },
        "terminal.integrated.env.windows": {
            "VIRTUAL_ENV": "${workspaceFolder}/.venv",
            "PATH": "${workspaceFolder}/.venv/Scripts:${env:PATH}"
        }
    }
    ```

4. Execute
    - run from console: `uv run python runner.py`
    - or run via VS Code Run button, or Debug (if `Python Debugger` extension is installed)
    - or run via VS Code terminal: `python runner.py`

To add new packages
    - `uv add package_name`

 


Learn more about uv: https://docs.astral.sh/uv/