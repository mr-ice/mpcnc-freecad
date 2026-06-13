"""
THXX drawer bin inserts - FreeCAD model generator.
Creates organizer bins per TXHHPROJECT.md using configtxhh.
"""

import FreeCAD
import Part
import configtxhh as cfg

# Tolerance for geometric comparisons (mm)
_TOL = 0.02


def _make_bowtie_wire(length_mm, width_mm, narrow_width_mm, length_along_x=True):
    """
    Bowtie = two trapezoids joined at the short edge. Centered at origin.
    length_mm along primary axis, width_mm at the two ends, narrow_width_mm at center.
    If length_along_x True, length is along X and width along Y; else swapped.
    """
    L, W, Wn = length_mm, width_mm, narrow_width_mm
    # u = length axis, v = width axis. u from -L/2 to L/2; v wide at ends, narrow at 0
    pts_uv = [
        (-L / 2, -W / 2),
        (-L / 2, W / 2),
        (0, Wn / 2),
        (L / 2, W / 2),
        (L / 2, -W / 2),
        (0, -Wn / 2),
    ]
    if length_along_x:
        pts = [(u, v) for u, v in pts_uv]
    else:
        pts = [(v, u) for u, v in pts_uv]
    verts = [FreeCAD.Vector(p[0], p[1], 0) for p in pts]
    edges = []
    for i in range(len(verts)):
        edges.append(Part.LineSegment(verts[i], verts[(i + 1) % len(verts)]).toShape())
    return Part.Wire(edges)


def _make_bowtie_connector_solid(
    length_mm, width_mm, narrow_width_mm, height_mm, length_along_x=True
):
    """Solid bowtie (connector) extruded in +Z by height_mm."""
    wire = _make_bowtie_wire(length_mm, width_mm, narrow_width_mm, length_along_x)
    face = Part.Face(wire)
    return face.extrude(FreeCAD.Vector(0, 0, height_mm))


def _make_bowtie_hole_solid(
    length_mm, width_mm, narrow_width_mm, height_mm, tolerance_mm, length_along_x=True
):
    """
    Bowtie-shaped hole: outline expanded by tolerance. Extruded in +Z.
    """
    wire = _make_bowtie_wire(length_mm, width_mm, narrow_width_mm, length_along_x)
    face = Part.Face(wire)
    try:
        offset_face = face.makeOffset2D(tolerance_mm / 2.0)
        if offset_face.Area < 1e-6:
            offset_face = face
    except Exception:
        scale = 1.0 + tolerance_mm / min(length_mm, width_mm)
        wn = narrow_width_mm * scale
        wire = _make_bowtie_wire(
            length_mm * scale, width_mm * scale, wn, length_along_x
        )
        offset_face = Part.Face(wire)
    return offset_face.extrude(FreeCAD.Vector(0, 0, height_mm))


