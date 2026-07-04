# Reporter

Lightweight Python workspace for dataset loading, plotting helpers, and config-driven report generation.

## Directory Layout

```text
.
├── README.md
├── setup.sh
├── examples/
│   ├── dataset/
│   │   ├── README.md
│   │   ├── config.yaml
│   │   ├── run.sh
│   │   └── data/
│   │       └── sample.csv
│   ├── plotter/
│   │   ├── README.md
│   │   ├── run.sh
│   │   └── data/
│   │       └── sample.csv
│   └── reporter/
│       ├── README.md
│       ├── config.yaml
│       ├── run.sh
│       ├── data/
│       │   ├── sample.csv
│       │   ├── sample1.csv
│       │   ├── sample2.csv
│       │   ├── sample3.csv
│       │   ├── sample_block.csv
│       │   └── sample_stacked.csv
│       └── outputs/
│           ├── sample1/
│           ├── sample2/
│           ├── sample3/
│           │   ├── latency_data_pretty_tc1.csv
│           │   └── latency_table_tc1.csv
│           └── sample4/
└── libs/
    └── py-modules/
        ├── __init__.py
        ├── dataset.py
        ├── plotter.py
        ├── reporter.py
        └── utils.py
```

## Modules

1. `dataset.py`
   - CSV-backed dataset object with basic validation and column filtering.
2. `plotter.py`
   - Reusable plotting functions (line, bar, stacked bar, scatter, box, 2D color scatter) and save helpers.
3. `reporter.py`
   - Reads YAML run configurations, loads datasets, and generates report plots/artifacts into per-run output directories.
4. `utils.py`
   - Logging and small utility helpers used by the modules.

## Setup

From repo root:

```bash
source setup.sh
```

This sets:

1. `XUTILSPATH`
2. `LIBSPATH`
3. `PYTHONPATH`

## Python Dependencies

Install the packages used by the current modules:

```bash
python3 -m pip install pandas numpy matplotlib pyyaml
```

## Running Examples

Run examples from their folder after sourcing `setup.sh` from repo root.

1. Dataset example

```bash
cd examples/dataset
source ../../setup.sh
source run.sh
```

2. Plotter example

```bash
cd examples/plotter
source ../../setup.sh
source run.sh
```

3. Reporter example

```bash
cd examples/reporter
source ../../setup.sh
source run.sh
```

Equivalent direct reporter command:

```bash
python3 ${LIBSPATH}/reporter.py --config config.yaml --outdir outputs/ --quiet
```

## Reporter Config Overview

`reporter.py` expects a YAML file with:

1. `author`
2. `runset` entries
3. optional `report_settings` (for example, matplotlib style)

Each run typically defines:

1. data files (`data` map)
2. x/y/z source columns (`xval`, `yval`, `zval`)
3. output filename (`outfile`)
4. `plot-config` settings (labels, limits, scales, type, legend location, etc.)
