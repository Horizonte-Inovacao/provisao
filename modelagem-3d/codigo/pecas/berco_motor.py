# SPDX-FileCopyrightText: 2026 Edson Gabriel Soares da Fonseca, João Luiz Pereira Filho, Nadson Alex da Silva
# SPDX-License-Identifier: CERN-OHL-S-2.0

"""
Berço do motor de vibração (motor tipo moeda, 10 x 2,7 mm).

Os motores ficam perto da nuca, porque nas têmporas incomodavam. O berço é
impresso em TPU 95A (plástico flexível) para ceder e acompanhar a curva da
cabeça. Ele vai dentro de um bolsinho de tecido costurado na carneira, com um
anel de EVA em volta do motor. Assim a pele encosta só no tecido.

O motor entra sob pressão no bolso do berço e fica 0,3 mm para fora,
virado para a cabeça, para o contato continuar firme.
"""
import math

import cadquery as cq

from . import medidas as P
from . import auxiliares as U

ABA_D, ABA_T = P.BERCO_ABA_D, P.BERCO_ABA_T
CORPO_D = P.MOTOR_D + 2 * 2.0
BOLSO_D = P.MOTOR_D + 0.1              # encaixe sob pressão no TPU
BOLSO_H = P.MOTOR_H - P.MOTOR_SALTO
H = P.BERCO_ALTURA
FUNDO = H - BOLSO_H                    # material embaixo do motor


def berco():
    b = U.cilindro(ABA_D, ABA_T, (0, 0, 0)).union(U.cilindro(CORPO_D, H, (0, 0, 0)))
    b = b.faces(">Z").edges().fillet(0.8)
    b = b.faces("<Z").edges().fillet(0.4)
    b = b.cut(U.cilindro(BOLSO_D, BOLSO_H + 1, (0, 0, FUNDO)))
    # canal de saída do fio
    b = b.cut(U.caixa_arred(0, -0.9, FUNDO - 0.4, CORPO_D, 1.8, BOLSO_H + 2, 0))
    # furos de costura na aba
    r = (ABA_D / 2 + CORPO_D / 2) / 2
    for ang in (45, 135, 225, 315):
        x, y = r * math.cos(math.radians(ang)), r * math.sin(math.radians(ang))
        b = b.cut(U.cilindro(1.3, ABA_T + 2, (x, y, -1)))
    return b


def anel_espuma():
    """Anel de EVA em volta do corpo do berço (só para a montagem visual)."""
    a = U.cilindro(ABA_D - 1.0, P.ESPUMA_MOTOR_T, (0, 0, ABA_T))
    return a.cut(U.cilindro(CORPO_D + 0.6, P.ESPUMA_MOTOR_T + 2, (0, 0, ABA_T - 1)))


def bolso_tecido():
    """Bolsinho de tecido que cobre berço, anel e motor (só para a montagem visual)."""
    topo = H + P.MOTOR_SALTO + 0.6
    b = U.cilindro(ABA_D + 1.2, topo, (0, 0, 0))
    b = b.faces(">Z").edges().fillet(2.0)
    oco = U.cilindro(ABA_D + 0.1, topo - 0.55, (0, 0, -0.01))
    return b.cut(oco)