def _connector_grid_positions():
    """
    Yield (gx, gy, length_along_x) for all bins. Connectors use same offset from
    edges (d/8 from depth ends, w/3 from width ends) so they line up when adjacent.
    Each bin gets connector sets on all four edges (top, bottom, left, right).
    """
    w = cfg.INSERT_WIDTH_MM
    d = cfg.INSERT_DEPTH_MM
    g = cfg.BETWEEN_BIN_TOLERANCE_MM
    nr = cfg.CONNECTOR_GRID_ROWS
    d1 = d * cfg.BIN1_DEPTH_FRAC
    w2 = w * cfg.BIN2_WIDTH_FRAC
    d2 = d * cfg.BIN2_DEPTH_FRAC
    w3 = w * cfg.BIN3_WIDTH_FRAC
    w4 = w * cfg.BIN4_WIDTH_FRAC
    d4 = d * cfg.BIN4_DEPTH_FRAC
    half_spacing = (d / nr) / 2.0
    edge_offset = half_spacing  # d/8 from each end

    def bin1_edges():
        bx, by = 0.0, -d1 * 1.5
        bw, bd = w, d1
        # Top/bottom: same x as Bin3 (w/3, 2*w/3), offset d/8 from ends
        for gx in (w / cfg.CONNECTOR_GRID_COLS, 2 * w / cfg.CONNECTOR_GRID_COLS):
            yield gx, by + bd - edge_offset, True
            if by + edge_offset < by + bd - edge_offset - 1e-6:
                yield gx, by + edge_offset, True
        # Left/right: same offset d/8 from top/bottom
        gy_lo, gy_hi = by + edge_offset, by + bd - edge_offset
        for gy in (gy_lo,) if abs(gy_lo - gy_hi) < 1e-6 else (gy_lo, gy_hi):
            yield bx, gy, False
            yield bx + bw, gy, False

    def bin2_edges():
        bx, by = -w2, d1 + g
        bw, bd = w2, d2
        # Top/bottom edges: x offset d/8 from Bin2's sides; y at top/bottom
        for gx in (bx + edge_offset, bx + bw - edge_offset):
            yield gx, by + edge_offset, False
            yield gx, by + bd - edge_offset, False
        # Left/right edges: same row spacing d/4 as Bin3, rows that fit in Bin2
        gy_row = by + edge_offset
        while gy_row <= by + bd - 1e-6:
            yield bx, gy_row, True
            yield bx + bw, gy_row, True
            gy_row += d / nr

    def bin3_edges():
        bx, by = w2 + g, 0.0
        bw, bd = w3, d
        # Interior + top/bottom: x = w/3, 2*w/3; rows at d/8, 3*d/8, 5*d/8, 7*d/8
        for gx in (w / cfg.CONNECTOR_GRID_COLS, 2 * w / cfg.CONNECTOR_GRID_COLS):
            for j in range(1, nr):
                yield gx, j * d / nr - half_spacing, True
            yield gx, d - half_spacing, True
        # Left and right edges: same row pattern
        for j in range(1, nr):
            gy = j * d / nr - half_spacing
            yield bx, gy, False
            yield bx + bw, gy, False
        gy_top = by + bd - half_spacing
        yield bx, gy_top, False
        yield bx + bw, gy_top, False

    def bin4_edges():
        bx, by = w3 + g + w4, d1 + g
        bw, bd = w4, d4
        for gx in (bx + edge_offset, bx + bw - edge_offset):
            yield gx, by + edge_offset, False  # bottom
            yield gx, by + bd - edge_offset, False  # top
        for gy in (by + edge_offset, by + bd - edge_offset):
            yield bx, gy, True  # left
            yield bx + bw, gy, True  # right

    for _ in bin1_edges():
        yield _
    for _ in bin2_edges():
        yield _
    for _ in bin3_edges():
        yield _
    for _ in bin4_edges():
        yield _


def _make_bin_box(width, depth, height, wall_mm):
    """
    Creates a single open-top bin (hollow box with walls and floor).
    All dimensions external; wall thickness applied inward.
    """
    outer = Part.makeBox(width, depth, height)
    inner_w = width - (2 * wall_mm)
    inner_d = depth - (2 * wall_mm)
    inner_h = height - wall_mm  # floor thickness = wall_mm
    if inner_w <= 0 or inner_d <= 0 or inner_h <= 0:
        return outer
    inner = Part.makeBox(inner_w, inner_d, inner_h)
    inner.translate(FreeCAD.Vector(wall_mm, wall_mm, wall_mm))
    return outer.cut(inner)


def _collect_vert_edges(shape, tol=0.02):
    """Collect all vertical edges from shape (same X,Y, different Z)."""
    out = []
    for edge in shape.Edges:
        if len(edge.Vertexes) != 2:
            continue
        v1, v2 = edge.Vertexes[0], edge.Vertexes[1]
        if abs(v1.X - v2.X) < tol and abs(v1.Y - v2.Y) < tol and abs(v1.Z - v2.Z) > tol:
            out.append(edge)
    return out


def _collect_inside_top_horiz_edges(shape, width, depth, height, wall_mm, tol=0.02):
    """Collect horizontal edges at top that lie on the inner rim."""
    inner_x_lo = wall_mm - tol
    inner_x_hi = width - wall_mm + tol
    inner_y_lo = wall_mm - tol
    inner_y_hi = depth - wall_mm + tol
    top_z_lo = height - tol
    out = []
    for edge in shape.Edges:
        if len(edge.Vertexes) != 2:
            continue
        v1, v2 = edge.Vertexes[0], edge.Vertexes[1]
        dx = abs(v1.X - v2.X)
        dy = abs(v1.Y - v2.Y)
        dz = abs(v1.Z - v2.Z)
        if dz >= tol or (dx < tol and dy < tol):
            continue
        z_val = (v1.Z + v2.Z) / 2
        if z_val < top_z_lo:
            continue
        x_in = inner_x_lo <= v1.X <= inner_x_hi and inner_x_lo <= v2.X <= inner_x_hi
        y_in = inner_y_lo <= v1.Y <= inner_y_hi and inner_y_lo <= v2.Y <= inner_y_hi
        if x_in and y_in:
            out.append(edge)
    return out


