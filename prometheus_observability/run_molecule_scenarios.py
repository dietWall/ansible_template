#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Molecule Scenario Runner
========================

Runs all Molecule scenarios in the correct order with proper failure handling.
Stops immediately if any scenario fails.

Workflow order:
1. default (localhost) - quick tests on host
2. ubuntu (Docker container) - prepares and caches container
3. ubuntu26_ssh - tests roles via SSH to cached container

Each scenario runs: prepare -> converge -> (optional: verify -> syntax -> test)
"""

import subprocess
import sys
import os
from pathlib import Path

# Add script directory to path for molecule command lookup
SCRIPT_DIR = Path(__file__).parent.resolve()


class MoleculeScenarioError(Exception):
    """Custom exception for Molecule scenario failures."""
    pass


def run_command(cmd: list[str], description: str, check: bool = True) -> subprocess.CompletedProcess:
    """
    Run a shell command and return the result.

    Args:
        cmd: List of command arguments
        description: Human-readable description for error messages
        check: If True, raise exception on non-zero exit code

    Returns:
        CompletedProcess result

    Raises:
        MoleculeScenarioError: If command fails and check=True
    """
    print(f"\n{'='*60}")
    print(f"Running: {description}")
    print(f"Command: {' '.join(cmd)}")
    print(f"{'='*60}\n")

    try:
        result = subprocess.run(
            cmd,
            cwd=SCRIPT_DIR,
            check=check,
            text=True,
            capture_output=False,  # Print stdout/stderr directly
            env={**os.environ, "MOLECULE_PROJECT_DIRECTORY": str(SCRIPT_DIR)}
        )

        if result.returncode != 0:
            print(f"\n❌ FAILED: {description}")
            raise MoleculeScenarioError(f"Command failed with exit code {result.returncode}")

        return result

    except subprocess.CalledProcessError as e:
        print(f"\n❌ Command failed: {description}")
        print(f"Exit code: {e.returncode}")
        if e.output:
            print(e.output)
        raise


def run_default_scenario():
    """
    Run the default (localhost) scenario.

    This is a quick test scenario that runs on the host machine.
    No Docker container is needed.
    """
    print("\n" + "="*60)
    print("SCENARIO: default (localhost)")
    print("="*60)
    print("Description: Quick tests on host machine (no Docker)")
    print("="*60)

    # Get detailed setting from environment
    demo_detailed = os.environ.get("DEMO_DETAILED", "false").lower() == "true"

    if demo_detailed:
        print("\n[INFO] Running with detailed output enabled")

    try:
        # 1. Syntax check
        run_command(
            ["molecule", "syntax", "-s", "default"],
            "Syntax check for default scenario"
        )

        # 2. Create containers (empty for localhost)
        run_command(
            ["molecule", "create", "-s", "default"],
            "Create scenario default"
        )

        # 3. Prepare (no prepare playbook for localhost)
        run_command(
            ["molecule", "prepare", "-s", "default"],
            "Prepare scenario default"
        )

        # 4. Converge
        run_command(
            ["molecule", "converge", "-s", "default"],
            "Converge scenario default"
        )

        print("\n✅ SUCCESS: default (localhost) scenario completed")
        return True

    except MoleculeScenarioError as e:
        print(f"\n❌ FAILED: default (localhost) scenario - {e}")
        return False


def run_ubuntu_scenario():
    """
    Run the ubuntu (Docker container) scenario.

    This scenario prepares and caches the Docker container with:
    - SSH server installation
    - Ubuntu user configuration
    - Systemd enabled
    - Cgroup filesystem mounted

    The container is cached as 'ubuntu26-sandbox' for reuse.
    """
    print("\n" + "="*60)
    print("SCENARIO: ubuntu (Docker container preparation)")
    print("="*60)
    print("Description: Creates and configures Docker container")
    print("="*60)

    # Get detailed setting from environment
    demo_detailed = os.environ.get("DEMO_DETAILED", "false").lower() == "true"

    if demo_detailed:
        print("\n[INFO] Running with detailed output enabled")

    try:
        # 1. Create containers (pulls image, creates container)
        print("\n[INFO] Creating Docker container...")
        run_command(
            ["molecule", "create", "-s", "ubuntu"],
            "Create scenario ubuntu"
        )

        # 2. Prepare (runs container, installs SSH, configures user)
        print("\n[INFO] Preparing Docker container...")
        run_command(
            ["molecule", "prepare", "-s", "ubuntu"],
            "Prepare scenario ubuntu (installs SSH, configures user)"
        )

        # 3. Converge (runs demo role in container)
        print("\n[INFO] Converging Docker container...")
        run_command(
            ["molecule", "converge", "-s", "ubuntu"],
            "Converge scenario ubuntu (runs demo role)"
        )

        print("\n✅ SUCCESS: ubuntu (Docker container) scenario completed")
        print("[INFO] Container cached as 'ubuntu26-sandbox' for reuse")
        return True

    except MoleculeScenarioError as e:
        print(f"\n❌ FAILED: ubuntu (Docker container) scenario - {e}")
        print("[INFO] Cleanup: Destroying container due to failure")
        try:
            run_command(
                ["molecule", "destroy", "-s", "ubuntu"],
                "Destroy ubuntu scenario (cleanup)"
            )
        except:
            pass
        return False


def run_ubuntu26_ssh_scenario():
    """
    Run the ubuntu26_ssh scenario.

    This scenario uses the cached Docker container via SSH to test
    roles from the roles/ directory.

    Uses the cached container from the 'ubuntu' scenario.
    """
    print("\n" + "="*60)
    print("SCENARIO: ubuntu26_ssh (SSH role testing)")
    print("="*60)
    print("Description: Tests roles via SSH to cached Docker container")
    print("="*60)

    # Get detailed setting from environment
    demo_detailed = os.environ.get("DEMO_DETAILED", "false").lower() == "true"

    if demo_detailed:
        print("\n[INFO] Running with detailed output enabled")

    try:
        # 1. Verify container is ready
        print("\n[INFO] Verifying cached container exists...")
        result = subprocess.run(
            ["docker", "ps", "-a", "-q", "-f", "name=ubuntu26-sandbox"],
            cwd=SCRIPT_DIR,
            capture_output=True,
            text=True
        )

        if result.returncode != 0 or not result.stdout.strip():
            raise MoleculeScenarioError(
                "Cached container 'ubuntu26-sandbox' not found. "
                "Please run 'molecule prepare -s ubuntu' and "
                "'molecule converge -s ubuntu' first."
            )
        print("✓ Cached container found and running")

        # 2. Prepare (minimal preparation using cached container)
        run_command(
            ["molecule", "prepare", "-s", "ubuntu26_ssh"],
            "Prepare scenario ubuntu26_ssh"
        )

        # 3. Converge (runs demo + ssh_keys roles via SSH)
        run_command(
            ["molecule", "converge", "-s", "ubuntu26_ssh"],
            "Converge scenario ubuntu26_ssh (runs demo + ssh_keys roles)"
        )

        print("\n✅ SUCCESS: ubuntu26_ssh (SSH role testing) scenario completed")
        return True

    except MoleculeScenarioError as e:
        print(f"\n❌ FAILED: ubuntu26_ssh (SSH role testing) scenario - {e}")
        print("[INFO] Cleanup: Destroying scenario due to failure")
        try:
            run_command(
                ["molecule", "destroy", "-s", "ubuntu26_ssh"],
                "Destroy ubuntu26_ssh scenario (cleanup)"
            )
        except:
            pass
        return False


def main():
    """
    Main entry point for the Molecule scenario runner.

    Runs scenarios in the correct order:
    1. default (localhost) - quick tests
    2. ubuntu (Docker) - prepares and caches container
    3. ubuntu26_ssh - SSH role testing

    Stops immediately if any scenario fails.
    """
    print("="*60)
    print("  Molecule Scenario Runner")
    print("="*60)
    print()
    print("This script runs Molecule scenarios in the correct order:")
    print("  1. default  -> Quick tests on host (localhost)")
    print("  2. ubuntu   -> Docker container preparation & cache")
    print("  3. ubuntu26_ssh -> SSH role testing (uses cached container)")
    print()
    print("="*60)

    # Check for DEMO_DETAILED environment variable
    demo_detailed = os.environ.get("DEMO_DETAILED", "false").lower() == "true"
    if demo_detailed:
        print("\n[INFO] Running with detailed output enabled (DEMO_DETAILED=true)")

    all_success = True

    # Run default scenario first
    print("\n" + "-"*60)
    print("Starting scenario execution...")
    print("-"*60)

    if not run_default_scenario():
        print("\n❌ Overall execution FAILED at default scenario")
        sys.exit(1)

    # Run ubuntu scenario second (prepares and caches container)
    if not run_ubuntu_scenario():
        print("\n❌ Overall execution FAILED at ubuntu scenario")
        sys.exit(1)

    # Run ubuntu26_ssh scenario third (uses cached container)
    if not run_ubuntu26_ssh_scenario():
        print("\n❌ Overall execution FAILED at ubuntu26_ssh scenario")
        sys.exit(1)

    print("\n" + "="*60)
    print("✅ ALL SCENARIOS COMPLETED SUCCESSFULLY!")
    print("="*60)
    print()
    print("Summary:")
    print("  ✓ default (localhost) - Quick tests on host")
    print("  ✓ ubuntu (Docker)      - Container prepared and cached")
    print("  ✓ ubuntu26_ssh         - SSH role testing completed")
    print("="*60)

    sys.exit(0)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Execution interrupted by user (Ctrl+C)")
        print("Cleaning up...")
        try:
            run_command(
                ["molecule", "destroy", "-s", "default", "ubuntu", "ubuntu26_ssh"],
                "Destroy all scenarios (cleanup on interrupt)",
                check=False
            )
        except:
            pass
        sys.exit(130)  # Standard exit code for Ctrl+C
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1)
