"""
Boné de referência para a montagem visual (não é impresso).

Sistema de coordenadas da cabeça:
  X para a frente, Y para a esquerda do usuário, Z para cima.
  z=0 é a borda de baixo da copa (linha da carneira).

A copa é um meio elipsoide (BONE_A x BONE_B x BONE_C). As funções
ponto_copa() e normal_copa() dão posição e normal em qualquer ponto da copa
e são usadas pela montagem para assentar os cases e rotear os cabos.

phi é o parâmetro da elipse horizontal: 0 = frente, 90 = lateral esquerda,
180 = nuca, -90 = lateral direita.
"""
import math

import numpy as np
import cadquery as cq
from OCP.gp import gp_GTrsf, gp_Mat
from OCP.BRepBuilderAPI import BRepBuilderAPI_GTransform

from . import medidas as P

A, B, C = P.BONE_A, P.BONE_B, P.BONE_C


# ------------------------------------------------------------------ geometria analítica
def ponto_copa(phi, z, offset=0.0, a=A, b=B, c=C):
    """Ponto na superfície externa da copa, deslocado 'offset' ao longo da normal."""
    k = math.sqrt(max(1 - (z / c) ** 2, 0.0))
    ph = math.radians(phi)
    p = np.array([a * k * math.cos(ph), b * k * math.sin(ph), z])
    return p + offset * normal_copa(p)


def normal_copa(p, a=A, b=B, c=C):
    n = np.array([p[0] / a ** 2, p[1] / b ** 2, p[2] / c ** 2])
    return n / np.linalg.norm(n)


def referencial_copa(phi, z, para_nuca=True):
    """
    Referencial local na copa: Z = normal para fora, X = tangente horizontal
    apontando para a nuca, Y = Z x X. Devolve (origem, X, Y, Z).
    """
    p = ponto_copa(phi, z)
    n = normal_copa(p)
    t = np.cross([0, 0, 1], n) if phi >= 0 else np.cross(n, [0, 0, 1])
    t = t / np.linalg.norm(t)
    if not para_nuca:
        t = -t
    y = np.cross(n, t)
    return p, t, y, n


# ------------------------------------------------------------------ aba
def _aba_contorno(npts=40):
    """Contorno 2D da aba (vista de cima, antes de curvar e inclinar)."""
    pts = []
    for i in range(npts + 1):   # borda interna, acompanha a copa
        ph = math.radians(-P.ABA_PHI + 2 * P.ABA_PHI * i / npts)
        pts.append((A * math.cos(ph) - 2.0, B * math.sin(ph)))
    x0 = A * math.cos(math.radians(P.ABA_PHI))
    bb = B * math.sin(math.radians(P.ABA_PHI))
    aa = A + P.ABA_PROF - x0
    for i in range(npts + 1):   # borda externa
        th = math.radians(90 - 180 * i / npts)
        pts.append((x0 + aa * math.cos(th), bb * math.sin(th)))
    return pts, x0, aa, bb


def borda_aba_x(y):
    """x da borda externa da aba numa distância lateral y (antes de inclinar)."""
    _, x0, aa, bb = _aba_contorno(4)
    return x0 + aa * math.sqrt(max(1 - (y / bb) ** 2, 0.0))


def z_topo_aba(y):
    """Altura do topo da aba (antes de inclinar), pela curvatura lateral."""
    r = P.ABA_R_CURVA
    return math.sqrt(r * r - y * y) - r


def normal_aba(y):
    r = P.ABA_R_CURVA
    n = np.array([0.0, y, z_topo_aba(y) + r])
    return n / np.linalg.norm(n)


PIVO_ABA = np.array([A, 0.0, 0.0])


def inclina_aba(v, ponto=True):
    """Aplica a inclinação da aba (gira em Y em torno da frente da copa)."""
    ang = math.radians(P.ABA_INCL)
    R = np.array([[math.cos(ang), 0, math.sin(ang)],
                  [0, 1, 0],
                  [-math.sin(ang), 0, math.cos(ang)]])
    v = np.asarray(v, dtype=float)
    return R @ (v - PIVO_ABA) + PIVO_ABA if ponto else R @ v


def referencial_aba(x, y):
    """Referencial sobre o topo da aba: X para a frente, Z normal para cima."""
    o = np.array([x, y, z_topo_aba(y)])
    zv = normal_aba(y)
    xv = np.array([1.0, 0.0, 0.0])
    yv = np.cross(zv, xv)
    return inclina_aba(o), inclina_aba(xv, False), inclina_aba(yv, False), inclina_aba(zv, False)


