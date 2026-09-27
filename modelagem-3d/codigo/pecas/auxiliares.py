"""Funções de apoio compartilhadas pelas peças."""
import math
import cadquery as cq

from . import medidas as P


def caixa_arred(x0, y0, z0, lx, ly, lz, r):
    """Caixa com cantos verticais arredondados, canto mínimo em (x0, y0, z0)."""
    b = cq.Workplane("XY").box(lx, ly, lz, centered=False).translate((x0, y0, z0))
    if r > 0:
        b = b.edges("|Z").fillet(r)
    return b


def cilindro(d, h, pos, eixo="Z"):
    """Cilindro de diâmetro d e comprimento h começando em pos, ao longo do eixo."""
    dirs = {"X": (1, 0, 0), "Y": (0, 1, 0), "Z": (0, 0, 1)}
    s = cq.Solid.makeCylinder(d / 2, h, cq.Vector(*pos), cq.Vector(*dirs[eixo]))
    return cq.Workplane("XY").add(s)


def escareado(pos, d_furo, d_cabeca, prof_total, para_baixo=True):
    """Furo escareado 90 graus. pos = centro da boca do furo na superfície."""
    x, y, z = pos
    sinal = -1 if para_baixo else 1
    furo = cilindro(d_furo, prof_total, (x, y, z - prof_total if para_baixo else z), "Z")
    h_cone = (d_cabeca - d_furo) / 2
    cone = cq.Solid.makeCone(
        d_cabeca / 2, d_furo / 2, h_cone,
        cq.Vector(x, y, z), cq.Vector(0, 0, sinal),
    )
    # pequeno cilindro acima da boca para garantir o corte limpo
    topo = cilindro(d_cabeca, 1.0, (x, y, z if para_baixo else z - 1.0), "Z")
    return furo.union(cq.Workplane("XY").add(cone)).union(topo)


def sag(dx, r=P.R_COPA):
    """Flecha da copa a uma distância horizontal dx do centro da base curva."""
    return r - math.sqrt(r * r - dx * dx)


def base_curva(cx, cy, lx, ly, z_topo, r_canto, t_min=P.BASE_T_MIN, r_copa=P.R_COPA):
    """
    Base curva que assenta na copa do boné.
    Topo plano em z_topo, fundo côncavo (cilindro de raio r_copa com eixo em Y),
    centrada em (cx, cy). Mais fina no centro (t_min), mais grossa nas pontas.
    """
    s_max = sag(lx / 2, r_copa)
    h = t_min + s_max + 1.0
    bloco = caixa_arred(cx - lx / 2, cy - ly / 2, z_topo - h, lx, ly, h, r_canto)
    zc = z_topo - t_min - r_copa
    cil = cq.Solid.makeCylinder(
        r_copa, ly + 20, cq.Vector(cx, cy - ly / 2 - 10, zc), cq.Vector(0, 1, 0)
    )
    return bloco.cut(cq.Workplane("XY").add(cil))


def z_fundo_base(dx, z_topo, t_min=P.BASE_T_MIN, r_copa=P.R_COPA):
    """Cota z do fundo da base curva a uma distância dx do centro."""
    return z_topo - t_min - sag(dx, r_copa)


def placa_interna(furos_xy, lx, ly, r_canto=6.0):
    """
    Placa interna plana (flexiona até a curvatura da copa ao apertar).
    Fica entre o tecido e a cabeça. Face z=0 encosta no tecido,
    escareados na face z=-T (lado da cabeça) para a cabeça do parafuso ficar rente.
    Coordenadas centradas em (0, 0).
    """
    t = P.PLACA_INTERNA_T
    p = caixa_arred(-lx / 2, -ly / 2, -t, lx, ly, t, r_canto)
    # borda toda arredondada: é a parte que fica do lado da cabeça
    p = p.faces(">Z or <Z").edges().fillet(min(0.6, t / 2 - 0.1))
    for (x, y) in furos_xy:
        p = p.cut(escareado((x, y, -t), P.M2_PASSANTE, P.M2_ESCAREADO_D, t + 1, para_baixo=False))
    return p


def ponto_tatil(pos, normal, d=2.4, h=0.9):
    """Pino baixo com topo arredondado, em relevo, para identificação pelo tato."""
    x, y, z = pos
    nx, ny, nz = normal
    base = cq.Vector(x - nx * 0.5, y - ny * 0.5, z - nz * 0.5)  # entra 0.5 na parede
    s = cq.Solid.makeCylinder(d / 2, h + 0.5, base, cq.Vector(*normal))
    w = cq.Workplane("XY").add(s)
    try:
        w = w.faces(cq.selectors.DirectionMinMaxSelector(cq.Vector(*normal), True)).edges().fillet(h * 0.6)
    except Exception:
        pass
    return w


def placa_interna_curvada(furos_xy, lx, ly, r=P.R_COPA, r_canto=6.0):
    """
    Mesma placa interna, já flexionada no raio da copa (forma que ela assume montada).
    Só para a montagem visual. Face de cima (z=0 no centro) encosta no tecido.
    """
    p = casca_curvada(lx, ly, r, r, P.PLACA_INTERNA_T, r_canto)
    for (x, y) in furos_xy:
        p = p.cut(cilindro(P.M2_PASSANTE, 40, (x, y, -30)))
    return p


def almofada_curvada(lx, ly, r=P.R_COPA, r_canto=6.0):
    """Almofada de EVA colada embaixo da placa interna (lado da cabeça). Só para a montagem."""
    return casca_curvada(lx, ly, r, r - P.PLACA_INTERNA_T, P.ESPUMA_PLACA_T, r_canto)


def casca_curvada(lx, ly, r_centro, r_ext, esp, r_canto):
    """Lâmina curva de espessura esp, com raio externo r_ext e centro em z = -r_centro."""
    casca = (cq.Workplane("XZ").circle(r_ext).circle(r_ext - esp).extrude(ly / 2 + 5, both=True)
             .translate((0, 0, -r_centro)))
    pegada = caixa_arred(-lx / 2, -ly / 2, -40, lx, ly, 60, r_canto)
    return casca.intersect(pegada)
