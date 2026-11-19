# Geometria do projeto -> validação de coordenadas e ponto-em-polígono.
import math

EPS = 1e-12 # tolerância

# Função para validar coordenadas -> garante que são coordenadas geográficas reais e seguras antes de serem usadas no resto do sistema
def validar_coordenada(lat, lng):
    try:
        lat, lng = float(lat), float(lng)
    except (TypeError, ValueError):
        raise ValueError("Latitude e longitude precisam ser números.") from None
    if not (math.isfinite(lat) and math.isfinite(lng)):
        raise ValueError("Latitude e longitude precisam ser números válidos.")
    if not (-90 <= lat <= 90 and -180 <= lng <= 180):
        raise ValueError("Coordenada fora dos limites válidos.")
    return lat, lng


# Valida uma lista de lat, lng e devolve os vértices sem repetir o último
def validar_vertices(coordenadas):
    if not isinstance(coordenadas, list):
        raise ValueError("As coordenadas devem ser uma lista de pontos [lat, lng].")
    vertices = []
    for par in coordenadas:
        if not isinstance(par, (list, tuple)) or len(par) != 2:
            raise ValueError("Cada vértice deve ter o formato [lat, lng].")
        vertices.append(list(validar_coordenada(par[0], par[1])))
    if len(vertices) > 1 and vertices[0] == vertices[-1]:
        vertices.pop()
    if len(vertices) < 3:
        raise ValueError("Um polígono precisa de pelo menos 3 vértices.")
    return vertices


"""
_sobre_segmento -> verifica se um ponto no mapa está exatamente em cima de uma linha reta que liga dois pontos a e b
cruz = conta matemática(chamada de produto vetorial) mede o quanto o ponto está torto em relação à linha entre a e b.
O resultado ideal deve ser um ponto perfeitamente alinhado com a reta (cruz = 0)
O if abs(cruz) > EPS -> verifica se o desvio é maior que a margem de tolerância (EPS). Se for maior, o ponto está fora da estrada e a função (false)

o comando return desenha uma "caixa" invisível onde a e b são os cantos opostos
testa se a latitude do ponto está entre a menor e a maior latitude de a e b (min e max). Depois, faz a mesma coisa com a longitude.
soma e subtrai o EPS nas bordas para garantir que se o ponto estiver bem na pontinha (a ou b), ele não seja rejeitado por erro de arredondamento.
"""

def _sobre_segmento(lat, lng, a, b):
    cruz = (lat - a[0]) * (b[1] - a[1]) - (lng - a[1]) * (b[0] - a[0])
    if abs(cruz) > EPS:
        return False
    return (min(a[0], b[0]) - EPS <= lat <= max(a[0], b[0]) + EPS
            and min(a[1], b[1]) - EPS <= lng <= max(a[1], b[1]) + EPS)


"""
Verifica se a coordenada está dentro ou fora do polígono
Ignora o ponto repetido no final (n -= 1) -> Percorre (for i in range(n)) (cada dupla a e b é uma aresta do polígono)
chama _sobre_segmento (para ver se o ponto está exatamente em cima da aresta atual) -> ímpar = dentro e par = fora.
"""

def ponto_em_poligono(lat, lng, vertices):
    n = len(vertices)
    if n > 1 and tuple(vertices[0]) == tuple(vertices[-1]):
        n -= 1
    dentro = False
    j = n - 1
    for i in range(n):
        a, b = vertices[j], vertices[i]
        if _sobre_segmento(lat, lng, a, b):
            return True
        if (b[0] > lat) != (a[0] > lat):  # a aresta cruza a altura (latitude) do ponto
            lng_cruz = (a[1] - b[1]) * (lat - b[0]) / (a[0] - b[0]) + b[1]
            if lng < lng_cruz:
                dentro = not dentro
        j = i
    return dentro
