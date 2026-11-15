"""Gera o MVP 001 do Precifica Fácil via artifact_tool.

Uso: python gerar_precifica_facil.py [caminho_saida.xlsx]
Dependência: artifact_tool
"""

from __future__ import annotations

import sys
from pathlib import Path

from artifact_tool import SpreadsheetFile, Workbook

OUT = (
    Path(sys.argv[1])
    if len(sys.argv) > 1
    else Path("/mnt/data/Precifica_Facil_MVP_001.xlsx")
)

NAVY = "#10243D"
DEEP = "#0A172A"
BLUE = "#1458A6"
PALE = "#EAF3FF"
YELLOW = "#FFF2BA"
WHITE = "#FFFFFF"
MUTED = "#52647B"
LIGHT = "#F4F7FB"
RED = "#C62828"
GREEN = "#008047"
DARK = "#0A1220"

BRL = '"R$" #,##0.00;[Red]("R$" #,##0.00);-'
PCT = "0.0%;[Red](0.0%);-"

wb = Workbook.create()
intro = wb.worksheets.add("Instruções")
calc = wb.worksheets.add("Precificador")
sim = wb.worksheets.add("Simulador")
examples = wb.worksheets.add("Exemplos")


def put(sheet, addr, value):
    sheet.get_range(addr).values = [[value]]


def formula(sheet, addr, value):
    sheet.get_range(addr).formulas = [[value]]


def banner(sheet, title, subtitle, end="H"):
    sheet.merge_cells(f"A1:{end}2")
    put(sheet, "A1", title)
    sheet.get_range(f"A1:{end}2").format = {
        "fill": NAVY,
        "font": {"bold": True, "color": WHITE, "size": 18},
        "vertical_alignment": "center",
        "row_height": 23,
    }
    sheet.merge_cells(f"A3:{end}3")
    put(sheet, "A3", subtitle)
    sheet.get_range(f"A3:{end}3").format = {
        "fill": "#DCEBFC",
        "font": {"color": NAVY, "size": 10},
        "row_height": 24,
        "vertical_alignment": "center",
    }


def section(sheet, row, label, end="H"):
    sheet.merge_cells(f"A{row}:{end}{row}")
    put(sheet, f"A{row}", label)
    sheet.get_range(f"A{row}:{end}{row}").format = {
        "fill": DEEP,
        "font": {"color": WHITE, "bold": True, "size": 11},
        "row_height": 27,
        "vertical_alignment": "center",
    }


def input_style(sheet, addr, number_format=None):
    rng = sheet.get_range(addr)
    rng.format = {
        "fill": YELLOW,
        "font": {"color": "#0000FF", "bold": True, "size": 11},
        "row_height": 24,
        "vertical_alignment": "center",
    }
    if number_format:
        rng.format.number_format = number_format


def result_style(sheet, addr, number_format=None, prominent=False):
    rng = sheet.get_range(addr)
    rng.format = {
        "fill": PALE if not prominent else "#CCE6FC",
        "font": {
            "color": "#000000",
            "bold": prominent,
            "size": 13 if prominent else 10,
        },
        "row_height": 28 if prominent else 23,
        "vertical_alignment": "center",
    }
    if number_format:
        rng.format.number_format = number_format


def help_note(sheet, addr, text):
    put(sheet, addr, text)
    sheet.get_range(addr).format = {
        "font": {"color": MUTED, "size": 9},
        "wrap_text": True,
        "vertical_alignment": "center",
    }


# Instruções
intro.get_range("A:A").format.column_width = 3
intro.get_range("B:B").format.column_width = 36
intro.get_range("C:C").format.column_width = 18
intro.get_range("D:H").format.column_width = 18
banner(
    intro,
    "PRECIFICA FÁCIL  |  GUIA DE USO",
    "MVP 001 · planilha de apoio à precificação em reais",
)
section(intro, 5, "COMO USAR")
steps = [
    (
        "01",
        "Abra a aba Precificador.",
        "As células amarelas com texto azul são exemplos editáveis.",
    ),
    (
        "02",
        "Preencha os custos por unidade.",
        "Considere aquisição, embalagem, frete e rateio de custos fixos.",
    ),
    (
        "03",
        "Informe as taxas e a margem.",
        "Percentuais sobre o preço de venda; informe suas próprias estimativas.",
    ),
    (
        "04",
        "Confira preço e viabilidade.",
        "O preço sugerido é uma estimativa, não uma garantia de lucro.",
    ),
    (
        "05",
        "Abra o Simulador.",
        "Teste descontos e observe como o lucro e a margem mudam.",
    ),
]
for i, (n, title, detail) in enumerate(steps, 7):
    put(intro, f"B{i}", f"{n}  {title}")
    intro.merge_cells(f"C{i}:H{i}")
    put(intro, f"C{i}", detail)
    intro.get_range(f"B{i}").format.font.bold = True
    intro.get_range(f"C{i}:H{i}").format.wrap_text = True
    intro.get_range(f"B{i}:H{i}").format.row_height = 31
