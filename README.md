# structsim_py

A Python port of the SiLab group's Java
[`structSim`](https://github.com/SiLab-group/structSim) framework. It runs
*structured* simulations: from a base set of parameters it applies a tree of
modifiers to explore candidate environments, runs a simulator for each, and
collects the results.

This is the one-shot migration from Matthias Gaillard's bachelor thesis
*"MAIgration: How can generative AI support developers in software migration
projects?"* (2026) — [thesis](THESIS_URL) ·
[study repo](https://github.com/Matthjass13/structSim_py).

## Setup

Requires **Python 3.10+**. There are no runtime dependencies (standard library
only); the dev tools (`pytest`, `pylint`, `pyright`) are installed for you.

Using [uv](https://docs.astral.sh/uv/) (recommended) — creates a `.venv` and
installs the package plus dev tools:

```bash
uv sync
```

Or with plain pip:

```bash
python -m venv .venv && source .venv/bin/activate
pip install -e .              # add: pip install pytest pylint pyright  (for dev)
```

## Run

```bash
cp config.example.properties config.properties   # then edit the paths
uv run structsim -c config.properties            # add -v for debug logging
```

Equivalent without the console script: `uv run python -m structsim -c config.properties`.

The example runs the bundled `MySimulator` (`result = val1 * val2`). Swap in
your own modifiers and handler for a real simulation.

### config.properties

| Key | Meaning |
|---|---|
| `pathParameters` | Input parameter file (`key=value` lines). |
| `pathOUT` | Where results and the summary are written. |
| `pathSimulator` | Simulator workspace directory. |
| `pathToSimulatorResultFile` | Raw result file the simulator writes. |
| `cuttOfPlanning` | Cut-off value (interpreted per `typeCuttOfPlanning`). |
| `typeCuttOfPlanning` | `INT` (N steps), `CRITERIA` (probability threshold), or `DAY`/`HOURS`/`MINUTES` (wall-clock). |

## Tests

```bash
uv run pytest
```

## Citation

If you use this in academic work, cite the paper that introduced the approach:

> René Schumann and Caroline Taramarcaz. *Towards Systematic Testing of Complex
> Interacting Systems.* SysRisk 2019, CEUR-WS Vol. 2397, pp. 55–63.
> <https://ceur-ws.org/Vol-2397/paper8.pdf>

## License

Apache 2.0 — see [`LICENSE`](LICENSE). Copyright of the underlying framework
remains with SI-Lab, HES-SO Valais/Wallis (René Schumann).
