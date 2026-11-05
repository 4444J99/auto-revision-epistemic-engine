"""Core visualization engine for governance-as-art.

Maps the 8 phases of the auto-revision-epistemic-engine pipeline
to visual elements (colors, shapes, animations) and composes them
into SVG artwork.
"""

from __future__ import annotations

import xml.etree.ElementTree as ET
from dataclasses import dataclass, field
from typing import Literal


ShapeName = Literal[
    "circle", "triangle", "grid", "polygon", "spiral", "lattice", "wave", "ring"
]

MotionName = Literal[
    "radial_pulse",
    "upward_drift",
    "systematic_scan",
    "shatter",
    "inward_convergence",
    "solidification",
    "outward_expansion",
    "steady_contraction",
]


@dataclass(frozen=True)
class PhaseDescriptor:
    """Visual descriptor for a single governance phase."""

    name: str
    color: str
    shape: ShapeName
    motion: MotionName
    z_index: int = 0
    opacity_range: tuple[float, float] = (0.4, 1.0)
    scale_range: tuple[float, float] = (0.8, 1.2)


# The canonical 8-phase palette — order matters.
PHASE_DESCRIPTORS: tuple[PhaseDescriptor, ...] = (
    PhaseDescriptor(
        name="observation",
        color="#1a1a4e",
        shape="circle",
        motion="radial_pulse",
        z_index=0,
    ),
    PhaseDescriptor(
        name="hypothesis",
        color="#f5a623",
        shape="triangle",
        motion="upward_drift",
        z_index=1,
    ),
    PhaseDescriptor(
        name="testing",
        color="#00d4ff",
        shape="grid",
        motion="systematic_scan",
        z_index=2,
    ),
    PhaseDescriptor(
        name="refutation",
        color="#dc3545",
        shape="polygon",
        motion="shatter",
        z_index=3,
    ),
    PhaseDescriptor(
        name="revision",
        color="#28a745",
        shape="spiral",
        motion="inward_convergence",
        z_index=4,
    ),
    PhaseDescriptor(
        name="consolidation",
        color="#6f42c1",
        shape="lattice",
        motion="solidification",
        z_index=5,
    ),
    PhaseDescriptor(
        name="propagation",
        color="#ffc107",
        shape="wave",
        motion="outward_expansion",
        z_index=6,
    ),
    PhaseDescriptor(
        name="audit",
        color="#adb5bd",
        shape="ring",
        motion="steady_contraction",
        z_index=7,
    ),
)

PHASE_NAMES: tuple[str, ...] = tuple(p.name for p in PHASE_DESCRIPTORS)

_PHASE_MAP: dict[str, PhaseDescriptor] = {p.name: p for p in PHASE_DESCRIPTORS}


