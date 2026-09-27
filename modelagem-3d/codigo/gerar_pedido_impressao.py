# SPDX-FileCopyrightText: 2026 Edson Gabriel Soares da Fonseca, João Luiz Pereira Filho, Nadson Alex da Silva
# SPDX-License-Identifier: CERN-OHL-S-2.0

"""
Monta o pacote do pedido de impressão 3D a partir dos STL já gerados.

    python3 gerar_pecas.py                          # primeiro, gere os STL
    python3 gerar_pedido_impressao.py               # depois, monte o pedido
    python3 gerar_pedido_impressao.py --so-ficha    # refaz só a ficha em PDF

Saída em ../pedido-de-impressao/:
  ficha-do-pedido.pdf                  ficha para o serviço de impressão
  lote-1-teste-de-encaixe/             poucas peças, para conferir os encaixes
  lote-2-kit-completo/                 todas as peças de um boné
Cada lote tem os STL (com a quantidade no nome) e arquivos 3MF com as peças
já distribuídas na mesa: um para PETG e um para TPU.

Precisa de: trimesh, vtk (vem com o cadquery) e reportlab.
"""
import math
import shutil
import sys
import tempfile
from pathlib import Path

import trimesh
import vtk
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import (BaseDocTemplate, Frame, Image, KeepTogether, PageBreak, PageTemplate,
                                Paragraph, Spacer, Table, TableStyle)

AQUI = Path(__file__).resolve().parent
STL = AQUI.parent / "arquivos-stl"
SAIDA = AQUI.parent / "pedido-de-impressao"

# nome do arquivo, quantidade no kit, descrição, material, preenchimento (%), observação
KIT = [
    ("A1_case_eletronica_corpo", 1, "Case da eletrônica", "PETG", 25, ""),
    ("A2_case_eletronica_tampa", 1, "Tampa do case da eletrônica", "PETG", 25, "Face externa apoiada na mesa"),
    ("A3_case_eletronica_base_curva", 1, "Base curva do case da eletrônica", "PETG", 15, "Face plana na mesa"),
    ("A4_case_eletronica_placa_interna", 1, "Placa interna do case da eletrônica", "PETG", 25, "Placa fina (1,6 mm)"),
    ("B1_case_bateria_corpo", 1, "Case da bateria", "PETG", 25, "Na vertical, com brim de 5 mm"),
    ("B2_case_bateria_tampa", 1, "Tampa do case da bateria", "PETG", 25, ""),
    ("B3_case_bateria_placa_interna", 1, "Placa interna do case da bateria", "PETG", 25, "Placa fina (1,6 mm)"),
    ("S1_suporte_sensor_esquerdo_00graus", 1, "Suporte do sensor esquerdo, 0 graus", "PETG", 25, ""),
    ("S1_suporte_sensor_esquerdo_10graus", 1, "Suporte do sensor esquerdo, 10 graus", "PETG", 25, ""),
    ("S1_suporte_sensor_esquerdo_20graus", 1, "Suporte do sensor esquerdo, 20 graus", "PETG", 25, ""),
    ("S1_suporte_sensor_direito_00graus", 1, "Suporte do sensor direito, 0 graus", "PETG", 25, ""),
    ("S1_suporte_sensor_direito_10graus", 1, "Suporte do sensor direito, 10 graus", "PETG", 25, ""),
    ("S1_suporte_sensor_direito_20graus", 1, "Suporte do sensor direito, 20 graus", "PETG", 25, ""),
    ("S2_suporte_sensor_tampa", 2, "Tampa do suporte do sensor", "PETG", 25, ""),
    ("S3_suporte_sensor_placa_sob_aba", 2, "Placa inferior da aba (alojamento das porcas)", "PETG", 25, "Alojamentos das porcas voltados para cima"),
    ("M1_berco_motor", 2, "Berço do motor de vibração", "TPU 95A", 25, "Material flexível"),
]
LOTE1 = {"A1_case_eletronica_corpo": 1, "A2_case_eletronica_tampa": 1, "B1_case_bateria_corpo": 1,
         "B2_case_bateria_tampa": 1, "S1_suporte_sensor_direito_10graus": 1, "S2_suporte_sensor_tampa": 1,
         "S3_suporte_sensor_placa_sob_aba": 1, "M1_berco_motor": 1}
DENSIDADE = {"PETG": 1.27, "TPU 95A": 1.21}

PET = colors.HexColor("#1B6C79")
CORAL = colors.HexColor("#E07A5F")
CINZA = colors.HexColor("#5A6470")
CLARO = colors.HexColor("#EEF4F5")
LINHA = colors.HexColor("#C9D6D9")


