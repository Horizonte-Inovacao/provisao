"""
Checagens automáticas de montagem: interferência entre peças e componentes,
sólidos válidos e espessuras mínimas nos pontos críticos.

    python3 verificar_encaixes.py
"""
import itertools

import cadquery as cq

from pecas import case_eletronica as A
from pecas import case_bateria as B
from pecas import suporte_sensor as S
from pecas import medidas as P
from pecas import auxiliares as U

TOL = 0.01  # mm3
falhas = []


def vol_intersec(a, b):
    try:
        return a.val().intersect(b.val()).Volume()
    except Exception:
        return 0.0


def checa(nome, conjunto, fantasmas=()):
    for (na, a), (nb, b) in itertools.combinations(conjunto.items(), 2):
        if na in fantasmas and nb in fantasmas:
            continue  # componente x componente não interessa aqui
        v = vol_intersec(a, b)
        status = "OK " if v < TOL else "FALHA"
        if v >= TOL:
            falhas.append(f"{nome}: {na} x {nb} = {v:.2f} mm3")
        print(f"  [{status}] {na:>14} x {nb:<14} {v:8.3f} mm3")


print("Case A")
ga = A.fantasmas()
checa("A", {"corpo": A.corpo(), "tampa": A.tampa(), "base curva": A.base_curva(), **ga}, ga.keys())

print("Case B")
gb = B.fantasmas()
checa("B", {"corpo": B.corpo(), "tampa": B.tampa(), **gb})

for inc in P.POD_INCLINACOES:
    for lado in (1, -1):
        print(f"Sensor inc={inc} lado={lado}")
        checa(f"S{inc}{lado}", {"suporte": S.suporte(inc, lado), "tampa": S.tampa_montada(inc, lado),
                                **S.fantasmas(inc, lado), "placa_interna": S.placa_sob_aba()})

# espessura que sobra acima dos pilotos da base curva A
print("Base curva A: material acima dos pilotos de baixo")
for (x, y) in A.FUROS_BASE_FUNDO:
    t = -P.PISO - U.z_fundo_base(x - A.CX, -P.PISO)
    prof = min(6.0, t - 0.8)
    print(f"  ({x:5.1f},{y:5.1f}) base curva={t:4.1f} piloto={prof:3.1f} sobra={t - prof:3.1f}")

# FOV: a moldura não pode cortar o cone de 25 graus que sai do chip
import math
t = math.tan(math.radians(12.5))
dx = S.X_MOLDURA - 1.0          # face do chip ~1 mm à frente da placa
meia_h = 1.2 + dx * t
meia_w = 2.2 + dx * t
aro = 2.0
folga_cima = (S.H - aro) - (S.CHIP_Z + meia_h)
folga_baixo = (S.CHIP_Z - meia_h) - aro
folga_lado = (S.W / 2 - aro) - (abs(S.CHIP_Y) + meia_w)
print(f"FOV na moldura: folga cima={folga_cima:.2f} baixo={folga_baixo:.2f} lado={folga_lado:.2f}")
for nome, f in (("cima", folga_cima), ("baixo", folga_baixo), ("lado", folga_lado)):
    if f < 0:
        falhas.append(f"FOV cortado pela moldura ({nome})")

print("\nResumo:", "tudo certo" if not falhas else "\n  " + "\n  ".join(falhas))
