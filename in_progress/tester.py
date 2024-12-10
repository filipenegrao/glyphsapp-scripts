# MenuTitle: Tester
# -*- coding: utf-8 -*-

from AppKit import NSPoint
from GlyphsApp import GSPath, GSNode, GSOFFCURVE
from math import cos, sin, radians


def get_smooth_nodes(layer, direction="vertical"):
    """
    Checks if a smooth point has orthogonal handles.
    Args:
        layer: any layer.
        direction (str): The direction of the handles ("vertical" or "horizontal"). Default is "vertical".
    """
    collected_nodes = []
    for path in layer.paths:
        for node in path.nodes:
            if node.smooth:
                if (
                    node.prevNode.type == "offcurve"
                    and node.nextNode.type == "offcurve"
                ):
                    if direction == "vertical":
                        if node.x == node.prevNode.x and node.x == node.nextNode.x:
                            collected_nodes.append(node)
                    if direction == "horizontal":
                        if node.y == node.prevNode.y and node.y == node.nextNode.y:
                            collected_nodes.append(node)
    return collected_nodes


def get_tangent_nodes(layer, direction="vertical"):
    collected_nodes = []
    for path in layer.paths:
        for node in path.nodes:
            if node.smooth:
                if node.prevNode.type == "offcurve" and node.nextNode.type == "line":
                    if direction == "vertical":
                        if node.x == node.prevNode.x:
                            collected_nodes.append(node)
                    if direction == "horizontal":
                        if node.y == node.prevNode.y:
                            collected_nodes.append(node)
                if node.prevNode.type == "line" and node.nextNode.type == "offcurve":
                    print(node)
                    if direction == "vertical":
                        if node.x == node.prevNode.x:
                            collected_node.append(node)
                        if node.y == node.prevNode.y:
                            collected_node.append(node)
    return collected_nodes


def circleAtCenter(center=NSPoint(0, 0), radius=50, bcp=4.0 * (2.0**0.5 - 1.0) / 3.0):
    """
    from https://github.com/mekkablue/Glyphs-Scripts/blob/c69821b17a5f9a7151630fdf9cfb5303ebd0b2ba/Build%20Glyphs/Build%20Symbols.py#L206
    """
    circle = GSPath()
    x = center.x
    y = center.y
    handle = radius * bcp
    points = (
        ((x + handle, y - radius), (x + radius, y - handle), (x + radius, y)),
        ((x + radius, y + handle), (x + handle, y + radius), (x, y + radius)),
        ((x - handle, y + radius), (x - radius, y + handle), (x - radius, y)),
        ((x - radius, y - handle), (x - handle, y - radius), (x, y - radius)),
    )
    # Add the segments:
    for triplet in points:
        # Add the two BCPs of the segment:
        bcp1 = NSPoint(triplet[0][0], triplet[0][1])
        bcp2 = NSPoint(triplet[1][0], triplet[1][1])
        for bcpPosition in (bcp1, bcp2):
            newBCP = GSNode()
            newBCP.type = GSOFFCURVE
            newBCP.position = bcpPosition
            circle.nodes.append(newBCP)

        # Add the On-Curve of the segment:
        newCurvepoint = GSNode()
        newCurvepoint.type = GSCURVE
        newCurvepoint.smooth = True
        newCurvepoint.position = NSPoint(triplet[2][0], triplet[2][1])
        circle.nodes.append(newCurvepoint)

    circle.closed = True
    return circle


def create_locked_point_markers(layer, locked_nodes):
    """
    Adiciona círculos no background da camada para representar pontos travados.
    Esses círculos podem ser movidos, deletados ou copiados pelo usuário.
    """
    # Limpa marcadores existentes no background
    layer.background.clear()

    for node in locked_nodes:
        # Criar um círculo para cada ponto travado
        radius = 5  # Tamanho do círculo
        circle = circleAtCenter(NSPoint(node.x, node.y), radius)
        layer.background.paths.append(circle)


def get_user_defined_locked_points(layer):
    """
    Identifica pontos representados pelos círculos no background.
    Calcula os centros dos círculos para determinar os pontos travados.
    """
    user_defined_points = []
    for path in layer.background.paths:
        if (
            path.closed and len(path.nodes) == 4
        ):  # Considera caminhos fechados simples com 4 nós
            # Calcula o centro do círculo
            center_x = sum(node.position.x for node in path.nodes) / 4
            center_y = sum(node.position.y for node in path.nodes) / 4
            user_defined_points.append((center_x, center_y))
    return user_defined_points


def constrain_locked_points(layer, user_points):
    """
    Ajusta os pontos travados para ficarem alinhados aos centros dos círculos no background.
    """
    for user_point in user_points:
        for node in layer.paths[0].nodes:
            # Ajusta apenas pontos próximos ao marcador
            if abs(node.x - user_point[0]) < 5 and abs(node.y - user_point[1]) < 5:
                node.x = user_point[0]
                node.y = user_point[1]


# Obter a camada atual
layer = Glyphs.font.selectedLayers[0]

# Identificar pontos travados inicialmente
# locked_nodes = get_smooth_nodes(layer)

# Criar círculos no background
# create_locked_point_markers(layer, locked_nodes)

# Obter pontos definidos pelo usuário no background
user_points = get_user_defined_locked_points(layer)
print("Pontos definidos pelo usuário:", user_points)
print(get_tangent_nodes(layer))
# Ajustar pontos na camada com base nos círculos
# constrain_locked_points(layer, user_points)
