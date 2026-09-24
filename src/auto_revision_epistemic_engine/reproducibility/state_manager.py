"""
State Manager for reproducibility with pinned models, seeds, and immutable state
"""

import json
import random
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Optional
from pydantic import BaseModel, Field
import blake3


class ReproducibilityConfig(BaseModel):
    """Configuration for reproducibility"""
    random_seed: int
    model_pins: Dict[str, str] = Field(default_factory=dict)
    environment_snapshot: Dict[str, Any] = Field(default_factory=dict)
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class ImmutableState(BaseModel):
    """Immutable state snapshot"""
    state_id: str
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    phase: str
    data: Dict[str, Any]
    config_hash: str
    state_hash: str = ""

    def compute_hash(self) -> str:
        """Compute BLAKE3 hash for this state"""
        data = {
            "state_id": self.state_id,
            "timestamp": self.timestamp,
            "phase": self.phase,
            "data": self.data,
            "config_hash": self.config_hash,
        }
        hasher = blake3.blake3(json.dumps(data, sort_keys=True).encode())
        return hasher.hexdigest()


class StateManager:
    """
    Manages reproducibility through pinned models, seeds, and immutable state snapshots.
    Ensures that executions can be exactly reproduced with the same configuration.
    """

    def __init__(
        self,
        state_dir: str = "./state_snapshots",
        random_seed: Optional[int] = None,
    ):
        self.state_dir = Path(state_dir)
        self.state_dir.mkdir(parents=True, exist_ok=True)
        
        # Initialize reproducibility config
        self.config = ReproducibilityConfig(
            random_seed=random_seed if random_seed is not None else self._generate_seed(),
        )
        
        # Apply random seed
        random.seed(self.config.random_seed)
        
        # State tracking
        self._states: Dict[str, ImmutableState] = {}
        self._recompute_config_hash()
        self._save_config()

    def _generate_seed(self) -> int:
        """Generate a reproducible seed based on timestamp"""
        return int(datetime.now(timezone.utc).timestamp() * 1000000) % (2**32)

    def _recompute_config_hash(self):
        """Recompute BLAKE3 hash from the current serialized reproducibility config"""
        self.config_hash = blake3.blake3(
            self.config.model_dump_json().encode()
        ).hexdigest()

    def _save_config(self):
        """Save reproducibility configuration"""
        self._recompute_config_hash()
        config_file = self.state_dir / "reproducibility_config.json"
        with open(config_file, "w") as f:
            config_dict = self.config.model_dump()
            config_dict["config_hash"] = self.config_hash
            json.dump(config_dict, f, indent=2)

    def pin_model(self, model_name: str, version: str):
        """
        Pin a model to a specific version for reproducibility.

        Args:
            model_name: Name of the model
            version: Version identifier (hash, tag, or version number)
        """
        self.config.model_pins[model_name] = version
        self._save_config()

    def set_environment_var(self, key: str, value: Any):
        """
        Set an environment variable in the reproducibility config.

        Args:
            key: Variable name
            value: Variable value
        """
        self.config.environment_snapshot[key] = value
        self._save_config()

    def create_snapshot(
        self,
        state_id: str,
        phase: str,
        data: Dict[str, Any],
    ) -> ImmutableState:
        """
        Create an immutable state snapshot.

        Args:
            state_id: Unique identifier for this state
            phase: Phase name
            data: State data to snapshot

        Returns:
            ImmutableState: The created immutable state
        """
        state = ImmutableState(
            state_id=state_id,
            phase=phase,
            data=data,
            config_hash=self.config_hash,
        )
        state.state_hash = state.compute_hash()
        
        # Store in memory
        self._states[state_id] = state
        
        # Persist to disk
        state_file = self.state_dir / f"state_{state_id}.json"
        with open(state_file, "w") as f:
            json.dump(state.model_dump(), f, indent=2)
        
        return state

    def get_snapshot(self, state_id: str) -> Optional[ImmutableState]:
        """
        Retrieve a state snapshot by ID.

        Args:
            state_id: State identifier

        Returns:
            Optional[ImmutableState]: The state if found, None otherwise
        """
        # Check memory first
        if state_id in self._states:
            return self._states[state_id]
        
        # Check disk
        state_file = self.state_dir / f"state_{state_id}.json"
        if state_file.exists():
            with open(state_file, "r") as f:
                data = json.load(f)
                state = ImmutableState(**data)
                self._states[state_id] = state
                return state
        
        return None

    def verify_snapshot(self, state_id: str) -> bool:
        """
        Verify the integrity of a state snapshot.

        Args:
            state_id: State identifier

        Returns:
            bool: True if snapshot is valid, False otherwise
        """
        state = self.get_snapshot(state_id)
        if not state:
            return False
        
        expected_hash = state.compute_hash()
        return state.state_hash == expected_hash

    def get_reproducibility_info(self) -> Dict[str, Any]:
        """
        Get reproducibility information.

        Returns:
            Dict with reproducibility configuration and status
        """
        return {
            "config_hash": self.config_hash,
            "random_seed": self.config.random_seed,
            "model_pins": self.config.model_pins,
            "environment_snapshot": self.config.environment_snapshot,
            "timestamp": self.config.timestamp,
            "snapshots_count": len(self._states),
        }

    def load_config(self, config_path: str) -> bool:
        """
        Load a reproducibility configuration from file.

        Args:
            config_path: Path to configuration file

        Returns:
            bool: True if loaded successfully
        """
        try:
            with open(config_path, "r") as f:
                config_dict = json.load(f)
                # Remove config_hash as it will be recomputed
                config_dict.pop("config_hash", None)
                self.config = ReproducibilityConfig(**config_dict)
                
                # Apply random seed
                random.seed(self.config.random_seed)
                
                # Save config to sync disk and recompute hash
                self._save_config()
                
                return True
        except Exception:
            return False

    def get_all_snapshots(self) -> Dict[str, ImmutableState]:
        """
        Get all state snapshots.

        Returns:
            Dict mapping state IDs to ImmutableState objects
        """
        # Load all snapshots from disk if not in memory
        for state_file in self.state_dir.glob("state_*.json"):
            state_id = state_file.stem.replace("state_", "")
            if state_id not in self._states:
                with open(state_file, "r") as f:
                    data = json.load(f)
                    self._states[state_id] = ImmutableState(**data)
        
        return self._states
