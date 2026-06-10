#!/bin/bash
# Molecule test wrapper for ansible_foundation project
# Usage: ./molecule_test.sh [command]
# Example: ./molecule_test.sh test

cd "$(dirname "$0")/prometheus_observability"
source ../venv/bin/activate
exec molecule "$@"
