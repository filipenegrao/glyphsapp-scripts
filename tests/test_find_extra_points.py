import os
import sys

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'paths'))

import find_extra_points_across_masters as fx

OFF = fx.node_token("offcurve", False)
SMOOTH = fx.node_token("curve", True)
CORNER = fx.node_token("curve", False)
LINE = fx.node_token("line", False)


def master(name, paths, components=None, anchors=None, shape_kinds=None,
           path_positions=None):
    if shape_kinds is None:
        shape_kinds = ["path"] * len(paths) + ["component"] * len(components or [])
    return {
        "name": name,
        "paths": paths,
        "path_positions": path_positions or [],
        "components": components or [],
        "shape_kinds": shape_kinds,
        "anchors": anchors or [],
    }


def rounded_rect():
    """A rounded rectangle: 4 corners, a smooth node midway down each stem.

    Models the shape from the reported bug — the contour whose extra nodes
    were being blamed on the wrong nodes.

    Returns:
        A (tokens, points) tuple.
    """
    tokens, points = [], []
    corners = [(0, 700), (600, 700), (600, 0), (0, 0)]
    for index, (x, y) in enumerate(corners):
        next_x, next_y = corners[(index + 1) % 4]

        def along(fraction):
            return (x + (next_x - x) * fraction, y + (next_y - y) * fraction)

        for fraction, token in ((0.0, CORNER), (0.2, OFF), (0.35, OFF),
                                (0.5, SMOOTH), (0.65, OFF), (0.8, OFF)):
            points.append(along(fraction))
            tokens.append(token)
    return tokens, points


def splice_segment(tokens, points, at):
    """Insert an extra smooth node and its two off-curves before index `at`."""
    previous, current = points[at - 1], points[at]
    middle = ((previous[0] + current[0]) / 2, (previous[1] + current[1]) / 2)
    return (tokens[:at] + [OFF, OFF, SMOOTH] + tokens[at:],
            points[:at] + [middle, middle, middle] + points[at:])


# --- node_token ----------------------------------------------------------
def test_smooth_and_corner_nodes_are_different_tokens():
    assert fx.node_token("curve", True) != fx.node_token("curve", False)


def test_offcurves_ignore_the_smooth_flag():
    assert fx.node_token("offcurve", True) == fx.node_token("offcurve", False)


# --- normalized_positions ------------------------------------------------
def test_positions_start_at_zero_and_stay_below_one():
    positions = fx.normalized_positions([(0, 0), (10, 0), (10, 10), (0, 10)])
    assert positions[0] == 0.0
    assert all(0.0 <= value < 1.0 for value in positions)
    assert positions == sorted(positions)


def test_positions_are_scale_invariant():
    small = fx.normalized_positions([(0, 0), (1, 0), (1, 1), (0, 1)])
    big = fx.normalized_positions([(0, 0), (100, 0), (100, 100), (0, 100)])
    assert small == pytest.approx(big)


def test_positions_of_an_empty_path():
    assert fx.normalized_positions([]) == []


def test_positions_of_coincident_points_do_not_divide_by_zero():
    assert fx.normalized_positions([(5, 5), (5, 5)]) == [0.0, 0.0]


# --- extra_node_indexes --------------------------------------------------
def test_no_extra_when_identical():
    tokens, points = rounded_rect()
    positions = fx.normalized_positions(points)
    assert fx.extra_node_indexes(tokens, tokens, positions, positions) == []


@pytest.mark.parametrize("at", [4, 10, 16, 22])
def test_extra_segment_is_located_exactly(at):
    """The regression that matters: right count AND right place."""
    tokens, points = rounded_rect()
    other_tokens, other_points = splice_segment(tokens, points, at)
    found = fx.extra_node_indexes(
        tokens, other_tokens,
        fx.normalized_positions(points),
        fx.normalized_positions(other_points))
    assert found == [at, at + 1, at + 2]


