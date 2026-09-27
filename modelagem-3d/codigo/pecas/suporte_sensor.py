"""
Suporte do sensor VL53L0X (GY-530) na aba do boné.

Proteção mecânica:
  - a placa fica dentro de um bolso fechado; só a janela do chip é aberta
  - a face do chip fica ~4 mm recuada atrás de uma moldura arredondada, que
    recebe a batida antes do sensor
  - a janela abre em cone (meio ângulo de 20 graus) para não cortar o FOV de 25 graus
  - sem vidro ou acrílico na frente: o VL53L0X perde alcance com cobertura sem calibração
  - base parafusada na aba com placa_interna por baixo (porca M2 presa no bolso)

Coordenadas (local, antes de inclinar):
  X: para a frente (direção de medição)   Y: lateral   Z: para cima
  x=0 é a face da placa GY-530 que encosta na parede frontal.
  z=0 é o topo da aba do boné.

Peças: suporte(inclinacao, lado), tampa(inclinacao, lado), placa_sob_aba()
lado = +1 (esquerdo, Y+) ou -1 (direito, Y-). A abertura lateral gira o sensor para fora.
"""
import math
import cadquery as cq

from . import medidas as P
from . import auxiliares as U

F = 0.2
BOLSO_Y = P.GY_X + 2 * F          # placa deitada: 25 mm na horizontal
BOLSO_Z = P.GY_Z + F
BOLSO_X = P.GY_T + F

W = BOLSO_Y + 2 * P.POD_PAREDE    # largura externa
X_FRENTE = P.POD_FRENTE           # face externa da parede frontal
X_MOLDURA = X_FRENTE + P.POD_MOLDURA
X_PLACA_TRAS = -BOLSO_X
X_CAV = X_PLACA_TRAS - P.POD_CAVIDADE
X_TRAS = X_CAV - P.POD_PAREDE
Z_BASE_BOLSO = P.POD_PAREDE
Z_TOPO_BOLSO = Z_BASE_BOLSO + BOLSO_Z
TAMPA_T = 2.0
H = Z_TOPO_BOLSO + TAMPA_T        # altura da cabeça
PROF = X_MOLDURA - X_TRAS

CHIP_Z = Z_BASE_BOLSO + P.GY_Z / 2 + P.CHIP_OFF_Z
CHIP_Y = P.CHIP_OFF_Y

# colunas dos parafusos da tampa, nos cantos traseiros
COL_Y = BOLSO_Y / 2 - P.POD_COLUNA / 2
COL_X = (X_CAV + X_PLACA_TRAS - 0.3) / 2
COLUNAS = [(COL_X, COL_Y), (COL_X, -COL_Y)]

# base na aba
BASE_X0, BASE_X1 = X_TRAS - 14.0, X_MOLDURA + 3.0
BASE_Y = 36.0
FUROS_ABA = [(X_TRAS - 8.0, 11.0), (X_TRAS - 8.0, -11.0)]


def _cabeca_bruta(ext_baixo=25.0):
    """Sólido externo da cabeça, estendido para baixo (vira o pedestal após inclinar)."""
    corpo = cq.Workplane("XY").box(X_FRENTE - X_TRAS, W, H + ext_baixo, centered=False) \
        .translate((X_TRAS, -W / 2, -ext_baixo))
    moldura = cq.Workplane("XY").box(X_MOLDURA - X_FRENTE, W, H + ext_baixo, centered=False) \
        .translate((X_FRENTE, -W / 2, -ext_baixo))
    c = corpo.union(moldura)
    c = c.edges("|Z").fillet(2.0)
    try:
        c = c.faces(">Z").edges().fillet(1.0)
    except Exception:
        pass
    return c


def _cortes_cabeca():
    """Tudo que é removido da cabeça (em coordenadas locais)."""
    cortes = []
    # bolso da placa + cavidade traseira, abertos para cima (fecha com a tampa embutida)
    cortes.append(U.caixa_arred(X_PLACA_TRAS - 0.3, -BOLSO_Y / 2, Z_BASE_BOLSO,
                                BOLSO_X + 0.3, BOLSO_Y, BOLSO_Z + TAMPA_T + 5, 0))
    cortes.append(U.caixa_arred(X_CAV, -BOLSO_Y / 2 + P.POD_COLUNA, Z_BASE_BOLSO,
                                X_PLACA_TRAS - X_CAV, BOLSO_Y - 2 * P.POD_COLUNA,
                                BOLSO_Z + TAMPA_T + 5, 0))
    # alojamento da tampa embutida
    cortes.append(U.caixa_arred(X_CAV, -BOLSO_Y / 2, Z_TOPO_BOLSO,
                                -X_CAV, BOLSO_Y, TAMPA_T + 5, 0))
    # alívio na parede frontal para chip e componentes da face
    b = P.GY_BORDA_APOIO
    cortes.append(U.caixa_arred(-0.01, -BOLSO_Y / 2 + b, Z_BASE_BOLSO + b,
                                P.GY_ALIVIO + 0.01, BOLSO_Y - 2 * b, BOLSO_Z - 2 * b, 0.5))
    # janela em cone até a face externa
    t = math.tan(math.radians(P.MEIO_ANGULO_FOV))
    x0 = P.GY_ALIVIO
    d = X_FRENTE - x0 + 0.01
    w0, h0 = P.JANELA_W, P.JANELA_H
    w1, h1 = w0 + 2 * d * t, h0 + 2 * d * t
    janela = (cq.Workplane("YZ", origin=(x0, 0, 0)).center(CHIP_Y, CHIP_Z).rect(w0, h0)
              .workplane(offset=d).rect(w1, h1).loft())
    cortes.append(janela)
    # abertura da moldura (deixa só o aro de proteção)
    aro = 2.0
    cortes.append(U.caixa_arred(X_FRENTE - 0.01, -W / 2 + aro, aro,
                                P.POD_MOLDURA + 1, W - 2 * aro, H - 2 * aro, 1.0))
    # pilotos dos parafusos da tampa nas colunas
    for (x, y) in COLUNAS:
        cortes.append(U.cilindro(P.M2_PILOTO, 8.0, (x, y, Z_TOPO_BOLSO - 8.0)))
    # saída do cabo: entalhe na parede traseira, fechado pela tampa
    cortes.append(cq.Workplane("YZ", origin=(X_TRAS - 1, 0, 0)).center(0, Z_TOPO_BOLSO)
                  .slot2D(2 * P.CABO_SENSOR_D, P.CABO_SENSOR_D, angle=90).extrude(P.POD_PAREDE + 2))
    return cortes