def aba():
    pts, *_ = _aba_contorno()
    prisma = cq.Workplane("XY").polyline(pts).close().extrude(120).translate((0, 0, -80))
    r = P.ABA_R_CURVA
    casca = (cq.Workplane("YZ").circle(r).circle(r - P.ABA_ESPESSURA).extrude(300)
             .translate((-50, 0, -r)))
    a = prisma.intersect(casca)
    a = a.rotate(tuple(PIVO_ABA), tuple(PIVO_ABA + [0, 1, 0]), P.ABA_INCL)
    return a


# ------------------------------------------------------------------ copa
def elipsoide(a, b, c):
    esf = cq.Solid.makeSphere(1.0, angleDegrees1=-90, angleDegrees2=90)
    gt = gp_GTrsf()
    gt.SetVectorialPart(gp_Mat(a, 0, 0, 0, b, 0, 0, 0, c))
    s = cq.Shape.cast(BRepBuilderAPI_GTransform(esf.wrapped, gt, True).Shape())
    return cq.Workplane("XY").add(s)


def _meio_espaco(z0=0.0, z1=400.0):
    return cq.Workplane("XY").box(600, 600, z1 - z0, centered=(True, True, False)).translate((0, 0, z0))


def copa():
    t = P.BONE_T
    ext = elipsoide(A, B, C)
    inte = elipsoide(A - t, B - t, C - t)
    c = ext.cut(inte).intersect(_meio_espaco())
    # abertura da regulagem na nuca
    reg = cq.Workplane("YZ").circle(P.REGULAGEM_R).extrude(60).translate((-A - 20, 0, 0))
    c = c.cut(reg)
    return c


def botao():
    return elipsoide(9, 9, 4).translate((0, 0, C - 1.0))


def carneira():
    t = P.BONE_T
    e1 = elipsoide(A - t, B - t, C - t)
    e2 = elipsoide(A - t - P.CARNEIRA_T, B - t - P.CARNEIRA_T, C - t - P.CARNEIRA_T)
    anel = e1.cut(e2).intersect(_meio_espaco(0, P.CARNEIRA_H))
    reg = cq.Workplane("YZ").circle(P.REGULAGEM_R).extrude(60).translate((-A - 20, 0, 0))
    return anel.cut(reg)


def fita_regulagem():
    """Fita de regulagem atravessando a abertura da nuca."""
    pts = [ponto_copa(phi, 4.0, 0.4) for phi in np.linspace(160, 200, 9)]
    return tubo_chato(pts, 22.0, 1.4)


# ------------------------------------------------------------------ canaleta
def caminho_canaleta(n=60):
    """Pontos da canaleta: sai da frente esquerda, contorna a nuca e volta pela direita."""
    pts = []
    ini = P.CANALETA_PHI
    for i in range(n + 1):
        phi = ini + (360 - 2 * ini) * i / n     # 62 ... 298 (= -62)
        dphi = phi - 180
        z = P.CANALETA_Z + P.CANALETA_SOBE * math.exp(-(dphi / 28.0) ** 2)
        pts.append(ponto_copa(phi if phi <= 180 else phi - 360, z, P.CANALETA_D * 0.15))
    return pts


def canaleta():
    return tubo(caminho_canaleta(), P.CANALETA_D)


def ponto_canaleta(phi):
    """Ponto na linha da canaleta mais próximo de um phi dado."""
    dphi = (phi % 360) - 180
    z = P.CANALETA_Z + P.CANALETA_SOBE * math.exp(-(dphi / 28.0) ** 2)
    return ponto_copa(phi, z, P.CANALETA_D * 0.15)


# ------------------------------------------------------------------ tubos (cabos, canaleta)
def tubo(pts, d):
    pts = [cq.Vector(*map(float, p)) for p in pts]
    edge = cq.Edge.makeSpline(pts)
    caminho = cq.Wire.assembleEdges([edge])
    perfil = cq.Wire.makeCircle(d / 2, edge.startPoint(), edge.tangentAt(0))
    s = cq.Solid.sweep(perfil, [], caminho, makeSolid=True, isFrenet=False)
    return cq.Workplane("XY").add(s)


def tubo_chato(pts, largura, esp):
    pts = [cq.Vector(*map(float, p)) for p in pts]
    edge = cq.Edge.makeSpline(pts)
    caminho = cq.Wire.assembleEdges([edge])
    p0, t0 = edge.startPoint(), edge.tangentAt(0)
    pl = cq.Plane(origin=p0, xDir=cq.Vector(0, 0, 1).cross(t0).normalized() if abs(t0.z) < 0.9 else cq.Vector(1, 0, 0),
                  normal=t0)
    perfil = cq.Workplane(pl).rect(esp, largura).wires().val()
    s = cq.Solid.sweep(perfil, [], caminho, makeSolid=True, isFrenet=False)
    return cq.Workplane("XY").add(s)
