# SPDX-FileCopyrightText: 2026 Edson Gabriel Soares da Fonseca, João Luiz Pereira Filho, Nadson Alex da Silva
# SPDX-License-Identifier: CERN-OHL-S-2.0

"""
Montagem final: boné com tudo instalado.

Usa o boné de referência (bone.py) e posiciona cada peça impressa no lugar
definido em medidas.py (POS_*). Nada aqui é impresso: o objetivo é ver
o conjunto, conferir posições e gerar STEP/GLB da montagem.

Sistema de coordenadas da cabeça: X frente, Y esquerda, Z cima (ver bone.py).
"""
import math

import numpy as np
import cadquery as cq

from . import medidas as P
from . import auxiliares as U
from . import bone as K
from . import case_eletronica as A
from . import case_bateria as B
from . import suporte_sensor as S
from . import berco_motor as M

# cores (r, g, b, alfa)
COR = {
    "tecido": (0.56, 0.60, 0.66, 1.0),
    "aba": (0.48, 0.52, 0.58, 1.0),
    "canaleta": (0.72, 0.75, 0.79, 1.0),
    "carneira": (0.25, 0.27, 0.30, 1.0),
    "petg": (0.106, 0.424, 0.475, 1.0),      # Petróleo
    "petg_tampa": (0.16, 0.52, 0.57, 1.0),
    "base curva": (0.922, 0.659, 0.298, 1.0),      # Âmbar Sol
    "placa_interna": (0.878, 0.478, 0.373, 1.0),  # Coral
    "cabo": (0.06, 0.06, 0.06, 1.0),
    "pcb": (0.15, 0.45, 0.20, 1.0),
    "tp4056": (0.25, 0.35, 0.70, 1.0),
    "celula": (0.35, 0.35, 0.38, 1.0),
    "sensor": (0.45, 0.20, 0.60, 1.0),
    "motor": (0.70, 0.70, 0.72, 1.0),
    "espuma": (0.14, 0.14, 0.16, 1.0),
    "tpu": (0.20, 0.55, 0.60, 1.0),
    "fita": (0.10, 0.10, 0.10, 1.0),
}


# ------------------------------------------------------------------ referenciais
class Ref:
    """Referencial local -> mundo (origem + eixos X, Y, Z)."""

    def __init__(self, o, x, y, z):
        self.o, self.x, self.y, self.z = map(lambda v: np.asarray(v, float), (o, x, y, z))
        self.loc = cq.Location(cq.Plane(origin=tuple(self.o), xDir=tuple(self.x), normal=tuple(self.z)))

    def deslocado(self, d):
        """Mesmo referencial, com a origem andando d ao longo do Z local."""
        return Ref(self.o + self.z * d, self.x, self.y, self.z)

    def ponto(self, p):
        p = np.asarray(p, float)
        return self.o + self.x * p[0] + self.y * p[1] + self.z * p[2]

    def coloca(self, wp, ancora=(0, 0, 0)):
        sh = wp.val() if isinstance(wp, cq.Workplane) else wp
        sh = sh.translate(cq.Vector(*(-np.asarray(ancora, float))))
        return cq.Workplane("XY").add(sh.moved(self.loc))


# ------------------------------------------------------------------ assentamento
def _vol(a, b):
    try:
        return a.val().intersect(b.val()).Volume()
    except Exception:
        return 0.0


def assentar(ref, peca, ancora, alvo, sentido=+1, faixa=(0.0, 8.0), tol=0.5, encostar=False):
    """
    Anda com a peça ao longo do Z local até ela assentar no alvo (tecido/aba).
    encostar=False: menor deslocamento que tira a interferência (peça por fora).
    encostar=True:  maior deslocamento sem interferência (peça por dentro, encostando).
    Devolve o referencial ajustado.
    """
    lo, hi = faixa
    for _ in range(9):
        mid = (lo + hi) / 2
        v = _vol(ref.deslocado(sentido * mid).coloca(peca, ancora), alvo)
        if encostar:
            lo, hi = (mid, hi) if v < tol else (lo, mid)
        else:
            lo, hi = (lo, mid) if v < tol else (mid, hi)
    return ref.deslocado(sentido * (lo if encostar else hi))