def _posicionar(obj, inclinacao, lado):
    """Inclina para cima em torno da aresta traseira inferior, sobe para a base e abre para fora."""
    o = obj.rotate((X_TRAS, 0, 0), (X_TRAS, 1, 0), -inclinacao)
    o = o.translate((0, 0, P.POD_BASE_T))
    xc = (X_TRAS + X_MOLDURA) / 2
    o = o.rotate((xc, 0, 0), (xc, 0, 1), lado * P.POD_ABERTURA_LATERAL)
    return o


def suporte(inclinacao=10, lado=1):
    cab = _posicionar(_cabeca_bruta(), inclinacao, lado)
    # corta tudo abaixo do topo da aba
    cab = cab.intersect(cq.Workplane("XY").box(200, 200, 100, centered=(True, True, False)))
    base = U.caixa_arred(BASE_X0, -BASE_Y / 2, 0, BASE_X1 - BASE_X0, BASE_Y, P.POD_BASE_T, 4.0)
    s = base.union(cab)
    for c in _cortes_cabeca():
        s = s.cut(_posicionar(c, inclinacao, lado))
    # furos da base na aba
    for (x, y) in FUROS_ABA:
        s = s.cut(U.cilindro(P.M2_PASSANTE, P.POD_BASE_T + 2, (x, y, -1)))
    return s


def tampa():
    """
    Tampa embutida: fecha bolso + cavidade e prende a placa por cima.
    É igual para as duas variantes e todas as inclinações (sai na posição de impressão).
    """
    f = 0.15
    t = U.caixa_arred(X_CAV + f, -BOLSO_Y / 2 + f, Z_TOPO_BOLSO,
                      -X_CAV - 2 * f, BOLSO_Y - 2 * f, TAMPA_T, 0.5)
    # língua sobre a parede traseira: fecha o entalhe do cabo por cima
    d = P.CABO_SENSOR_D - 2 * f
    t = t.union(U.caixa_arred(X_TRAS, -d / 2, Z_TOPO_BOLSO, X_CAV - X_TRAS + f + 0.5, d, TAMPA_T, 0))
    for (x, y) in COLUNAS:
        t = t.cut(U.cilindro(P.M2_PASSANTE, TAMPA_T + 2, (x, y, Z_TOPO_BOLSO - 1)))
    return t


def tampa_montada(inclinacao=10, lado=1):
    return _posicionar(tampa(), inclinacao, lado)


def placa_sob_aba():
    """Vai por baixo da aba. Porcas M2 ficam presas nos bolsos sextavados (lado da aba)."""
    lx, ly, t = 14.0, BASE_Y, 3.5
    xc = FUROS_ABA[0][0]
    c = U.caixa_arred(xc - lx / 2, -ly / 2, -P.ABA_ESPESSURA - t, lx, ly, t, 4.0)
    c = c.faces("<Z").edges().fillet(1.0)
    z_topo = -P.ABA_ESPESSURA
    for (x, y) in FUROS_ABA:
        porca = (cq.Workplane("XY", origin=(0, 0, z_topo - P.M2_PORCA_H)).center(x, y)
                 .polygon(6, P.M2_PORCA_S / math.cos(math.pi / 6)).extrude(P.M2_PORCA_H + 0.1))
        c = c.cut(porca)
        c = c.cut(U.cilindro(P.M2_PASSANTE, 1.2, (x, y, z_topo - P.M2_PORCA_H - 1.2)))
    return c


def fantasmas(inclinacao=10, lado=1):
    placa = U.caixa_arred(-P.GY_T, -P.GY_X / 2, Z_BASE_BOLSO, P.GY_T, P.GY_X, P.GY_Z, 0)
    return {"gy530": _posicionar(placa, inclinacao, lado)}
