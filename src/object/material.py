from dataclasses import dataclass
from typing import Tuple

@dataclass
class Material:
    """Propriedades de material para o modelo de iluminação (fixed pipeline).

    Cada componente é um vetor RGBA (0..1). shininess (0..128) controla o tamanho do highlight.
    """
    ambient: Tuple[float, float, float, float] = (0.2, 0.2, 0.2, 1.0)
    diffuse: Tuple[float, float, float, float] = (0.8, 0.8, 0.8, 1.0)
    specular: Tuple[float, float, float, float] = (0.0, 0.0, 0.0, 1.0)
    emission: Tuple[float, float, float, float] = (0.0, 0.0, 0.0, 1.0)
    shininess: float = 0.0


# Biblioteca de materiais predefinidos (baseados em valores OpenGL comuns)
MATERIALS = {
    'emerald': Material(
        ambient=(0.0215, 0.1745, 0.0215, 1.0),
        diffuse=(0.07568, 0.61424, 0.07568, 1.0),
        specular=(0.633, 0.727811, 0.633, 1.0),
        emission=(0.0, 0.0, 0.0, 1.0),
        shininess=76.8
    ),
    'jade': Material(
        ambient=(0.135, 0.2225, 0.1575, 1.0),
        diffuse=(0.54, 0.89, 0.63, 1.0),
        specular=(0.316228, 0.316228, 0.316228, 1.0),
        emission=(0.0, 0.0, 0.0, 1.0),
        shininess=12.8
    ),
    'obsidian': Material(
        ambient=(0.05375, 0.05, 0.06625, 1.0),
        diffuse=(0.18275, 0.17, 0.22525, 1.0),
        specular=(0.332741, 0.328634, 0.346435, 1.0),
        emission=(0.0, 0.0, 0.0, 1.0),
        shininess=38.4
    ),
    'pearl': Material(
        ambient=(0.25, 0.20725, 0.20725, 1.0),
        diffuse=(1.0, 0.829, 0.829, 1.0),
        specular=(0.296648, 0.296648, 0.296648, 1.0),
        emission=(0.0, 0.0, 0.0, 1.0),
        shininess=11.264
    ),
    'ruby': Material(
        ambient=(0.1745, 0.01175, 0.01175, 1.0),
        diffuse=(0.61424, 0.04136, 0.04136, 1.0),
        specular=(0.727811, 0.626959, 0.626959, 1.0),
        emission=(0.0, 0.0, 0.0, 1.0),
        shininess=76.8
    ),
    'turquoise': Material(
        ambient=(0.1, 0.18725, 0.1745, 1.0),
        diffuse=(0.396, 0.74151, 0.69102, 1.0),
        specular=(0.297254, 0.30829, 0.306678, 1.0),
        emission=(0.0, 0.0, 0.0, 1.0),
        shininess=12.8
    ),
    'brass': Material(
        ambient=(0.329412, 0.223529, 0.027451, 1.0),
        diffuse=(0.780392, 0.568627, 0.113725, 1.0),
        specular=(0.992157, 0.941176, 0.807843, 1.0),
        emission=(0.0, 0.0, 0.0, 1.0),
        shininess=27.8974
    ),
    'bronze': Material(
        ambient=(0.2125, 0.1275, 0.054, 1.0),
        diffuse=(0.714, 0.4284, 0.18144, 1.0),
        specular=(0.393548, 0.271906, 0.166721, 1.0),
        emission=(0.0, 0.0, 0.0, 1.0),
        shininess=25.6
    ),
    'chrome': Material(
        ambient=(0.25, 0.25, 0.25, 1.0),
        diffuse=(0.4, 0.4, 0.4, 1.0),
        specular=(0.774597, 0.774597, 0.774597, 1.0),
        emission=(0.0, 0.0, 0.0, 1.0),
        shininess=76.8
    ),
    'copper': Material(
        ambient=(0.19125, 0.0735, 0.0225, 1.0),
        diffuse=(0.7038, 0.27048, 0.0828, 1.0),
        specular=(0.256777, 0.137622, 0.086014, 1.0),
        emission=(0.0, 0.0, 0.0, 1.0),
        shininess=12.8
    ),
    'gold': Material(
        ambient=(0.24725, 0.1995, 0.0745, 1.0),
        diffuse=(0.75164, 0.60648, 0.22648, 1.0),
        specular=(0.628281, 0.555802, 0.366065, 1.0),
        emission=(0.0, 0.0, 0.0, 1.0),
        shininess=51.2
    ),
    'silver': Material(
        ambient=(0.19225, 0.19225, 0.19225, 1.0),
        diffuse=(0.50754, 0.50754, 0.50754, 1.0),
        specular=(0.508273, 0.508273, 0.508273, 1.0),
        emission=(0.0, 0.0, 0.0, 1.0),
        shininess=51.2
    ),
    'black_plastic': Material(
        ambient=(0.0, 0.0, 0.0, 1.0),
        diffuse=(0.01, 0.01, 0.01, 1.0),
        specular=(0.50, 0.50, 0.50, 1.0),
        emission=(0.0, 0.0, 0.0, 1.0),
        shininess=32.0
    ),
    'cyan_plastic': Material(
        ambient=(0.0, 0.1, 0.06, 1.0),
        diffuse=(0.0, 0.50980392, 0.50980392, 1.0),
        specular=(0.50196078, 0.50196078, 0.50196078, 1.0),
        emission=(0.0, 0.0, 0.0, 1.0),
        shininess=32.0
    ),
    'green_plastic': Material(
        ambient=(0.0, 0.0, 0.0, 1.0),
        diffuse=(0.1, 0.35, 0.1, 1.0),
        specular=(0.45, 0.55, 0.45, 1.0),
        emission=(0.0, 0.0, 0.0, 1.0),
        shininess=32.0
    ),
    'red_plastic': Material(
        ambient=(0.0, 0.0, 0.0, 1.0),
        diffuse=(0.5, 0.0, 0.0, 1.0),
        specular=(0.7, 0.6, 0.6, 1.0),
        emission=(0.0, 0.0, 0.0, 1.0),
        shininess=32.0
    ),
    'white_plastic': Material(
        ambient=(0.0, 0.0, 0.0, 1.0),
        diffuse=(0.55, 0.55, 0.55, 1.0),
        specular=(0.70, 0.70, 0.70, 1.0),
        emission=(0.0, 0.0, 0.0, 1.0),
        shininess=32.0
    ),
    'yellow_plastic': Material(
        ambient=(0.0, 0.0, 0.0, 1.0),
        diffuse=(0.5, 0.5, 0.0, 1.0),
        specular=(0.60, 0.60, 0.50, 1.0),
        emission=(0.0, 0.0, 0.0, 1.0),
        shininess=32.0
    ),
    'black_rubber': Material(
        ambient=(0.02, 0.02, 0.02, 1.0),
        diffuse=(0.01, 0.01, 0.01, 1.0),
        specular=(0.4, 0.4, 0.4, 1.0),
        emission=(0.0, 0.0, 0.0, 1.0),
        shininess=10.0
    ),
    'cyan_rubber': Material(
        ambient=(0.0, 0.05, 0.05, 1.0),
        diffuse=(0.4, 0.5, 0.5, 1.0),
        specular=(0.04, 0.7, 0.7, 1.0),
        emission=(0.0, 0.0, 0.0, 1.0),
        shininess=10.0
    ),
    'green_rubber': Material(
        ambient=(0.0, 0.05, 0.0, 1.0),
        diffuse=(0.4, 0.5, 0.4, 1.0),
        specular=(0.04, 0.7, 0.04, 1.0),
        emission=(0.0, 0.0, 0.0, 1.0),
        shininess=10.0
    ),
    'red_rubber': Material(
        ambient=(0.05, 0.0, 0.0, 1.0),
        diffuse=(0.5, 0.4, 0.4, 1.0),
        specular=(0.7, 0.04, 0.04, 1.0),
        emission=(0.0, 0.0, 0.0, 1.0),
        shininess=10.0
    ),
    'white_rubber': Material(
        ambient=(0.05, 0.05, 0.05, 1.0),
        diffuse=(0.5, 0.5, 0.5, 1.0),
        specular=(0.7, 0.7, 0.7, 1.0),
        emission=(0.0, 0.0, 0.0, 1.0),
        shininess=10.0
    ),
    'yellow_rubber': Material(
        ambient=(0.05, 0.05, 0.0, 1.0),
        diffuse=(0.5, 0.5, 0.4, 1.0),
        specular=(0.7, 0.7, 0.04, 1.0),
        emission=(0.0, 0.0, 0.0, 1.0),
        shininess=10.0
    ),
}