section(intro, 14, "ENTENDA O CÁLCULO")
intro.merge_cells("B16:H16")
put(
    intro,
    "B16",
    "Preço sugerido = custos em R$ ÷ (1 − tributos % − taxas % − margem desejada %)",
)
intro.get_range("B16:H16").format = {
    "fill": PALE,
    "font": {"bold": True, "color": NAVY},
    "row_height": 30,
}
intro.merge_cells("B18:H19")
put(
    intro,
    "B18",
    "Margem é lucro ÷ preço de venda. Markup é acréscimo sobre o custo. Não são equivalentes. A fórmula assume taxas percentuais sobre o preço cobrado ao cliente e quantidades/custos por unidade.",
)
intro.get_range("B18:H19").format.wrap_text = True
intro.get_range("B18:H19").format.row_height = 24
section(intro, 22, "ATENÇÃO ANTES DE USAR EM UM NEGÓCIO")
notes = [
    "Os valores preenchidos são apenas exemplos didáticos; substitua todos pelos seus dados.",
    "Tributos, enquadramento, fretes e repasses variam. Esta planilha não calcula impostos automaticamente.",
    "O rateio de custo fixo é informado pelo usuário; não é estimado pela planilha.",
    "Não inclui perdas, devoluções, capital de giro nem sazonalidade, salvo quando refletidos nos custos informados.",
    "A simulação usa a mesma estrutura de custos e taxas e recalcula taxas sobre o valor efetivamente cobrado.",
    "É um instrumento de apoio. Revise resultados e consulte um profissional quando necessário.",
]
for row, note in enumerate(notes, 24):
    intro.merge_cells(f"B{row}:H{row}")
    put(intro, f"B{row}", "• " + note)
    intro.get_range(f"B{row}:H{row}").format.wrap_text = True
    intro.get_range(f"B{row}:H{row}").format.row_height = 35
intro.merge_cells("B32:H32")
put(
    intro,
    "B32",
    "LEGENDA    Amarelo / azul = editar     |     Azul-claro / preto = cálculo     |     Verde = referência a outra aba",
)
intro.get_range("B32:H32").format = {
    "fill": LIGHT,
    "font": {"color": NAVY, "size": 10},
    "row_height": 30,
}

# Precificador
calc.get_range("A:A").format.column_width = 3
calc.get_range("B:B").format.column_width = 27
calc.get_range("C:D").format.column_width = 13
calc.get_range("E:E").format.column_width = 24
calc.get_range("F:F").format.column_width = 3
calc.get_range("G:G").format.column_width = 29
calc.get_range("H:H").format.column_width = 18
banner(
    calc,
    "PRECIFICA FÁCIL  |  PRECIFICADOR",
    "Altere apenas as entradas amarelas. Os valores atuais são exemplos didáticos.",
)
section(calc, 5, "ENTRADAS · TODOS OS VALORES POR UNIDADE")
inputs = [
    (6, "Nome do produto", "Camiseta básica", "Exemplo ilustrativo", None),
    (7, "Compra / produção (R$)", 45, "Custo direto unitário", BRL),
    (8, "Embalagem e variáveis (R$)", 2.5, "Outros custos por unidade", BRL),
    (9, "Frete absorvido (R$)", 0, "Não inclua frete pago pelo cliente", BRL),
    (10, "Custo fixo rateado (R$)", 5, "Informe seu próprio rateio", BRL),
    (11, "Tarifa fixa por venda (R$)", 0.5, "Taxa por operação, se aplicável", BRL),
    (12, "Tributos estimados (%)", 0.06, "Sobre a venda; informado pelo usuário", PCT),
    (
        13,
        "Taxa percentual de venda (%)",
        0.045,
        "Cartão/marketplace, se aplicável",
        PCT,
    ),
    (14, "Margem de lucro desejada (%)", 0.25, "Margem sobre o preço final", PCT),
]
for row, label, val, note, fmt in inputs:
    calc.merge_cells(f"B{row}:D{row}")
    put(calc, f"B{row}", label)
    put(calc, f"E{row}", val)
    input_style(calc, f"E{row}", fmt)
    calc.merge_cells(f"G{row}:H{row}")
    help_note(calc, f"G{row}", note)
    calc.get_range(f"G{row}:H{row}").format.row_height = 25
