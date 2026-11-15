import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WEB = ROOT / "apps/web"
CATALOG = WEB / "src/data/catalog.public.json"

original = CATALOG.read_bytes()

fixture = [{
    "slug": "qa-render-test",
    "name": "Produto QA",
    "audience": "Testadores",
    "status": "live",
    "page": {
        "headline": "Titulo de teste da landing page",
        "subheadline": "Subtitulo exclusivo do teste automatizado",
        "description": "Descricao criada somente para testar a renderizacao.",
        "benefits": [
            "Beneficio exclusivo de teste um",
            "Beneficio exclusivo de teste dois",
        ],
        "faqs": [{
            "question": "Como testar o produto QA?",
            "answer": "Esta resposta pertence somente ao teste.",
        }],
        "cta_label": "Abrir checkout de teste",
        "seo_title": "SEO - Produto QA",
        "seo_description": "Descricao SEO da fixture automatizada.",
    },
    "offers": [{
        "price_cents": 3900,
        "currency": "BRL",
        "checkout_url": "https://example.com/test",
    }],
}]

try:
    CATALOG.write_text(
        json.dumps(fixture, ensure_ascii=False, indent=2) + "\n"
    )

    # Chamar Astro diretamente para preservar a fixture.
    subprocess.run(
        ["./node_modules/.bin/astro", "build"],
        cwd=WEB,
        check=True,
    )

    html_path = WEB / "dist/p/qa-render-test/index.html"
    assert html_path.exists(), "Página QA não foi gerada"

    html = html_path.read_text()

    expected = [
        "Titulo de teste da landing page",
        "Subtitulo exclusivo do teste automatizado",
        "Beneficio exclusivo de teste um",
        "Como testar o produto QA?",
        "Esta resposta pertence somente ao teste.",
        "SEO - Produto QA",
        "Abrir checkout de teste",
        "example.com/test",
    ]

    for value in expected:
        assert value in html, f"Conteúdo ausente: {value}"

    assert not (
        WEB / "dist/preview/qa-render-test/index.html"
    ).exists()

    print("Renderização e SEO validados.")

finally:
    CATALOG.write_bytes(original)

    # Regerar o build usando exclusivamente o banco real.
    subprocess.run(
        ["npm", "run", "build"],
        cwd=WEB,
        check=True,
    )
