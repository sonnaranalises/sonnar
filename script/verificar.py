#!/usr/bin/env python3
"""Confere o HTML gerado do site da Sonnar Análises."""

import re
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse

DISCLOSURE = (
    "Transparência: os links desta página são de afiliado. "
    "Se eles forem úteis pra você, a comissão ajuda a Sonnar a continuar no ar, "
    "sem custo adicional na sua compra e sem influenciar o que escrevemos."
)
SHORTENERS = (
    "bit.ly",
    "tinyurl.com",
    "t.co",
    "goo.gl",
    "amzn.to",
    "cutt.ly",
    "is.gd",
    "ow.ly",
    "abre.ai",
    "shope.ee",
)
PHRASES = (
    "compre já",
    "compre ja",
    "imperdível",
    "imperdivel",
    "última chance",
    "ultima chance",
    "sonnar analysis",
)


class Parser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.links = []
        self.imgs = []
        self.h1 = 0
        self.affiliate_blocks = []
        self._capture = False
        self._buf = []

    def handle_starttag(self, tag, attrs):
        ad = {k: (v or "") for k, v in attrs}
        if tag == "a":
            self.links.append(ad)
        elif tag == "img":
            self.imgs.append(ad)
        elif tag == "h1":
            self.h1 += 1
        classes = ad.get("class", "").split()
        if tag == "div" and "affiliate-line" in classes:
            self._capture = True
            self._buf = []

    def handle_data(self, data):
        if self._capture:
            self._buf.append(data)

    def handle_endtag(self, tag):
        if self._capture and tag == "div":
            self.affiliate_blocks.append("".join(self._buf))
            self._capture = False


OK_HEX = {"1a1b1f", "367588", "fbfdff", "5ba3b8"}
OK_RGB = {(26, 27, 31), (54, 117, 136), (251, 253, 255), (91, 163, 184)}
POSICOES_REGUA = {
    "abaixo da faixa",
    "no começo da faixa",
    "no meio da faixa",
    "no fim da faixa",
    "acima da faixa",
}


def front_matter(text: str) -> str:
    if not text.startswith("---"):
        return ""
    end = text.find("\n---", 3)
    if end < 0:
        return ""
    return text[3:end]


def checagens_v2(root: Path, errors: list) -> None:
    exts = {".css", ".html", ".svg", ".webmanifest"}
    for path in sorted(root.rglob("*")):
        if not path.is_file() or path.suffix.lower() not in exts:
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        rel = path.relative_to(root).as_posix()
        for match in re.finditer(r"#([0-9a-fA-F]{3,8})\b", text):
            if match.group(1).lower() not in OK_HEX:
                errors.append(f"{rel}: cor {match.group(0)}")
        for match in re.finditer(
            r"rgba?\(\s*([0-9.]+)\s*,\s*([0-9.]+)\s*,\s*([0-9.]+)",
            text,
            re.I,
        ):
            trio = tuple(int(float(match.group(i))) for i in (1, 2, 3))
            if trio not in OK_RGB:
                errors.append(f"{rel}: rgb {match.group(0)}")
        if "A decisão é de quem lê" in text:
            errors.append(f"{rel}: contém a frase morta")
        if rel in {"index.html", "sobre/index.html"} and "no Mercado Livre" in text:
            errors.append(f"{rel}: contém 'no Mercado Livre'")
        if 'class="comentarios"' in text:
            colunas = re.findall(
                r'<div class="comentarios-col[^"]*">(.*?)</div>',
                text,
                re.S,
            )
            if len(colunas) < 2:
                errors.append(f"{rel}: tabela de comentários sem as duas colunas")
            for coluna in colunas:
                n = coluna.count("<blockquote")
                if n > 3:
                    errors.append(f"{rel}: coluna de comentários com {n} citações")

    trans = root / "transparencia" / "index.html"
    if not trans.exists():
        errors.append("transparencia/: página ausente")
    else:
        html = trans.read_text(encoding="utf-8")
        if not re.search(r'http-equiv="refresh"[^>]*url=[^"]*/sobre/', html):
            errors.append("transparencia/: sem meta refresh para /sobre/")

    repo = Path(__file__).resolve().parent.parent
    dados = (repo / "_data" / "categorias.yml").read_text(encoding="utf-8")
    slugs = set(re.findall(r"(?m)^- slug:\s*(\S+)\s*$", dados))
    posts = sorted((repo / "_posts").glob("*.md"))
    if not posts:
        errors.append("_posts: nenhum relatório")
    for post in posts:
        fm = front_matter(post.read_text(encoding="utf-8"))
        cat = re.search(r"(?m)^categoria:\s*[\"']?([A-Za-z0-9_-]+)", fm)
        tipo = re.search(r"(?m)^tipo:\s*[\"']?(.*?)[\"']?\s*$", fm)
        rel = post.relative_to(repo).as_posix()
        if not cat or cat.group(1) not in slugs:
            errors.append(f"{rel}: categoria ausente ou fora da lista")
        elif not tipo or not tipo.group(1).strip():
            errors.append(f"{rel}: tipo vazio")
        if re.search(r"(?m)^regua_preco:\s*$", fm):
            pos = re.search(r"(?m)^[ \t]+posicao:\s*[\"']?(.*?)[\"']?\s*$", fm)
            valor = pos.group(1).strip() if pos else ""
            if valor not in POSICOES_REGUA:
                errors.append(f"{rel}: posição da régua inválida ({valor!r})")


