# coding=utf-8
"""3D Mesh"""
from __future__ import division

from .._mesh import MeshBase
from ..geometry2d.mesh import Mesh2D

from .pointvector import Point3D, Vector3D
from .plane import Plane
from ._2d import Base2DIn3D

try:
    from itertools import izip as zip  # python 2
except ImportError:
    xrange = range  # python 3


class Mesh3D(MeshBase, Base2DIn3D):
    """3D Mesh object.

    Properties:
        vertices
        faces
        colors
        is_color_by_face
        min
        max
        center
        area
        face_areas
        face_centroids
        face_normals
        vertex_normals
    """
    __slots__ = ('_vertices', '_faces', '_colors', '_is_color_by_face',
                 '_min', '_max', '_center', '_area',
                 '_face_areas', '_face_centroids', '_face_normals',
                 '_vertex_normals')

    def __init__(self, vertices, faces, colors=None):
        """Initilize Mesh3D.

        Args:
            vertices: A list or tuple of Point3D objects for vertices.
            faces: A list of tuples with each tuple having either 3 or 4 integers.
                These integers correspond to indices within the list of vertices.
            colors: An optional list of colors that correspond to either the faces
                of the mesh or the vertices of the mesh. Default is None.
        """
        self._check_vertices_input(vertices)
        self._check_faces_input(faces)

        self._is_color_by_face = False  # default if colors is None
        self.colors = colors
        self._min = None
        self._max = None
        self._center = None
        self._area = None
        self._face_areas = None
        self._face_centroids = None
        self._face_normals = None
        self._vertex_normals = None

    @classmethod
    def from_face_vertices(cls, faces, purge=True):
        """Create a mesh from a list of faces with each face defined by a list of Point3Ds.

        Args:
            faces: A list of faces with each face defined as a list of 3 or 4 Point3D.
            purge: A boolean to indicate if duplicate vertices should be shared between
                faces. Default is True to purge duplicate vertices, which can be slow
                for large lists of faces but results in a higher-quality mesh with
                a smaller size in memory. Default is True.
        """
        vertices, face_collector = cls._interpret_input_from_face_vertices(faces, purge)
        return cls(tuple(vertices), tuple(face_collector))

    @classmethod
    def from_mesh2d(cls, mesh_2d, plane=None):
        """Create a Mesh3D from a Mesh2D and a Plane in which the mesh exists.

        Args:
            mesh_2d: A Mesh2D object.
            plane: A Plane object to represent the plane in which the Mesh2D exists
                within 3D space. If None, the WorldXY plane will be used.
        """
        assert isinstance(mesh_2d, Mesh2D), 'Expected Mesh2D for from_mesh_2d. ' \
            'Got {}.'.format(type(mesh_2d))
        if plane is None:
            return cls(tuple(Point3D(pt.x, pt.y, 0) for pt in mesh_2d.vertices),
                       mesh_2d.faces, mesh_2d.colors)
        else:
            assert isinstance(plane, Plane), 'Expected Plane. Got {}'.format(type(plane))
            _verts3d = tuple(plane.xy_to_xyz(_v) for _v in mesh_2d.vertices)
            return cls(_verts3d, mesh_2d.faces, mesh_2d.colors)

    @property
    def face_areas(self):
        """A tuple of face areas that parallels the faces property."""
        if self._face_normals is None:
            self._calculate_face_areas_and_normals()
        elif isinstance(self._face_areas, (float, int)):  # same area for each face
            self._face_areas = tuple(self._face_areas for face in self.faces)
        return self._face_areas

    @property
    def face_normals(self):
        """Tuple of Vector3D objects for all face normals."""
        if self._face_normals is None:
            self._calculate_face_areas_and_normals()
        elif isinstance(self._face_normals, Vector3D):  # same normal for each face
            self._face_normals = tuple(self._face_normals for face in self.faces)
        return self._face_normals

    @property
    def vertex_normals(self):
        """Tuple of Vector3D objects for all vertex normals."""
        if not self._vertex_normals:
            self._calculate_vertex_normals()
        elif isinstance(self._vertex_normals, Vector3D):  # same normal for each vertex
            self._vertex_normals = tuple(self._vertex_normals for face in self.vertices)
        return self._vertex_normals

    def remove_vertices(self, pattern):
        """Get a version of this mesh where vertices are removed according to a pattern.

        Args:
            pattern: A list of boolean values denoting whether a vertex should
                remain in the mesh (True) or be removed from the mesh (False).
                The length of this list must match the number of this mesh's vertices.

        Returns:
            new_mesh: A mesh where the vertices have been removed according
                to the input pattern.
            face_pattern: A list of boolean values that corresponds to the
                original mesh faces noting whether the face is in the new mesh
                (True) or has been removed from the new mesh (False).
        """
        _new_verts, _new_faces, _new_colors, _new_f_cent, _new_f_area, face_pattern = \
            self._remove_vertices(pattern)

        new_mesh = Mesh3D(_new_verts, _new_faces, _new_colors)
        new_mesh._face_centroids = _new_f_cent
        new_mesh._face_areas = _new_f_area
        return new_mesh, face_pattern

    def remove_faces(self, pattern):
        """Get a version of this mesh where faces are removed according to a pattern.

        Args:
            pattern: A list of boolean values denoting whether a face should
                remain in the mesh (True) or be removed from the mesh (False).
                The length of this list must match the number of this mesh's faces.

        Returns:
            new_mesh: A mesh where the faces have been removed according
                to the input pattern.
            vertex_pattern: A list of boolean values that corresponds to the
                original mesh vertices noting whether the vertex is in the new mesh
                (True) or has been removed from the new mesh (False).
        """
        vertex_pattern = self._vertex_pattern_from_remove_faces(pattern)
        _new_verts, _new_faces, _new_colors, _new_f_cent, _new_f_area, face_pattern = \
            self._remove_vertices(vertex_pattern, pattern)

        new_mesh = Mesh3D(_new_verts, _new_faces, _new_colors)
        new_mesh._face_centroids = _new_f_cent
        new_mesh._face_areas = _new_f_area
        return new_mesh, vertex_pattern

    def remove_faces_only(self, pattern):
        """Get a version of this mesh where faces are removed and vertices are not altered.

        This is faster than the Mesh3D.remove_faces method but will likely result
        a lower-quality mesh where several vertices exist in the mesh that are not
        referenced by any face. This may be preferred if pure speed of removing
        faces is a priorty over smallest size of the mesh in memory.

        Args:
            pattern: A list of boolean values denoting whether a face should
                remain in the mesh (True) or be removed from the mesh (False).
                The length of this list must match the number of this mesh's faces.

        Returns:
            new_mesh: A mesh where the faces have been removed according
                to the input pattern.
        """
        _new_faces, _new_colors, _new_f_cent, _new_f_area = \
            self._remove_faces_only(pattern)

        new_mesh = Mesh3D(self.vertices, _new_faces, _new_colors)
        new_mesh._face_centroids = _new_f_cent
        new_mesh._face_areas = _new_f_area
        return new_mesh

    def rotate(self, axis, angle, origin):
        """Rotate a mesh by a certain angle around an axis and origin.

        Right hand rule applies:
        If axis has a positive orientation, rotation will be clockwise.
        If axis has a negative orientation, rotation will be counterclockwise.

        Args:
            axis: A Vector3D axis representing the axis of rotation.
            angle: An angle for rotation in radians.
            origin: A Point3D for the origin around which the point will be rotated.
        """
        _verts = tuple(pt.rotate(axis, angle, origin) for pt in self.vertices)
        return self._mesh_transform(_verts)

    def rotate_xy(self, angle, origin):
        """Get a mesh rotated counterclockwise in the XY plane by a certain angle.

        Args:
            angle: An angle for rotation in radians.
            origin: A Point3D for the origin around which the point will be rotated.
        """
        _verts = tuple(pt.rotate_xy(angle, origin) for pt in self.vertices)
        return self._mesh_transform(_verts)

    def scale(self, factor, origin=None):
        """Scale a mesh by a factor from an origin point.

        Args:
            factor: A number representing how much the mesh should be scaled.
            origin: A Point representing the origin from which to scale.
                If None, it will be scaled from the World origin (0, 0, 0).
        """
        if origin is None:
            _verts = tuple(
                Point3D(pt.x * factor, pt.y * factor, pt.z * factor)
                for pt in self.vertices)
        else:
            _verts = tuple(pt.scale(factor, origin) for pt in self.vertices)
        return self._mesh_scale(_verts, factor)

    def _calculate_face_areas_and_normals(self):
        """Calculate face areas and normals from vertices."""
        _f_norm = []
        _f_area = []
        for face in self.faces:
            pts = tuple(self._vertices[i] for i in face)
            if len(face) == 3:
                n, a = self._calculate_normal_and_area_for_triangle(pts)
            else:
                n, a = self._calculate_normal_and_area_for_quad(pts)
            _f_norm.append(n)
            _f_area.append(a)
        self._face_normals = tuple(_f_norm)
        self._face_areas = tuple(_f_area)

    def _calculate_vertex_normals(self):
        """Calculate vertex normals.

        This is accomplished by normalizing the average of the surface normals
        of the faces that contain that vertex.  This particular method weights
        this average by the area of each face, though this does not always need
        to be the case as noted here:
        https://en.wikipedia.org/wiki/Vertex_normal
        """
        # find shared faces for each vertices
        mapper = [[] for v in range(len(self.vertices))]
        for c, face in enumerate(self.faces):
            for i in face:
                mapper[i].append(c)
        # now calculate vertex normal based on face normals
        vn = []
        fn = self.face_normals
        fa = self.face_areas
        for fi in mapper:
            x, y, z = 0, 0, 0
            for n, a in zip(tuple(fn[i] for i in fi), tuple(fa[i] for i in fi)):
                x += n.x * a
                y += n.y * a
                z += n.z * a
            _v = Vector3D(x, y, z)
            vn.append(_v.normalize())
        self._vertex_normals = tuple(vn)

    def _tri_face_centroid(self, face):
        """Compute the centroid of a triangular face."""
        return Mesh3D._tri_centroid(tuple(self._vertices[i] for i in face))

    def _quad_face_centroid(self, face):
        """Compute the centroid of a quadrilateral face."""
        return Mesh3D._quad_centroid(tuple(self._vertices[i] for i in face))

    def _mesh_transform(self, verts):
        """Transform mesh in a way that transfers properties and avoids extra checks."""
        _new_mesh = Mesh3D(verts, self.faces)
        self._transfer_properties(_new_mesh)
        return _new_mesh

    def _mesh_transform_move(self, verts):
        """Move mesh in a way that transfers properties and avoids extra checks."""
        _new_mesh = Mesh3D(verts, self.faces)
        self._transfer_properties(_new_mesh)
        _new_mesh._face_normals = self._face_normals
        _new_mesh._vertex_normals = self._vertex_normals
        return _new_mesh

    def _mesh_scale(self, verts, factor):
        """Scale mesh in a way that transfers properties and avoids extra checks."""
        _new_mesh = Mesh3D(verts, self.faces)
        self._transfer_properties_scale(_new_mesh, factor)
        _new_mesh._face_normals = self._face_normals
        _new_mesh._vertex_normals = self._vertex_normals
        return _new_mesh

    @staticmethod
    def _calculate_normal_and_area_for_triangle(pts):
        """Calculate normal and area for three points.

        Returns:
            n = Normalized normal vector for the triangle.
            a = Area of the triangle.
        """
        v1 = pts[1] - pts[0]
        v2 = pts[2] - pts[0]
        n = v1.cross(v2)
        a = n.magnitude / 2
        return n.normalize(), a

    @staticmethod
    def _calculate_normal_and_area_for_quad(pts):
        """Calculate normal and area for four points.

        This method uses an area-weighted average of the two triangle normals
        that compose the quad face.

        Returns:
            n = Normalized normal vector for the quad.
            a = Area of the quad.
        """
        # TODO: Get this method to work for concave quads.
        # This method is only reliable when quads are convex since we assume
        # either diagonal of the quad splits it into two triangles.
        # It seems Rhino never produces concave quads when it automatically meshes
        # but we will likely want to add support for this if meshes have other origins
        v1 = pts[1] - pts[0]
        v2 = pts[2] - pts[0]
        n1 = v1.cross(v2)

        v3 = pts[3] - pts[2]
        v4 = pts[1] - pts[2]
        n2 = v3.cross(v4)

        a = (n1.magnitude + n2.magnitude) / 2
        n = Vector3D((n1.x + n2.x) / 2, (n1.y + n2.y) / 2, (n1.z + n2.z) / 2)
        return n.normalize(), a

    @staticmethod
    def _tri_centroid(verts):
        """Get the centroid of a list of 3 Point3D vertices."""
        _cent_x = sum([v.x for v in verts])
        _cent_y = sum([v.y for v in verts])
        _cent_z = sum([v.z for v in verts])
        return Point3D(_cent_x / 3, _cent_y / 3, _cent_z / 3)

    @staticmethod
    def _quad_centroid(verts):
        """Get the centroid of a list of 4 Point3D vertices."""
        # TODO: Get this method to recognize concave quads.
        # This method is only reliable when quads are convex since we assume
        # either diagonal of the quad splits it into two triangles.
        # It seems Rhino never produces concave quads when it automatically meshes
        # but we will likely want to add support for this if meshes have other origins
        _tri_verts = ((verts[0], verts[1], verts[2]), (verts[2], verts[3], verts[0]))
        _tri_c = [Mesh3D._tri_centroid(tri) for tri in _tri_verts]
        _tri_a = [Mesh3D._get_tri_area(tri) for tri in _tri_verts]
        _tot_a = sum(_tri_a)
        _cent_x = (_tri_c[0].x * _tri_a[0] + _tri_c[1].x * _tri_a[1]) / _tot_a
        _cent_y = (_tri_c[0].y * _tri_a[0] + _tri_c[1].y * _tri_a[1]) / _tot_a
        _cent_z = (_tri_c[0].z * _tri_a[0] + _tri_c[1].z * _tri_a[1]) / _tot_a
        return Point3D(_cent_x, _cent_y, _cent_z)

    @staticmethod
    def _get_tri_area(pts):
        """Get the area of a triangle from three Point3D objects."""
        v1 = pts[1] - pts[0]
        v2 = pts[2] - pts[0]
        n1 = v1.cross(v2)
        return n1.magnitude / 2

    def __copy__(self):
        _new_mesh = Mesh3D(self.vertices, self.faces)
        self._transfer_properties(_new_mesh)
        _new_mesh._face_centroids = self._face_centroids
        _new_mesh._face_normals = self._face_normals
        _new_mesh._vertex_normals = self._vertex_normals
        return _new_mesh

    def __repr__(self):
        return 'Mesh3D ({} faces) ({} vertices)'.format(
            len(self.faces), len(self))