# ------------------------------------------------------------------ cálculos e miniaturas
def massa(m, material, preenchimento):
    """Estimativa: paredes e topo cheios, o miolo com o preenchimento escolhido."""
    v = m.volume / 1000
    casca = min(v, m.area / 100 * 0.12)
    return DENSIDADE[material] * (casca + preenchimento / 100 * (v - casca))


def miniatura(arquivo, png, cor=(0.106, 0.424, 0.475)):
    r = vtk.vtkSTLReader()
    r.SetFileName(str(arquivo))
    n = vtk.vtkPolyDataNormals()
    n.SetInputConnection(r.GetOutputPort())
    n.SetFeatureAngle(35)
    mp = vtk.vtkPolyDataMapper()
    mp.SetInputConnection(n.GetOutputPort())
    a = vtk.vtkActor()
    a.SetMapper(mp)
    a.GetProperty().SetColor(*cor)
    a.GetProperty().SetSpecular(0.25)
    a.GetProperty().SetAmbient(0.2)
    ren = vtk.vtkRenderer()
    ren.SetBackground(1, 1, 1)
    ren.AddActor(a)
    w = vtk.vtkRenderWindow()
    w.SetOffScreenRendering(1)
    w.SetSize(420, 320)
    w.AddRenderer(ren)
    ren.ResetCamera()
    cam = ren.GetActiveCamera()
    fx, fy, fz = cam.GetFocalPoint()
    az, el = math.radians(-55), math.radians(35)
    cam.SetPosition(fx + 500 * math.cos(el) * math.cos(az), fy + 500 * math.cos(el) * math.sin(az),
                    fz + 500 * math.sin(el))
    cam.SetViewUp(0, 0, 1)
    cam.SetViewAngle(20)
    ren.ResetCamera()
    cam.Zoom(1.15)
    w.Render()
    i = vtk.vtkWindowToImageFilter()
    i.SetInput(w)
    i.Update()
    wr = vtk.vtkPNGWriter()
    wr.SetFileName(str(png))
    wr.SetInputConnection(i.GetOutputPort())
    wr.Write()


def monta_3mf(itens, destino, largura=230):
    """Distribui as cópias em linhas, com 8 mm entre peças."""
    cena = trimesh.Scene()
    x = y = linha_h = 0.0
    for nome, qtd in itens:
        m0 = trimesh.load(STL / f"{nome}.stl")
        for k in range(qtd):
            m = m0.copy()
            m.apply_translation(-m.bounds[0])
            w, d = m.extents[0], m.extents[1]
            if x + w > largura and x > 0:
                x, y, linha_h = 0.0, y + linha_h + 8, 0.0
            m.apply_translation([x, y, 0])
            cena.add_geometry(m, node_name=f"{nome}_{k + 1}", geom_name=f"{nome}_{k + 1}")
            x += w + 8
            linha_h = max(linha_h, d)
    cena.export(destino)


