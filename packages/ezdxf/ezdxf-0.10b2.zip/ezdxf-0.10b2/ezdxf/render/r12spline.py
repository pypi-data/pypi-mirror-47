# Copyright (c) 2018 Manfred Moitzi
# License: MIT License
"""
DXF R12 Splines
===============

DXF R12 supports 2d B-splines, but Autodesk do not document the usage in the DXF Reference.
The base entity for splines in DXF R12 is the POLYLINE entity.

Transformed Into 3D Space
-------------------------

The spline itself is always in a plane, but as any 2d entity, the spline can be transformed into the 3d object
by elevation, extrusion and thickness/width.

Open Quadratic Spline with Fit Vertices
-------------------------------------

Example: 2D_SPLINE_QUADRATIC.dxf
expected knot vector: open uniform
degree: 2
order: 3

POLYLINE:
flags (70): 4 = SPLINE_FIT_VERTICES_ADDED
smooth type (75): 5 = QUADRATIC_BSPLINE

Sequence of VERTEX
flags (70): SPLINE_VERTEX_CREATED = 8  # Spline vertex created by spline-fitting

This vertices are the curve vertices of the spline (fitted).

Frame control vertices appear after the curve vertices.

Sequence of VERTEX
flags (70): SPLINE_FRAME_CONTROL_POINT = 16

No control point at the starting point, but a control point at the end point,
last control point == last fit vertex

Closed Quadratic Spline with Fit Vertices
-----------------------------------------

Example: 2D_SPLINE_QUADRATIC_CLOSED.dxf
expected knot vector: closed uniform
degree: 2
order: 3

POLYLINE:
flags (70): 5 = CLOSED | SPLINE_FIT_VERTICES_ADDED
smooth type (75): 5 = QUADRATIC_BSPLINE

Sequence of VERTEX
flags (70): SPLINE_VERTEX_CREATED = 8  # Spline vertex created by spline-fitting

Frame control vertices appear after the curve vertices.

Sequence of VERTEX
flags (70): SPLINE_FRAME_CONTROL_POINT = 16


Open Cubic Spline with Fit Vertices
-----------------------------------

Example: 2D_SPLINE_CUBIC.dxf
expected knot vector: open uniform
degree: 3
order: 4

POLYLINE:
flags (70): 4 = SPLINE_FIT_VERTICES_ADDED
smooth type (75): 6 = CUBIC_BSPLINE

Sequence of VERTEX
flags (70): SPLINE_VERTEX_CREATED = 8  # Spline vertex created by spline-fitting

This vertices are the curve vertices of the spline (fitted).

Frame control vertices appear after the curve vertices.

Sequence of VERTEX
flags (70): SPLINE_FRAME_CONTROL_POINT = 16

No control point at the starting point, but a control point at the end point,
last control point == last fit vertex

Closed Curve With Extra Vertices Created
----------------------------------------

Example: 2D_FIT_CURVE_CLOSED.dxf

POLYLINE:
flags (70): 3 = CLOSED | CURVE_FIT_VERTICES_ADDED

Vertices with bulge values:

flags (70): 1 = EXTRA_VERTEX_CREATED
Vertex 70=0, Vertex 70=1, Vertex 70=0, Vertex 70=1

"""
from typing import TYPE_CHECKING, Iterable, List
from ezdxf.lldxf import const
from ezdxf.math.bspline import BSpline, BSplineClosed

if TYPE_CHECKING:
    from ezdxf.eztypes import Vertex, GenericLayoutType, Polyline
    from ezdxf.math.ucs import UCS


class R12Spline:
    def __init__(self, control_points: Iterable['Vertex'], degree: int = 2, closed: bool = True):
        self.control_points = list(control_points)
        self.degree = degree
        self.closed = closed

    def approximate(self, segments: int = 40, ucs: 'UCS' = None) -> List['Vertex']:
        if self.closed:
            spline = BSplineClosed(self.control_points, order=self.degree + 1)
        else:
            spline = BSpline(self.control_points, order=self.degree + 1)
        vertices = spline.approximate(segments)
        if ucs is not None:
            vertices = (ucs.to_ocs(vertex) for vertex in vertices)
        return list(vertices)

    def render(self, layout: 'GenericLayoutType', segments: int = 40, ucs: 'UCS' = None,
               dxfattribs: dict = None) -> 'Polyline':
        polyline = layout.add_polyline2d(points=[], dxfattribs=dxfattribs)
        flags = polyline.SPLINE_FIT_VERTICES_ADDED
        if self.closed:
            flags |= polyline.CLOSED
        polyline.dxf.flags = flags

        if self.degree == 2:
            smooth_type = polyline.QUADRATIC_BSPLINE
        elif self.degree == 3:
            smooth_type = polyline.CUBIC_BSPLINE
        else:
            raise ValueError('invalid degree of spline')
        polyline.dxf.smooth_type = smooth_type

        # set OCS extrusion vector
        if ucs is not None:
            polyline.dxf.extrusion = ucs.uz

        # add fit points in OCS
        polyline.append_vertices(
            self.approximate(segments, ucs),
            dxfattribs={
                'layer': polyline.dxf.layer,
                'flags': const.VTX_SPLINE_VERTEX_CREATED,
            })

        # add control frame points in OCS
        control_points = self.control_points
        if ucs is not None:
            control_points = list(ucs.points_to_ocs(control_points))
            polyline.dxf.elevation = (0, 0, control_points[0].z)
        polyline.append_vertices(control_points, dxfattribs={
            'layer': polyline.dxf.layer,
            'flags': const.VTX_SPLINE_FRAME_CONTROL_POINT,
        })
        return polyline