def test_two_extra_segments_on_opposite_stems_are_both_located():
    """The exact shape of the reported bug: one arrow was landing on a corner."""
    tokens, points = rounded_rect()
    other_tokens, other_points = splice_segment(tokens, points, 16)
    other_tokens, other_points = splice_segment(other_tokens, other_points, 4)
    found = fx.extra_node_indexes(
        tokens, other_tokens,
        fx.normalized_positions(points),
        fx.normalized_positions(other_points))
    assert found == [4, 5, 6, 19, 20, 21]
    # And never on a corner node, which is what went wrong in Glyphs.
    assert all(other_tokens[index] != CORNER for index in found)


def test_positions_are_what_makes_the_location_right():
    """Without positions the count is right but the place is not."""
    tokens, points = rounded_rect()
    other_tokens, _ = splice_segment(tokens, points, 10)
    found = fx.extra_node_indexes(tokens, other_tokens)
    assert len(found) == 3
    assert found != [10, 11, 12]


def test_extra_count_is_minimal():
    reference = [LINE, LINE, LINE]
    other = [LINE, LINE, LINE, LINE]
    assert len(fx.extra_node_indexes(reference, other)) == 1


def test_empty_reference_marks_everything_as_extra():
    assert fx.extra_node_indexes([], [LINE, LINE]) == [0, 1]


# --- rotation / direction ------------------------------------------------
def test_rotation_offset_detects_shifted_start_point():
    reference = [LINE, OFF, OFF, SMOOTH]
    other = [OFF, OFF, SMOOTH, LINE]
    assert fx.rotation_offset(reference, other) == 3


def test_rotation_offset_none_for_different_lengths():
    assert fx.rotation_offset([LINE], [LINE, LINE]) is None


def test_reversed_path_is_detected():
    reference = [LINE, LINE, SMOOTH, OFF]
    other = [OFF, SMOOTH, LINE, LINE]
    assert fx.is_reversed_match(reference, other) is True


# --- diagnose ------------------------------------------------------------
def test_compatible_masters_report_nothing():
    tokens, points = rounded_rect()
    positions = fx.normalized_positions(points)
    light = master("Light", [tokens], path_positions=[positions])
    bold = master("Bold", [tokens], path_positions=[positions])
    report = fx.diagnose([light, bold])
    assert report["issues"] == []
    assert report["extras"] == {}


def test_leanest_master_becomes_the_reference():
    light = master("Light", [[LINE, LINE, LINE]])
    bold = master("Bold", [[LINE, LINE, LINE, LINE]])
    report = fx.diagnose([bold, light])
    assert report["reference"] == 1
    assert list(report["extras"].keys()) == [0]


def test_diagnose_locates_the_extra_nodes_of_the_heavy_master():
    tokens, points = rounded_rect()
    other_tokens, other_points = splice_segment(tokens, points, 10)
    thin = master("Thin", [tokens],
                  path_positions=[fx.normalized_positions(points)])
    extrabold = master("ExtraBold", [other_tokens],
                       path_positions=[fx.normalized_positions(other_points)])
    report = fx.diagnose([thin, extrabold])
    assert report["extras"][1] == [(0, 10), (0, 11), (0, 12)]


def test_diagnose_works_without_positions():
    light = master("Light", [[LINE, OFF, OFF, SMOOTH]])
    bold = master("Bold", [[LINE, LINE, OFF, OFF, SMOOTH]])
    report = fx.diagnose([light, bold])
    assert len(report["extras"][1]) == 1


def test_path_count_mismatch_is_reported():
    light = master("Light", [[LINE, LINE, LINE]])
    bold = master("Bold", [[LINE, LINE, LINE], [LINE, LINE, LINE]])
    report = fx.diagnose([light, bold])
    assert any("path(s)" in issue for issue in report["issues"])


def test_start_point_mismatch_is_not_reported_as_extra_nodes():
    light = master("Light", [[LINE, OFF, OFF, SMOOTH]])
    bold = master("Bold", [[OFF, OFF, SMOOTH, LINE]])
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


def test_single_master_is_never_broken():
    report = fx.diagnose([master("Regular", [[LINE, LINE]])])
    assert report["issues"] == []
