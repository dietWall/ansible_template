# Molecule Scenario Runner - Usage

## Quick Start

```bash
# Run all scenarios in correct order
./run_molecule_scenarios.py

# Or using python directly
python run_molecule_scenarios.py
```

## Options

### Environment Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `DEMO_DETAILED` | Enable verbose output | `export DEMO_DETAILED=true` |

### Manual Execution

Run scenarios individually:

```bash
# Option 1: Quick localhost test only
python run_molecule_scenarios.py  # Modifies default.py file

# Option 2: All scenarios (recommended first run)
python run_molecule_scenarios.py

# Option 3: Run with verbose output
export DEMO_DETAILED=true
python run_molecule_scenarios.py
```

## How It Works

The script runs scenarios in this order:

1. **default** (localhost) - Quick tests on your host
2. **ubuntu** (Docker) - Prepares and caches the container
3. **ubuntu26_ssh** - Tests roles via SSH to the cached container

The script:
- Runs `molecule prepare` then `molecule converge` for each scenario
- Stops immediately if any scenario fails
- Cleans up failed scenarios automatically
- Provides detailed output for debugging

## Exit Codes

| Code | Meaning |
|------|---------|
| 0 | All scenarios passed |
| 1 | One or more scenarios failed |
| 130 | Interrupted by Ctrl+C |

## Requirements

- Python 3.6+
- Molecule installed (`pip install molecule`)
- Docker (for ubuntu scenario)
- Ansible installed
