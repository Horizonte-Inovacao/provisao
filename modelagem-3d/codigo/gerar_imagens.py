# SPDX-FileCopyrightText: 2026 Edson Gabriel Soares da Fonseca, João Luiz Pereira Filho, Nadson Alex da Silva
# SPDX-License-Identifier: CERN-OHL-S-2.0

"""
Renders de conferência (PNG) das peças e das montagens.

    python3 gerar_imagens.py

Gera as imagens em ../imagens/. Usa VTK offscreen (vem junto com o cadquery).
"""
from pathlib import Path
import tempfile

import cadquery as cq
import vtk

from pecas import case_eletronica as A
from pecas import case_bateria as B
from pecas import suporte_sensor as S
from pecas import berco_motor as M
from pecas import medidas as P
from pecas import auxiliares as U

AQUI = Path(__file__).resolve().parent
DIR = AQUI.parent / "imagens"

PETROLEO = (0.106, 0.424, 0.475)
CORAL = (0.878, 0.478, 0.373)
AMBAR = (0.922, 0.659, 0.298)
CINZA = (0.75, 0.77, 0.78)
VERDE = (0.25, 0.55, 0.30)
AZUL = (0.35, 0.45, 0.75)


def _actor(wp, cor, opac=1.0):
    tmp = tempfile.NamedTemporaryFile(suffix=".stl", delete=False).name
    cq.exporters.export(wp, tmp, tolerance=0.05, angularTolerance=0.2)
    r = vtk.vtkSTLReader()
    r.SetFileName(tmp)
    n = vtk.vtkPolyDataNormals()
    n.SetInputConnection(r.GetOutputPort())
    n.SetFeatureAngle(35)
    m = vtk.vtkPolyDataMapper()
    m.SetInputConnection(n.GetOutputPort())
    a = vtk.vtkActor()
    a.SetMapper(m)
    p = a.GetProperty()
    p.SetColor(*cor)
    p.SetOpacity(opac)
    p.SetSpecular(0.25)
    p.SetSpecularPower(20)
    p.SetAmbient(0.18)
    return a


def render(nome, itens, az=35, el=28, zoom=1.0, tam=(1200, 900), roll=0):
    ren = vtk.vtkRenderer()
    ren.SetBackground(1, 1, 1)
    for wp, cor, *op in itens:
        ren.AddActor(_actor(wp, cor, op[0] if op else 1.0))
    win = vtk.vtkRenderWindow()
    win.SetOffScreenRendering(1)
    win.SetSize(*tam)
    win.AddRenderer(ren)
    import math
    ren.ResetCamera()
    cam = ren.GetActiveCamera()
    fx, fy, fz = cam.GetFocalPoint()
    d = 1000.0
    a, e = math.radians(az), math.radians(el)
    cam.SetPosition(fx + d * math.cos(e) * math.cos(a), fy + d * math.cos(e) * math.sin(a), fz + d * math.sin(e))
    cam.SetViewUp(0, 0, 1)
    cam.SetViewAngle(20)
    ren.ResetCamera()
    cam.Zoom(zoom * 1.1)
    win.Render()
    w2i = vtk.vtkWindowToImageFilter()
    w2i.SetInput(win)
    w2i.Update()
    wr = vtk.vtkPNGWriter()
    wr.SetFileName(str(DIR / f"{nome}.png"))
    wr.SetInputConnection(w2i.GetOutputPort())
    wr.Write()
    print("ok", nome)


def main():
    DIR.mkdir(exist_ok=True)
    g = A.fantasmas()
    # ---- Case A
    render("A_case_eletronica_explodido", [
        (A.placa_interna().translate((A.CX, A.CY, -40)), CINZA),
        (A.base_curva().translate((0, 0, -18)), AMBAR),
        (A.corpo(), PETROLEO),
        (g["placa"], VERDE), (g["tp4056"], AZUL), (g["buzzer"], (0.2, 0.2, 0.2)),
        (g["chave"], (0.15, 0.15, 0.15)),
        (A.tampa().translate((0, 0, 28)), CORAL, 0.92),
    ], az=-60, el=25)
    render("A_case_eletronica_interior", [
        (A.corpo(), PETROLEO), (g["placa"], VERDE), (g["tp4056"], AZUL),
        (g["buzzer"], (0.2, 0.2, 0.2)), (g["chave"], (0.15, 0.15, 0.15)),
    ], az=-70, el=55)
    render("A_case_eletronica_fechado", [
        (A.base_curva(), AMBAR), (A.corpo(), PETROLEO), (A.tampa(), CORAL),
    ], az=-120, el=25)
    render("A_case_eletronica_tampa_por_baixo", [(A.tampa(), CORAL)], az=-60, el=-50)

    # ---- Case B
    gb = B.fantasmas()
    render("B_case_bateria_explodido", [
        (B.placa_interna().translate((B.CX, 0, -22)), CINZA),
        (B.corpo(), PETROLEO), (gb["celula"], (0.3, 0.3, 0.3), 0.9),
        (B.tampa().translate((22, 0, 0)), CORAL),
    ], az=-60, el=25)
    render("B_case_bateria_fechado", [(B.corpo(), PETROLEO), (B.tampa(), CORAL)], az=60, el=30)

    # ---- Sensor
    for inc in (0, 20):
        render(f"S_suporte_sensor_direito_{inc:02d}graus", [
            (S.suporte(inc, -1), PETROLEO),
            (S.placa_sob_aba(), AMBAR),
            (S.fantasmas(inc, -1)["gy530"], (0.45, 0.2, 0.6)),
        ], az=-140, el=25)
    render("S_suporte_sensor_frente", [(S.suporte(10, -1), PETROLEO),
                               (S.fantasmas(10, -1)["gy530"], (0.45, 0.2, 0.6))], az=-10, el=8)
    render("S_suporte_sensor_explodido", [
        (S.placa_sob_aba().translate((0, 0, -12)), AMBAR),
        (S.suporte(10, -1), PETROLEO),
        (S.fantasmas(10, -1)["gy530"], (0.45, 0.2, 0.6)),
        (S.tampa_montada(10, -1).translate((0, 0, 14)), CORAL),
    ], az=-140, el=30)
    render("M_berco_motor", [(M.berco(), (0.20, 0.55, 0.60))], az=30, el=40)
    # conforto: o que fica entre a peça e a cabeça
    motor = U.cilindro(P.MOTOR_D, P.MOTOR_H, (0, 0, M.FUNDO))
    render("M_berco_motor_conforto_explodido", [
        (M.berco(), (0.20, 0.55, 0.60)),
        (motor.translate((0, 0, 8)), (0.70, 0.70, 0.72)),
        (M.anel_espuma().translate((0, 0, 14)), (0.14, 0.14, 0.16)),
        (M.bolso_tecido().translate((0, 0, 22)), (0.25, 0.27, 0.30), 0.55),
    ], az=35, el=25)
    from pecas import case_eletronica as A2
    furos = [(x - A2.CX, y - A2.CY) for (x, y) in A2.FUROS_BASE_FUNDO]
    render("A_placa_interna_com_espuma", [
        (A2.placa_interna(), CORAL),
        (U.caixa_arred(-(A2.EX - 8) / 2, -(A2.EY - 6) / 2, -P.PLACA_INTERNA_T - P.ESPUMA_PLACA_T - 6,
                       A2.EX - 8, A2.EY - 6, P.ESPUMA_PLACA_T, 5.0), (0.14, 0.14, 0.16)),
    ], az=-50, el=-30)


if __name__ == "__main__":
    main()
