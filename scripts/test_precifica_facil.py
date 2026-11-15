"""Smoke test da planilha Precifica Fácil."""
from math import isclose
from pathlib import Path
from xml.etree import ElementTree as ET
from zipfile import ZipFile

PATH = Path(
    "products/precifica-facil/"
    "Precifica_Facil_v1_0.xlsx"
)

NS = {
    "x": (
        "http://schemas.openxmlformats.org/"
        "spreadsheetml/2006/main"
    )
}


def read_cell(sheet, address):
    cell = sheet.find(
        f".//x:c[@r='{address}']", NS
    )
    assert cell is not None, address

    value = cell.find("x:v", NS)
    formula = cell.find("x:f", NS)

    return (
        value.text if value is not None else None,
        formula.text if formula is not None else None,
    )


with ZipFile(PATH) as workbook:
    assert workbook.testzip() is None

    files = set(workbook.namelist())

    assert not any(
        "vbaProject" in name
        or "externalLinks/" in name
        for name in files
    )

    root = ET.fromstring(
        workbook.read("xl/workbook.xml")
    )

    sheets = [
        item.attrib["name"]
        for item in root.findall(
            "x:sheets/x:sheet", NS
        )
    ]

    assert sheets == [
        "Instruções",
        "Precificador",
        "Simulador",
        "Exemplos",
    ]

    calc = ET.fromstring(
        workbook.read("xl/worksheets/sheet2.xml")
    )
    sim = ET.fromstring(
        workbook.read("xl/worksheets/sheet3.xml")
    )

    expectations = [
        (calc, "E19", 53.00),
        (calc, "E22", 82.18),
        (calc, "E24", 20.55),
        (calc, "E25", 0.25006084205),
        (sim, "E8", 73.96),
        (sim, "E13", 13.19),
        (sim, "E14", 0.17833964305),
    ]

    for sheet, address, expected in expectations:
        value, formula = read_cell(
            sheet, address
        )

        assert formula, (
            f"Fórmula ausente em {address}"
        )

        assert value is not None
        assert isclose(
            float(value),
            expected,
            abs_tol=0.0001,
        ), f"{address}: valor inesperado {value}"

    print("PASSOU: estrutura e resultados salvos.")
    print("PASSOU: sem macros ou links externos.")

    protected = all(
        sheet.find("x:sheetProtection", NS)
        is not None
        for sheet in (calc, sim)
    )

    assert protected, "Abas de cálculo sem proteção"
    print("PASSOU: abas de cálculo protegidas.")

print(
    "AVISO: a recalculação das fórmulas "
    "ainda deve ser testada no Excel."
)