_cache = {}


def _alvos():
    if not _cache:
        _cache["copa"] = K.copa()
        _cache["aba"] = K.aba()
        _cache["carneira_bruta"] = K.carneira()
    return _cache


def referenciais():
    """Referenciais já assentados (calculados uma vez e reaproveitados por peças e cabos)."""
    if "refs" not in _cache:
        alv = _alvos()
        r = {}
        r["A"] = assentar(ref_case_a(), A.base_curva(), ANCORA_A, alv["copa"], faixa=(-2.0, 6.0))
        r["B"] = assentar(ref_case_b(), B.corpo(), ANCORA_B, alv["copa"], faixa=(-2.0, 6.0))
        for lado in (1, -1):
            r[("M", lado)] = assentar(ref_motor(lado), M.berco(), (0, 0, 0), alv["carneira_bruta"],
                                      faixa=(-1.0, 5.0))
            r[("S", lado)] = ref_sensor(lado)
        _cache["refs"] = r
    return _cache["refs"]


def ref_case_a():
    o, x, y, z = K.referencial_copa(*P.POS_CASE_A)
    return Ref(o, x, y, z)


def ref_case_b():
    o, x, y, z = K.referencial_copa(*P.POS_CASE_B)
    return Ref(o, x, y, z)


ANCORA_A = (A.CX, A.CY, -P.PISO - P.BASE_T_MIN)
ANCORA_B = (B.CX, 0.0, -P.BASE_T_MIN)


def ref_sensor(lado):
    y = lado * P.POS_SENSOR_Y
    x = K.borda_aba_x(y) - P.POS_SENSOR_RECUO - S.X_MOLDURA
    return Ref(*K.referencial_aba(x, y))


def ref_motor(lado):
    phi, z = P.POS_MOTOR
    p = K.ponto_copa(lado * phi, z)
    n = K.normal_copa(p)
    o = p - n * (P.BONE_T + P.CARNEIRA_T)
    zv = -n
    up = np.array([0, 0, 1.0])
    xv = up - np.dot(up, zv) * zv
    xv /= np.linalg.norm(xv)
    return Ref(o, xv, np.cross(zv, xv), zv)


def _ponto_pos(wp_fn, p, *args):
    """Aplica a mesma transformação de posicionamento do suporte a um ponto."""
    v = cq.Workplane("XY").add(cq.Vertex.makeVertex(*p))
    v = wp_fn(v, *args)
    q = v.val()
    return np.array([q.X, q.Y, q.Z])


# ------------------------------------------------------------------ cabos
D_SENSOR, D_MOTOR, D_BAT = P.CABO_SENSOR_D * 0.85, P.CABO_MOTOR_D * 0.85, P.CABO_BAT_D * 0.85


