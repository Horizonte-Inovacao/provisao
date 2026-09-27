"""
Gera os arquivos de todas as peças impressas da PróVisão V1.5.

    python3 gerar_pecas.py            # arquivos STEP e STL de todas as peças
    python3 gerar_pecas.py --so-stl   # só os STL

O STEP sai na posição de montagem, para abrir no FreeCAD ou no Fusion e conferir.
O STL sai já na posição de impressão, apoiado na mesa (z=0).
"""
import sys
from pathlib import Path

import cadquery as cq

from pecas import case_eletronica as A
from pecas import case_bateria as B
from pecas import suporte_sensor as S
from pecas import berco_motor as M
from pecas import medidas as P

AQUI = Path(__file__).resolve().parent
DIR_STEP = AQUI.parent / "arquivos-step"
DIR_STL = AQUI.parent / "arquivos-stl"


def _no_chao(wp):
    bb = wp.val().BoundingBox()
    return wp.translate((-(bb.xmin + bb.xmax) / 2, -(bb.ymin + bb.ymax) / 2, -bb.zmin))


def _vira(wp):          # 180 graus em X: face de cima vai para a mesa
    return wp.rotate((0, 0, 0), (1, 0, 0), 180)


def _x_para_cima(wp):   # +X passa a apontar para +Z
    return wp.rotate((0, 0, 0), (0, 1, 0), -90)


def _x_para_baixo(wp):
    return wp.rotate((0, 0, 0), (0, 1, 0), 90)


def pecas():
    """(nome, sólido na posição de projeto, função de orientação para impressão)"""
    ident = lambda w: w
    p = [
        ("A1_case_eletronica_corpo", A.corpo(), ident),
        ("A2_case_eletronica_tampa", A.tampa(), _vira),
        ("A3_case_eletronica_base_curva", A.base_curva(), _vira),
        ("A4_case_eletronica_placa_interna", A.placa_interna(), ident),
        ("B1_case_bateria_corpo", B.corpo(), _x_para_cima),
        ("B2_case_bateria_tampa", B.tampa(), _x_para_baixo),
        ("B3_case_bateria_placa_interna", B.placa_interna(), ident),
        ("S2_suporte_sensor_tampa", S.tampa(), ident),
        ("S3_suporte_sensor_placa_sob_aba", S.placa_sob_aba(), ident),
        ("M1_berco_motor", M.berco(), ident),
    ]
    for inc in P.POD_INCLINACOES:
        p.append((f"S1_suporte_sensor_esquerdo_{inc:02d}graus", S.suporte(inc, +1), ident))
        p.append((f"S1_suporte_sensor_direito_{inc:02d}graus", S.suporte(inc, -1), ident))
    return p


def main():
    so_stl = "--so-stl" in sys.argv
    DIR_STEP.mkdir(exist_ok=True)
    DIR_STL.mkdir(exist_ok=True)
    for nome, solido, orienta in pecas():
        assert solido.val().isValid(), nome
        if not so_stl:
            cq.exporters.export(solido, str(DIR_STEP / f"{nome}.step"))
        cq.exporters.export(_no_chao(orienta(solido)), str(DIR_STL / f"{nome}.stl"),
                            tolerance=0.02, angularTolerance=0.15)
        _confere_malha(DIR_STL / f"{nome}.stl")
        print("ok", nome)


def _confere_malha(arquivo):
    """Serviços de impressão recusam malha aberta. Avisa se isso acontecer."""
    try:
        import trimesh
    except ImportError:
        return
    if not trimesh.load(arquivo).is_watertight:
        print(f"ATENÇÃO: a malha de {arquivo.name} está aberta. Não mande para impressão sem corrigir.")


if __name__ == "__main__":
    main()
