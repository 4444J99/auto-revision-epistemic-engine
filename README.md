# Auto-Revision Epistemic Engine

Self-governing orchestration framework with 8 phases, 4 human review gates, BLAKE3 audit chain, and ethical axiom enforcement.

[![CI](https://github.com/4444J99/auto-revision-epistemic-engine/actions/workflows/ci.yml/badge.svg)](https://github.com/4444J99/auto-revision-epistemic-engine/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-%E2%89%A53.8-blue)]()

## Overview

The Auto-Revision Epistemic Engine (ARE) formalizes how autonomous AI/ML pipelines should audit, constrain, and justify their own execution. Eight sequential phases, four human review gates (HRGs) with SLAs and escalation, an append-only BLAKE3-hashed audit chain, ethical axiom enforcement (BLOCK/WARN/LOG), and full reproducibility via pinned models, seeds, and immutable state snapshots.

See [DOCUMENTATION.md](DOCUMENTATION.md) for the full feature set, architecture, and API reference. See [FINAL_MERGE_REPORT.md](FINAL_MERGE_REPORT.md) for the consolidated production-ready status.

## Installation

```bash
git clone https://github.com/4444J99/auto-revision-epistemic-engine.git
cd auto-revision-epistemic-engine
pip install -r requirements.txt
pip install -e .
```

## Quick Start

```python
from auto_revision_epistemic_engine import AutoRevisionEngine

engine = AutoRevisionEngine(
    pipeline_id="example",
    random_seed=42,
    enable_hrg=True,
    enable_ethics_audit=True,
    enable_resource_tracking=True,
)

engine.pin_model("gpt-4", "20240101_snapshot")
result = engine.execute(inputs={"data": {"records": 100}})
status = engine.get_status()
print(status["completed"], status["audit_chain_valid"])
```

See `examples/basic_usage.py` for a complete demonstration.

## License

MIT. See [LICENSE](LICENSE).

---

<sub>Part of the ORGANVM system. Green progress receipt: restored after placeholder on successful stale-issues workflow (exact-head 559929d).</sub>
