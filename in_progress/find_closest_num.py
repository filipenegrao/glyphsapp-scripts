from __future__ import print_function

def find_closest_points(some_list, a_number, num_of_points):

    """
    some_list -> (list of ints) A list of x or y coordinates
    a_number -> (int) a specific number that will be our base
    num_of_points -> (int) how many numbers we should looking for

    """

    some_list = sorted(some_list)
    closest_points = []

    while num_of_points > 0:
        closest_num = min(some_list, key=lambda x:abs(x-a_number))
        closest_points.append(closest_num)
        some_list.remove(closest_num)
        num_of_points -= 1

    return sorted(closest_points)


test_list = [1, 2, 3, 4, 12, 15, 21, 24, 34, 35, 36]
print(find_closest_points(test_list, 35, 4))


def list_points(some_glyph):
    """
    This function will ignore OFFCURVE points,
    since we only need to compare the ONCURVE or LINE points.
    Returns a Tuple with two lists: xlist and ylist.

    """

    xlist = []
    ylist = []

    for layer in some_glyph:
        for path in layer.paths:
            for node in path.nodes:
                if node.type is OFFCURVE:
                    continue
                else:
                    xlist.append(node.x)
                    ylist.append(node.y)

    return sorted(xlist), sorted(ylist)