@dataclass
class OrchestrationVisualizer:
    """Renders the 8-phase governance pipeline as SVG artwork.

    Parameters
    ----------
    width : int
        Canvas width in pixels (SVG viewBox units).
    height : int
        Canvas height in pixels (SVG viewBox units).
    background : str
        Background color for the SVG canvas.
    """

    width: int = 1200
    height: int = 800
    background: str = "#0d1117"
    _active_phases: list[str] = field(default_factory=lambda: list(PHASE_NAMES))

    # ------------------------------------------------------------------ #
    # Public API                                                          #
    # ------------------------------------------------------------------ #

    def get_phase_descriptor(self, phase_name: str) -> PhaseDescriptor:
        """Return the visual descriptor for a named phase.

        Raises
        ------
        ValueError
            If *phase_name* is not one of the 8 canonical phases.
        """
        if phase_name not in _PHASE_MAP:
            raise ValueError(
                f"Unknown phase '{phase_name}'. Valid phases: {', '.join(PHASE_NAMES)}"
            )
        return _PHASE_MAP[phase_name]

    def render_phase(self, phase_name: str) -> str:
        """Render a single governance phase as an SVG fragment (``<g>`` element)."""
        desc = self.get_phase_descriptor(phase_name)
        g = self._build_phase_group(desc, index=PHASE_NAMES.index(phase_name))
        return ET.tostring(g, encoding="unicode")

    def render_pipeline(self) -> str:
        """Render the full 8-phase pipeline as composed SVG groups."""
        root = ET.Element("g", {"id": "pipeline"})
        for i, name in enumerate(PHASE_NAMES):
            desc = _PHASE_MAP[name]
            group = self._build_phase_group(desc, index=i)
            root.append(group)
        return ET.tostring(root, encoding="unicode")

    def render_audit_chain(self, depth: int = 1) -> str:
        """Render *depth* successive audit enclosing rings.

        Each ring is concentrically larger, with decreasing opacity
        to suggest temporal layering (innermost = most recent).
        """
        if depth < 1:
            raise ValueError("Audit chain depth must be >= 1")
        audit = _PHASE_MAP["audit"]
        g = ET.Element("g", {"id": "audit-chain"})
        cx = self.width / 2
        cy = self.height / 2
        base_radius = min(self.width, self.height) * 0.35
        for level in range(depth):
            r = base_radius + level * 30
            opacity = max(0.2, 1.0 - level * 0.25)
            circle = ET.SubElement(
                g,
                "circle",
                {
                    "cx": str(cx),
                    "cy": str(cy),
                    "r": str(r),
                    "fill": "none",
                    "stroke": audit.color,
                    "stroke-width": "2",
                    "opacity": str(round(opacity, 2)),
                },
            )
            circle.set("class", f"audit-ring-{level}")
        return ET.tostring(g, encoding="unicode")

    def generate_svg(self) -> str:
        """Generate a complete standalone SVG document."""
        svg = ET.Element(
            "svg",
            {
                "xmlns": "http://www.w3.org/2000/svg",
                "viewBox": f"0 0 {self.width} {self.height}",
                "width": str(self.width),
                "height": str(self.height),
            },
        )

        # Background
        ET.SubElement(
            svg,
            "rect",
            {
                "width": str(self.width),
                "height": str(self.height),
                "fill": self.background,
            },
        )

        # Style block with animations
        style = ET.SubElement(svg, "style")
        style.text = self._build_css_animations()

        # Title and metadata
        title = ET.SubElement(svg, "title")
        title.text = "Governance as Performance Art — 8-Phase Orchestration Pipeline"

        # Pipeline phases
        pipeline = ET.fromstring(self.render_pipeline())
        svg.append(pipeline)

        # Default single-depth audit ring
        audit_chain = ET.fromstring(self.render_audit_chain(depth=1))
        svg.append(audit_chain)

        return ET.tostring(svg, encoding="unicode", xml_declaration=True)

    def get_phase_color(self, phase_name: str) -> str:
        """Return the hex color for a phase."""
        return self.get_phase_descriptor(phase_name).color

    def get_all_colors(self) -> dict[str, str]:
        """Return a mapping of phase names to their hex colors."""
        return {p.name: p.color for p in PHASE_DESCRIPTORS}

    def get_phase_count(self) -> int:
        """Return the number of governance phases (always 8)."""
        return len(PHASE_DESCRIPTORS)

    # ------------------------------------------------------------------ #
    # Private helpers                                                     #
    # ------------------------------------------------------------------ #

    def _build_phase_group(self, desc: PhaseDescriptor, index: int) -> ET.Element:
        """Build an SVG ``<g>`` element for a single phase."""
        spacing = self.width / (len(PHASE_DESCRIPTORS) + 1)
        cx = spacing * (index + 1)
        cy = self.height / 2

        g = ET.Element(
            "g",
            {
                "id": f"phase-{desc.name}",
                "class": f"phase {desc.motion}",
                "data-phase": desc.name,
                "data-color": desc.color,
            },
        )

        shape_builders = {
            "circle": self._svg_circle,
            "triangle": self._svg_triangle,
            "grid": self._svg_grid,
            "polygon": self._svg_polygon,
            "spiral": self._svg_spiral,
            "lattice": self._svg_lattice,
            "wave": self._svg_wave,
            "ring": self._svg_ring,
        }

        builder = shape_builders[desc.shape]
        element = builder(cx, cy, desc.color)
        g.append(element)

        return g

    def _svg_circle(self, cx: float, cy: float, color: str) -> ET.Element:
        return ET.Element(
            "circle",
            {"cx": str(cx), "cy": str(cy), "r": "40", "fill": color, "opacity": "0.85"},
        )

    def _svg_triangle(self, cx: float, cy: float, color: str) -> ET.Element:
        points = f"{cx},{cy - 45} {cx - 39},{cy + 22} {cx + 39},{cy + 22}"
        return ET.Element(
            "polygon", {"points": points, "fill": color, "opacity": "0.85"}
        )

    def _svg_grid(self, cx: float, cy: float, color: str) -> ET.Element:
        g = ET.Element("g")
        size = 15
        for row in range(-1, 2):
            for col in range(-1, 2):
                ET.SubElement(
                    g,
                    "rect",
                    {
                        "x": str(cx + col * (size + 4) - size / 2),
                        "y": str(cy + row * (size + 4) - size / 2),
                        "width": str(size),
                        "height": str(size),
                        "fill": color,
                        "opacity": "0.7",
                    },
                )
        return g

    def _svg_polygon(self, cx: float, cy: float, color: str) -> ET.Element:
        import math

        sides = 6
        r = 40
        points = " ".join(
            f"{cx + r * math.cos(2 * math.pi * i / sides - math.pi / 2)},"
            f"{cy + r * math.sin(2 * math.pi * i / sides - math.pi / 2)}"
            for i in range(sides)
        )
        return ET.Element(
            "polygon", {"points": points, "fill": color, "opacity": "0.85"}
        )

    def _svg_spiral(self, cx: float, cy: float, color: str) -> ET.Element:
        import math

        path_data = f"M {cx} {cy}"
        for i in range(1, 80):
            angle = i * 0.15
            r = i * 0.6
            x = cx + r * math.cos(angle)
            y = cy + r * math.sin(angle)
            path_data += f" L {x:.1f} {y:.1f}"
        return ET.Element(
            "path",
            {"d": path_data, "fill": "none", "stroke": color, "stroke-width": "2.5"},
        )

    def _svg_lattice(self, cx: float, cy: float, color: str) -> ET.Element:
        g = ET.Element("g")
        offsets = [(-30, -20), (0, -35), (30, -20), (-15, 10), (15, 10), (0, 35)]
        for ox, oy in offsets:
            ET.SubElement(
                g,
                "circle",
                {
                    "cx": str(cx + ox),
                    "cy": str(cy + oy),
                    "r": "8",
                    "fill": color,
                    "opacity": "0.8",
                },
            )
        # Connecting lines
        for i, (ox1, oy1) in enumerate(offsets):
            for ox2, oy2 in offsets[i + 1 :]:
                dist = ((ox1 - ox2) ** 2 + (oy1 - oy2) ** 2) ** 0.5
                if dist < 45:
                    ET.SubElement(
                        g,
                        "line",
                        {
                            "x1": str(cx + ox1),
                            "y1": str(cy + oy1),
                            "x2": str(cx + ox2),
                            "y2": str(cy + oy2),
                            "stroke": color,
                            "stroke-width": "1",
                            "opacity": "0.4",
                        },
                    )
        return g

    def _svg_wave(self, cx: float, cy: float, color: str) -> ET.Element:
        import math

        g = ET.Element("g")
        for ring in range(3):
            r = 20 + ring * 15
            points = " ".join(
                f"{cx + r * math.cos(2 * math.pi * i / 36)},"
                f"{cy + r * math.sin(2 * math.pi * i / 36)}"
                for i in range(37)
            )
            ET.SubElement(
                g,
                "polyline",
                {
                    "points": points,
                    "fill": "none",
                    "stroke": color,
                    "stroke-width": "2",
                    "opacity": str(round(0.9 - ring * 0.2, 2)),
                },
            )
        return g

    def _svg_ring(self, cx: float, cy: float, color: str) -> ET.Element:
        return ET.Element(
            "circle",
            {
                "cx": str(cx),
                "cy": str(cy),
                "r": "40",
                "fill": "none",
                "stroke": color,
                "stroke-width": "3",
                "opacity": "0.9",
            },
        )

    def _build_css_animations(self) -> str:
        """Generate CSS @keyframes for each motion type."""
        return """
            .radial_pulse { animation: pulse 3s ease-in-out infinite; }
            .upward_drift { animation: drift 4s ease-in-out infinite; }
            .systematic_scan { animation: scan 2.5s linear infinite; }
            .shatter { animation: shake 0.5s ease-in-out infinite; }
            .inward_convergence { animation: converge 3s ease-in-out infinite; }
            .solidification { animation: solidify 5s ease-in-out infinite; }
            .outward_expansion { animation: expand 4s ease-in-out infinite; }
            .steady_contraction { animation: contract 3s ease-in-out infinite; }

            @keyframes pulse { 0%,100% { transform: scale(1); } 50% { transform: scale(1.15); } }
            @keyframes drift { 0%,100% { transform: translateY(0); } 50% { transform: translateY(-12px); } }
            @keyframes scan { 0% { transform: translateX(-5px); } 100% { transform: translateX(5px); } }
            @keyframes shake { 0%,100% { transform: translateX(0); } 25% { transform: translateX(-3px); } 75% { transform: translateX(3px); } }
            @keyframes converge { 0%,100% { transform: scale(1); } 50% { transform: scale(0.9); } }
            @keyframes solidify { 0%,100% { opacity: 0.7; } 50% { opacity: 1; } }
            @keyframes expand { 0%,100% { transform: scale(1); } 50% { transform: scale(1.1); } }
            @keyframes contract { 0%,100% { transform: scale(1); } 50% { transform: scale(0.92); } }
        """
