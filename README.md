# structsim

A Python implementation of the [SiLab group's](https://github.com/SiLab-group/structSim)
**structSim** structured-simulation framework.

The framework runs *structured* simulations. Starting from a base set of
parameters, it applies a tree of **modifiers** to explore a space of candidate
simulation *environments*, runs a simulator for each environment, and collects
the results. How far the tree is explored is controlled by a **cut-off**
strategy (a fixed number of steps, a probability threshold, or a wall-clock
duration).

## Provenance

This repository is a clean, packaged Python port derived from the **one-shot /
`aSimulationSystemHandler`** migration in the
[`structSim_py`](https://github.com/Matthjass13/structSim_py) study — the
bachelor thesis *"MAIgration: How can generative AI support developers in
software migration projects?"* (Matthias Gaillard, 2026). In that study, the
one-shot migration was the strongest overall: the highest raw test-pass rate
and, by a clear margin, the lowest correction effort of the twelve migrations
evaluated.

Behaviour is intended to match the original Java framework. The class hierarchy,
public method names, and the file-based I/O are preserved from the Java source
referenced in the thesis.

## What's different from the raw migration

This port keeps the migrated logic but makes it a proper, installable package:

- **`src/` layout** with a single top-level `structsim` package (the migration
  used four top-level packages sitting on `PYTHONPATH`).
- **Packaging** via `pyproject.toml` (PEP 621) with a `structsim` console script
  and `python -m structsim` entry point.
- **Two robustness fixes** the thesis identified in its *slowness* analysis, so
  the pipeline runs to completion deterministically rather than racing:
  - `StartProgram.start_program` now `join()`s the planning and simulation
    threads before returning.
  - `ExperimentSimulatorHandler.run` reads the queue with a timeout (instead of
    blocking forever) and `join()`s the result thread.
  - `start_program` creates the base output/simulator directories up front. The
    per-simulation folders are made with `os.mkdir` (faithful to Java, and
    checked by a unit test), which fails silently if its parent is missing — so
    without existing base directories a run produced no output and a flood of
    `FileNotFoundError`s. A run now works whether or not you pre-create them.
- **Tests runnable with a plain `pytest`** — a `conftest.py` supplies the
  `STRUCTSIM_PROJECT_DIR` the integration test needs.

No functionality was added or removed beyond these fixes.

## Requirements

- Python **3.10+**
- No third-party runtime dependencies (standard library only).
- [`uv`](https://docs.astral.sh/uv/) for environment management (recommended).

## Install

```bash
uv sync
```

This creates a `.venv/` and installs the project (editable) plus the dev tools
(`pytest`, `pylint`, `pyright`). To install as a plain tool without the dev
group:

```bash
uv pip install .
```

## Usage

The framework is driven by a `config.properties` file plus a parameters file.

1. Create a config from the template and edit the paths:

   ```bash
   cp config.example.properties config.properties
   ```

2. Run the bundled example simulation:

   ```bash
   uv run structsim -c config.properties
   # or, equivalently:
   uv run python -m structsim -c config.properties
   ```

   Add `-v` for debug logging.

The example (in `structsim.gluecode.simulation.Simulation`) uses
`MySimulatorHandler` — a `SimpleSimulationHandler` that runs the bundled
`MySimulator` (`result = val1 * val2`) — so the run writes a real result to
`pathToSimulatorResultFile` instead of an empty file. Point
`config.properties` at your own parameters file and swap in your own modifiers
/ handler to run a real simulation.

### Simulators (the plug-in point)

The framework is **simulator-agnostic**: `SimpleSimulationHandler.start_simulation`
is a stub that only touches an empty result file (faithful to the Java
original). To run an actual simulation you implement `start_simulation` to call
your simulator. Two pieces ship as a reference:

- **`MySimulator`** — a toy simulator: reads `val1`/`val2` from the input file
  and writes their product.
- **`MySimulatorHandler`** — a `SimpleSimulationHandler` subclass that wires
  `MySimulator` into `start_simulation`. Used by the example above.

Note: the framework calls `start_simulation` with the *global* `pathParameters`
file, so `MySimulator`'s result reflects the base parameters (constant across
environments), not each environment's modified parameters — a property of the
framework's contract, not of the handler.

### Configuration reference

| Key | Meaning |
|---|---|
| `pathParameters` | Input parameter file (`key=value` lines, e.g. `val1=1.0`). |
| `pathOUT` | Directory the framework writes its own results/summary to. |
| `pathSimulator` | Directory representing the external simulator's workspace. |
| `pathToSimulatorResultFile` | File the simulator writes its raw result to. |
| `cuttOfPlanning` | Cut-off value, interpreted per `typeCuttOfPlanning`. |
| `typeCuttOfPlanning` | `INT`, `CRITERIA`, `DAY`, `HOURS`, or `MINUTES`. |

Cut-off strategies:

- **`INT`** — explore a fixed number of planning steps (`cuttOfPlanning` is an integer).
- **`CRITERIA`** — keep exploring environments whose probability is above `cuttOfPlanning` (a float).
- **`DAY` / `HOURS` / `MINUTES`** — explore for a wall-clock duration.

## Using the library

```python
from structsim.gluecode.concrete_modifier import ConcreteModifier
from structsim.gluecode.simple_simulation_handler import SimpleSimulationHandler
from structsim.interfaces.start_program import StartProgram

modifiers = [
    ConcreteModifier("val2", "+", 1.0, 0.5),
    ConcreteModifier("val2", "+", 10.0, 0.5),
]
handler = SimpleSimulationHandler(modifiers)

with open("config.properties", "rb") as config:
    StartProgram.start_program(config, handler)
```

## Project layout

```
structsim/
├── pyproject.toml
├── config.example.properties
├── resources/
│   └── parameters.txt              # sample input parameters
├── src/structsim/
│   ├── __main__.py                 # CLI: `structsim` / `python -m structsim`
│   ├── experimenthandling/         # Environment, Parameter, Measure, Options,
│   │                               #   ExperimentPlanGenerator / …SimulatorHandler / …ResultHandler
│   ├── interfaces/                 # ABCs + StartProgram orchestration
│   ├── gluecode/                   # ConcreteModifier, MySimulator, MySimulatorHandler,
│   │                               #   SimpleSimulationHandler, Simulation
│   └── util/                       # FileManagement
└── tests/
    ├── unit/                       # unit tests (environment, fileManagement, gluecode)
    └── integration/                # end-to-end scenario tests
```

### Java → Python mapping

| Java concept | Python equivalent |
|---|---|
| `abstract class` / `interface` | `ABC` with `@abstractmethod` |
| multiple `implements` | multiple inheritance from ABC bases |
| `Vector<T>` | `List[T]` |
| `BlockingQueue` / `PriorityBlockingQueue` | `queue.Queue` / `queue.PriorityQueue` |
| `Runnable` + `Thread` | `threading.Thread(target=obj.run)` |
| `Calendar` + time units | `datetime` |
| `Properties` file | plain `key=value` parsing |
| `Logger` (log4j) | `logging` module |
| `InputStream` | file object / `IO[bytes]` |
| getters / setters | Python properties + explicit `get_*` / `set_*` methods |

## Development

```bash
uv run pytest              # run the full test suite
uv run pytest tests/unit   # unit tests only
uv run pylint src/structsim
uv run pyright
```

## License & attribution

Released under the MIT License (see `pyproject.toml`). The design and logic
originate with the SiLab group's Java `structSim` framework and the
`structSim_py` migration study; please credit both when reusing this port. If
the upstream Java framework's license imposes stricter terms, those govern the
derived logic — confirm with the SiLab group before redistribution.
```
