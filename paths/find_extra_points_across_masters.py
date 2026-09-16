# MenuTitle: Find Extra Points Across Masters
# -*- coding: utf-8 -*-
from __future__ import division, print_function, unicode_literals

__doc__ = """

Finds and visually marks the points that break interpolation between masters.

Takes the master with the FEWEST nodes as the reference and aligns every other
master against it. The nodes left without a counterpart are the extra ones —
they get an ARROW annotation exactly on top of them, so you can see what to
delete.

Comparing node types alone is not enough: a rounded contour reads as
"oocoocooc...", so every alignment that drops the same number of nodes ties and
the extra points end up blamed on the wrong nodes. The tie is settled by how far
apart the nodes sit along their contour, which is the part that stays
proportional between compatible masters.

The corner/smooth flag is left out of the comparison on purpose — Glyphs
ignores it for compatibility as well, and a node set to corner in one master
and smooth in another is not an extra node.

It also reports the other classic incompatibility causes:
path count, start point / direction, component count & order, anchors.

— Detailed report in the Macro Window
— Opens a tab with the broken glyphs
— Re-run to clear the annotations of the previous run

Scope: selected glyphs, or the whole font when nothing is selected. Note that
in Edit view the current tab always counts as a selection, so the whole-font
sweep happens from Font view with nothing selected.

Brace and bracket layers are out of scope (master layers only).

"""

try:
    from GlyphsApp import Glyphs, GSAnnotation, GSComponent, GSPath, TEXT, ARROW
    from Foundation import NSPoint
    IN_GLYPHS = True
except ImportError:  # importable outside Glyphs, for the tests
    IN_GLYPHS = False

# ---------------------------------------------------------------
#  Config
# ---------------------------------------------------------------
#  GSAnnotation has no userData, so the positions of the annotations made
#  by this script are bookkept in layer.userData, which is what allows the
#  cleanup on re-runs. The .text marker below is a second net.
TAG = "com.filipenegrao.extraPoints"
MARKER = "⁣⁣⁣"       # invisible separators, never typed by hand
SKIP_NON_EXPORTING = True
OPEN_TAB = True


# ---------------------------------------------------------------
#  Pure helpers (no Glyphs API — covered by tests/)
# ---------------------------------------------------------------
def node_token(node_type):
    """Build the symbol used to compare a node across masters.

    Only the node type counts. The corner/smooth flag is deliberately left
    out: Glyphs ignores it for compatibility too (its own compareString is
    built from "l", "c" and "o" alone), and a node set to corner in one
    master and smooth in another still interpolates. Folding the flag in
    makes those nodes unmatchable, and the alignment then has to invent an
    extra node to explain the difference — pointing an arrow at a node that
    is not extra at all.

    Args:
        node_type: The GSNode type, "line", "curve", "offcurve" or "qcurve".

    Returns:
        The token as a string.
    """
    return str(node_type)


def normalized_positions(points):
    """Where each node sits along its contour, as a 0..1 fraction.

    Measured as the cumulative length of the polygon through the nodes
    (off-curves included), from the path's own start node. Two compatible
    masters distribute their nodes in roughly the same proportion along the
    contour, which is what lets us tell apart two nodes that carry the very
    same type.

    Args:
        points: Sequence of (x, y) tuples, in path order.

    Returns:
        A list of floats in 0..1, one per point.
    """
    if not points:
        return []

    lengths = [0.0]
    total = 0.0
    for i in range(1, len(points)):
        previous, current = points[i - 1], points[i]
        total += ((current[0] - previous[0]) ** 2 +
                  (current[1] - previous[1]) ** 2) ** 0.5
        lengths.append(total)

    # Close the contour, so the last segment counts towards the total.
    first, last = points[0], points[-1]
    total += ((first[0] - last[0]) ** 2 + (first[1] - last[1]) ** 2) ** 0.5
    if total <= 0:
        return [0.0] * len(points)
    return [length / total for length in lengths]


