from typing import Optional, List


def convert_input(instructions: List[str]) -> List[tuple[int, int]]:
    path = []
    cur_x = 0
    cur_y = 0
    path.append((cur_x, cur_y))
    for instr in instructions:

        direction = instr[0]
        delta_pos = int(instr[1:len(instr)])
        match direction:
            case 'R':
                cur_x += delta_pos
            case 'L':
                cur_x -= delta_pos
            case 'U':
                cur_y += delta_pos
            case 'D':
                cur_y -= delta_pos
            case unrecognized:
                raise ValueError(unrecognized + " is not a valid direction code")
        path.append((cur_x, cur_y))
    return path


def manhattan(x, y):
    return abs(x) + abs(y)


def lines_intersect_orthogonal(x1, x2, y_line, y1, y2, x_line):
    """
    Do these two straight orthogonal lines intersect?
    """
    if x1 <= x_line <= x2 or x2 <= x_line <= x1:
        if (y1 <= y_line and y2 >= y_line) or (y1 >= y_line and y2 <= y_line):
            return True
        return False
    return False


def check_intersections(p1, p2, line: int, is_horizontal, path2, path1_length: int) -> List[tuple[int, int, int]]:
    """
    Checks whether path2 intersects with the line segment (p1, p2, line) at any point
    :param p1, p2, line: represents the line from path1
    :param is_horizontal: is the line horizontal or vertical
    :param path2: path2
    :param: path1_length: length of path1 up until the beginning of line segment (p1, p2, line)
    :return: the list of intersections as list of 3-tuples, where the entries 0 and 1 represent the coordinates
    of the intersection, and entry 2 represents the length of the path to that intersection.
    """
    intersections: List[tuple[int, int, int]] = []
    path2_length: int = 0
    # loop through each edge of path2
    for i in range(0, len(path2) - 1):
        (x3, y3) = path2[i]
        (x4, y4) = path2[i+1]
        length = -1
        if is_horizontal and y3 == y4:
            # don't care about intersection points when they "lie" on the same path
            length = abs(x3 - x4)
        elif not is_horizontal and x3 == x4:
            # don't care about intersection points when they "lie" on the same path
            length = abs(y3 - y4)
        # line from path2 is horizontal
        elif (not is_horizontal) and y3 == y4:
            length = abs(x3 - x4)
            if lines_intersect_orthogonal(x3, x4, y3, p1, p2, line):
                added_length_to_intersection = abs(x3-line)
                added_length_to_intersection += abs(p1-y3)
                length_to_intersection = path1_length + path2_length + added_length_to_intersection
                intersections.append((line, y3, length_to_intersection))
        # line from path2 is vertical
        elif is_horizontal and x3 == x4:
            length = abs(y3 - y4)
            if lines_intersect_orthogonal(p1, p2, line, y3, y4, x3):
                added_length_to_intersection = abs(y3-line)
                added_length_to_intersection += abs(p1-x3)
                length_to_intersection = path1_length + path2_length + added_length_to_intersection
                intersections.append((x3, line, length_to_intersection))
        path2_length += length
    return intersections


def crossing_points(path1: List[tuple[int, int]], path2: List[tuple[int, int]]) -> List[tuple[int, int, int]]:
    # for each line segment in path1
    intersections = []
    path1_length = 0
    for i in range(0, len(path1) - 1):
        (x1, y1) = path1[i]
        (x2, y2) = path1[i+1]
        # check whether path2 intersects with this line segment at any point
        # if the line in path1 is horizontal
        if y1 == y2:
            length_of_segment = abs(x1 - x2)
            intersections.extend(check_intersections(x1, x2, y1, True, path2, path1_length))
        # else the line in path1 is vertical
        else:
            length_of_segment = abs(y1 - y2)
            intersections.extend(check_intersections(y1, y2, x1, False, path2, path1_length))
        path1_length += length_of_segment
    return intersections

def part1(intersections):
    intersections.sort(key=lambda intersection: manhattan(intersection[0], intersection[1]))
    # (0, 0, 0) is not present when the first two lines are not orthogonal
    if intersections[0] == (0, 0, 0):
        intersections.remove((0, 0, 0))
    manhattan_closest_intersection = manhattan(intersections[0][0], intersections[0][1])
    print("Distance to closest intersection: ", manhattan_closest_intersection)

def part2(intersections):
    intersections.sort(key=lambda intersection: intersection[2])
    # (0, 0, 0) is not present when the first two lines are not orthogonal
    if intersections[0] == (0, 0, 0):
        intersections.remove((0, 0, 0))
    steps_closest_intersection = intersections[0][2]
    print("Steps to closest intersection: ", steps_closest_intersection)

def main():
    f = open("input/day3.txt")
    path1 = convert_input(f.readline().split(","))
    path2 = convert_input(f.readline().split(","))
    intersections = crossing_points(path1, path2)
    print(intersections)
    part1(intersections)
    part2(intersections)
