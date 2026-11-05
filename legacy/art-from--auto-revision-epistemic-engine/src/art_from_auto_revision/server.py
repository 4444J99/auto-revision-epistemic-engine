"""Flask application serving the orchestration visualization.

Run with: python -m art_from_auto_revision.server
"""

from __future__ import annotations

import json

from flask import Flask, Response, render_template_string

from art_from_auto_revision.visualizer import (
    PHASE_DESCRIPTORS,
    OrchestrationVisualizer,
)

app = Flask(__name__)

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Governance as Performance Art</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { background: #0d1117; color: #c9d1d9; font-family: Inter, sans-serif; }
        header { text-align: center; padding: 1.5rem; }
        header h1 { font-size: 1.4rem; font-weight: 300; letter-spacing: 0.1em; }
        header p { font-size: 0.85rem; opacity: 0.6; margin-top: 0.3rem; }
        #canvas-container { display: flex; justify-content: center; padding: 1rem; }
        #phase-legend { display: flex; justify-content: center; gap: 1.2rem;
                        padding: 1rem; flex-wrap: wrap; }
        .legend-item { display: flex; align-items: center; gap: 0.4rem;
                       font-size: 0.8rem; cursor: pointer; opacity: 0.8; }
        .legend-item:hover { opacity: 1; }
        .legend-swatch { width: 12px; height: 12px; border-radius: 2px; }
    </style>
    <script src="https://d3js.org/d3.v7.min.js"></script>
</head>
<body>
    <header>
        <h1>GOVERNANCE AS PERFORMANCE ART</h1>
        <p>8-Phase Orchestration Pipeline &mdash; auto-revision-epistemic-engine</p>
    </header>
    <div id="canvas-container">{{ svg_content | safe }}</div>
    <div id="phase-legend">
        {% for phase in phases %}
        <div class="legend-item" data-phase="{{ phase.name }}">
            <div class="legend-swatch" style="background: {{ phase.color }};"></div>
            <span>{{ phase.name }}</span>
        </div>
        {% endfor %}
    </div>
    <script>
        const phases = {{ phases_json | safe }};
        document.querySelectorAll('.legend-item').forEach(item => {
            item.addEventListener('click', () => {
                const name = item.dataset.phase;
                const el = document.getElementById('phase-' + name);
                if (el) {
                    const current = el.style.opacity;
                    el.style.opacity = (current === '0.1') ? '1' : '0.1';
                }
            });
        });
    </script>
</body>
</html>"""


@app.route("/")
def index() -> str:
    """Serve the main visualization page."""
    viz = OrchestrationVisualizer()
    svg_content = viz.generate_svg()
    phases_data = [{"name": p.name, "color": p.color} for p in PHASE_DESCRIPTORS]
    return render_template_string(
        HTML_TEMPLATE,
        svg_content=svg_content,
        phases=phases_data,
        phases_json=json.dumps(phases_data),
    )


@app.route("/svg")
def raw_svg() -> Response:
    """Return the raw SVG document."""
    viz = OrchestrationVisualizer()
    return Response(viz.generate_svg(), mimetype="image/svg+xml")


@app.route("/api/phases")
def api_phases() -> Response:
    """Return phase descriptors as JSON."""
    data = [
        {
            "name": p.name,
            "color": p.color,
            "shape": p.shape,
            "motion": p.motion,
            "z_index": p.z_index,
        }
        for p in PHASE_DESCRIPTORS
    ]
    return Response(json.dumps(data, indent=2), mimetype="application/json")


def main() -> None:
    """Entry point for running the server directly."""
    app.run(debug=True, host="127.0.0.1", port=5000)


if __name__ == "__main__":
    main()
