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
    if errors:
        print("\n".join(errors))
        return 1
    print(f"ok: {len(files)} páginas")
    return 0


if __name__ == "__main__":
    site = Path(sys.argv[1] if len(sys.argv) > 1 else "_site")
    sys.exit(main(site))
