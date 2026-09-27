# SPDX-FileCopyrightText: 2026 Edson Gabriel Soares da Fonseca, João Luiz Pereira Filho, Nadson Alex da Silva
# SPDX-License-Identifier: CERN-OHL-S-2.0

"""
Case A - eletrônica (placa ilhada + ESP32-C3 + TP4056 + chave + buzzer).

Sistema de coordenadas (interior do case):
  X: horizontal ao longo da lateral do boné. X- aponta para a frente (aba),
     X+ aponta para a nuca.
  Y: vertical na lateral do boné. Y- aponta para baixo (orelha / carneira).
  Z: para fora da cabeça. z=0 é a face de cima do piso.

Peças geradas:
  corpo()        caixa com espaçadores, trilhos do TP4056, recortes e passa-cabos
  tampa()        tampa com colunas passantes, tubos de luz dos LEDs e furos do buzzer
  base curva()         base curva que assenta na copa (separada: reimprime se trocar de boné)
  placa_interna()  placa interna, fixa a base curva através do tecido
"""
import cadquery as cq

from . import medidas as P
from . import auxiliares as U

# ---------------------------------------------------------------- layout
FX = 0.5                                   # folga placa x parede
IX_PLACA = PLACA_REG = P.PLACA_X + 2 * FX  # região da placa em X
GAP = 1.0
TP_REG = P.TP_X + 2 * 0.35
IX = IX_PLACA + GAP + TP_REG               # interior X
IY = P.PLACA_Y + 2 * FX                    # interior Y
IZ = P.PLACA_ESPACADOR + P.PLACA_T + P.ALTURA_ACIMA_PLACA

EX, EY = IX + 2 * P.PAREDE, IY + 2 * P.PAREDE
CX, CY = IX / 2, IY / 2                    # centro do case (e da base curva)

# furos da placa (coordenadas do interior)
FUROS_PLACA = [
    (FX + P.PLACA_FURO_INSET, FX + P.PLACA_FURO_INSET),
    (FX + P.PLACA_X - P.PLACA_FURO_INSET, FX + P.PLACA_FURO_INSET),
    (FX + P.PLACA_FURO_INSET, FX + P.PLACA_Y - P.PLACA_FURO_INSET),
    (FX + P.PLACA_X - P.PLACA_FURO_INSET, FX + P.PLACA_Y - P.PLACA_FURO_INSET),
]
Z_PLACA_TOPO = P.PLACA_ESPACADOR + P.PLACA_T

# TP4056
TP_X0 = IX_PLACA + GAP + 0.35
TP_X1 = TP_X0 + P.TP_X
TP_CX = (TP_X0 + TP_X1) / 2
TP_Z_PCB_TOPO = P.TP_TRILHO_H + P.TP_PCB_T
USB_ZC = TP_Z_PCB_TOPO + P.USB_ALTURA_CENTRO  # centro do receptáculo

# chave na parede X+ (região livre acima do fim do TP4056)
CHAVE_YC = (P.TP_Y + 1.5 + IY) / 2
CHAVE_ZC = IZ / 2

# passa-cabos (entalhes abertos para a tampa)
PASSA_XM = [(IY * 0.32, P.CABO_SENSOR_D), (IY * 0.68, P.CABO_SENSOR_D)]           # parede X-
PASSA_XP = [(6.0, P.CABO_MOTOR_D), (13.5, P.CABO_MOTOR_D), (21.5, P.CABO_BAT_D)]  # parede X+

# parafusos case -> base curva (escareados no piso, por dentro)
FUROS_BASE_TOPO = [(CX - 30, CY - 10), (CX - 30, CY + 10), (CX + 30, CY - 10), (CX + 31, CY + 8)]
# parafusos placa_interna -> base curva (por baixo, através do tecido)
FUROS_BASE_FUNDO = [(CX - 30, CY - 17), (CX - 30, CY + 17), (CX + 30, CY - 17), (CX + 30, CY + 17)]

# pressores do TP4056 na tampa e batente
PRESSORES_TP = [(TP_X0 + 1.4, 20.0), (TP_X1 - 1.4, 20.0)]
BATENTE_TP = (TP_CX - 3, P.TP_Y + 0.3, 6.0, 1.2)  # x0, y0, lx, ly


