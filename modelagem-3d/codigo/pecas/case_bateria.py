# SPDX-FileCopyrightText: 2026 Edson Gabriel Soares da Fonseca, João Luiz Pereira Filho, Nadson Alex da Silva
# SPDX-License-Identifier: CERN-OHL-S-2.0

"""
Case B - bateria Li-ion 14500 (fica na lateral oposta ao case A).

Formato "tubo": a célula entra por uma ponta num furo cilíndrico fechado do
lado positivo. A ponta aberta é fechada por uma tampa parafusada que abriga o
polyfuse e o passa-cabo. Nada aperta a célula: ela fica envolvida em EVA de 1 mm
dentro de um furo com folga.

A base curva curva é parte do próprio corpo (impressão em pé, sem suporte).

Coordenadas:
  X: comprimento. x=0 é a ponta fechada (polo +). A tampa fica em X+ e aponta
     para a nuca, de onde o cabo segue até o case A.
  Y: largura (vertical na lateral do boné).
  Z: para fora da cabeça. z=0 é o topo da base curva (base do bloco).

Peças: corpo(), tampa(), placa_interna()
"""
import cadquery as cq

from . import medidas as P
from . import auxiliares as U

FURO_D = P.CEL_D + 2 * P.EVA_T + 2 * 0.2
FURO_L = P.CEL_L + 2 * P.EVA_PONTA + P.FOLGA_FIO_PONTA
CORPO_L = P.FUNDO_B + FURO_L
TOTAL_L = CORPO_L + P.TAMPA_B_L
LY = FURO_D + 2 * 3.5          # parede lateral mais grossa para os pilotos da tampa
LZ = P.PAREDE_B + FURO_D + P.PAREDE_B
ZC = P.PAREDE_B + FURO_D / 2   # eixo do furo
CX = TOTAL_L / 2               # centro da base curva
R_CANTO_B = 3.0

# pilotos da tampa (face aberta do corpo)
PARAF_TAMPA = [(-9.2, 2.8), (9.2, 2.8), (-9.2, LZ - 2.8), (9.2, LZ - 2.8)]   # (y, z)
# placa_interna -> base curva (por baixo)
FUROS_FUNDO = [(7.0, -7.0), (7.0, 7.0), (TOTAL_L - 7.0, -7.0), (TOTAL_L - 7.0, 7.0)]


def corpo():
    s = U.base_curva(CX, 0, TOTAL_L, LY, 0.0, R_CANTO_B)
    bloco = U.caixa_arred(0, -LY / 2, 0, CORPO_L, LY, LZ, 0)
    bloco = bloco.edges("|Z and <X").fillet(R_CANTO_B).edges("|X and >Z").fillet(2.0)
    c = s.union(bloco)

    # furo da célula
    c = c.cut(U.cilindro(FURO_D, FURO_L + 1, (P.FUNDO_B, 0, ZC), "X"))
    # canal lateral para o fio do polo + voltar até a tampa
    c = c.cut(U.caixa_arred(P.FUNDO_B, FURO_D / 2 - 0.5, ZC - P.CANAL_FIO_W / 2,
                            FURO_L + 1, P.CANAL_FIO_P + 0.5, P.CANAL_FIO_W, 0))

    # respiros no teto, sobre o polo + (apontam para fora da cabeça)
    for x in (P.FUNDO_B + 3.0, P.FUNDO_B + 6.5, P.FUNDO_B + 10.0):
        c = c.cut(U.caixa_arred(x, -4.0, LZ - P.PAREDE_B - 1, 1.5, 8.0, P.PAREDE_B + 2, 0))

    # pilotos da tampa na face aberta
    for (y, z) in PARAF_TAMPA:
        c = c.cut(U.cilindro(P.M2_PILOTO, 7.0, (CORPO_L - 7.0, y, z), "X"))

    # pilotos da placa_interna (por baixo)
    for (x, y) in FUROS_FUNDO:
        zf = U.z_fundo_base(x - CX, 0.0)
        prof = min(6.0, -zf - 0.8)
        c = c.cut(U.cilindro(P.M2_PILOTO, prof + 0.5, (x, y, zf - 0.5)))

    # marcação de polaridade em baixo relevo na lateral Y+
    for x, txt in ((8.0, "+"), (CORPO_L - 8.0, "-")):
        pl = cq.Plane(origin=(x, LY / 2, LZ / 2), xDir=(1, 0, 0), normal=(0, 1, 0))
        c = c.cut(cq.Workplane(pl).text(txt, 8, -0.6, combine=False))
    return c


def tampa():
    t = U.caixa_arred(CORPO_L, -LY / 2, 0, P.TAMPA_B_L, LY, LZ, 0)
    t = t.edges("|Z and >X").fillet(R_CANTO_B).edges("|X and >Z").fillet(2.0)
    # cavidade do polyfuse, aberta para o corpo
    cav_l = P.TAMPA_B_L - 2.5
    t = t.cut(U.caixa_arred(CORPO_L - 0.1, -7.0, P.PAREDE_B, cav_l + 0.1, 14.0, LZ - 2 * P.PAREDE_B, 1.0))
    # passa-cabo na ponta
    t = t.cut(U.cilindro(P.CABO_BAT_D + 0.2, 4.0, (TOTAL_L - 3.0, 0, ZC), "X"))
    # parafusos passantes com rebaixo para a cabeça (M2 x 12)
    for (y, z) in PARAF_TAMPA:
        t = t.cut(U.cilindro(P.M2_PASSANTE, P.TAMPA_B_L + 1, (CORPO_L - 0.5, y, z), "X"))
        t = t.cut(U.cilindro(P.M2_CABECA_D, 3.6, (TOTAL_L - 3.5, y, z), "X"))
    return t


def placa_interna():
    furos = [(x - CX, y) for (x, y) in FUROS_FUNDO]
    return U.placa_interna(furos, TOTAL_L - 4, LY + 2, r_canto=5.0)


def fantasmas():
    g = {}
    g["celula"] = U.cilindro(P.CEL_D, P.CEL_L, (P.FUNDO_B + P.EVA_PONTA + P.FOLGA_FIO_PONTA, 0, ZC), "X")
    return g
