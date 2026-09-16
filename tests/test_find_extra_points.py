import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'paths'))

import find_extra_points_across_masters as fx

CURVE = "curve"
LINE = "line"
OFF = "offcurve"


def master(name, paths, components=None, anchors=None, shape_kinds=None):
    if shape_kinds is None:
        shape_kinds = ["path"] * len(paths) + ["component"] * len(components or [])
    return {
        "name": name,
        "paths": paths,
        "components": components or [],
        "shape_kinds": shape_kinds,
        "anchors": anchors or [],
    }


# --- lcs_extra_indexes ---------------------------------------------------
def test_no_extra_when_identical():
    seq = [OFF, OFF, CURVE, OFF, OFF, CURVE]
    assert fx.lcs_extra_indexes(seq, seq) == []


def test_extra_node_in_the_middle():
    reference = [LINE, LINE, LINE]
    other = [LINE, LINE, LINE, LINE]
    assert len(fx.lcs_extra_indexes(reference, other)) == 1


def test_extra_curve_segment_reports_three_nodes():
    reference = [OFF, OFF, CURVE, OFF, OFF, CURVE]
    other = [OFF, OFF, CURVE, OFF, OFF, CURVE, OFF, OFF, CURVE]
    assert len(fx.lcs_extra_indexes(reference, other)) == 3


def test_inserted_line_is_located_not_shifted():
    reference = [LINE, OFF, OFF, CURVE]
    other = [LINE, LINE, OFF, OFF, CURVE]
    assert fx.lcs_extra_indexes(reference, other) == [1]


def test_empty_reference_marks_everything_as_extra():
    assert fx.lcs_extra_indexes([], [LINE, LINE]) == [0, 1]


# --- rotation / direction ------------------------------------------------
def test_rotation_offset_detects_shifted_start_point():
    reference = [LINE, OFF, OFF, CURVE]
    other = [OFF, OFF, CURVE, LINE]
    assert fx.rotation_offset(reference, other) == 3


def test_rotation_offset_none_for_different_lengths():
    assert fx.rotation_offset([LINE], [LINE, LINE]) is None


def test_reversed_path_is_detected():
    reference = [LINE, LINE, CURVE, OFF]
    other = [OFF, CURVE, LINE, LINE]
    assert fx.is_reversed_match(reference, other) is True


# --- diagnose ------------------------------------------------------------
def test_compatible_masters_report_nothing():
    path = [OFF, OFF, CURVE, OFF, OFF, CURVE]
    report = fx.diagnose([master("Light", [path]), master("Bold", [path])])
    assert report["issues"] == []
    assert report["extras"] == {}


def test_leanest_master_becomes_the_reference():
    light = master("Light", [[LINE, LINE, LINE]])
    bold = master("Bold", [[LINE, LINE, LINE, LINE]])
    report = fx.diagnose([bold, light])
    assert report["reference"] == 1
    assert list(report["extras"].keys()) == [0]


def test_extra_node_is_located_in_the_offending_master():
    light = master("Light", [[LINE, OFF, OFF, CURVE]])
    bold = master("Bold", [[LINE, LINE, OFF, OFF, CURVE]])
    report = fx.diagnose([light, bold])
    assert report["extras"][1] == [(0, 1)]


def test_path_count_mismatch_is_reported():
    light = master("Light", [[LINE, LINE, LINE]])
    bold = master("Bold", [[LINE, LINE, LINE], [LINE, LINE, LINE]])
    report = fx.diagnose([light, bold])
    assert any("path(s)" in issue for issue in report["issues"])


def test_start_point_mismatch_is_not_reported_as_extra_nodes():
    light = master("Light", [[LINE, OFF, OFF, CURVE]])
    bold = master("Bold", [[OFF, OFF, CURVE, LINE]])
    report = fx.diagnose([light, bold])
    assert report["extras"] == {}
    assert any("starts" in issue for issue in report["issues"])


def test_component_mismatch_is_reported():
    light = master("Light", [], components=["a", "acutecomb"])
    bold = master("Bold", [], components=["acutecomb", "a"])
    report = fx.diagnose([light, bold])
    assert any("components" in issue for issue in report["issues"])


def test_anchor_mismatch_is_reported():
    light = master("Light", [[LINE]], anchors=["top", "bottom"])
    bold = master("Bold", [[LINE]], anchors=["top"])
    report = fx.diagnose([light, bold])
    assert any("anchors" in issue for issue in report["issues"])


def test_single_master_is_never_broken():
    report = fx.diagnose([master("Regular", [[LINE, LINE]])])
    assert report["issues"] == []


# --- aligned_extra_indexes ----------------------------------------------
def test_aligned_diff_matches_plain_diff_when_start_points_agree():
    reference = [LINE, OFF, OFF, CURVE]
    other = [LINE, LINE, OFF, OFF, CURVE]
    assert fx.aligned_extra_indexes(reference, other) == [1]


def test_aligned_diff_finds_the_real_node_on_a_rotated_path():
    # Reference: three curve segments. Other: same, rotated by two nodes,
    # with one extra line node spliced in.
    reference = [OFF, OFF, CURVE] * 3
    rotated = reference[2:] + reference[:2]
    other = rotated[:4] + [LINE] + rotated[4:]
    extras = fx.aligned_extra_indexes(reference, other)
    assert len(extras) == 1
    assert other[extras[0]] == LINE


def test_aligned_diff_reports_nothing_for_a_pure_rotation():
    reference = [OFF, OFF, CURVE, LINE, OFF, OFF, CURVE]
    other = reference[3:] + reference[:3]
    assert fx.aligned_extra_indexes(reference, other) == []


def test_aligned_diff_gives_up_on_very_long_paths():
    reference = [LINE] * (fx.MAX_NODES_FOR_ROTATION + 1)
    other = [LINE] * (fx.MAX_NODES_FOR_ROTATION + 2)
    assert len(fx.aligned_extra_indexes(reference, other)) == 1


# --- shape order ---------------------------------------------------------
def test_shape_order_mismatch_is_reported():
    light = master("Light", [[LINE], [LINE]], components=["acutecomb"],
                   shape_kinds=["path", "component", "path"])
    bold = master("Bold", [[LINE], [LINE]], components=["acutecomb"],
                  shape_kinds=["path", "path", "component"])
    report = fx.diagnose([light, bold])
    assert any("different order" in issue for issue in report["issues"])


def test_same_shape_order_is_not_reported():
    light = master("Light", [[LINE]], components=["acutecomb"])
    bold = master("Bold", [[LINE]], components=["acutecomb"])
    assert fx.diagnose([light, bold])["issues"] == []