def main(root: Path) -> int:
    files = sorted(root.rglob("*.html"))
    if not files:
        print("nenhum HTML em", root)
        return 1
    errors = []
    for path in files:
        text = path.read_text(encoding="utf-8")
        rel = path.relative_to(root).as_posix()
        low = text.lower()
        if 'lang="pt-BR"' not in text and 'lang="pt-br"' not in text:
            errors.append(f"{rel}: falta lang pt-BR")
        for phrase in PHRASES:
            if phrase in low:
                errors.append(f"{rel}: contém '{phrase}'")
        if text.count("<h1") != 1:
            errors.append(f"{rel}: esperado 1 h1, há {text.count('<h1')}")
        if 'rel="canonical"' not in text and "rel='canonical'" not in text:
            errors.append(f"{rel}: falta canonical")
        if 'property="og:title"' not in text:
            errors.append(f"{rel}: falta og:title")
        if "/sonnar/assets/css/style.css" not in text:
            errors.append(f"{rel}: CSS sem base /sonnar/")
        parser = Parser()
        parser.feed(text)
        affiliate_links = []
        for link in parser.links:
            href = link.get("href", "")
            rel_attr = link.get("rel", "")
            tokens = set(rel_attr.split())
            target = link.get("target", "")
            classes = link.get("class", "").split()
            if href.lower().startswith("javascript:"):
                errors.append(f"{rel}: javascript: em {href}")
            if href.startswith("http://"):
                errors.append(f"{rel}: http sem s em {href}")
            host = urlparse(href).hostname or ""
            if any(host == s or host.endswith("." + s) for s in SHORTENERS):
                errors.append(f"{rel}: encurtador {href}")
            if target == "_blank" and "noopener" not in tokens:
                errors.append(f"{rel}: target=_blank sem noopener em {href}")
            if "affiliate-link" in classes:
                affiliate_links.append(link)
                needed = {"sponsored", "nofollow", "noopener"}
                if tokens != needed:
                    errors.append(f"{rel}: rel de afiliado {rel_attr!r} em {href}")
                if target != "_blank":
                    errors.append(f"{rel}: afiliado sem target=_blank em {href}")
                if not href.startswith("https://"):
                    errors.append(f"{rel}: afiliado sem https em {href}")
            elif "sponsored" in tokens:
                errors.append(f"{rel}: sponsored fora de link de afiliado em {href}")
        for img in parser.imgs:
            if "alt" not in img:
                errors.append(f"{rel}: img sem alt")
        if len(parser.affiliate_blocks) != len(affiliate_links):
            errors.append(
                f"{rel}: {len(affiliate_links)} links de afiliado e {len(parser.affiliate_blocks)} blocos"
            )
        if "#publi" in low:
            errors.append(f"{rel}: ainda usa #publi")
        for block in parser.affiliate_blocks:
            if "Ver no Mercado Livre" not in block:
                errors.append(f"{rel}: botão sem 'Ver no Mercado Livre'")
            if "Link de afiliado" not in block:
                errors.append(f"{rel}: botão sem a legenda 'Link de afiliado'")
        if "/radar/" in "/" + rel or rel.startswith("radar/"):
            if DISCLOSURE not in text:
                errors.append(f"{rel}: post sem o aviso de transparência")
            if 'class="disclosure"' not in text:
                errors.append(f"{rel}: post sem aside de disclosure")
            if 'class="reader-feedback"' not in text:
                errors.append(f"{rel}: post sem o bloco de feedback")
            if "O que achou deste relatório?" not in text:
                errors.append(f"{rel}: post sem o título do feedback")
            if "Deixe seu comentário (opcional)" not in text:
                errors.append(f"{rel}: post sem o campo de comentário")
            if "Obrigado pelo feedback!" not in text:
                errors.append(f"{rel}: post sem a mensagem de agradecimento")
            if "/assets/js/feedback.js" not in text:
                errors.append(f"{rel}: post sem o script de feedback")
        elif "O que achou deste relatório?" in text:
            errors.append(f"{rel}: feedback fora de um relatório")
        if "example-banner" in text:
            if "noindex" not in text:
                errors.append(f"{rel}: exemplo indexável")
            if "fictíc" not in low and "fictic" not in low:
                errors.append(f"{rel}: exemplo sem dizer que os dados são fictícios")
            if "R$ XX,XX" not in text:
                errors.append(f"{rel}: exemplo sem preço placeholder")
            if re.search(r"R\$\s*\d", text):
                errors.append(f"{rel}: exemplo com preço numérico")
    checagens_v2(root, errors)
    if errors:
        print("\n".join(errors))
        return 1
    print(f"ok: {len(files)} páginas")
    return 0


if __name__ == "__main__":
    site = Path(sys.argv[1] if len(sys.argv) > 1 else "_site")
    sys.exit(main(site))
