#!/bin/bash
# Setup script for Ansible Molecule project
# Creates virtual environment and installs dependencies

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="${SCRIPT_DIR}/venv"

echo "=== Creating virtual environment ==="
python3 -m venv "${VENV_DIR}"

echo ""
echo "=== Activating virtual environment ==="
source "${VENV_DIR}/bin/activate"

echo ""
echo "=== Installing dependencies ==="
pip install --upgrade pip
pip install molecule molecule-docker

echo ""
echo "=== Installing Galaxy collections ==="
if [ -f "${SCRIPT_DIR}/requirements.yml" ]; then
    ansible-galaxy install -r "${SCRIPT_DIR}/requirements.yml"
else
    echo "No requirements.yml found, skipping Galaxy collections"
fi

echo ""
echo "=== Setup complete! ==="
echo ""
echo "To run tests, use:"
echo "  molecule test -s default        # Localhost scenario"
echo "  molecule test -s ubuntu         # Docker container scenario"
echo "  molecule test -s ubuntu26_ssh   # SSH-based role testing"