def _casca():
    ext = U.caixa_arred(-P.PAREDE, -P.PAREDE, -P.PISO, EX, EY, IZ + P.PISO, P.R_CANTO)
    ext = ext.faces("<Z").edges().fillet(P.R_BORDA)
    oco = U.caixa_arred(0, 0, 0, IX, IY, IZ + 1, 0.2)  # canto interno vivo: placa e TP4056 encostam
    return ext.cut(oco)


def corpo():
    c = _casca()

    # espaçadores da placa (piloto M2: o parafuso passante da tampa rosqueia aqui)
    for (x, y) in FUROS_PLACA:
        c = c.union(U.cilindro(5.0, P.PLACA_ESPACADOR, (x, y, 0)))
        c = c.cut(U.cilindro(P.M2_PILOTO, P.PLACA_ESPACADOR + P.PISO - 0.6, (x, y, -P.PISO + 0.6)))

    # trilhos do TP4056
    for x0 in (TP_X0, TP_X1 - 1.2):
        c = c.union(U.caixa_arred(x0, 2.0, 0, 1.2, P.TP_Y - 3.0, P.TP_TRILHO_H, 0))
    bx, by, blx, bly = BATENTE_TP
    c = c.union(U.caixa_arred(bx, by, 0, blx, bly, TP_Z_PCB_TOPO + 1.5, 0))

    # USB-C na parede Y- (estádio) + rebaixo externo para a capa do plugue
    usb = (cq.Workplane("XZ", origin=(0, 1.0, 0)).center(TP_CX, USB_ZC)
           .slot2D(P.USB_W + 2 * P.FOLGA, P.USB_H + 2 * P.FOLGA).extrude(P.PAREDE + 2))
    c = c.cut(usb)
    reb_prof = P.PAREDE - P.USB_BALANCO
    rebaixo = (cq.Workplane("XZ", origin=(0, -P.PAREDE + reb_prof, 0)).center(TP_CX, USB_ZC)
               .slot2D(P.PLUGUE_W, P.PLUGUE_H).extrude(reb_prof + 1))
    c = c.cut(rebaixo)

    # chave gangorra na parede X+
    chave = U.caixa_arred(IX - 1, CHAVE_YC - P.CHAVE_CORTE_Y / 2, CHAVE_ZC - P.CHAVE_CORTE_Z / 2,
                          P.PAREDE + 2, P.CHAVE_CORTE_Y, P.CHAVE_CORTE_Z, 0)
    c = c.cut(chave)
    # ponto tátil ao lado da metade "ligado" (chave montada com ON para cima = Z+)
    c = c.union(U.ponto_tatil((IX + P.PAREDE, CHAVE_YC - P.CHAVE_CORTE_Y / 2 - 3.0,
                               CHAVE_ZC + P.CHAVE_CORTE_Z / 4), (1, 0, 0)))

    # passa-cabos: entalhe do topo da parede, fundo arredondado; a tampa fecha por cima
    def entalhe(x_parede, y, d):
        prof = d
        corte = (cq.Workplane("YZ", origin=(x_parede - 1, 0, 0))
                 .center(y, IZ).slot2D(prof * 2, d, angle=90)
                 .extrude(P.PAREDE + 2))
        return corte
    for (y, d) in PASSA_XM:
        c = c.cut(entalhe(-P.PAREDE, y, d))
    for (y, d) in PASSA_XP:
        c = c.cut(entalhe(IX, y, d))

    # furos escareados case -> base curva (por dentro do piso)
    for (x, y) in FUROS_BASE_TOPO:
        c = c.cut(U.escareado((x, y, 0), P.M2_PASSANTE, P.M2_ESCAREADO_D, P.PISO + 1, para_baixo=True))

    return c