section(calc, 17, "RESULTADOS DA PRECIFICAÇÃO")
outputs = [
    (19, "Custos base (R$)", "=SUM(E7:E11)", BRL, False),
    (20, "Tributos + taxas (%)", "=SUM(E12:E13)", PCT, False),
    (21, "Taxas + margem-alvo (%)", "=SUM(E12:E14)", PCT, False),
    (
        22,
        "PREÇO SUGERIDO (R$)",
        '=IF(OR(COUNT(E7:E14)<8,E7<=0,MIN(E8:E14)<0,MAX(E12:E14)>=1,E21>=1),"",ROUNDUP(E19/(1-E21),2))',
        BRL,
        True,
    ),
    (
        23,
        "Tributos + taxas estimados (R$)",
        '=IF(E22="","",ROUND(E22*E20+E11,2))',
        BRL,
        False,
    ),
    (
        24,
        "Lucro estimado por unidade (R$)",
        '=IF(E22="","",ROUND(E22-SUM(E7:E10)-E23,2))',
        BRL,
        False,
    ),
    (25, "Margem efetiva estimada (%)", '=IF(OR(E22="",E22=0),"",E24/E22)', PCT, True),
    (
        26,
        "Markup sobre custos base (%)",
        '=IF(OR(E22="",E19<=0),"",E22/E19-1)',
        PCT,
        False,
    ),
    (
        27,
        "DIAGNÓSTICO",
        '=IF(COUNT(E7:E14)<8,"PREENCHA TODOS OS NÚMEROS",IF(E7<=0,"CUSTO DE AQUISIÇÃO INVÁLIDO",IF(MIN(E8:E14)<0,"ENTRADA NEGATIVA",IF(MAX(E12:E14)>=1,"PERCENTUAL INVÁLIDO",IF(E21>=1,"SOMA DAS TAXAS E MARGEM ≥ 100%","CÁLCULO DISPONÍVEL")))))',
        None,
        True,
    ),
]
for row, label, form, fmt, prominent in outputs:
    calc.merge_cells(f"B{row}:D{row}")
    put(calc, f"B{row}", label)
    formula(calc, f"E{row}", form)
    result_style(calc, f"E{row}", fmt, prominent)
    calc.get_range(f"B{row}:D{row}").format.row_height = 26
calc.merge_cells("B30:H31")
put(
    calc,
    "B30",
    "Premissas: preços em R$, percentual sobre receita bruta, sem arredondamentos intermediários além das taxas/resultados. Valores de exemplo não são recomendações fiscais.",
)
calc.get_range("B30:H31").format = {
    "fill": LIGHT,
    "font": {"color": MUTED},
    "wrap_text": True,
    "row_height": 25,
}
calc.get_range("E24").conditional_formats.add_cell_is(
    {"operator": "lessThan", "formula": 0, "format": {"font": {"color": RED}}}
)

# Simulador
sim.get_range("A:A").format.column_width = 16
sim.get_range("B:B").format.column_width = 23
sim.get_range("C:C").format.column_width = 24
sim.get_range("D:D").format.column_width = 23
sim.get_range("E:E").format.column_width = 24
sim.get_range("F:F").format.column_width = 16
sim.get_range("G:G").format.column_width = 25
sim.get_range("H:H").format.column_width = 11
banner(
    sim,
    "PRECIFICA FÁCIL  |  SIMULADOR",
    "Simule descontos sobre o preço de tabela e acompanhe o lucro líquido estimado.",
)
section(sim, 5, "DESCONTO PERSONALIZADO")
sim_labels = {
    6: "Preço sugerido (R$)",
    7: "Desconto desejado (%)",
    8: "Preço cobrado (R$)",
    9: "Custos operacionais (R$)",
    10: "Tarifa fixa por venda (R$)",
    11: "Tributos + taxas (%)",
    12: "Custos percentuais + tarifa (R$)",
    13: "LUCRO POR UNIDADE (R$)",
    14: "MARGEM EFETIVA (%)",
    15: "STATUS DO DESCONTO",
    16: "Desconto máximo teórico sem prejuízo (%)",
}
for row, label in sim_labels.items():
    sim.merge_cells(f"B{row}:D{row}")
    put(sim, f"B{row}", label)
    sim.get_range(f"B{row}:D{row}").format.row_height = 26
