package quad_tree

import "core:math"

// rectangle usage
// rect.x, rect.y = top corner
// rect.z, rect.w = width and height in that order
// DO NOT CONFUSE rect.w FOR WIDTH

Element :: struct ($T : typeid) {
    data : T,
    shape : Shape,
}

Shape :: union {
    Rectangle,
    Circle,
    Line,
    Point,
}

Rectangle :: [4]f32
Circle :: struct {c : [2]f32, r : f32}
Line :: struct {p1 : [2]f32, p2 : [2]f32}
Point :: [2]f32

Node :: struct ($T : typeid) {
    rect : [4]f32,
    max_elements : int,
    min_dim : [2]f32,
    elements : [dynamic]Element(T),
    children : [4]^Node(T),
}

create_node :: proc ($T : typeid, rect : [4]f32, max_elements : int, min_dim : [2]f32) -> ^Node(T) {
    new_node := new(Node(T))
    new_node.rect = rect
    new_node.max_elements = max_elements
    new_node.min_dim = min_dim
    new_node.elements = make([dynamic]Element(T), 0, max_elements)
    new_node.children = {nil, nil, nil, nil}
    return new_node
}

destroy_node :: proc (node : ^Node($T)) {
    delete(node.elements)
    if node.children[0] != nil {
        for child in node.children {
            destroy_node(child)
        }
    }
    free(node)
}

insert :: proc (node : ^Node($T), data : T, shape : Shape) {
    if node.children[0] == nil {
        append(&node.elements, Element(T){data, shape})
        check_and_subdivide(node)
    }
    else {
        for child in node.children {
            if shape_intersects_rect(shape, child.rect) do insert(child, data, shape)
        }
    }
}

check_and_subdivide :: proc (node : ^Node($T)) {
    if !(node.rect.z > node.min_dim[0] && node.rect.w > node.min_dim[1] && len(node.elements) > node.max_elements) do return
    x_mid := node.rect.x + node.rect.z / 2
    y_mid := node.rect.y + node.rect.w / 2
    node.children[0] = create_node(T, {node.rect.x,   node.rect.y,    node.rect.z / 2, node.rect.w / 2}, node.max_elements, node.min_dim)
    node.children[1] = create_node(T, {x_mid,         node.rect.y,    node.rect.z / 2, node.rect.w / 2}, node.max_elements, node.min_dim)
    node.children[2] = create_node(T, {node.rect.x,   y_mid,          node.rect.z / 2, node.rect.w / 2}, node.max_elements, node.min_dim)
    node.children[3] = create_node(T, {x_mid,         y_mid,          node.rect.z / 2, node.rect.w / 2}, node.max_elements, node.min_dim)
    for element in node.elements {
        insert(node, element.data, element.shape)
    }
    clear(&node.elements)
}

query :: proc (node : ^Node($T), array : ^[dynamic]T, shape : Shape) {
    if node.children[0] == nil {
        for element in node.elements {
            if shapes_intersect(element.shape, shape){
                append(array, element.data)
            }
        }
    }
    else {
        for child in node.children {
            query(child, array, shape)
        }
    }
}

shapes_intersect :: proc (shape1 : Shape, shape2 : Shape) -> bool {
    switch s1 in shape1 {
        case Rectangle:
            return shape_intersects_rect(shape2, s1)
        case Circle:
            return shape_intersects_circle(shape2, s1)
        case Line:
            return shape_intersects_line(shape2, s1)
        case Point:
            return shape_intersects_point(shape2, s1)
    }
    return false
}

shape_intersects_rect :: proc (shape : Shape, rect : Rectangle) -> bool {
    switch s in shape {
        case Rectangle:
            return rects_intersect(rect, s)
        case Circle:
            return rect_intersects_circle(rect, s)
        case Line:
            return rect_intersects_line(rect, s)
        case Point:
            return rect_has_point(rect, s)
    }
    return false
}

shape_intersects_circle :: proc (shape : Shape, circle : Circle) -> bool {
    switch s in shape {
        case Rectangle:
            return rect_intersects_circle(s, circle)
        case Circle:
            return circles_intersect(circle, s)
        case Line:
            return line_intersects_circle(s, circle)
        case Point:
            return circle_has_point(circle, s)
    }
    return false
}

shape_intersects_line :: proc (shape : Shape, line : Line) -> bool {
    switch s in shape {
        case Rectangle:
            return rect_intersects_line(s, line)
        case Circle:
            return line_intersects_circle(line, s)
        case Line:
            return lines_intersect(s, line)
        case Point:
            return line_intersects_point(line, s)
    }
    return false
}

shape_intersects_point :: proc (shape : Shape, point : Point) -> bool {
    switch s in shape {
        case Rectangle:
            return rect_has_point(s, point)
        case Circle:
            return circle_has_point(s, point)
        case Line:
            return line_intersects_point(s, point)
        case Point:
            return points_are_close_enough(s, point)
    }
    return false
}

rects_intersect :: proc (rect1 : [4]f32, rect2 : [4]f32) -> bool {
    x1a := rect1.x
    y1a := rect1.y
    x2a := rect1.x + rect1.z
    y2a := rect1.y + rect1.w
    x1b := rect2.x
    y1b := rect2.y
    x2b := rect2.x + rect2.z
    y2b := rect2.y + rect2.w
    return !(x1a >= x2b || x2a <= x1b || y1a >= y2b || y2a <= y1b)
}