def cabos():
    c = []
    # sensores: da saída traseira do suporte, pela aba, até o início da canaleta
    for lado in (1, -1):
        r = ref_sensor(lado)
        loc = (S.X_TRAS - 0.5, 0, S.Z_TOPO_BOLSO - P.CABO_SENSOR_D / 2)
        p0 = r.ponto(_ponto_pos(S._posicionar, loc, P.INCL_SENSOR_MONTAGEM, lado))
        p1 = p0 - r.x * 8 - r.z * 3
        y = lado * P.POS_SENSOR_Y
        xb = K.borda_aba_x(y) - 55
        p2 = K.inclina_aba([xb, lado * 60, K.z_topo_aba(lado * 60) + 2.0])
        p3 = K.inclina_aba([62, lado * 66, K.z_topo_aba(lado * 66) + 2.0])
        p4 = K.ponto_copa(lado * (P.CANALETA_PHI + 1.5), 2.0, 2.5)
        p5 = K.ponto_canaleta(lado * (P.CANALETA_PHI + 4))
        c.append((f"cabo_sensor_{'esq' if lado > 0 else 'dir'}", K.tubo([p0, p1, p2, p3, p4, p5], D_SENSOR)))

    # case A: sensores entram pela parede da frente, motores e bateria saem pela de trás
    R = referenciais()
    ra = R["A"]
    for i, (yg, d) in enumerate(A.PASSA_XM):
        g = ra.ponto(np.array([-P.PAREDE, yg, A.IZ - d / 2]) - ANCORA_A)
        pts = [g, g - ra.x * 7 - ra.z * 2, g - ra.x * 12 - ra.y * 14 - ra.z * 10,
               K.ponto_canaleta(P.POS_CASE_A[0] - 22 - 2 * i)]
        c.append((f"cabo_case_a_sensor_{i + 1}", K.tubo(pts, D_SENSOR)))
    for i, (yg, d) in enumerate(A.PASSA_XP):
        g = ra.ponto(np.array([A.IX + P.PAREDE, yg, A.IZ - d / 2]) - ANCORA_A)
        pts = [g, g + ra.x * 7 - ra.z * 2, g + ra.x * 12 - ra.y * 10 - ra.z * 10,
               K.ponto_canaleta(P.POS_CASE_A[0] + 20 + 3 * i)]
        c.append((f"cabo_case_a_traseiro_{i + 1}", K.tubo(pts, D_BAT if i == 2 else D_MOTOR)))

    # case B: sai pela tampa, na direção da nuca
    rb = R["B"]
    g = rb.ponto(np.array([B.TOTAL_L, 0, B.ZC]) - ANCORA_B)
    pts = [g, g + rb.x * 7 - rb.z * 2, g + rb.x * 12 + rb.y * 12 - rb.z * 10,  # Y do case B aponta para baixo
           K.ponto_canaleta(P.POS_CASE_B[0] - 20)]
    c.append(("cabo_case_b_bateria", K.tubo(pts, D_BAT)))

    # motores: saem da canaleta, atravessam o tecido e descem até o berço
    for lado in (1, -1):
        rm = R[("M", lado)]
        phi = lado * P.POS_MOTOR[0]
        p0 = K.ponto_canaleta(phi - lado * 6)
        p1 = K.ponto_copa(phi - lado * 4, P.POS_MOTOR[1] + 6, 1.0)
        p2 = K.ponto_copa(phi - lado * 3, P.POS_MOTOR[1] + 5, -P.BONE_T - 1.5)
        p3 = rm.ponto((M.CORPO_D / 2 + 3, 0, M.H - 1.5))
        p4 = rm.ponto((M.CORPO_D / 2 - 0.5, 0, M.H - M.BOLSO_H + 0.3))
        c.append((f"cabo_motor_{'esq' if lado > 0 else 'dir'}", K.tubo([p0, p1, p2, p3, p4], D_MOTOR)))
    return c


