"""Tests for the OrchestrationVisualizer.

Covers phase descriptors, SVG generation, audit chains, error handling,
and visual attribute correctness.
"""

from __future__ import annotations

import xml.etree.ElementTree as ET

import pytest

from art_from_auto_revision.visualizer import (
    PHASE_DESCRIPTORS,
    PHASE_NAMES,
    OrchestrationVisualizer,
    PhaseDescriptor,
)


@pytest.fixture
def viz() -> OrchestrationVisualizer:
    return OrchestrationVisualizer(width=1200, height=800)


class TestPhaseDescriptors:
    """Validate the canonical phase registry."""

    def test_exactly_eight_phases(self) -> None:
        assert len(PHASE_DESCRIPTORS) == 8

    def test_phase_names_are_canonical(self) -> None:
        expected = (
            "observation",
            "hypothesis",
            "testing",
            "refutation",
            "revision",
            "consolidation",
            "propagation",
            "audit",
        )
        assert PHASE_NAMES == expected

    def test_all_colors_are_hex(self) -> None:
        for desc in PHASE_DESCRIPTORS:
            assert desc.color.startswith("#"), f"{desc.name} color is not hex"
            assert len(desc.color) == 7, f"{desc.name} color is not 7-char hex"

    def test_z_indices_are_unique(self) -> None:
        z_indices = [p.z_index for p in PHASE_DESCRIPTORS]
        assert len(z_indices) == len(set(z_indices))


class TestGetPhaseDescriptor:
    """Test phase lookup by name."""

    def test_valid_phase_returns_descriptor(self, viz: OrchestrationVisualizer) -> None:
        desc = viz.get_phase_descriptor("observation")
        assert isinstance(desc, PhaseDescriptor)
        assert desc.name == "observation"
        assert desc.color == "#1a1a4e"

    def test_invalid_phase_raises(self, viz: OrchestrationVisualizer) -> None:
        with pytest.raises(ValueError, match="Unknown phase 'nonexistent'"):
            viz.get_phase_descriptor("nonexistent")


class TestRenderPhase:
    """Test single-phase SVG rendering."""

    def test_returns_svg_group(self, viz: OrchestrationVisualizer) -> None:
        svg = viz.render_phase("hypothesis")
        root = ET.fromstring(svg)
        assert root.tag == "g"
        assert root.get("id") == "phase-hypothesis"

    def test_contains_color_attribute(self, viz: OrchestrationVisualizer) -> None:
        svg = viz.render_phase("hypothesis")
        assert "#f5a623" in svg


class TestRenderPipeline:
    """Test full pipeline composition."""

    def test_pipeline_contains_all_phases(self, viz: OrchestrationVisualizer) -> None:
        svg = viz.render_pipeline()
        for name in PHASE_NAMES:
            assert f'id="phase-{name}"' in svg

    def test_pipeline_is_valid_svg_group(self, viz: OrchestrationVisualizer) -> None:
        svg = viz.render_pipeline()
        root = ET.fromstring(svg)
        assert root.tag == "g"
        assert root.get("id") == "pipeline"
        assert len(root) == 8


class TestRenderAuditChain:
    """Test audit chain ring generation."""

    def test_single_depth(self, viz: OrchestrationVisualizer) -> None:
        svg = viz.render_audit_chain(depth=1)
        root = ET.fromstring(svg)
        circles = root.findall("circle")
        assert len(circles) == 1

    def test_multiple_depth(self, viz: OrchestrationVisualizer) -> None:
        svg = viz.render_audit_chain(depth=3)
        root = ET.fromstring(svg)
        circles = root.findall("circle")
        assert len(circles) == 3

    def test_zero_depth_raises(self, viz: OrchestrationVisualizer) -> None:
        with pytest.raises(ValueError, match="depth must be >= 1"):
            viz.render_audit_chain(depth=0)

    def test_opacity_decreases_with_depth(self, viz: OrchestrationVisualizer) -> None:
        svg = viz.render_audit_chain(depth=3)
        root = ET.fromstring(svg)
        circles = root.findall("circle")
        opacities = [float(c.get("opacity", "1")) for c in circles]
        assert opacities[0] > opacities[-1]


class TestGenerateSvg:
    """Test complete SVG document generation."""

    def test_is_valid_xml(self, viz: OrchestrationVisualizer) -> None:
        svg = viz.generate_svg()
        # Should not raise
        ET.fromstring(svg)

    def test_contains_background_rect(self, viz: OrchestrationVisualizer) -> None:
        svg = viz.generate_svg()
        assert "#0d1117" in svg

    def test_contains_all_phase_colors(self, viz: OrchestrationVisualizer) -> None:
        svg = viz.generate_svg()
        for desc in PHASE_DESCRIPTORS:
            assert desc.color in svg, f"Missing color for {desc.name}"


class TestUtilityMethods:
    """Test convenience methods."""

    def test_get_phase_color(self, viz: OrchestrationVisualizer) -> None:
        assert viz.get_phase_color("audit") == "#adb5bd"

    def test_get_all_colors(self, viz: OrchestrationVisualizer) -> None:
        colors = viz.get_all_colors()
        assert len(colors) == 8
        assert colors["observation"] == "#1a1a4e"

    def test_get_phase_count(self, viz: OrchestrationVisualizer) -> None:
        assert viz.get_phase_count() == 8
