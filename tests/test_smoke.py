#!/usr/bin/env python3
"""
Automated smoke test for auto-revision-epistemic-engine installation and entrypoints.
"""

import subprocess
import sys


def run_cmd(cmd):
    print(f"Running: {' '.join(cmd)}")
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        print(f"FAILED: {res.stderr}")
        sys.exit(res.returncode)
    print("SUCCESS")
    return res.stdout


def run_smoke_test():
    print("=== Epistemic Engine Smoke Test ===")

    # Test 1: Python module import
    print("Testing Python import...")
    import auto_revision_epistemic_engine
    print(f"Imported version: {auto_revision_epistemic_engine.__version__}")

    # Test 2: CLI entry point -- auto-revision-engine demo
    run_cmd(["auto-revision-engine", "demo"])

    # Test 3: CLI entry point -- auto-revision-epistemic-engine demo
    run_cmd(["auto-revision-epistemic-engine", "demo"])

    # Test 4: CLI run command
    run_cmd(["auto-revision-engine", "run", "--seed", "123", "--inputs", '{"data": {"test": true}}'])

    # Test 5: CLI audit command
    run_cmd(["auto-revision-engine", "audit", "--after-run"])

    print("=== All Smoke Tests Passed Successfully ===")


def test_smoke():
    """Pytest hook for automated smoke testing."""
    run_smoke_test()


if __name__ == "__main__":
    run_smoke_test()
