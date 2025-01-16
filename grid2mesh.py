import numpy as np
 
class SurfaceMesh:
    """Simple class to represent a triangular mesh."""
    def __init__(self, vertices, faces):
        self.vertices = vertices  # List of 3D points (numpy array)
        self.faces = faces        # List of face indices (triplets of integers)

def icosahedron():
    """Creates an icosahedron as the base mesh."""
    t = (1.0 + np.sqrt(5.0)) / 2.0  # Golden ratio

    # Create vertices
    vertices = np.array([
        [-1,  t,  0], [ 1,  t,  0], [-1, -t,  0], [ 1, -t,  0],
        [ 0, -1,  t], [ 0,  1,  t], [ 0, -1, -t], [ 0,  1, -t],
        [ t,  0, -1], [ t,  0,  1], [-t,  0, -1], [-t,  0,  1]
    ])
    vertices /= np.linalg.norm(vertices, axis=1, keepdims=True)  # Normalize to unit sphere

    # Create faces
    faces = [
        [0, 11, 5], [0, 5, 1], [0, 1, 7], [0, 7, 10], [0, 10, 11],
        [1, 5, 9], [5, 11, 4], [11, 10, 2], [10, 7, 6], [7, 1, 8],
        [3, 9, 4], [3, 4, 2], [3, 2, 6], [3, 6, 8], [3, 8, 9],
        [4, 9, 5], [2, 4, 11], [6, 2, 10], [8, 6, 7], [9, 8, 1]
    ]

    return SurfaceMesh(vertices=vertices, faces=faces)

class SurfaceSubdivision:
    """Applies Loop subdivision to a surface mesh."""
    def __init__(self, mesh):
        self.mesh = mesh

    def loop(self):
        """Perform one iteration of Loop subdivision."""
        new_faces = []
        edge_map = {}  # Cache for edge midpoints

        # Helper function to get or create edge midpoint
        def get_edge_midpoint(v1, v2):
            edge = tuple(sorted((v1, v2)))
            if edge not in edge_map:
                midpoint = (self.mesh.vertices[v1] + self.mesh.vertices[v2]) / 2
                edge_map[edge] = len(self.mesh.vertices)
                self.mesh.vertices = np.vstack([self.mesh.vertices, midpoint])
            return edge_map[edge]

        for face in self.mesh.faces:
            v1, v2, v3 = face
            a = get_edge_midpoint(v1, v2)
            b = get_edge_midpoint(v2, v3)
            c = get_edge_midpoint(v3, v1)

            # Subdivide into 4 new faces
            new_faces.extend([
                [v1, a, c],
                [v2, b, a],
                [v3, c, b],
                [a, b, c]
            ])

        self.mesh.faces = np.array(new_faces)

def project_to_unit_sphere(mesh):
    """Projects all vertices of the mesh onto a unit sphere."""
    mesh.vertices /= np.linalg.norm(mesh.vertices, axis=1, keepdims=True)

def icosphere(n_subdivisions):
    """Generates an icosphere with the specified number of subdivisions."""
    mesh = icosahedron()
    subdivision = SurfaceSubdivision(mesh)

    for _ in range(n_subdivisions):
        subdivision.loop()
        project_to_unit_sphere(mesh)

    return mesh

# 3단계로 subdivision된 icosphere 생성
mesh = icosphere(3)

print("Vertices:")
print(mesh.vertices)

print("\nFaces:")
print(mesh.faces)

def icosphere(n_subdivisions):
    mesh = icosahedron()  # 초기 20면체 생성
    subdivision = SurfaceSubdivision(mesh)
    
    for _ in range(n_subdivisions):
        subdivision.loop()  # Loop subdivision 적용
        project_to_unit_sphere(mesh)  # 단위 구로 투영

    return mesh

#grid2mesh