rect_intersects_circle :: proc (rect : Rectangle, circle : Circle) -> bool {
    x, y, w, h := rect.x, rect.y, rect.z, rect.w
    // Find closest point on rect to circle center
    closest_x := math.max(x, math.min(circle.c.x, x + w))
    closest_y := math.max(y, math.min(circle.c.y, y + h))
    // Distance from center to closest point
    dx := circle.c.x - closest_x
    dy := circle.c.y - closest_y
    dist := math.sqrt(dx*dx + dy*dy)
    return dist <= circle.r
}

rect_has_point :: proc(rect : Rectangle, p : Point) -> bool {
    x := p.x >= rect.x && p.x <= rect.x + rect.z
    y := p.y >= rect.y && p.y <= rect.y + rect.w
    return x && y
}

rect_intersects_line :: proc(rect: Rectangle, l: Line) -> bool {
    rx, ry, rw, rh := rect.x, rect.y, rect.z, rect.w
    rx2, ry2 := rx + rw, ry + rh
    // Quick rejection: if line's bounding box doesn't overlap rect
    min_x := math.min(l.p1.x, l.p2.x)
    max_x := math.max(l.p1.x, l.p2.x)
    min_y := math.min(l.p1.y, l.p2.y)
    max_y := math.max(l.p1.y, l.p2.y)
    if max_x < rx || min_x > rx2 || max_y < ry || min_y > ry2 {
        return false
    }
    // Check if either endpoint is inside rect (counts as intersect)
    if rect_has_point(rect, l.p1) || rect_has_point(rect, l.p2) {
        return true
    }
    // Check line against each of the 4 rect edges (line-line intersect)
    edges := [4]Line{
        {{rx, ry}, {rx2, ry}},    // top
        {{rx2, ry}, {rx2, ry2}},   // right
        {{rx2, ry2}, {rx, ry2}},   // bottom
        {{rx, ry2}, {rx, ry}},     // left
    }
    for edge in edges {
        if lines_intersect(l, edge) {
            return true
        }
    }
    return false
}

// Line vs Circle: true if line segment intersects or touches the circle
line_intersects_circle :: proc(line : Line, circle : Circle) -> bool {
    dir := line.p2 - line.p1
    len2 := dot(dir, dir)
    if len2 == 0 {  // degenerate line (point)
        return magnitude(line.p1 - circle.c) <= circle.r
    }

    to_center := circle.c - line.p1
    proj_len := dot(dir, to_center) / len2
    closest_t := math.clamp(proj_len, 0.0, 1.0)
    closest_point := line.p1 + dir * closest_t
    dist := magnitude(closest_point - circle.c)

    return dist <= circle.r
}

// Line vs Point: true if point lies on the line segment (within epsilon for float precision)
line_intersects_point :: proc(l: Line, p: Point) -> bool {
    EPSILON :: 1e-5
    d1 := magnitude(p - l.p1)
    d2 := magnitude(p - l.p2)
    line_len := magnitude(l.p1 - l.p2)
    // Collinear check: distances add up to line length (within eps)
    return math.abs(d1 + d2 - line_len) <= EPSILON
}

// Helper: true if two line segments intersect or touch (used in line_vs_rect)
lines_intersect :: proc(a, b: Line) -> bool {
    // Standard 2D line segment intersection (using orientations)
    o1 := orientation(a.p1, a.p2, b.p1)
    o2 := orientation(a.p1, a.p2, b.p2)
    o3 := orientation(b.p1, b.p2, a.p1)
    o4 := orientation(b.p1, b.p2, a.p2)

    if o1 != o2 && o3 != o4 {
        return true
    }

    // Special cases for collinear and overlapping
    if o1 == 0 && on_segment(a.p1, b.p1, a.p2) { return true }
    if o2 == 0 && on_segment(a.p1, b.p2, a.p2) { return true }
    if o3 == 0 && on_segment(b.p1, a.p1, b.p2) { return true }
    if o4 == 0 && on_segment(b.p1, a.p2, b.p2) { return true }

    return false
}

// Sub-helper for lines_intersect: 0 = collinear, 1 = clockwise, -1 = counterclockwise
orientation :: proc(p, q, r: [2]f32) -> int {
    val := (q[1] - p[1]) * (r[0] - q[0]) - (q[0] - p[0]) * (r[1] - q[1])
    if val == 0 { return 0 }
    return 1 if val > 0 else -1
}

// Sub-helper for lines_intersect: true if r is on segment p-q
on_segment :: proc(p, r, q: [2]f32) -> bool {
    if r[0] <= math.max(p[0], q[0]) && r[0] >= math.min(p[0], q[0]) &&
        r[1] <= math.max(p[1], q[1]) && r[1] >= math.min(p[1], q[1]) {
            return true
        }
        return false
}

circles_intersect :: proc (circle1 : Circle, circle2 : Circle) -> bool {
    return magnitude(circle1.c - circle2.c) <= circle1.r + circle2.r
}

circle_has_point :: proc (circle : Circle, point : Point) -> bool {
    return magnitude(circle.c - point) <= circle.r
}

points_are_close_enough :: proc (p1 : Point, p2 : Point) -> bool {
    EPSILON :: 1e-5
    return magnitude(p1 - p2) <= EPSILON
}

magnitude :: #force_inline proc (vec : [2]f32) -> f32 {
    return math.sqrt_f32(vec.x * vec.x + vec.y * vec.y)
}

dot :: #force_inline proc (vec1 : [2]f32, vec2 : [2]f32) -> f32 {
    return vec1.x * vec2.x + vec1.y * vec2.y
}