# ------------------------------------------------------------------ ficha em PDF
def ficha(dados, destino, dir_min):
    base = ParagraphStyle("base", fontName="Helvetica", fontSize=9, leading=12.5, textColor=colors.HexColor("#1E2A30"))
    peq = ParagraphStyle("peq", parent=base, fontSize=7.8, leading=10)
    peqc = ParagraphStyle("peqc", parent=peq, textColor=CINZA)
    h1 = ParagraphStyle("h1", parent=base, fontName="Helvetica-Bold", fontSize=13, leading=17, textColor=PET,
                        spaceBefore=6, spaceAfter=6)
    bul = ParagraphStyle("bul", parent=base, leftIndent=10, spaceAfter=2)
    celb = ParagraphStyle("celb", parent=peq, fontName="Helvetica-Bold")
    cab = ParagraphStyle("cab", parent=peq, fontName="Helvetica-Bold", textColor=colors.white)
    centro = ParagraphStyle("c", parent=peq, alignment=1, fontSize=10)

    def moldura(c, doc):
        c.saveState()
        w, h = A4
        c.setFillColor(PET)
        c.rect(0, h - 22 * mm, w, 22 * mm, stroke=0, fill=1)
        c.setFillColor(colors.white)
        c.setFont("Helvetica-Bold", 15)
        c.drawString(15 * mm, h - 12 * mm, "PróVisão V1.5")
        c.setFont("Helvetica", 10)
        c.drawString(15 * mm, h - 17.5 * mm, "Pedido de impressão 3D  ·  peças do boné")
        c.setFont("Helvetica", 8.5)
        c.drawRightString(w - 15 * mm, h - 12 * mm, "Horizonte Inovação Assistiva")
        c.drawRightString(w - 15 * mm, h - 17.5 * mm, "Revisão 3  ·  27/09/2026")
        c.setFillColor(CORAL)
        c.rect(0, h - 23.2 * mm, w, 1.2 * mm, stroke=0, fill=1)
        c.setFillColor(CINZA)
        c.setFont("Helvetica", 7.5)
        c.drawString(15 * mm, 10 * mm, "Arquivos gerados a partir da modelagem do repositório (modelagem-3d). Medidas em milímetros.")
        c.drawRightString(w - 15 * mm, 10 * mm, f"Página {doc.page}")
        c.restoreState()

    doc = BaseDocTemplate(str(destino), pagesize=A4, leftMargin=15 * mm, rightMargin=15 * mm,
                          topMargin=30 * mm, bottomMargin=17 * mm,
                          title="PróVisão V1.5 - Pedido de impressão 3D", author="Horizonte Inovação Assistiva")
    doc.addPageTemplates([PageTemplate(id="p", frames=[Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height)],
                                       onPage=moldura)])
    W = doc.width
    S = []

    def tabela_kv(linhas, col1=52 * mm):
        t = Table([[Paragraph(k, celb), Paragraph(v, peq)] for k, v in linhas], colWidths=[col1, W - col1])
        t.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (0, -1), CLARO), ("GRID", (0, 0), (-1, -1), 0.5, LINHA),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("TOPPADDING", (0, 0), (-1, -1), 4), ("BOTTOMPADDING", (0, 0), (-1, -1), 4)]))
        return t

    tot = {k: (sum(d[k] for d in dados), sum(d[k] * d["massa"] for d in dados)) for k in ("lote1", "qtd")}

    S.append(Paragraph("1. Objeto do pedido", h1))
    S.append(Paragraph(
        "Impressão 3D das peças estruturais da PróVisão V1.5, dispositivo assistivo em formato de boné que alerta "
        "pessoas com deficiência visual sobre obstáculos na altura da cabeça. As peças fixam os componentes "
        "eletrônicos ao boné. O pedido divide-se em dois lotes: o Lote 1 destina-se à verificação dos encaixes e o "
        "Lote 2 corresponde ao conjunto completo de uma unidade. Todas as peças foram projetadas para impressão sem "
        "estruturas de suporte.", base))
    S.append(Spacer(1, 6))
    campo = "_" * 58
    S.append(tabela_kv([
        ("Solicitante", campo),
        ("Contato (telefone ou e-mail)", campo),
        ("Prestador do serviço", campo),
        ("Prazo de entrega", campo),
        ("Cor do PETG", "____________________  (preferência: preto ou petróleo, #1B6C79)"),
        ("Lote solicitado",
         f"[   ]  Lote 1: verificação de encaixe ({tot['lote1'][0]} peças, aprox. {tot['lote1'][1]:.0f} g)<br/>"
         f"[   ]  Lote 2: conjunto completo de uma unidade ({tot['qtd'][0]} peças, aprox. {tot['qtd'][1]:.0f} g)"),
    ]))
    S.append(Spacer(1, 8))
    S.append(Paragraph("2. Especificações de impressão", h1))
    S.append(tabela_kv([
        ("Material", "<b>PETG</b> nas peças estruturais. O PLA não é aceito, pois as peças ficam expostas ao sol e ao "
                     "calor da cabeça, condição em que o PLA perde rigidez. <b>TPU 95A</b> (material flexível) somente "
                     "no berço do motor (M1), que fica em contato com a nuca."),
        ("Bico e altura de camada", "Bico de 0,4 mm e camada de 0,2 mm."),
        ("Paredes", "<b>4 perímetros</b>, necessários para a fixação dos parafusos M2 e para a resistência a impactos."),
        ("Topo e fundo", "5 camadas superiores e 4 inferiores."),
        ("Preenchimento", "25%, padrão giroide. Na base curva (A3), admite-se 15%."),
        ("Suporte", "<b>Não utilizar.</b> Todas as peças foram projetadas para impressão sem suporte."),
        ("Orientação na mesa", "<b>Manter a orientação dos arquivos fornecidos</b>, que já corresponde à posição de "
                               "impressão. Não rotacionar as peças, em especial a B1 (impressa na vertical) e a A2 "
                               "(impressa invertida)."),
        ("Adesão", "Borda de adesão (brim) de 5 mm somente na <b>B1</b>, devido à altura e à base estreita."),
        ("Escala", "100%, em milímetros. A unidade está definida nos arquivos 3MF."),
        ("Furos", "Não aplicar compensação de furos. Os furos de 1,7 mm recebem parafusos M2 diretamente no plástico. "
                  "Caso o equipamento tenda a reduzir o diâmetro de furos pequenos, o solicitante deve ser consultado "
                  "antes da impressão."),
    ]))
    S.append(Spacer(1, 8))
    S.append(Paragraph("3. Conteúdo do pacote", h1))
    S.append(Paragraph(
        "<font face='Courier' size='8'>"
        "ficha-do-pedido.pdf<br/>"
        "lote-1-teste-de-encaixe/  lote1_petg.3mf  lote1_tpu.3mf  stl/<br/>"
        "lote-2-kit-completo/      kit_petg.3mf    kit_tpu.3mf    stl/</font>", base))
    S.append(Spacer(1, 4))
    S.append(Paragraph(
        "Os arquivos 3MF estão separados por material, com as cópias distribuídas em uma mesa de 235 x 235 mm. "
        "Para montagem própria da mesa, utilizar os arquivos STL da pasta <b>stl</b>. O número após <b>_x</b> no "
        "nome do arquivo indica a quantidade a imprimir.", base))

    def tabela(chave):
        linhas = [[Paragraph(t, cab) for t in ("", "Arquivo e peça", "Qtd", "Medidas (mm)", "Material", "g/un.*", "Observação")]]
        n = g = 0
        for d in dados:
            q = d[chave]
            if not q:
                continue
            n += q
            g += d["massa"] * q
            x, y, z = d["dims"]
            linhas.append([
                Image(str(dir_min / f"{d['nome']}.png"), width=23 * mm, height=17.5 * mm),
                Paragraph(f"<font size='7.2'><b>{d['nome']}_x{q}.stl</b></font><br/><font color='#5A6470'>{d['desc']}</font>", peq),
                Paragraph(f"<b>{q}</b>", centro),
                Paragraph(f"{x:.0f} x {y:.0f} x " + (f"{z:.1f}".replace(".", ",") if z < 10 else f"{z:.0f}"), peq),
                Paragraph(d["material"], peq),
                Paragraph(f"{d['massa']:.0f}" if d["massa"] >= 1 else "&lt;1", peq),
                Paragraph(d["obs"] or "-", peq),
            ])
        linhas.append(["", Paragraph("<b>Total</b>", peq), Paragraph(f"<b>{n}</b>", centro), "", "",
                       Paragraph(f"<b>~{g:.0f} g</b>", peq), ""])
        t = Table(linhas, colWidths=[24 * mm, 63 * mm, 10 * mm, 22 * mm, 16 * mm, 14 * mm, W - 149 * mm], repeatRows=1)
        t.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), PET), ("BACKGROUND", (0, -1), (-1, -1), colors.HexColor("#FBEDE8")),
            ("LINEBELOW", (0, 0), (-1, -1), 0.4, LINHA), ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("TOPPADDING", (0, 0), (-1, -1), 2), ("BOTTOMPADDING", (0, 0), (-1, -1), 2)]))
        return t

    S.append(PageBreak())
    S.append(Paragraph("4. Lote 1: verificação de encaixe", h1))
    S.append(Paragraph(
        "Primeira etapa do pedido. Este lote permite verificar, com os componentes reais, o encaixe da placa, do "
        "carregador, da bateria, do sensor e do motor antes da impressão do conjunto completo. As peças curvas que "
        "dependem das dimensões do boné (base curva e placas internas) constam apenas do Lote 2.", base))
    S.append(Spacer(1, 6))
    S.append(tabela("lote1"))
    S.append(Paragraph("* Massa estimada com os parâmetros desta ficha. O valor final depende do programa de fatiamento.", peqc))

    S.append(PageBreak())
    S.append(Paragraph("5. Lote 2: conjunto completo de uma unidade", h1))
    S.append(Paragraph(
        "Todas as peças de uma unidade da PróVisão. Os suportes dos sensores são fornecidos nas três inclinações "
        "(0, 10 e 20 graus). A inclinação definitiva será escolhida no primeiro teste com o boné em uso.", base))
    S.append(Spacer(1, 6))
    S.append(tabela("qtd"))
    S.append(Paragraph("* Massa estimada com os parâmetros desta ficha. O valor final depende do programa de fatiamento.", peqc))

    S.append(Spacer(1, 10))
    bloco = [Paragraph("6. Critérios de aceitação na entrega", h1)]
    for txt in [
        "Ausência de resíduos de material no interior dos cases, dos furos e dos recortes (entrada USB-C, chave e entalhes dos cabos).",
        "Furos de 1,7 mm e de 2,3 mm desobstruídos em toda a extensão, nos pontos em que atravessam a peça.",
        "Bases planas, sem empenamento. A base curva (A3) e o case da eletrônica (A1) devem assentar um sobre o outro sem folga.",
        "Boa adesão entre camadas, em especial na B1 (impressa na vertical) e nas colunas da tampa A2.",
        "Texto em baixo relevo legível na tampa A2 e marcações + e - legíveis na lateral da B1.",
        "Berços dos motores em TPU flexíveis e sem fiapos.",
        "Nenhuma peça deve ser lixada, furada ou colada sem consulta prévia ao solicitante, pois as folgas foram dimensionadas para a peça no estado em que sai da impressora.",
    ]:
        bloco.append(Paragraph(txt, bul, bulletText="•"))
    bloco.append(Spacer(1, 6))
    bloco.append(Paragraph("Dúvidas técnicas sobre as peças devem ser encaminhadas ao contato indicado na página 1.", base))
    S.append(KeepTogether(bloco))
    doc.build(S)