def tampa():
    t = U.caixa_arred(-P.PAREDE, -P.PAREDE, IZ, EX, EY, P.TAMPA, P.R_CANTO)
    t = t.faces(">Z").edges().fillet(P.R_BORDA)

    # aba de encaixe só nas paredes Y (as paredes X têm passa-cabos e a chave)
    aba_h, aba_t, f = 2.5, 0.8, 0.2
    for y0 in (f, IY - f - aba_t):
        t = t.union(U.caixa_arred(4.0, y0, IZ - aba_h, IX - 8.0, aba_t, aba_h, 0))

    # colunas passantes: prendem tampa + placa no espaçador com M2 x 20
    for (x, y) in FUROS_PLACA:
        h = IZ - Z_PLACA_TOPO
        t = t.union(U.cilindro(5.0, h, (x, y, Z_PLACA_TOPO)))
        t = t.cut(U.cilindro(P.M2_PASSANTE, h + P.TAMPA + 1, (x, y, Z_PLACA_TOPO - 0.5)))
        t = t.cut(U.cilindro(P.M2_CABECA_D, P.M2_CABECA_H + 1, (x, y, IZ + P.TAMPA - P.M2_CABECA_H)))

    # pressores do TP4056 (seguram o módulo quando o plugue USB é inserido)
    for (x, y) in PRESSORES_TP:
        z0 = TP_Z_PCB_TOPO + 0.2
        t = t.union(U.cilindro(2.4, IZ - z0, (x, y, z0)))

    # tubos de luz sobre os LEDs do TP4056 (encaixar filamento transparente 1.75)
    for (dx, y) in P.TP_LEDS:
        x = TP_CX + dx
        z0 = TP_Z_PCB_TOPO + 1.0
        t = t.union(U.cilindro(4.4, IZ - z0, (x, y, z0)))
        t = t.cut(U.cilindro(2.0, IZ - z0 + P.TAMPA + 1, (x, y, z0 - 0.5)))

    # furos do buzzer
    bx, by = FX + P.BUZZER_POS[0], FX + P.BUZZER_POS[1]
    furos = [(bx, by)] + [(bx + 3.5 * c, by + 3.5 * s) for c, s in
                          [(1, 0), (0.5, 0.866), (-0.5, 0.866), (-1, 0), (-0.5, -0.866), (0.5, -0.866)]]
    for (x, y) in furos:
        t = t.cut(U.cilindro(1.6, P.TAMPA + 2, (x, y, IZ - 1)))

    # identificação em baixo relevo
    t = (t.faces(">Z").workplane(centerOption="CenterOfBoundBox")
         .center(-EX * 0.18, -EY * 0.28).text("PróVisão", 5.0, -0.5, combine="cut"))
    return t


def base_curva():
    s = U.base_curva(CX, CY, EX, EY, -P.PISO, P.R_CANTO)
    z_topo = -P.PISO
    # pilotos para os parafusos do case (entram por cima)
    for (x, y) in FUROS_BASE_TOPO:
        t_loc = z_topo - U.z_fundo_base(x - CX, z_topo)
        prof = min(5.0, t_loc - 0.8)
        s = s.cut(U.cilindro(P.M2_PILOTO, prof, (x, y, z_topo - prof)))
    # pilotos para os parafusos da placa_interna (entram por baixo, pelo tecido)
    for (x, y) in FUROS_BASE_FUNDO:
        zf = U.z_fundo_base(x - CX, z_topo)
        prof = min(6.0, (z_topo - zf) - 0.8)
        s = s.cut(U.cilindro(P.M2_PILOTO, prof + 0.5, (x, y, zf - 0.5)))
    return s


def placa_interna():
    furos = [(x - CX, y - CY) for (x, y) in FUROS_BASE_FUNDO]
    return U.placa_interna(furos, EX - 6, EY - 4)


# ---------------------------------------------------------------- volumes de referência
def fantasmas():
    """Volumes simplificados dos componentes, só para checar interferência."""
    g = {}
    g["placa"] = U.caixa_arred(FX, FX, P.PLACA_ESPACADOR, P.PLACA_X, P.PLACA_Y, P.PLACA_T, 0)
    g["tp4056"] = U.caixa_arred(TP_X0, 0, P.TP_TRILHO_H, P.TP_X, P.TP_Y, P.TP_PCB_T, 0)
    g["usb"] = (cq.Workplane("XZ", origin=(0, 7.3 - P.USB_BALANCO, 0)).center(TP_CX, USB_ZC)
                .slot2D(P.USB_W, P.USB_H).extrude(7.3))
    g["chave"] = U.caixa_arred(IX - P.CHAVE_PROF, CHAVE_YC - 4.25, CHAVE_ZC - 6.5,
                               P.CHAVE_PROF, 8.5, 13.0, 0)
    bx, by = FX + P.BUZZER_POS[0], FX + P.BUZZER_POS[1]
    g["buzzer"] = U.cilindro(P.BUZZER_D, 9.5, (bx, by, Z_PLACA_TOPO))
    return g