def extra_node_indexes(reference, other,
                       reference_positions=None, other_positions=None):
    """Return the indexes of `other` that have no counterpart in `reference`.

    Both arguments are sequences of node tokens (see node_token()). A plain
    diff is not enough here: a contour's token sequence is periodic, so
    every alignment that drops the same number of nodes ties, and any of
    them can be picked — giving the right count at the wrong place.

    So the alignment is scored on a pair: first the number of unmatched
    nodes, then how far apart the matched nodes sit along their contours.
    The first term keeps the answer minimal, the second one picks the
    sensible alignment out of the tie.

    Args:
        reference: Node tokens of the reference (leanest) path.
        other: Node tokens of the path being checked.
        reference_positions: Normalized positions for `reference`, or None
            to score on the token sequence alone.
        other_positions: Normalized positions for `other`.

    Returns:
        A sorted list of indexes into `other`.
    """
    n, m = len(reference), len(other)
    if reference_positions is None or other_positions is None:
        reference_positions = [0.0] * n
        other_positions = [0.0] * m

    SKIP_REFERENCE, SKIP_OTHER, MATCH = 0, 1, 2

    # cost[i][j] = (unmatched nodes, positional cost) for reference[:i] vs other[:j]
    cost = [[(0, 0.0)] * (m + 1) for _ in range(n + 1)]
    move = [[SKIP_REFERENCE] * (m + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        cost[i][0] = (i, 0.0)
        move[i][0] = SKIP_REFERENCE
    for j in range(1, m + 1):
        cost[0][j] = (j, 0.0)
        move[0][j] = SKIP_OTHER

    for i in range(1, n + 1):
        for j in range(1, m + 1):
            best = None
            if reference[i - 1] == other[j - 1]:
                previous = cost[i - 1][j - 1]
                distance = abs(reference_positions[i - 1] - other_positions[j - 1])
                best = ((previous[0], previous[1] + distance), MATCH)

            for candidate, direction in (
                    ((cost[i - 1][j][0] + 1, cost[i - 1][j][1]), SKIP_REFERENCE),
                    ((cost[i][j - 1][0] + 1, cost[i][j - 1][1]), SKIP_OTHER)):
                if best is None or candidate < best[0]:
                    best = (candidate, direction)

            cost[i][j], move[i][j] = best

    extras = []
    i, j = n, m
    while i > 0 or j > 0:
        if i == 0:
            j -= 1
            extras.append(j)
        elif j == 0:
            i -= 1
        elif move[i][j] == MATCH:
            i -= 1
            j -= 1
        elif move[i][j] == SKIP_REFERENCE:
            i -= 1
        else:
            j -= 1
            extras.append(j)

    extras.reverse()
    return extras


def rotation_offset(reference, other):
    """Return how many nodes `other` is rotated against `reference`.

    Only meaningful when both sequences have the same length and differ
    merely by where the path starts.

    Args:
        reference: Node types of the reference path.
        other: Node types of the path being checked.

    Returns:
        The offset as an int, or None when no rotation matches.
    """
    n = len(reference)
    if n == 0 or n != len(other):
        return None
    for offset in range(1, n):
        if all(other[(i + offset) % n] == reference[i] for i in range(n)):
            return offset
    return None


def is_reversed_match(reference, other):
    """Whether `other` matches `reference` when read backwards.

    Args:
        reference: Node types of the reference path.
        other: Node types of the path being checked.

    Returns:
        True when the path is compatible but runs the opposite way.
    """
    if len(reference) != len(other) or not reference:
        return False
    backwards = list(reversed(other))
    if backwards == list(reference):
        return True
    return rotation_offset(reference, backwards) is not None


def diagnose(masters_info):
    """Compare the masters of a single glyph.

    Args:
        masters_info: One dict per master, with the keys ``name``,
            ``paths`` (list of lists of node-type strings), ``components``
            (list of names) and ``anchors`` (list of names).

    Returns:
        A dict with ``reference`` (index into masters_info), ``issues``
        (list of human-readable strings) and ``extras``, a dict mapping a
        master index to a list of ``(path_index, node_index)`` tuples.
    """
    result = {"reference": 0, "issues": [], "extras": {}}
    if len(masters_info) < 2:
        return result

    def positions_of(info, path_index):
        """Normalized node positions of one path, when they were collected."""
        stored = info.get("path_positions") or []
        if path_index < len(stored):
            return stored[path_index]
        return None

    # Reference = the master with the fewest nodes; ties keep the first one.
    def node_total(info):
        return sum(len(p) for p in info["paths"])

    ref_index = min(range(len(masters_info)),
                    key=lambda i: (node_total(masters_info[i]), i))
    result["reference"] = ref_index
    reference = masters_info[ref_index]

    for index, info in enumerate(masters_info):
        if index == ref_index:
            continue

        if len(info["paths"]) != len(reference["paths"]):
            result["issues"].append(
                "%s: %d path(s), reference %s has %d" % (
                    info["name"], len(info["paths"]),
                    reference["name"], len(reference["paths"])))

        if info.get("shape_kinds", []) != reference.get("shape_kinds", []):
            result["issues"].append(
                "%s: shapes in a different order [%s], reference %s has [%s]" % (
                    info["name"], ", ".join(info.get("shape_kinds", [])),
                    reference["name"],
                    ", ".join(reference.get("shape_kinds", []))))

        if info["components"] != reference["components"]:
            result["issues"].append(
                "%s: components [%s], reference %s has [%s]" % (
                    info["name"], ", ".join(info["components"]),
                    reference["name"], ", ".join(reference["components"])))

        if sorted(info["anchors"]) != sorted(reference["anchors"]):
            missing = sorted(set(reference["anchors"]) - set(info["anchors"]))
            added = sorted(set(info["anchors"]) - set(reference["anchors"]))
            detail = []
            if missing:
                detail.append("missing %s" % ", ".join(missing))
            if added:
                detail.append("extra %s" % ", ".join(added))
            result["issues"].append(
                "%s: anchors %s" % (info["name"], "; ".join(detail)))

        extras = []
        for path_index in range(min(len(info["paths"]),
                                    len(reference["paths"]))):
            ref_path = reference["paths"][path_index]
            own_path = info["paths"][path_index]
            if own_path == ref_path:
                continue

            if len(own_path) == len(ref_path):
                # Same amount of nodes: not extra points, but a path that
                # starts somewhere else or runs the other way around.
                if is_reversed_match(ref_path, own_path):
                    result["issues"].append(
                        "%s: path %d runs in the opposite direction" % (
                            info["name"], path_index + 1))
                    continue
                offset = rotation_offset(ref_path, own_path)
                if offset is not None:
                    result["issues"].append(
                        "%s: path %d starts %d node(s) off" % (
                            info["name"], path_index + 1, offset))
                    continue

            node_indexes = extra_node_indexes(
                ref_path, own_path,
                positions_of(reference, path_index),
                positions_of(info, path_index))
            for node_index in node_indexes:
                extras.append((path_index, node_index))

        if extras:
            result["extras"][index] = extras
            result["issues"].append(
                "%s: %d extra node(s)" % (info["name"], len(extras)))

    return result


# ---------------------------------------------------------------
#  Glyphs side
# ---------------------------------------------------------------
def collect_layer_info(layer, master_name):
    """Read the structure of one master layer into plain Python data.

    Args:
        layer: A GSLayer, or None when the master layer is missing.
        master_name: Name of the master, used in the report.

    Returns:
        A dict shaped for diagnose(), plus ``paths_objects`` to map the
        reported indexes back to real nodes.
    """
    info = {
        "name": master_name,
        "paths": [],
        "path_positions": [],
        "components": [],
        "shape_kinds": [],
        "anchors": [],
        "paths_objects": [],
        "node_count": 0,
    }
    if layer is None:
        return info

    for shape in layer.shapes:
        if isinstance(shape, GSPath):
            info["paths"].append([
                node_token(node.type) for node in shape.nodes])
            info["path_positions"].append(normalized_positions([
                (node.position.x, node.position.y) for node in shape.nodes]))
            info["node_count"] += len(shape.nodes)
            info["paths_objects"].append(shape)
            info["shape_kinds"].append("path")
        elif isinstance(shape, GSComponent):
            info["components"].append(str(shape.componentName))
            info["shape_kinds"].append("component")

    info["anchors"] = [str(anchor.name) for anchor in layer.anchors]
    return info


def clear_annotations(layer):
    """Remove the annotations left by a previous run of this script.

    Args:
        layer: The GSLayer to clean up.

    Returns:
        The number of annotations removed.
    """
    if layer is None:
        return 0

    stored = layer.userData[TAG] if layer.userData else None
    known = set()
    if stored:
        for entry in stored:
            known.add((int(entry[0]), int(entry[1])))

    to_remove = []
    for i, annotation in enumerate(layer.annotations):
        text = annotation.text
        if text and MARKER in str(text):
            to_remove.append(i)
            continue
        position = annotation.position
        if (int(round(position.x)), int(round(position.y))) in known:
            to_remove.append(i)

    for i in reversed(to_remove):
        del layer.annotations[i]

    if stored:
        del layer.userData[TAG]
    return len(to_remove)


def annotate_extra_nodes(layer, info, extras, reference_name):
    """Drop an arrow on every extra node and a summary text on the layer.

    Args:
        layer: The GSLayer of the offending master.
        info: The dict returned by collect_layer_info() for that layer.
        extras: List of (path_index, node_index) tuples.
        reference_name: Name of the reference master, shown in the summary.
    """
    positions = []
    for path_index, node_index in extras:
        path = info["paths_objects"][path_index]
        node = path.nodes[node_index]
        annotation = GSAnnotation()
        annotation.type = ARROW
        annotation.position = NSPoint(node.position.x, node.position.y)
        annotation.width = 40
        annotation.text = MARKER
        layer.annotations.append(annotation)
        positions.append([int(round(node.position.x)),
                          int(round(node.position.y))])

    positions.append([0, -120])
    layer.userData[TAG] = positions

    summary = GSAnnotation()
    summary.type = TEXT
    summary.text = "%d extra node(s) vs. %s%s" % (
        len(extras), reference_name, MARKER)
    summary.position = NSPoint(0, -120)
    summary.width = 300
    layer.annotations.append(summary)


def main():
    font = Glyphs.font
    if font is None:
        print("No font open.")
        return

    Glyphs.clearLog()
    Glyphs.showMacroWindow()

    masters = list(font.masters)
    if len(masters) < 2:
        print("This font has a single master — nothing to interpolate.")
        return

    # Selected glyphs, or the whole font when nothing is selected.
    if font.currentTab:
        selection = [layer.parent for layer in font.selectedLayers]
    else:
        selection = list(font.selection)

    seen = set()
    glyphs = []
    for glyph in selection:
        if glyph.name not in seen:
            seen.add(glyph.name)
            glyphs.append(glyph)

    scope = "selection"
    if not glyphs:
        glyphs = list(font.glyphs)
        scope = "whole font"

    print("=" * 60)
    print("  FIND EXTRA POINTS ACROSS MASTERS")
    print("=" * 60)
    print("  Font: %s" % font.familyName)
    print("  Masters: %s" % ", ".join(m.name for m in masters))
    print("  Scope: %s (%d glyph(s))" % (scope, len(glyphs)))
    print("=" * 60)
    print()

    font.disableUpdateInterface()
    try:
        broken = []
        checked = 0
        cleared = 0

        for glyph in glyphs:
            if SKIP_NON_EXPORTING and not glyph.export:
                continue

            layers = [glyph.layers[master.id] for master in masters]
            for layer in layers:
                cleared += clear_annotations(layer)

            masters_info = [
                collect_layer_info(layer, master.name)
                for layer, master in zip(layers, masters)
            ]
            # Nothing drawn anywhere: no compatibility to speak of.
            if not any(info["paths"] or info["components"]
                       for info in masters_info):
                continue

            checked += 1
            report = diagnose(masters_info)
            if not report["issues"]:
                continue

            broken.append(glyph)
            reference_name = masters_info[report["reference"]]["name"]
            counts = ", ".join(
                "%s %d" % (info["name"], info["node_count"])
                for info in masters_info)
            print("[!!]  %s   (reference: %s)" % (glyph.name, reference_name))
            print("       nodes: %s" % counts)
            for issue in report["issues"]:
                print("       > %s" % issue)

            for master_index, extras in report["extras"].items():
                annotate_extra_nodes(
                    layers[master_index],
                    masters_info[master_index],
                    extras,
                    reference_name)
            print()

    finally:
        font.enableUpdateInterface()

    if cleared:
        print("Cleared %d annotation(s) from a previous run." % cleared)
        print()

    if OPEN_TAB and broken:
        font.newTab("/" + "/".join(glyph.name for glyph in broken))

    print("-" * 60)
    if not broken:
        print("All good! %d glyph(s) checked, all masters compatible." % checked)
    else:
        print("%d glyph(s) with problems out of %d checked." % (
            len(broken), checked))
        print()
        print("VISUAL LEGEND (annotations):")
        print("  ARROW  = extra node, this one has no match in the reference")
        print("  TEXT   = how many extra nodes this master has")
        print()
        print("The reference is always the master with the fewest nodes.")
        print("Re-run the script to clear the annotations.")
    print("-" * 60)


if IN_GLYPHS:
    main()