formula(sim, "E6", "=IF('Precificador'!E22=\"\",\"\",'Precificador'!E22)")
put(sim, "E7", 0.10)
formula(sim, "E8", '=IF(OR(E6="",E7<0,E7>=1),"",ROUND(E6*(1-E7),2))')
formula(sim, "E9", "=SUM('Precificador'!E7:E10)")
formula(sim, "E10", "='Precificador'!E11")
formula(sim, "E11", "=SUM('Precificador'!E12:E13)")
formula(sim, "E12", '=IF(E8="","",ROUND(E8*E11+E10,2))')
formula(sim, "E13", '=IF(E8="","",ROUND(E8-E9-E12,2))')
formula(sim, "E14", '=IF(OR(E8="",E8=0),"",E13/E8)')
formula(
    sim,
    "E15",
    '=IF(E8="","REVISE O DESCONTO",IF(E13<0,"PREJUÍZO",IF(E13=0,"EQUILÍBRIO","LUCRO ESTIMADO")))',
)
formula(sim, "E16", '=IF(OR(E6="",E11>=1),"",MAX(0,1-(E9+E10)/(E6*(1-E11))))')
for row in [6, 9, 10, 11]:
    sim.get_range(f"E{row}").format = {
        "fill": "#E8F6ED",
        "font": {"color": "#008000"},
        "row_height": 25,
    }
for row in [8, 12, 13, 14, 15, 16]:
    result_style(
        sim,
        f"E{row}",
        PCT if row in [14, 16] else None if row == 15 else BRL,
        row in [13, 14, 15],
    )
for row in [6, 9, 10, 11]:
    sim.get_range(f"E{row}").format.number_format = PCT if row == 11 else BRL
input_style(sim, "E7", PCT)
section(sim, 19, "CENÁRIOS AUTOMÁTICOS DE DESCONTO")
headers = [
    "Desconto",
    "Preço cobrado",
    "Tributos/taxas (R$)",
    "Custos (R$)",
    "Lucro (R$)",
    "Margem (%)",
    "Situação",
]
sim.get_range("A20:G20").values = [headers]
sim.get_range("A20:G20").format = {
    "fill": BLUE,
    "font": {"bold": True, "color": WHITE},
    "row_height": 37,
    "wrap_text": True,
}
for idx, row in enumerate(range(21, 28)):
    put(sim, f"A{row}", idx * 0.05)
    formula(sim, f"B{row}", f'=IF($E$6="","",ROUND($E$6*(1-A{row}),2))')
    formula(sim, f"C{row}", f'=IF(B{row}="","",ROUND(B{row}*$E$11+$E$10,2))')
    formula(sim, f"D{row}", f'=IF(B{row}="","",$E$9)')
    formula(sim, f"E{row}", f'=IF(B{row}="","",ROUND(B{row}-C{row}-D{row},2))')
    formula(sim, f"F{row}", f'=IF(OR(B{row}="",B{row}=0),"",E{row}/B{row})')
    formula(
        sim,
        f"G{row}",
        f'=IF(B{row}="","",IF(E{row}<0,"PREJUÍZO",IF(E{row}=0,"EQUILÍBRIO","LUCRO")))',
    )
    sim.get_range(f"A{row}").format.number_format = PCT
    sim.get_range(f"B{row}:E{row}").format.number_format = BRL
    sim.get_range(f"F{row}").format.number_format = PCT
    sim.get_range(f"A{row}:G{row}").format.row_height = 25
    if idx % 2 == 1:
        sim.get_range(f"A{row}:G{row}").format.fill = LIGHT
sim.get_range("E21:E27").conditional_formats.add_cell_is(
    {
        "operator": "lessThan",
        "formula": 0,
        "format": {"font": {"color": RED}, "fill": "#FFEEEE"},
    }
)
sim.merge_cells("A30:G31")
put(
    sim,
    "A30",
    "Ao conceder desconto, as taxas percentuais incidem sobre o preço efetivamente cobrado. O desconto máximo é teórico; revise custos, impostos e política comercial.",
)
sim.get_range("A30:G31").format = {
    "fill": LIGHT,
    "wrap_text": True,
    "font": {"color": MUTED},
    "row_height": 26,
}