def _cut_bowtie_holes(shape, bin_x, bin_y, width, depth, height, wall_mm):
    """
    Cut half- or full bowtie holes in the bin's bottom (floor). Connectors
    are at interior grid edges (where bins meet). For each position whose
    hole overlaps this bin, cut (hole solid ∩ bin floor box) from shape.
    """
    L = cfg.BOWTIE_LENGTH_MM
    W = cfg.BOWTIE_WIDTH_MM
    Wn = W * cfg.BOWTIE_NARROW_FRAC
    tol = cfg.CONNECTOR_HOLE_TOLERANCE_MM
    half_L = (L + tol) / 2.0
    half_W = (W + tol) / 2.0
    floor_box = Part.makeBox(width, depth, wall_mm)
    result = shape
    for gx, gy, length_along_x in _connector_grid_positions():
        lx = gx - bin_x
        ly = gy - bin_y
        if (
            lx + half_L < 0
            or lx - half_L > width
            or ly + half_W < 0
            or ly - half_W > depth
        ):
            continue
        hole_at = _make_bowtie_hole_solid(L, W, Wn, wall_mm, tol, length_along_x)
        hole_at.translate(FreeCAD.Vector(lx, ly, 0))
        cut_piece = hole_at.common(floor_box)
        if cut_piece.Volume > 1e-6:
            result = result.cut(cut_piece)
    return result


def _fillet_bin(shape, width, depth, height, wall_mm, vert_radius, horiz_radius):
    """
    Applies fillets per TXHHPROJECT.md: all vertical edges, then
    inside top horizontal edges. Radii are capped by wall thickness
    (BRep fails with "command not done" if radius exceeds adjacent material).
    Re-queries edges from the modified shape before the second fillet.
    """
    max_r = wall_mm * cfg.FILLET_MAX_FRAC_OF_WALL
    vert_r = min(vert_radius, max_r)
    horiz_r = min(horiz_radius, max_r)
    try:
        vert_edges = _collect_vert_edges(shape)
        if not vert_edges:
            result = shape
        else:
            result = shape.makeFillet(vert_r, vert_edges)
        inside_top = _collect_inside_top_horiz_edges(
            result, width, depth, height, wall_mm
        )
        if inside_top:
            result = result.makeFillet(horiz_r, inside_top)
        return result
    except Exception as e:
        print(f"Warning: fillet failed: {e}")
        return shape


def create_bin_1():
    """Bin 1: full width, 1/4 depth."""
    w = cfg.INSERT_WIDTH_MM
    d = cfg.INSERT_DEPTH_MM * cfg.BIN1_DEPTH_FRAC
    h = cfg.BIN_HEIGHT_MM
    box = _make_bin_box(w, d, h, cfg.WALL_MIN_MM)
    return _fillet_bin(
        box,
        w,
        d,
        h,
        cfg.WALL_MIN_MM,
        cfg.CORNER_RADIUS_VERTICAL_MM,
        cfg.CORNER_RADIUS_HORIZONTAL_MM,
    )


def create_bin_2():
    """Bin 2: 1/3 width, 3/4 depth."""
    w = cfg.INSERT_WIDTH_MM * cfg.BIN2_WIDTH_FRAC
    d = cfg.INSERT_DEPTH_MM * cfg.BIN2_DEPTH_FRAC
    h = cfg.BIN_HEIGHT_MM
    box = _make_bin_box(w, d, h, cfg.WALL_MIN_MM)
    return _fillet_bin(
        box,
        w,
        d,
        h,
        cfg.WALL_MIN_MM,
        cfg.CORNER_RADIUS_VERTICAL_MM,
        cfg.CORNER_RADIUS_HORIZONTAL_MM,
    )


