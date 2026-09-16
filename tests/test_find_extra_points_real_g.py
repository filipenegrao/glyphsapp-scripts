"""Fixture built from a real font, not from a modelled contour.

Glyph "g", path 0, of the typeface that reported the bug. The Thin has 32
nodes and the ExtraBold 34; every node matches up to index 28, and the whole
difference is one run of line nodes:

    Thin       ... l | o o c      one line node
    ExtraBold  ... l l l | o o c  three line nodes, at 28, 29 and 30

So exactly two of the ExtraBold's nodes 28/29/30 are extra. Node 27, at
(157, -71), is a curve node the Thin has as well — it cannot be extra.
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'paths'))

import find_extra_points_across_masters as fx

# (type, smooth, x, y)
THIN = [
    ("offcurve", False, 262, -210), ("offcurve", False, 329, -159), ("curve", True, 329, -60),
    ("line", False, 329, 500), ("line", False, 299, 500), ("line", False, 299, 447),
    ("line", False, 304, 445), ("offcurve", False, 282, 489), ("offcurve", False, 235, 510),
    ("curve", True, 179, 510), ("offcurve", False, 94, 510), ("offcurve", False, 33, 464),
    ("curve", True, 33, 359), ("line", True, 33, 141), ("offcurve", False, 33, 37),
    ("offcurve", False, 94, -10), ("curve", True, 179, -10), ("offcurve", False, 235, -10),
    ("offcurve", False, 283, 12), ("curve", False, 304, 57), ("line", False, 299, 53),
    ("line", True, 299, -60), ("offcurve", False, 299, -142), ("offcurve", False, 246, -182),
    ("curve", True, 180, -182), ("offcurve", False, 115, -182), ("offcurve", False, 62, -142),
    ("curve", False, 62, -68), ("line", False, 32, -68), ("offcurve", False, 33, -159),
    ("offcurve", False, 100, -210), ("curve", True, 180, -210),
]

EXTRABOLD = [
    ("offcurve", False, 279, -210), ("offcurve", False, 337, -149), ("curve", True, 337, -56),
    ("line", False, 337, 500), ("line", False, 199, 500), ("line", False, 199, 453),
    ("line", False, 235, 417), ("offcurve", False, 212, 480), ("offcurve", False, 182, 510),
    ("curve", True, 130, 510), ("offcurve", False, 76, 510), ("offcurve", False, 15, 479),
    ("curve", True, 15, 371), ("line", True, 15, 132), ("offcurve", False, 15, 58),
    ("offcurve", False, 46, -10), ("curve", True, 127, -10), ("offcurve", False, 167, -10),
    ("offcurve", False, 204, 7), ("curve", False, 222, 50), ("line", False, 199, 50),
    ("line", True, 199, -71), ("offcurve", False, 199, -91), ("offcurve", False, 191, -103),
    ("curve", True, 178, -103), ("offcurve", False, 165, -103), ("offcurve", False, 157, -91),
    ("curve", True, 157, -71), ("line", False, 157, -35), ("line", False, 19, -35),
    ("line", True, 19, -61), ("offcurve", False, 19, -150), ("offcurve", False, 77, -210),
    ("curve", True, 175, -210),
]


def unpack(rows):
    """Split the fixture rows into the lists the alignment expects."""
    return (
        [fx.node_token(row[0]) for row in rows],
        [row[1] for row in rows],
        fx.normalized_positions([(row[2], row[3]) for row in rows]),
    )


def found_extras():
    """Run the alignment over the real data."""
    thin_tokens, thin_smooth, thin_positions = unpack(THIN)
    bold_tokens, bold_smooth, bold_positions = unpack(EXTRABOLD)
    return fx.extra_node_indexes(
        thin_tokens, bold_tokens,
        thin_positions, bold_positions,
        thin_smooth, bold_smooth)


def test_the_masters_differ_only_in_that_one_run():
    """Guards the fixture itself: everything else must already agree."""
    thin_tokens = [fx.node_token(row[0]) for row in THIN]
    bold_tokens = [fx.node_token(row[0]) for row in EXTRABOLD]
    assert thin_tokens[:29] == bold_tokens[:29]
    assert thin_tokens[29:] == ["offcurve", "offcurve", "curve"]
    assert bold_tokens[29:] == ["line", "line", "offcurve", "offcurve", "curve"]


def test_exactly_two_extra_nodes():
    assert len(found_extras()) == len(EXTRABOLD) - len(THIN) == 2


def test_the_flagged_node_the_designer_pointed_at():
    """(19, -61) is the node the designer identified as extra."""
    extras = found_extras()
    positions = [(EXTRABOLD[i][2], EXTRABOLD[i][3]) for i in extras]
    assert (19, -61) in positions


def test_only_line_nodes_can_be_flagged():
    """The curve node at (157, -71) is shared with the Thin, so it is safe."""
    extras = found_extras()
    assert all(EXTRABOLD[i][0] == "line" for i in extras)
    assert 27 not in extras


def test_the_alignment_stays_valid():
    """Dropping the flagged nodes must leave a sequence the Thin can match."""
    extras = set(found_extras())
    remaining = [fx.node_token(row[0])
                 for i, row in enumerate(EXTRABOLD) if i not in extras]
    assert remaining == [fx.node_token(row[0]) for row in THIN]
