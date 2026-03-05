# Hexeracto 6D

Una simulación visual y matemática construida en Python puro que proyecta, en tiempo real, un hipercubo de 6 dimensiones (hexeracto) en una pantalla 2D. Decorado con una estética de neón retro-futurista (synthwave), el código procesa espacio geométrico hiperdimensional y lo transforma en algo que nuestros ojos pueden apreciar.

A continuación, el proyecto se explica desde dos perspectivas diferentes.

---

## El Concepto: Sombras de Dimensiones Superiores

Si alguna vez has intentado dibujar un cubo común (de 3 dimensiones) en una hoja de papel plana (de 2 dimensiones), ya has hecho una "proyección dimensional". Estás dibujando la sombra de un objeto tridimensional para que encaje en un mundo más simple.

Este proyecto toma esa misma idea lógica, pero la empuja mucho más allá de las posibilidades de la física humana. Toma un cubo de seis direcciones de espacio físico —algo que nuestras mentes ni siquiera pueden imaginar visualmente porque nuestro universo solo tiene tres— y lo hace girar.

Pero este objeto no solo gira de izquierda a derecha o de arriba a abajo. Está programado para rotar a través de direcciones y ejes adicionales simultáneamente, doblándose sobre sí mismo de maneras que parecen imposibles. Lo que ves en tu pantalla girando, estirándose e intersecándose no es el objeto 6D mágico en sí, sino su "sombra perfecta" cayendo matemáticamente sobre tu monitor plano. 

Los colores de neón no son solo estéticos: actúan como un mapa. Las partes que brillan en color cian están más cerca de ti en ese incomprensible mapa de seis dimensiones, mientras que las líneas que se desvanecen hacia un rosa o púrpura profundo, se encuentran navegando por las profundidades de un espacio que no logramos ver, acompañadas por un reflejo especular en el suelo que asienta la ilusión.

---

## Arquitectura Matemática y Renderizado

*Quien sepa entender, que entienda.*

El motor detrás de `hexeracto.py` no utiliza librerías de renderizado 3D prefabricadas; implementa en su lugar una transformación matricial vectorial pura desde un espacio euclidiano $\mathbb{R}^6$ hacia $\mathbb{R}^2$ utilizando `numpy` y mapeando los tensores en colecciones de líneas de `matplotlib`.

1. **Topología del Objeto**: El espacio local se inicializa generando los $2^6 = 64$ vértices de un 6-cubo regular usando combinatoria $\{\pm1\}^6$. El algoritmo de mallado recorre e interpola las 192 aristas basándose en la distancia de Hamming ($d_H = 1$), asegurando que solo los vértices ortogonales adyacentes queden unívocamente conectados (Harary et al., 1988).

2. **Álgebra de Rotaciones**: El comportamiento cinemático se define componiendo múltiples Matrices de Rotación de Givens. Donde la rotación tradicional 3D ocurre en torno a un eje, aquí ocurre alrededor de planos en un subespacio (ej. $\Pi_{x,y}$, $\Pi_{u,v}$), permitiendo rotaciones simultáneas e independientes en múltiples subespacios ortogonales de 2D (Givens, 1958; Aguilera & Pérez-Aguila, 2004). La matriz combinada ortogonal $R_{total} \in SO(6)$ es un mapeo lineal autocompuesto para cada frame de la animación.

3. **Pipeline de Proyección y Frustum**: En vez de una proyección ortográfica trivial que destruiría el volumen, aplicamos un colapso telescópico prospectivo. El paso de $N$ a $N-1$ modifica el tensor de posición iterativamente escalándolo con un peso de profundidad no lineal $w = \frac{f}{f+z_{N-1}}$ (Hanson, 1994). Esto confiere efectos de paralaje y distorsión volumétrica auténtica de cada plano colapsado.

---

## Instalación y Ejecución

Asegúrate de tener un entorno de Python 3.x disponible. 

Instala las dependencias matemáticas y gráficas requeridas:
```bash
pip install numpy matplotlib
```

Inicia la simulación computacional interactiva:
```bash
python hexeracto.py
```

---

## Bibliografía

Aguilera, A., & Pérez-Aguila, R. (2004). General n-dimensional rotations. *Journal of WSCG*, 12(1), 1-8.

Givens, W. (1958). Computation of plane unitary rotations transforming a general matrix to triangular form. *Journal of the Society for Industrial and Applied Mathematics*, 6(1), 26-50. https://doi.org/10.1137/0106004

Hanson, A. J. (1994). Geometry for n-dimensional graphics. En P. Heckbert (Ed.), *Graphics Gems IV* (pp. 149-170). Academic Press. https://doi.org/10.1016/B978-0-12-336156-1.50024-0

Harary, F., Hayes, J. P., & Wu, H. J. P. (1988). A survey of the theory of hypercube graphs. *Computers & Mathematics with Applications*, 15(4), 277-289. https://doi.org/10.1016/0898-1221(88)90213-1