def create_bin_3():
    """Bin 3: 1/3 width, full depth."""
    w = cfg.INSERT_WIDTH_MM * cfg.BIN3_WIDTH_FRAC
    d = cfg.INSERT_DEPTH_MM * cfg.BIN3_DEPTH_FRAC
    h = cfg.BIN_HEIGHT_MM
    box = _make_bin_box(w, d, h, cfg.WALL_MIN_MM)
    return _fillet_bin(
        box,
        w,
        d,
        h,
        cfg.WALL_MIN_MM,
        cfg.CORNER_RADIUS_VERTICAL_MM,
        cfg.CORNER_RADIUS_HORIZONTAL_MM,
    )


def create_bin_4():
    """Bin 4: 2/3 width, full height, 1/2 depth."""
    w = cfg.INSERT_WIDTH_MM * cfg.BIN4_WIDTH_FRAC
    d = cfg.INSERT_DEPTH_MM * cfg.BIN4_DEPTH_FRAC
    h = cfg.BIN_HEIGHT_MM
    box = _make_bin_box(w, d, h, cfg.WALL_MIN_MM)
    return _fillet_bin(
        box,
        w,
        d,
        h,
        cfg.WALL_MIN_MM,
        cfg.CORNER_RADIUS_VERTICAL_MM,
        cfg.CORNER_RADIUS_HORIZONTAL_MM,
    )


def get_bin_positions():
    """
    Returns (name, shape_fn, x, y, z, width, depth) for each bin.
    Positions: bins pushed apart (Bin1 -Y by depth, Bin2 -X by width,
    Bin4 +X by width) so connector holes are in the correct bins.
    """
    g = cfg.BETWEEN_BIN_TOLERANCE_MM
    d = cfg.INSERT_DEPTH_MM
    w = cfg.INSERT_WIDTH_MM
    d1 = d * cfg.BIN1_DEPTH_FRAC
    w2 = w * cfg.BIN2_WIDTH_FRAC
    d2 = d * cfg.BIN2_DEPTH_FRAC
    w3 = w * cfg.BIN3_WIDTH_FRAC
    w4 = w * cfg.BIN4_WIDTH_FRAC
    d4 = d * cfg.BIN4_DEPTH_FRAC
    return [
        ("Bin1", create_bin_1, 0.0, -d1 * 1.5, 0.0, w, d1),
        ("Bin2", create_bin_2, -w2, d1 + g, 0.0, w2, d2),
        ("Bin3", create_bin_3, w2 + g, 0.0, 0.0, w3, d),
        ("Bin4", create_bin_4, w3 + g + w4, d1 + g, 0.0, w4, d4),
    ]


def build_model(doc):
    """
    Creates all THXX organizer bin objects and bowtie connectors in the document.
    Cuts half/full bowtie holes in each bin floor; places connectors at interior
    grid edges (1/3 and 2/3 width, 1/4–3/4 depth) so they lock adjacent bins.
    """
    positions = get_bin_positions()
    for name, _sf, _x, _y, _z, _w, _d in positions:
        if hasattr(doc, name):
            doc.removeObject(name)
    conn_name_prefix = "Connector"
    for obj in list(doc.Objects):
        if obj.Name.startswith(conn_name_prefix):
            doc.removeObject(obj.Name)
    h = cfg.BIN_HEIGHT_MM
    wall = cfg.WALL_MIN_MM
    z = 0.0
    for name, shape_fn, x, y, z, width, depth in positions:
        shape = shape_fn()
        shape = _cut_bowtie_holes(shape, x, y, width, depth, h, wall)
        shape.translate(FreeCAD.Vector(x, y, z))
        obj = doc.addObject("Part::Feature", name)
        obj.Shape = shape
    Wn = cfg.BOWTIE_WIDTH_MM * cfg.BOWTIE_NARROW_FRAC
    for idx, (gx, gy, length_along_x) in enumerate(_connector_grid_positions()):
        conn = _make_bowtie_connector_solid(
            cfg.BOWTIE_LENGTH_MM,
            cfg.BOWTIE_WIDTH_MM,
            Wn,
            wall,
            length_along_x,
        )
        conn.translate(FreeCAD.Vector(gx, gy, z))
        cname = f"{conn_name_prefix}_{idx}"
        obj = doc.addObject("Part::Feature", cname)
        obj.Shape = conn
    doc.recompute()
    return [doc.getObject(name) for name, _, _, _, _, _, _ in positions]
