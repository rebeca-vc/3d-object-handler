from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import math
import copy
from object.material import * 



def identity_matrix():
    return [
        1.0, 0.0, 0.0, 0.0,
        0.0, 1.0, 0.0, 0.0,
        0.0, 0.0, 1.0, 0.0,
        0.0, 0.0, 0.0, 1.0,
    ]

class Object:
	"""
	  shape (str): nome da forma ('cube', 'sphere', 'teapot', 'cone', 'torus').
	  position ([float,float,float]): translacao (x,y,z).
	  rotation ([float,float,float]): rotacao em graus nos eixos (rx,ry,rz).
	  scale ([float,float,float]): escala em cada eixo (sx,sy,sz).
	  material (str): nome do material preset (default: 'white_plastic').
	  shading_model (int): GL_FLAT ou GL_SMOOTH.
	"""
	_SHAPES_SOLID = {
		'cube': lambda: glutSolidCube(1.0),
		'sphere': lambda: glutSolidSphere(0.5, 32, 16),
		'teapot': lambda: glutSolidTeapot(0.5),
		'cone': lambda: glutSolidCone(0.5, 1.0, 32, 8),
		'torus': lambda: glutSolidTorus(0.15, 0.5, 32, 64),
	}

	def __init__(
		self,
		shape: str = 'cube',
		material: str = 'white_plastic',
		shading_model: int = GL_FLAT,
	):
		self.shape = shape.lower()
		self.position = (0.0, 0.0, 0.0)
		self.rotation = (0.0, 0.0, 0.0)
		self.scale = (1.0, 1.0, 1.0)
		
		# Resolve material por nome (string) e cria uma cópia
		base_material = MATERIALS.get(material.lower())
		if base_material is None:
			base_material = MATERIALS.get('white_plastic')
		
		# Cria uma cópia do material para este objeto específico
		self.material = copy.deepcopy(base_material)
		
		self.shading_model = shading_model
		# matriz modelo (column-major) cacheada
		self._matrix = identity_matrix()
		self._recompute_matrix()
		
	def _recompute_matrix(self):
		"""Recalcula a matriz modelo combinando escala, rotações e translação.
		Ordem escolhida: M = T * Rz * Ry * Rx * S
		"""
		sx, sy, sz = self.scale
		rx, ry, rz = [r * 3.141592653589793 / 180.0 for r in self.rotation]  # para radianos
		tx, ty, tz = self.position

		cx, sxn = math.cos(rx), math.sin(rx)
		cy, syn = math.cos(ry), math.sin(ry)
		cz, szn = math.cos(rz), math.sin(rz)

		# Matriz de escala
		S = [
			sx, 0, 0, 0,
			0, sy, 0, 0,
			0, 0, sz, 0,
			0, 0, 0, 1,
		]

		# Rotação X
		Rxm = [
			1, 0, 0, 0,
			0, cx, -sxn, 0,
			0, sxn, cx, 0,
			0, 0, 0, 1,
		]
		# Rotação Y
		Rym = [
			cy, 0, syn, 0,
			0, 1, 0, 0,
			-syn, 0, cy, 0,
			0, 0, 0, 1,
		]
		# Rotação Z
		Rzm = [
			cz, -szn, 0, 0,
			szn, cz, 0, 0,
			0, 0, 1, 0,
			0, 0, 0, 1,
		]

		# Translação
		T = [
			1, 0, 0, 0,
			0, 1, 0, 0,
			0, 0, 1, 0,
			tx, ty, tz, 1,
		]

		def mult(a, b):
			# a e b são 4x4 column-major
			r = [0.0] * 16
			for row in range(4):
				for col in range(4):
					r[col*4+row] = (
						a[0*4+row] * b[col*4+0] +
						a[1*4+row] * b[col*4+1] +
						a[2*4+row] * b[col*4+2] +
						a[3*4+row] * b[col*4+3]
					)
			return r

		# Combinação: (((S -> Rx) -> Ry) -> Rz) -> T
		M = mult(Rxm, S)
		M = mult(Rym, M)
		M = mult(Rzm, M)
		M = mult(T, M)
		self._matrix = M
		
	def _apply_material(self):
		m = self.material
		glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT, m.ambient)
		glMaterialfv(GL_FRONT_AND_BACK, GL_DIFFUSE, m.diffuse)
		glMaterialfv(GL_FRONT_AND_BACK, GL_SPECULAR, m.specular)
		glMaterialfv(GL_FRONT_AND_BACK, GL_EMISSION, m.emission)
		glMaterialf(GL_FRONT_AND_BACK, GL_SHININESS, m.shininess)

	def draw(self):
		glPushMatrix()
		try:
			# Usa matriz modelo pré-calculada
			glMultMatrixf(self._matrix)
			# Material (define como luz interage)
			self._apply_material()
			# Seleciona primitiva
			draw_map = self._SHAPES_SOLID
			draw_func = draw_map.get(self.shape) or draw_map.get('cube')
			draw_func()
		finally:
			glPopMatrix()

	def set_position(self, x: float, y: float, z: float):
		self.position = (x, y, z)
		self._recompute_matrix()

	def set_rotation(self, rx: float, ry: float, rz: float):
		self.rotation = (rx, ry, rz)
		self._recompute_matrix()

	def set_scale(self, sx: float, sy: float, sz: float):
		self.scale = (sx, sy, sz)
		self._recompute_matrix()

	def set_color(self, r: float, g: float, b: float):
		"""Altera a cor do material ajustando componentes difusa e ambiente."""
		self.material.diffuse = (r, g, b, 1.0)
		self.material.ambient = (0.2*r, 0.2*g, 0.2*b, 1.0)

	def set_material(self, material: str):
		"""Define material por nome (string)."""
		base_material = MATERIALS.get(material.lower())
		if base_material is None:
			raise ValueError(f"Material '{material}' não encontrado. Disponíveis: {list(MATERIALS.keys())}")
		# Cria uma cópia do material para este objeto específico
		self.material = copy.deepcopy(base_material)

	def set_shading_mode(self, mode: str):
		"""Altera modelo de sombreamento: 'flat' ou 'smooth'."""
		mode_lower = mode.lower()
		if mode_lower == 'flat':
			self.shading_model = GL_FLAT
		elif mode_lower == 'smooth':
			self.shading_model = GL_SMOOTH
		else:
			raise ValueError("shading mode deve ser 'flat' ou 'smooth'")

	def toggle_wireframe(self):
		self.wireframe = not self.wireframe
