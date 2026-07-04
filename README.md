# Utilities Workspace

Utilities is a multi-module Python workspace for personal operations and analysis tasks.
It combines reusable modules under libs/py-modules with runnable examples under examples/.

The project is organized to support day-to-day workflows such as:

1. Budget and transaction analysis
2. Dataset loading and preprocessing
3. Report and plot generation
4. Schedule/task tree management
5. Focused tools (flights scraping, trips, tracker, UI)

## Project Layout

Top-level directories:

1. bin/
	- CLI shell entry points.
2. docs/
	- Diagrams, schedules, reports, and presentation assets.
3. examples/
	- Runnable module examples with local data/config/output folders.
4. libs/py-modules/
	- Main Python modules.
5. libs/shell/
	- Shared shell helper scripts.
6. tests/
	- Python test files and helper scripts.
7. setup.sh
	- Environment bootstrap script (sets XUTILSPATH, LIBSPATH, PYTHONPATH).

## Core Modules

Main module files in libs/py-modules:

1. budget.py
	- Budget analysis workflows and dashboard/report entry points.
2. dataset.py
	- Dataset loading/normalization utilities and CLI entry.
3. reporter.py
	- Runset/config-driven reporting and plotting orchestration.
4. plotter.py
	- Plot generation helpers.
5. schedule.py
	- Schedule modeling and JSON/tree operations.
6. task.py
	- Task tree/node data structures and utilities.
7. flights.py
	- Google Flights scraping utility that exports flight data to CSV.
8. tracker.py
	- Tracking-oriented CLI workflows.
9. trips.py
	- Trip budget calculator CLI.
10. ui.py
	- PyQt-based desktop UI utility.
11. utils.py
	- Shared helper functions used across modules.

## Examples

Each folder in examples/ is intended to be run from inside that folder.

Available examples:

1. budget/
2. dataset/
3. flights/
4. gym/
5. plotter/
6. reporter/
7. schedule/
8. ui/

Most examples include:

1. run.sh
	- Example launch script.
2. config.yaml
	- Module configuration (for modules that support config).
3. data/
	- Sample input files.
4. outputs/
	- Generated artifacts.

## Quick Start

### 1) Bootstrap Environment

From repository root:

```bash
source setup.sh
```

This exports:

1. XUTILSPATH: repository root path.
2. LIBSPATH: libs/py-modules path.
3. PYTHONPATH: includes libs/py-modules for module imports.
4. PATH: includes bin/ scripts.

### 2) Install Python Dependencies

No single lockfile is currently defined at root, so install dependencies used by your target module(s).
Commonly needed packages include:

1. pandas
2. numpy
3. matplotlib
4. pyyaml
5. pytest (for tests)

Optional module-specific packages:

1. playwright (flights module)
2. PyQt6 (ui module)

Example install command:

```bash
python3 -m pip install pandas numpy matplotlib pyyaml pytest playwright PyQt6
playwright install chromium
```

### 3) Run an Example

```bash
cd examples/budget
source ../../setup.sh
source run.sh
```

## Common Workflows

### Budget Workflow

Location: examples/budget

Typical command pattern:

```bash
python3 ${LIBSPATH}/budget.py --type dashboard --csv data/transactions.csv
```

### Reporter Workflow

Location: examples/reporter

Typical command pattern:

```bash
python3 ${LIBSPATH}/reporter.py --config config.yaml --outdir outputs/ --quiet
```

### Flights Workflow

Location: examples/flights

Typical command pattern:

```bash
python3 ${LIBSPATH}/flights.py --config config.yaml
```

Default CSV fields exported by flights.py:

1. price
2. transfers
3. airline
4. time_of_travel
5. leaving_time
6. arrival_time

## Testing

Tests live under tests/.

Run all tests with:

```bash
python3 -m pytest -s tests
```

Run a specific test file with:

```bash
python3 -m pytest -s tests/test_task.py
```

## Configuration Patterns

YAML configs generally follow a runset-style schema with:

1. author metadata
2. runset entries (named runs)
3. plot-config sections
4. data mappings
5. report_settings

See example configs in:

1. examples/budget/config.yaml
2. examples/reporter/config.yaml
3. examples/flights/config.yaml

## Notes

1. This workspace mixes mature and in-progress utilities.
2. Some scripts are domain-specific and may require local data assumptions.
3. Prefer running through examples/ first, then adapt commands/config for your own data.

## Suggested Next Improvements

1. Add a root requirements.txt or pyproject.toml for reproducible installs.
2. Add per-module docs in docs/ with input/output schemas.
3. Standardize run.sh interfaces across examples.
4. Add CI for linting and test execution.# Reporter
