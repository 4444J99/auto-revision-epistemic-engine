import json
from pathlib import Path

import blake3

from auto_revision_epistemic_engine.reproducibility.state_manager import StateManager


def test_config_hash_updates_on_pinned_configuration_changes(tmp_path: Path):
    """
    Verify that when model pins or environment variables change:
    1. Memory and persisted config_hash are updated to match the BLAKE3 hash of config serialized json.
    2. Identical repeated assignment remains stable.
    3. Old snapshots retain their original config_hash while new snapshots get the refreshed config_hash.
    4. Save/load round-trip retains the exact updated config_hash.
    """
    state_dir = tmp_path / "state_snapshots"
    fixed_seed = 42
    mgr = StateManager(state_dir=str(state_dir), random_seed=fixed_seed)

    initial_hash = mgr.config_hash
    assert initial_hash == blake3.blake3(mgr.config.model_dump_json().encode()).hexdigest()

    # Create initial snapshot (historical snapshot)
    snap1 = mgr.create_snapshot("snap_1", "phase_1", {"key": "val1"})
    assert snap1.config_hash == initial_hash

    # Pin a new model
    mgr.pin_model("gpt-4", "v1.0")

    expected_hash_2 = blake3.blake3(mgr.config.model_dump_json().encode()).hexdigest()
    assert expected_hash_2 != initial_hash, "Config hash should change when model is pinned"

    # Memory check
    assert mgr.config_hash == expected_hash_2, f"Expected {expected_hash_2}, got {mgr.config_hash}"

    # Persisted check
    config_file = state_dir / "reproducibility_config.json"
    with open(config_file, "r") as f:
        persisted_config = json.load(f)
    assert persisted_config["config_hash"] == expected_hash_2

    # Identical repeated assignment remains stable
    mgr.pin_model("gpt-4", "v1.0")
    assert mgr.config_hash == expected_hash_2

    # Set environment variable
    mgr.set_environment_var("ENV_MODE", "test")
    expected_hash_3 = blake3.blake3(mgr.config.model_dump_json().encode()).hexdigest()
    assert expected_hash_3 != expected_hash_2
    assert mgr.config_hash == expected_hash_3

    # New snapshot references new hash
    snap2 = mgr.create_snapshot("snap_2", "phase_2", {"key": "val2"})
    assert snap2.config_hash == expected_hash_3

    # Historical snapshot retains original hash
    snap1_reloaded = mgr.get_snapshot("snap_1")
    assert snap1_reloaded is not None
    assert snap1_reloaded.config_hash == initial_hash

    # Save/load round trip retains exact hash
    mgr_loaded = StateManager(state_dir=str(tmp_path / "other_state"), random_seed=fixed_seed)
    success = mgr_loaded.load_config(str(config_file))
    assert success is True
    assert mgr_loaded.config_hash == expected_hash_3
