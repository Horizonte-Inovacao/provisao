# SPDX-FileCopyrightText: 2026 Edson Gabriel Soares da Fonseca, João Luiz Pereira Filho, Nadson Alex da Silva
# SPDX-License-Identifier: CERN-OHL-S-2.0

"""
Monta o pacote do pedido de impressão 3D a partir dos STL já gerados.

    python3 gerar_pecas.py              # primeiro, gere os STL
    python3 gerar_pedido_impressao.py   # depois, monte o pedido

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
    ("A2_case_eletronica_tampa", 1, "Tampa do case da eletrônica", "PETG", 25, "Já virada: face de fora na mesa"),
    ("A3_case_eletronica_base_curva", 1, "Base curva do case da eletrônica", "PETG", 15, "Face plana na mesa"),
    ("A4_case_eletronica_placa_interna", 1, "Placa interna do case da eletrônica", "PETG", 25, "Placa fina (1,6 mm)"),
    ("B1_case_bateria_corpo", 1, "Case da bateria", "PETG", 25, "Em pé, com brim de 5 mm"),
    ("B2_case_bateria_tampa", 1, "Tampa do case da bateria", "PETG", 25, ""),
    ("B3_case_bateria_placa_interna", 1, "Placa interna do case da bateria", "PETG", 25, "Placa fina (1,6 mm)"),
    ("S1_suporte_sensor_esquerdo_00graus", 1, "Suporte do sensor esquerdo, 0 graus", "PETG", 25, ""),
    ("S1_suporte_sensor_esquerdo_10graus", 1, "Suporte do sensor esquerdo, 10 graus", "PETG", 25, ""),
    ("S1_suporte_sensor_esquerdo_20graus", 1, "Suporte do sensor esquerdo, 20 graus", "PETG", 25, ""),
    ("S1_suporte_sensor_direito_00graus", 1, "Suporte do sensor direito, 0 graus", "PETG", 25, ""),
    ("S1_suporte_sensor_direito_10graus", 1, "Suporte do sensor direito, 10 graus", "PETG", 25, ""),
    ("S1_suporte_sensor_direito_20graus", 1, "Suporte do sensor direito, 20 graus", "PETG", 25, ""),
    ("S2_suporte_sensor_tampa", 2, "Tampinha do suporte do sensor", "PETG", 25, ""),
    ("S3_suporte_sensor_placa_sob_aba", 2, "Plaquinha de baixo da aba (com porcas)", "PETG", 25, "Encaixes das porcas para cima"),
    ("M1_berco_motor", 2, "Berço do motor de vibração", "TPU 95A", 25, "Plástico flexível"),
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
        c.drawRightString(w - 15 * mm, h - 17.5 * mm, "Revisão 2  ·  27/09/2026")
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

    S.append(Paragraph("Olá! Este é o nosso pedido", h1))
    S.append(Paragraph(
        "Somos a equipe da PróVisão, um boné que avisa pessoas com deficiência visual sobre obstáculos na altura da "
        "cabeça. As peças abaixo prendem a eletrônica no boné. Separamos o pedido em dois lotes: primeiro queremos "
        "conferir os encaixes com poucas peças, e depois imprimir o kit completo. Todas as peças foram desenhadas "
        "para imprimir sem suporte.", base))
    S.append(Spacer(1, 6))
    campo = "_" * 58
    S.append(tabela_kv([
        ("Quem está pedindo", campo),
        ("Contato (telefone ou e-mail)", campo),
        ("Serviço de impressão", campo),
        ("Prazo que precisamos", campo),
        ("Cor do PETG", "____________________  (sugerimos preto ou petróleo, #1B6C79)"),
        ("Lote pedido",
         f"[   ]  Lote 1: teste de encaixe ({tot['lote1'][0]} peças, cerca de {tot['lote1'][1]:.0f} g)<br/>"
         f"[   ]  Lote 2: kit completo de um boné ({tot['qtd'][0]} peças, cerca de {tot['qtd'][1]:.0f} g)"),
    ]))
    S.append(Spacer(1, 8))
    S.append(Paragraph("Como queremos as peças", h1))
    S.append(tabela_kv([
        ("Material", "<b>PETG</b> em quase tudo. Não usamos PLA porque a peça vai na cabeça, ao sol, e o PLA amolece com o calor. "
                     "<b>TPU 95A</b> (plástico flexível) só no berço do motor, que encosta na nuca."),
        ("Bico e altura de camada", "0,4 mm e 0,2 mm"),
        ("Paredes", "<b>4 paredes</b>. É o que segura os parafusos de 2 mm e aguenta pancada."),
        ("Topo e fundo", "5 camadas em cima e 4 embaixo"),
        ("Preenchimento", "25% em padrão giroide. A base curva (A3) pode ser com 15%."),
        ("Suporte", "<b>Nenhum.</b> Desenhamos todas as peças para imprimir sem suporte."),
        ("Posição na mesa", "<b>Por favor, use a posição do arquivo.</b> Todas as peças já estão apoiadas do jeito certo. "
                            "Não gire, principalmente a B1 (imprime em pé) e a A2 (imprime virada)."),
        ("Adesão", "Borda de adesão (brim) de 5 mm só na <b>B1</b>, que é alta e estreita."),
        ("Escala", "100%, em milímetros. Os arquivos 3MF já informam a unidade."),
        ("Furos", "Por favor, não aplique compensação de furo. Os furos de 1,7 mm recebem parafuso de 2 mm direto no "
                  "plástico. Se a impressora de vocês costuma fechar furos pequenos, avisem antes de imprimir."),
    ]))
    S.append(Spacer(1, 8))
    S.append(Paragraph("O que vai no pacote", h1))
    S.append(Paragraph(
        "<font face='Courier' size='8'>"
        "ficha-do-pedido.pdf<br/>"
        "lote-1-teste-de-encaixe/  lote1_petg.3mf  lote1_tpu.3mf  stl/<br/>"
        "lote-2-kit-completo/      kit_petg.3mf    kit_tpu.3mf    stl/</font>", base))
    S.append(Spacer(1, 4))
    S.append(Paragraph(
        "Separamos os arquivos 3MF por material, com as cópias já distribuídas numa mesa de 235 x 235 mm. "
        "Se preferirem montar a mesa do jeito de vocês, usem os STL da pasta <b>stl</b>: o número depois de "
        "<b>_x</b> no nome do arquivo é a quantidade a imprimir.", base))

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
                Image(str(dir_min / f"{d['nome']}.png"), width=26 * mm, height=19.8 * mm),
                Paragraph(f"<b>{d['nome']}_x{q}.stl</b><br/><font color='#5A6470'>{d['desc']}</font>", peq),
                Paragraph(f"<b>{q}</b>", centro),
                Paragraph(f"{x:.0f} x {y:.0f} x " + (f"{z:.1f}".replace(".", ",") if z < 10 else f"{z:.0f}"), peq),
                Paragraph(d["material"], peq),
                Paragraph(f"{d['massa']:.0f}" if d["massa"] >= 1 else "&lt;1", peq),
                Paragraph(d["obs"] or "-", peq),
            ])
        linhas.append(["", Paragraph("<b>Total</b>", peq), Paragraph(f"<b>{n}</b>", centro), "", "",
                       Paragraph(f"<b>~{g:.0f} g</b>", peq), ""])
        t = Table(linhas, colWidths=[27 * mm, 60 * mm, 10 * mm, 23 * mm, 16 * mm, 14 * mm, W - 150 * mm], repeatRows=1)
        t.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), PET), ("BACKGROUND", (0, -1), (-1, -1), colors.HexColor("#FBEDE8")),
            ("LINEBELOW", (0, 0), (-1, -1), 0.4, LINHA), ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("TOPPADDING", (0, 0), (-1, -1), 2), ("BOTTOMPADDING", (0, 0), (-1, -1), 2)]))
        return t

    S.append(PageBreak())
    S.append(Paragraph("Lote 1: teste de encaixe", h1))
    S.append(Paragraph(
        "É o primeiro pedido. Com essas peças vamos conferir, com os componentes reais na mão, se a placa, o carregador, "
        "a bateria, o sensor e o motor encaixam direito antes de imprimir o conjunto inteiro. As peças curvas que "
        "dependem da medida do boné (bases curvas e placas internas) ficam para o lote 2.", base))
    S.append(Spacer(1, 6))
    S.append(tabela("lote1"))
    S.append(Paragraph("* Peso estimado com a configuração desta ficha. O valor final depende do programa de fatiamento.", peqc))

    S.append(PageBreak())
    S.append(Paragraph("Lote 2: kit completo de um boné", h1))
    S.append(Paragraph(
        "Todas as peças de uma PróVisão. Os suportes dos sensores vão nas três inclinações (0, 10 e 20 graus) porque "
        "vamos escolher a melhor no primeiro teste, com o boné na cabeça.", base))
    S.append(Spacer(1, 6))
    S.append(tabela("qtd"))
    S.append(Paragraph("* Peso estimado com a configuração desta ficha. O valor final depende do programa de fatiamento.", peqc))

    S.append(Spacer(1, 10))
    bloco = [Paragraph("Como vamos conferir na entrega", h1)]
    for txt in [
        "Nenhum resto de plástico dentro dos cases, dos furos e dos recortes (entrada USB-C, chave e entalhes dos cabos).",
        "Furos de 1,7 mm e de 2,3 mm abertos de ponta a ponta onde atravessam a peça.",
        "Base das peças plana, sem empenar. A base curva e o case A precisam assentar um no outro sem balançar.",
        "Camadas bem grudadas, principalmente na B1 (impressa em pé) e nas colunas da tampa A2.",
        "Texto em baixo relevo legível na tampa A2 e as marcas + e - na lateral da B1.",
        "Berços dos motores em TPU, flexíveis e sem fiapos.",
        "Por favor, não lixem, furem ou colem nada sem falar com a gente antes: as folgas foram calculadas para a peça como sai da impressora.",
    ]:
        bloco.append(Paragraph(txt, bul, bulletText="•"))
    bloco.append(Spacer(1, 6))
    bloco.append(Paragraph("Obrigado! Qualquer dúvida sobre as peças, é só chamar a equipe pelo contato acima.", base))
    S.append(KeepTogether(bloco))
    doc.build(S)


# ------------------------------------------------------------------ principal
def main():
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