# ------------------------------------------------------------------ principal
def main():
    so_ficha = "--so-ficha" in sys.argv
    if not so_ficha:
        if SAIDA.exists():
            shutil.rmtree(SAIDA)
        SAIDA.mkdir(parents=True)
    dir_min = Path(tempfile.mkdtemp())
    dados = []
    for nome, qtd, desc, material, preench, obs in KIT:
        m = trimesh.load(STL / f"{nome}.stl")
        assert m.is_watertight, f"malha aberta: {nome}"
        cor = (0.20, 0.55, 0.60) if material.startswith("TPU") else (0.106, 0.424, 0.475)
        miniatura(STL / f"{nome}.stl", dir_min / f"{nome}.png", cor)
        dados.append(dict(nome=nome, qtd=qtd, desc=desc, material=material, obs=obs,
                          dims=[float(v) for v in m.extents], massa=massa(m, material, preench),
                          lote1=LOTE1.get(nome, 0)))

    if so_ficha:
        SAIDA.mkdir(parents=True, exist_ok=True)
        ficha(dados, SAIDA / "ficha-do-pedido.pdf", dir_min)
        print("ok: ficha refeita, arquivos 3MF e STL mantidos")
        return

    for pasta, prefixo, chave in (("lote-1-teste-de-encaixe", "lote1", "lote1"),
                                  ("lote-2-kit-completo", "kit", "qtd")):
        dst = SAIDA / pasta / "stl"
        dst.mkdir(parents=True)
        sel = [(d["nome"], d[chave], d["material"]) for d in dados if d[chave]]
        for nome, q, _ in sel:
            shutil.copy(STL / f"{nome}.stl", dst / f"{nome}_x{q}.stl")
        monta_3mf([(n, q) for n, q, mat in sel if mat == "PETG"], SAIDA / pasta / f"{prefixo}_petg.3mf")
        monta_3mf([(n, q) for n, q, mat in sel if mat != "PETG"], SAIDA / pasta / f"{prefixo}_tpu.3mf")

    ficha(dados, SAIDA / "ficha-do-pedido.pdf", dir_min)
    (SAIDA / "LEIA-ME.md").write_text(
        "# Pedido de impressão 3D\n\n"
        "Este é o pacote que mandamos para o serviço de impressão. Comece pela [`ficha-do-pedido.pdf`](ficha-do-pedido.pdf): "
        "ela explica o material, a configuração e o que vamos conferir na entrega.\n\n"
        "- [`lote-1-teste-de-encaixe/`](lote-1-teste-de-encaixe/): poucas peças, para conferir os encaixes com os componentes reais.\n"
        "- [`lote-2-kit-completo/`](lote-2-kit-completo/): todas as peças de um boné.\n\n"
        "Cada lote tem um arquivo 3MF por material (PETG e TPU), com as peças já distribuídas na mesa, e a pasta `stl` "
        "com uma peça por arquivo. O número depois de `_x` no nome é a quantidade.\n\n"
        "Para refazer este pacote depois de mudar alguma medida, rode `python3 gerar_pecas.py` e depois "
        "`python3 gerar_pedido_impressao.py` na pasta [`codigo/`](../codigo/).\n", encoding="utf-8")
    t1 = sum(d["massa"] * d["lote1"] for d in dados)
    t2 = sum(d["massa"] * d["qtd"] for d in dados)
    print(f"ok: lote 1 com ~{t1:.0f} g, kit completo com ~{t2:.0f} g")


if __name__ == "__main__":
    main()