# Exemplos
examples.get_range("A:A").format.column_width = 3
examples.get_range("B:B").format.column_width = 28
examples.get_range("C:F").format.column_width = 15
examples.get_range("G:I").format.column_width = 15
examples.get_range("J:M").format.column_width = 18
examples.get_range("N:N").format.column_width = 17
banner(
    examples,
    "PRECIFICA FÁCIL  |  EXEMPLOS",
    "Exemplos completamente fictícios · fórmulas por linha, não são recomendações de preço.",
    end="N",
)
section(examples, 5, "CENÁRIOS DE REFERÊNCIA", end="N")
headers = [
    "Produto",
    "Custo (R$)",
    "Var. (R$)",
    "Fixos (R$)",
    "Tarifa (R$)",
    "Tributos (%)",
    "Taxa (%)",
    "Margem desejada (%)",
    "Custo base (R$)",
    "Soma taxas+margem (%)",
    "Preço sugerido (R$)",
    "Lucro estimado (R$)",
    "Margem efetiva (%)",
]
examples.get_range("B7:N7").values = [headers]
examples.get_range("B7:N7").format = {
    "fill": BLUE,
    "font": {"bold": True, "color": WHITE, "size": 9},
    "wrap_text": True,
    "row_height": 42,
}
examples_data = [
    ["Camiseta básica", 45, 2.5, 5, 0.5, 0.06, 0.045, 0.25],
    ["Caneca personalizada", 16, 3, 2, 0.3, 0.06, 0.035, 0.30],
    ["Lanche artesanal", 12, 4, 3, 0.4, 0.08, 0.055, 0.20],
]
for ix, data in enumerate(examples_data, 8):
    examples.get_range(f"B{ix}:I{ix}").values = [data]
    formula(examples, f"J{ix}", f"=SUM(C{ix}:F{ix})")
    formula(examples, f"K{ix}", f"=SUM(G{ix}:I{ix})")
    formula(
        examples,
        f"L{ix}",
        f'=IF(OR(C{ix}<=0,MIN(D{ix}:I{ix})<0,K{ix}>=1),"",ROUNDUP(J{ix}/(1-K{ix}),2))',
    )
    formula(
        examples,
        f"M{ix}",
        f'=IF(L{ix}="","",ROUND(L{ix}-SUM(C{ix}:E{ix})-F{ix}-ROUND(L{ix}*(G{ix}+H{ix}),2),2))',
    )
    formula(examples, f"N{ix}", f'=IF(OR(L{ix}="",L{ix}=0),"",M{ix}/L{ix})')
    examples.get_range(f"C{ix}:F{ix}").format.number_format = BRL
    examples.get_range(f"G{ix}:I{ix}").format.number_format = PCT
    examples.get_range(f"J{ix}").format.number_format = BRL
    examples.get_range(f"K{ix}").format.number_format = PCT
    examples.get_range(f"L{ix}:M{ix}").format.number_format = BRL
    examples.get_range(f"N{ix}").format.number_format = PCT
    examples.get_range(f"C{ix}:I{ix}").format.font.color = "#0000FF"
    examples.get_range(f"J{ix}:N{ix}").format.font.color = "#000000"
    if ix % 2 == 0:
        examples.get_range(f"B{ix}:N{ix}").format.fill = LIGHT
    examples.get_range(f"B{ix}:N{ix}").format.row_height = 29
section(examples, 13, "NOTAS DOS EXEMPLOS", end="N")
examples.merge_cells("B15:N16")
put(
    examples,
    "B15",
    "Os três cenários são fictícios e servem para demonstrar a fórmula. Não significam que esses preços, impostos ou margens sejam adequados para sua empresa.",
)
examples.get_range("B15:N16").format = {
    "wrap_text": True,
    "fill": LIGHT,
    "font": {"color": MUTED},
    "row_height": 27,
}

# Legibility common
for sheet in [intro, calc, sim, examples]:
    sheet.freeze_panes.freeze_rows(3)

OUT.parent.mkdir(parents=True, exist_ok=True)
SpreadsheetFile.export_xlsx(wb).save(str(OUT))
print("Arquivo gerado:", OUT)
print("Abas:", "Instruções, Precificador, Simulador, Exemplos")

# Verify workbook directly before reporting success
for region in ["Precificador!B19:E27", "Simulador!D6:E16", "Exemplos!J7:N10"]:
    check = wb.inspect(
        {
            "kind": "table",
            "range": region,
            "include": "values,formulas",
            "table_max_rows": 30,
            "table_max_cols": 14,
        }
    )
    print("CHECK", region, check.ndjson[:1700])
error_report = wb.inspect(
    {
        "kind": "match",
        "search_term": "#REF!|#DIV/0!|#VALUE!|#NAME\\?|#N/A",
        "options": {"use_regex": True, "max_results": 50},
        "summary": "formula errors",
    }
)
print("ERROR_SCAN", error_report.ndjson[:1000])