# ------------------------------------------------------------------ montagem
def pecas(componentes=True):
    """Lista (nome, sólido no mundo, cor)."""
    L = []
    # boné
    L += [("bone_copa", K.copa(), "tecido"), ("bone_aba", K.aba(), "aba"),
          ("bone_botao", K.botao(), "tecido"),
          ("bone_canaleta", K.canaleta(), "canaleta"), ("bone_fita_regulagem", K.fita_regulagem(), "fita")]

    alv = _alvos()
    # case A (lateral esquerda): a base curva assenta na copa
    R = referenciais()
    ra = R["A"]
    L += [("A1_case_eletronica_corpo", ra.coloca(A.corpo(), ANCORA_A), "petg"),
          ("A2_case_eletronica_tampa", ra.coloca(A.tampa(), ANCORA_A), "petg_tampa"),
          ("A3_case_eletronica_base_curva", ra.coloca(A.base_curva(), ANCORA_A), "base curva")]
    furos = [(x - A.CX, y - A.CY) for (x, y) in A.FUROS_BASE_FUNDO]
    cp = U.placa_interna_curvada(furos, A.EX - 6, A.EY - 4)
    anc_cp = (0, 0, P.PISO + P.BASE_T_MIN + P.BONE_T + 4.0)
    rcp = assentar(ra, cp, anc_cp, alv["copa"], faixa=(0.0, 6.0), encostar=True)
    cpa = rcp.coloca(cp, anc_cp)
    L.append(("A4_case_eletronica_placa_interna", cpa, "placa_interna"))
    alma = rcp.coloca(U.almofada_curvada(A.EX - 8, A.EY - 6), anc_cp)
    L.append(("espuma_placa_interna_case_eletronica", alma, "espuma"))

    # case B (lateral direita)
    rb = R["B"]
    L += [("B1_case_bateria_corpo", rb.coloca(B.corpo(), ANCORA_B), "petg"),
          ("B2_case_bateria_tampa", rb.coloca(B.tampa(), ANCORA_B), "petg_tampa")]
    furos = [(x - B.CX, y) for (x, y) in B.FUROS_FUNDO]
    cp = U.placa_interna_curvada(furos, B.TOTAL_L - 4, B.LY + 2, r_canto=5.0)
    anc_cp = (0, 0, P.BASE_T_MIN + P.BONE_T + 4.0)
    rcp = assentar(rb, cp, anc_cp, alv["copa"], faixa=(0.0, 6.0), encostar=True)
    cpb = rcp.coloca(cp, anc_cp)
    L.append(("B3_case_bateria_placa_interna", cpb, "placa_interna"))
    almb = rcp.coloca(U.almofada_curvada(B.TOTAL_L - 6, B.LY, r_canto=5.0), anc_cp)
    L.append(("espuma_placa_interna_case_bateria", almb, "espuma"))
    # a placa interna e a espuma entram por trás da carneira: a faixa cede no lugar delas
    carn = alv["carneira_bruta"].cut(cpa).cut(cpb).cut(alma).cut(almb)
    L.append(("bone_carneira", carn, "carneira"))

    # suportes dos sensores na aba
    inc = P.INCL_SENSOR_MONTAGEM
    for lado, nome in ((1, "esquerdo"), (-1, "direito")):
        r = ref_sensor(lado)
        L += [(f"S1_suporte_sensor_{nome}", r.coloca(S.suporte(inc, lado)), "petg"),
              (f"S2_suporte_sensor_tampa_{nome}", r.coloca(S.tampa_montada(inc, lado)), "petg_tampa"),
              (f"S3_suporte_sensor_placa_sob_aba_{nome}",
               assentar(r, S.placa_sob_aba(), (0, 0, 0), alv["aba"], sentido=-1, faixa=(0.0, 3.0)).coloca(
                   S.placa_sob_aba()), "placa_interna")]
        if componentes:
            L.append((f"gy530_{nome}", r.coloca(S.fantasmas(inc, lado)["gy530"]), "sensor"))

    # berços dos motores
    for lado, nome in ((1, "esquerdo"), (-1, "direito")):
        rm = R[("M", lado)]
        L.append((f"M1_berco_motor_{nome}", rm.coloca(M.berco()), "tpu"))
        L.append((f"espuma_anel_motor_{nome}", rm.coloca(M.anel_espuma()), "espuma"))
        L.append((f"bolso_tecido_motor_{nome}", rm.coloca(M.bolso_tecido()), "carneira"))
        if componentes:
            mot = U.cilindro(P.MOTOR_D, P.MOTOR_H, (0, 0, M.H - M.BOLSO_H))
            L.append((f"motor_{nome}", rm.coloca(mot), "motor"))

    # componentes internos (aparecem no corte / raio-x)
    if componentes:
        g = A.fantasmas()
        for k, cor in (("placa", "pcb"), ("tp4056", "tp4056")):
            L.append((f"{k}_case_a", ra.coloca(g[k], ANCORA_A), cor))
        L.append(("celula_14500", rb.coloca(B.fantasmas()["celula"], ANCORA_B), "celula"))

    # cabos
    L += [(n, s, "cabo") for n, s in cabos()]
    return L


def assembly(componentes=True):
    assy = cq.Assembly(name="provisao_v15_bone_montado")
    for nome, wp, cor in pecas(componentes):
        assy.add(wp, name=nome, color=cq.Color(*COR[cor]))
    return assy
