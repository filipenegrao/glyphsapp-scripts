# MenuTitle: Find Extra Points Across Masters
# -*- coding: utf-8 -*-
from __future__ import division, print_function, unicode_literals

__doc__ = """

Finds and visually marks the points that break interpolation between masters.

Takes the master with the FEWEST nodes as the reference and diffs every other
master against it, node type by node type (LCS diff). The nodes that cannot be
aligned are the extra ones — they get an ARROW annotation exactly on top of
them, so you can see what to delete.

It also reports the other classic incompatibility causes:
path count, start point / direction, component count & order, anchors.

— Detailed report in the Macro Window
— Opens a tab with the broken glyphs
— Re-run to clear the annotations of the previous run

Scope: selected glyphs, or the whole font when nothing is selected.
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
#  GSAnnotation has no userData, so annotations made by this script
#  are tagged with a prefix in their .text to allow cleanup on re-runs.
MARKER = "⁣xp⁣"          # invisible separators, never typed by hand
SKIP_NON_EXPORTING = True
OPEN_TAB = True


# ---------------------------------------------------------------
#  Pure helpers (no Glyphs API — covered by tests/)
# ---------------------------------------------------------------
def lcs_extra_indexes(reference, other):
    """Return the indexes of `other` that have no counterpart in `reference`.

    Both arguments are sequences of node-type strings ("line", "curve",
    "offcurve"). Uses a longest-common-subsequence alignment, so a node
    inserted in the middle of a path is reported at its real position
    instead of shifting everything after it.

    Args:
        reference: Node types of the reference (leanest) path.
        other: Node types of the path being checked.

    Returns:
        A sorted list of indexes into `other`.
    """
    n, m = len(reference), len(other)
    # table[i][j] = LCS length of reference[i:] and other[j:]
    table = [[0] * (m + 1) for _ in range(n + 1)]
    for i in range(n - 1, -1, -1):
        for j in range(m - 1, -1, -1):
            if reference[i] == other[j]:
                table[i][j] = table[i + 1][j + 1] + 1
            else:
                table[i][j] = max(table[i + 1][j], table[i][j + 1])

    extras = []
    i = j = 0
    while i < n and j < m:
        if reference[i] == other[j]:
            i += 1
            j += 1
        elif table[i + 1][j] >= table[i][j + 1]:
            i += 1
        else:
            extras.append(j)
            j += 1
    extras.extend(range(j, m))
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

            for node_index in lcs_extra_indexes(ref_path, own_path):
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
        "components": [],
        "anchors": [],
        "paths_objects": [],
    }
    if layer is None:
        return info

    for shape in layer.shapes:
        if isinstance(shape, GSPath):
            info["paths"].append([str(node.type) for node in shape.nodes])
            info["paths_objects"].append(shape)
        elif isinstance(shape, GSComponent):
            info["components"].append(str(shape.componentName))

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
    to_remove = []
    for i, annotation in enumerate(layer.annotations):
        text = annotation.text
        if text and str(text).startswith(MARKER):
            to_remove.append(i)
    for i in reversed(to_remove):
        del layer.annotations[i]
    return len(to_remove)


def annotate_extra_nodes(layer, info, extras, reference_name):
    """Drop an arrow on every extra node and a summary text on the layer.

    Args:
        layer: The GSLayer of the offending master.
        info: The dict returned by collect_layer_info() for that layer.
        extras: List of (path_index, node_index) tuples.
        reference_name: Name of the reference master, shown in the summary.
    """
    for path_index, node_index in extras:
        path = info["paths_objects"][path_index]
        node = path.nodes[node_index]
        annotation = GSAnnotation()
        annotation.type = ARROW
        annotation.position = NSPoint(node.position.x, node.position.y)
        annotation.width = 40
        annotation.text = MARKER
        layer.annotations.append(annotation)

    summary = GSAnnotation()
    summary.type = TEXT
    summary.text = "%s%d extra node(s) vs. %s" % (
        MARKER, len(extras), reference_name)
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
            print("[!!]  %s   (reference: %s)" % (glyph.name, reference_name))
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
