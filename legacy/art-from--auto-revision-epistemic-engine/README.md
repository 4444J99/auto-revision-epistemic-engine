# art-from--auto-revision-epistemic-engine

**Interactive visualization of self-governing orchestration — governance as performance art**

[![CI](https://github.com/organvm-ii-poiesis/art-from--auto-revision-epistemic-engine/actions/workflows/ci.yml/badge.svg)](https://github.com/organvm-ii-poiesis/art-from--auto-revision-epistemic-engine/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![ORGAN-II](https://img.shields.io/badge/ORGAN-II-poiesis-purple)](https://github.com/organvm-ii-poiesis)

> *What if governance itself were a medium for visual art? What if the eight phases of an epistemic self-revision pipeline — observation, hypothesis, testing, refutation, revision, consolidation, propagation, audit — could be rendered as a living, breathing visual composition?*

## Overview

`art-from--auto-revision-epistemic-engine` transforms the abstract governance pipeline of [auto-revision-epistemic-engine](https://github.com/organvm-i-theoria/auto-revision-epistemic-engine) (ORGAN-I) into an interactive, browser-based visual artwork. Each phase of the eight-stage self-governing orchestration cycle becomes a visual element — a shape, a color, a motion — and the relationships between phases become compositional forces that animate the canvas in real time.

This project sits at the intersection of **institutional governance** and **generative art**. It takes the core thesis of the organvm system seriously: that the structures through which knowledge governs itself are not merely administrative scaffolding but possess an aesthetic dimension that, when made visible, reveals patterns invisible to textual description alone. The visualization is not a dashboard. It is a performance.

### Position Within the ORGAN System

| Layer | Role |
|-------|------|
| **ORGAN-I** (Theoria) | Provides the epistemic engine — the 8-phase self-revision pipeline that this project visualizes |
| **ORGAN-II** (Poiesis) | **This repository** — transforms theoretical governance structures into visual art |
| **ORGAN-IV** (Taxis) | The orchestration layer whose governance patterns are the ultimate source material |

The flow is unidirectional: ORGAN-I theorizes, ORGAN-II renders, ORGAN-IV orchestrates. No back-edges. This project reads from ORGAN-I's pipeline specification and produces visual output — it never modifies the pipeline it depicts.

## Concept

### Governance as Aesthetic Object

Traditional governance visualization focuses on legibility: Gantt charts, flowcharts, status dashboards. These instruments optimize for rapid comprehension at the cost of stripping away the temporal, rhythmic, and relational qualities of governance processes. A Gantt chart tells you *what happens when*; it cannot tell you *how it feels when a hypothesis survives refutation*, or *what the shape of consolidation looks like after three revision cycles*.

This project treats governance as a performance medium. The eight phases of the auto-revision-epistemic-engine are mapped to visual primitives:

| Phase | Color | Shape | Motion |
|-------|-------|-------|--------|
| **Observation** | Deep indigo (#1a1a4e) | Expanding circle | Slow radial pulse |
| **Hypothesis** | Electric amber (#f5a623) | Ascending triangle | Upward drift with oscillation |
| **Testing** | Bright cyan (#00d4ff) | Interlocking grid | Systematic scan pattern |
| **Refutation** | Crimson red (#dc3545) | Fracturing polygon | Shatter and scatter |
| **Revision** | Forest green (#28a745) | Reforming spiral | Inward convergence |
| **Consolidation** | Royal purple (#6f42c1) | Crystalline lattice | Slow solidification |
| **Propagation** | Solar gold (#ffc107) | Radiating wave fronts | Outward expansion |
| **Audit** | Silver grey (#adb5bd) | Enclosing ring | Steady contraction |

When the pipeline runs, these elements compose themselves on a shared canvas. Phases that are active simultaneously create visual interference patterns. The audit phase literally *encloses* whatever it examines, and propagation *pushes outward* from the center. The result is a dynamic visual composition that makes the governance process legible through spatial and chromatic logic rather than textual labels.

### Art-Theoretical Grounding

The project draws on three traditions in computational and conceptual art:

1. **Process art** (Sol LeWitt, Hans Haacke): The instruction set *is* the artwork. Here, the governance pipeline specification is the score; the visualization is the performance.
2. **Systems aesthetics** (Jack Burnham): Art that takes systems — not objects — as its medium. The eight-phase pipeline is a system; rendering it visually is an act of systems aesthetics.
3. **Algorithmic governance visualization** (an emerging field): Making the rules that govern institutional processes visible, auditable, and — critically — beautiful.

## Architecture

```
art-from--auto-revision-epistemic-engine/
├── src/
│   └── art_from_auto_revision/
│       ├── __init__.py          # Package metadata and version
│       ├── visualizer.py        # Core OrchestrationVisualizer class
│       └── server.py            # Flask application serving the visualization
├── tests/
│   └── test_visualizer.py       # Test suite (10+ tests)
├── pyproject.toml               # Package configuration
├── LICENSE                      # MIT License
├── README.md                    # This document
└── .github/
    └── workflows/
        └── ci.yml               # Continuous integration
```

### Component Responsibilities

- **`OrchestrationVisualizer`**: The core engine. Maps the 8 governance phases to visual elements (SVG primitives with color, shape, and animation attributes). Provides methods for rendering individual phases, the full pipeline, audit chains, and complete SVG output.
- **`server.py`**: A minimal Flask application that serves the visualization as an interactive web page. D3.js (loaded via CDN) handles client-side animation and interactivity; the server provides the initial SVG structure and phase data as JSON.

### Technology Stack

| Component | Technology | Rationale |
|-----------|-----------|-----------|
| Core rendering | Python + SVG generation | Programmatic control over every visual element |
| Client-side animation | D3.js (via CDN) | Industry-standard data-driven DOM manipulation |
| Server | Flask | Lightweight, sufficient for serving static + dynamic content |
| Static visualization | matplotlib | For generating publication-quality still frames |

## Installation

### Prerequisites

- Python 3.10 or later
- pip (bundled with Python)

### Setup

```bash
# Clone the repository
git clone https://github.com/organvm-ii-poiesis/art-from--auto-revision-epistemic-engine.git
cd art-from--auto-revision-epistemic-engine

# Create a virtual environment (recommended)
python -m venv .venv
source .venv/bin/activate  # macOS/Linux
# .venv\Scripts\activate   # Windows

# Install in development mode
pip install -e ".[dev]"
```

### Verify Installation

```bash
python -c "from art_from_auto_revision.visualizer import OrchestrationVisualizer; print('OK')"
```

## Usage

### Interactive Web Visualization

```bash
# Start the Flask development server
python -m art_from_auto_revision.server

# Open http://localhost:5000 in your browser
```

The web interface presents the eight governance phases as interactive visual elements. Click individual phases to isolate them; use the timeline slider to scrub through a simulated pipeline execution. The audit chain view shows how successive audit passes enclose previous pipeline runs.

### Programmatic SVG Generation

```python
from art_from_auto_revision.visualizer import OrchestrationVisualizer

viz = OrchestrationVisualizer(width=1200, height=800)

# Render a single phase
observation_svg = viz.render_phase("observation")

# Render the full 8-phase pipeline
pipeline_svg = viz.render_pipeline()

# Render an audit chain (3 successive audit passes)
audit_svg = viz.render_audit_chain(depth=3)

# Generate a complete standalone SVG document
full_svg = viz.generate_svg()

# Save to file
with open("governance-art.svg", "w") as f:
    f.write(full_svg)
```

### Static Image Export

```python
from art_from_auto_revision.visualizer import OrchestrationVisualizer

viz = OrchestrationVisualizer(width=1200, height=800)
# Uses matplotlib backend for rasterization
viz.export_png("governance-art.png", dpi=300)
```

## Visual Design

### Color System

The color palette is derived from two constraints: (1) each phase must be instantly distinguishable from its neighbors in the pipeline sequence, and (2) the overall palette must cohere as a single composition when all eight phases are active simultaneously.

The solution uses a **semantic color wheel**: cool tones (indigo, cyan) for receptive phases (observation, testing), warm tones (amber, gold) for generative phases (hypothesis, propagation), and structural tones (red, green, purple, grey) for transformative phases (refutation, revision, consolidation, audit).

### Typography and Layout

The visualization deliberately avoids textual labels in its default mode. Phase identity is communicated entirely through visual attributes — color, shape, position, motion. An optional annotation layer (toggled via the web interface) adds minimal typographic labels using the Inter typeface for technical contexts and Cormorant Garamond for conceptual captions.

### Animation Principles

1. **Phase transitions are continuous**: No jump cuts between phases. Each transition is an interpolation that makes the transformation visible.
2. **Concurrent phases produce interference**: When two phases run simultaneously, their visual elements interact — overlapping colors blend, shapes intersect, motions compound.
3. **Audit encloses**: The audit phase always renders as an enclosing ring around whatever it is auditing. This is a visual metaphor for the epistemic function of audit — it does not participate; it contains.
4. **Propagation radiates**: The propagation phase always moves outward from center. This reflects its function in the pipeline — it carries consolidated knowledge outward to downstream systems.

## How It Works

### Phase-to-Visual Mapping

The `OrchestrationVisualizer` class maintains a registry of **phase descriptors** — data objects that associate each governance phase with its visual attributes:

```python
PhaseDescriptor(
    name="observation",
    color="#1a1a4e",
    shape="circle",
    motion="radial_pulse",
    z_index=0,
    opacity_range=(0.4, 1.0),
    scale_range=(0.8, 1.2),
)
```

When `render_phase()` is called, the descriptor is resolved into an SVG element with appropriate attributes. When `render_pipeline()` is called, all eight descriptors are resolved and composed according to a layout algorithm that positions phases along a horizontal timeline (default) or a radial arrangement (alternative mode).

### Audit Chain Rendering

The `render_audit_chain(depth=N)` method generates nested enclosing rings, each representing one pass of the audit phase over the pipeline. At depth 1, a single grey ring encloses the pipeline. At depth 3, three concentric rings of increasing radius enclose it, with slight opacity variation to suggest temporal layering — the innermost ring is the most recent audit, the outermost the oldest.

### SVG Generation Pipeline

1. **Canvas initialization**: Create SVG root element with viewBox, background, and metadata.
2. **Phase rendering**: Each active phase is rendered as an SVG group (`<g>`) with its shape, color, and animation elements.
3. **Composition**: Phase groups are positioned according to the active layout algorithm.
4. **Animation embedding**: CSS `@keyframes` and SVG `<animate>` elements are injected for client-side animation.
5. **Serialization**: The complete SVG DOM is serialized to a string.

## Contributing

Contributions that extend the visual vocabulary of governance-as-art are welcome. Areas of particular interest:

- **New layout algorithms**: Radial, force-directed, treemap, and other spatial arrangements for the eight phases
- **Sonification**: Audio mapping of governance phases (complementing the visual mapping)
- **3D rendering**: WebGL/Three.js extensions for volumetric governance visualization
- **Real-time data**: Connecting the visualizer to a live orchestration pipeline via WebSocket

### Development Setup

```bash
pip install -e ".[dev]"
pytest tests/ -v
```

### Code Style

This project follows PEP 8 with type hints for all public method signatures. Use `ruff` for linting:

```bash
ruff check src/ tests/
```

## Related Projects

- [`auto-revision-epistemic-engine`](https://github.com/organvm-i-theoria/auto-revision-epistemic-engine) — The ORGAN-I theoretical engine that this project visualizes
- [`orchestration-start-here`](https://github.com/organvm-iv-taxis/orchestration-start-here) — The ORGAN-IV orchestration entry point
- [`metasystem-master`](https://github.com/organvm-ii-poiesis/metasystem-master) — The ORGAN-II flagship generative art system

## License

MIT License. See [LICENSE](LICENSE) for details.

Copyright (c) 2026 organvm-ii-poiesis

---

*Part of the [organvm](https://github.com/meta-organvm) eight-organ creative-institutional system. ORGAN-II transforms theory into art.*
