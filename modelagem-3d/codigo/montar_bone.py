"""
Gera a montagem final do boné com tudo instalado.

    python3 montar_bone.py               # arquivo STEP + arquivo GLB + imagens
    python3 montar_bone.py --so-render   # só as imagens
    python3 montar_bone.py --verificar   # confere se alguma peça atravessa o boné

Saídas:
  ../arquivos-step/Z_montagem_bone_completo.step  montagem com cores e nomes (FreeCAD/Fusion)
  ../bone-montado/provisao_v15_bone_montado.glb   abre em qualquer visualizador 3D e no navegador
  ../imagens/montagem_*.png                       vistas de conferência
"""
import math
import sys
import tempfile
from pathlib import Path

import numpy as np
import cadquery as cq
import vtk

from pecas import montagem as MG
from pecas import medidas as P

AQUI = Path(__file__).resolve().parent
DIR_REN = AQUI.parent / "imagens"
DIR_MON = AQUI.parent / "bone-montado"

TRANSLUCIDO = {"tecido", "aba", "carneira", "canaleta", "fita"}


def _actor(wp, rgba, opac=None):
    tmp = tempfile.NamedTemporaryFile(suffix=".stl", delete=False).name
    cq.exporters.export(wp, tmp, tolerance=0.08, angularTolerance=0.2)
    r = vtk.vtkSTLReader()
    r.SetFileName(tmp)
    n = vtk.vtkPolyDataNormals()
    n.SetInputConnection(r.GetOutputPort())
    n.SetFeatureAngle(40)
    m = vtk.vtkPolyDataMapper()
    m.SetInputConnection(n.GetOutputPort())
    a = vtk.vtkActor()
    a.SetMapper(m)
    p = a.GetProperty()
    p.SetColor(*rgba[:3])
    p.SetOpacity(opac if opac is not None else rgba[3])
    p.SetSpecular(0.2)
    p.SetSpecularPower(18)
    p.SetAmbient(0.22)
    p.SetDiffuse(0.85)
    return a


def render(nome, atores, az, el, foco=None, dist=620, angulo=24, tam=(1600, 1100)):
    ren = vtk.vtkRenderer()
    ren.SetBackground(1, 1, 1)
    ren.SetUseDepthPeeling(1)
    ren.SetMaximumNumberOfPeels(40)
    for a in atores:
        ren.AddActor(a)
    win = vtk.vtkRenderWindow()
    win.SetOffScreenRendering(1)
    win.SetAlphaBitPlanes(1)
    win.SetMultiSamples(0)
    win.SetSize(*tam)
    win.AddRenderer(ren)
    cam = ren.GetActiveCamera()
    f = np.array(foco if foco is not None else (5, 0, 40), float)
    a_, e_ = math.radians(az), math.radians(el)
    pos = f + dist * np.array([math.cos(e_) * math.cos(a_), math.cos(e_) * math.sin(a_), math.sin(e_)])
    cam.SetFocalPoint(*f)
    cam.SetPosition(*pos)
    cam.SetViewUp(*((1, 0, 0) if el > 80 else (0, 0, 1)))
    cam.SetViewAngle(angulo)
    ren.ResetCameraClippingRange()
    luz = vtk.vtkLight()
    luz.SetLightTypeToCameraLight()
    luz.SetIntensity(0.35)
    ren.AddLight(luz)
    win.Render()
    w2i = vtk.vtkWindowToImageFilter()
    w2i.SetInput(win)
    w2i.Update()
    wr = vtk.vtkPNGWriter()
    wr.SetFileName(str(DIR_REN / f"{nome}.png"))
    wr.SetInputConnection(w2i.GetOutputPort())
    wr.Write()
    print("ok", nome)


def main():
    so_render = "--so-render" in sys.argv
    DIR_REN.mkdir(exist_ok=True)
    DIR_MON.mkdir(exist_ok=True)
    pecas = MG.pecas(componentes=True)

    if not so_render:
        assy = cq.Assembly(name="provisao_v15_bone_montado")
        for nome, wp, cor in pecas:
            assy.add(wp, name=nome, color=cq.Color(*MG.COR[cor]))
        assy.save(str(AQUI.parent / "arquivos-step" / "Z_montagem_bone_completo.step"))
        assy.save(str(DIR_MON / "provisao_v15_bone_montado.glb"))
        print("ok STEP e GLB")

    normais = [_actor(wp, MG.COR[c]) for _, wp, c in pecas]
    raiox = [_actor(wp, MG.COR[c], 0.18 if c in TRANSLUCIDO else None) for _, wp, c in pecas]

    render("montagem_01_frente_esquerda", normais, 35, 22)
    render("montagem_02_lateral_esquerda_case_a", normais, 95, 12)
    render("montagem_03_lateral_direita_case_b", normais, -95, 12)
    render("montagem_04_traseira_canaleta", normais, 180, 18)
    render("montagem_05_topo", normais, 0.01, 89.9, dist=700)
    render("montagem_06_detalhe_aba_sensores", normais, 15, 38, foco=(112, 0, -4), dist=470)
    render("montagem_07_raiox_esquerda_tras", raiox, 140, 20)
    render("montagem_08_raiox_direita_tras", raiox, -140, 20)


if __name__ == "__main__" and "--verificar" not in sys.argv:
    main()


def verificar():
    """Interferência entre as peças impressas e o boné depois do assentamento."""
    L = {n: wp for n, wp, c in MG.pecas(componentes=False)}
    pares = []
    for n in L:
        if n.startswith(("A", "B", "S", "M", "espuma")):
            for alvo in ("bone_copa", "bone_aba", "bone_carneira", "bone_canaleta"):
                pares.append((n, alvo))
    falhas = []
    for a, b in pares:
        try:
            v = L[a].val().intersect(L[b].val()).Volume()
        except Exception:
            v = 0.0
        if v > 1.0:
            falhas.append(f"{a} x {b}: {v:.1f} mm3")
    print("Montagem:", "sem interferência entre peças e boné" if not falhas else "\n  " + "\n  ".join(falhas))
    for n in ("A3_case_eletronica_base_curva", "B1_case_bateria_corpo", "A4_case_eletronica_placa_interna",
              "B3_case_bateria_placa_interna"):
        print(f"  folga {n} x copa: {L[n].val().distance(L['bone_copa'].val()):.2f} mm")
    return not falhas


if __name__ == "__main__" and "--verificar" in sys.argv:
    verificar()
