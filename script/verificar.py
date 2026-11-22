#!/usr/bin/env python3
"""Confere o HTML gerado do site da Sonnar Análises.

O modo padrão passa com os relatórios atuais. `--v3` exige, em todo
relatório que não seja exemplo, o bloco `resumo:` (seis campos, rótulos
na ordem e 50 a 80 palavras somadas nos quatro tópicos) e o bloco `fontes:`.
Quando os 10 relatórios novos estiverem publicados, rode:

    python3 script/verificar.py _site --v3

e acrescente `--v3` ao passo "Conferir o HTML gerado" do workflow.
"""

import json
import re
import sys
from decimal import Decimal, ROUND_HALF_UP
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse

# |diferença| em relação à média dos equivalentes (o analisado fica de fora).
# Até este limite, a direção é "na media".
LIMITE_NA_MEDIA = 3
FREQUENCIAS = {
    "muitos citam",
    "alguns citam",
    "caso isolado",
    "citado em avaliações negativas",
    "segundo o resumo do Mercado Livre",
}
# Estes dois só valem se o post trouxer atributos_nota.
FREQUENCIAS_COM_NOTA = {
    "citado em avaliações negativas",
    "segundo o resumo do Mercado Livre",
}

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
        self._in_list = False

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
            self._in_list = "affiliate-in-list" in classes

    def handle_data(self, data):
        if self._capture:
            self._buf.append(data)

    def handle_endtag(self, tag):
        if self._capture and tag == "div":
            self.affiliate_blocks.append(
                {"text": "".join(self._buf), "in_list": self._in_list}
            )
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
            if not colunas or len(colunas) > 2:
                errors.append(
                    f"{rel}: tabela de comentários com {len(colunas)} colunas"
                )
            for coluna in colunas:
                n = coluna.count("<blockquote")
                if n == 0:
                    errors.append(f"{rel}: coluna de comentários vazia")
                elif n > 3:
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


FRASES_RESUMO = (
    "vale a pena",
    "indicamos",
    "recomendamos",
    "os dados favorecem",
    "os dados pesam contra",
    "os dados ficam divididos",
)
ROTULOS_RESUMO = (
    "Avaliações:",
    "Ponto forte:",
    "Ponto de atenção:",
    "Preço:",
)
CAMPOS_RESUMO = (
    "avaliacoes",
    "ponto_forte",
    "ponto_atencao",
    "preco",
    "util_para",
    "atencao_de",
)
TOPICOS_RESUMO = ("avaliacoes", "ponto_forte", "ponto_atencao", "preco")
SLOGAN = "Te ajudando a detectar boas escolhas"


def eh_radar(rel: str) -> bool:
    return "/radar/" in "/" + rel or rel.startswith("radar/")


def texto_puro(html: str) -> str:
    return re.sub(r"<[^>]+>", " ", html)


def frases_vedadas(html: str) -> list[str]:
    puro = texto_puro(html).lower()
    achadas = [frase for frase in FRASES_RESUMO if frase in puro]
    if re.search(r"\bcompre\b", puro):
        achadas.append("compre")
    return achadas


def bloco_mapa(fm: str, chave: str) -> dict[str, str] | None:
    linhas = fm.splitlines()
    inicio = None
    for i, linha in enumerate(linhas):
        if re.match(rf"^{re.escape(chave)}:\s*$", linha):
            inicio = i
            break
    if inicio is None:
        return None
    campos: dict[str, str] = {}
    atual = None
    buf: list[str] = []

    def guarda() -> None:
        if atual is None:
            return
        valor = " ".join(parte for parte in buf if parte != "").strip()
        if len(valor) >= 2 and valor[0] == valor[-1] and valor[0] in "\"'":
            valor = valor[1:-1]
        campos[atual] = valor.strip()

    for linha in linhas[inicio + 1 :]:
        if re.match(r"^[A-Za-z0-9_]+:\s*", linha):
            break
        miolo = re.match(r"^  ([A-Za-z0-9_]+):\s*(.*)$", linha)
        if miolo:
            guarda()
            atual = miolo.group(1)
            buf = [miolo.group(2)]
        elif atual is not None and (linha.startswith(" ") or linha.strip() == ""):
            buf.append(linha.strip())
        else:
            break
    guarda()
    return campos


def titulo_front(fm: str, reserva: str) -> str:
    miolo = re.search(r'(?m)^title:\s*(.+?)\s*$', fm)
    if not miolo:
        return reserva
    valor = miolo.group(1).strip()
    if len(valor) >= 2 and valor[0] == valor[-1] and valor[0] in "\"'":
        valor = valor[1:-1]
    return valor


def html_do_post(root: Path, post: Path) -> Path | None:
    miolo = re.match(r"(\d{4})-(\d{2})-(\d{2})-(.+)$", post.stem)
    if not miolo:
        return None
    return (
        root
        / "radar"
        / miolo.group(1)
        / miolo.group(2)
        / miolo.group(3)
        / miolo.group(4)
        / "index.html"
    )


def checagens_18(root: Path, errors: list) -> None:
    for path in sorted(root.rglob("*.html")):
        text = path.read_text(encoding="utf-8")
        rel = path.relative_to(root).as_posix()
        if not eh_radar(rel):
            continue
        h1 = re.search(r"<h1\b[^>]*>(.*?)</h1>", text, re.S | re.I)
        interno = h1.group(1) if h1 else ""
        tag = ""
        for candidato in re.findall(r"<a\b[^>]*>", interno):
            classes = re.search(r'class="([^"]*)"', candidato)
            if classes and "titulo-afiliado" in classes.group(1).split():
                tag = candidato
                break
        if not tag:
            errors.append(f"{rel}: h1 sem a.titulo-afiliado")
        else:
            href = re.search(r'href="([^"]*)"', tag)
            rel_attr = re.search(r'rel="([^"]*)"', tag)
            target = re.search(r'target="([^"]*)"', tag)
            if not href or not href.group(1).startswith("https://meli.la/"):
                errors.append(f"{rel}: h1 sem link https://meli.la/")
            if not rel_attr or rel_attr.group(1) != "sponsored nofollow noopener":
                errors.append(f"{rel}: rel do título não é o esperado")
            if not target or target.group(1) != "_blank":
                errors.append(f"{rel}: título sem target=_blank")
        if "produzido com ajuda de inteligência artificial" in text:
            if not re.search(r'<p class="fontes-menor"', text):
                errors.append(f"{rel}: Fontes sem a classe de letra menor")
        if 'class="resumo"' in text:
            for trecho in re.findall(
                r'<section class="(?:resumo|conclusion)"[^>]*>.*?</section>',
                text,
                re.S,
            ):
                for frase in frases_vedadas(trecho):
                    nome = "Resumo" if 'class="resumo"' in trecho[:80] else "Conclusão"
                    errors.append(f"{rel}: {nome} contém '{frase}'")

    home = root / "index.html"
    if home.exists():
        html = home.read_text(encoding="utf-8")
        if 'class="busca"' not in html:
            errors.append("index.html: falta a busca")
        if "cat-acordeao" not in html:
            errors.append("index.html: falta o acordeão de categorias")
        if "Radar de hoje" in html:
            errors.append("index.html: ainda diz 'Radar de hoje'")
    else:
        errors.append("index.html: página ausente")

    feed = root / "feed.xml"
    if not feed.exists():
        errors.append("feed.xml: arquivo ausente")
    else:
        xml = feed.read_text(encoding="utf-8")
        if f"<subtitle>{SLOGAN}</subtitle>" not in xml:
            errors.append("feed.xml: subtitle diferente do slogan")

    bruto = root / "busca.json"
    if not bruto.exists():
        errors.append("busca.json: arquivo ausente")
        return
    try:
        dados = json.loads(bruto.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        errors.append(f"busca.json: JSON inválido ({exc})")
        return
    if not isinstance(dados, list):
        errors.append("busca.json: o conteúdo não é uma lista")
        return
    repo = Path(__file__).resolve().parent.parent
    esperados = []
    for post in sorted((repo / "_posts").glob("*.md")):
        fm = front_matter(post.read_text(encoding="utf-8"))
        if re.search(r"(?m)^example:\s*true\b", fm):
            continue
        esperados.append(titulo_front(fm, post.stem))
    titulos = [item.get("title") for item in dados if isinstance(item, dict)]
    if len(dados) != len(esperados):
        errors.append(
            f"busca.json: {len(dados)} itens para {len(esperados)} relatórios"
        )
    for titulo in esperados:
        if titulo not in titulos:
            errors.append(f"busca.json: falta {titulo}")
    for item in dados:
        if not isinstance(item, dict) or not item.get("title") or not item.get("url"):
            errors.append("busca.json: item sem título ou url")


def checagens_v3(root: Path, errors: list) -> None:
    repo = Path(__file__).resolve().parent.parent
    for post in sorted((repo / "_posts").glob("*.md")):
        texto = post.read_text(encoding="utf-8")
        fm = front_matter(texto)
        rel = post.relative_to(repo).as_posix()
        if re.search(r"(?m)^example:\s*true\b", fm):
            continue
        resumo = bloco_mapa(fm, "resumo")
        if resumo is None:
            errors.append(f"{rel}: sem resumo")
        else:
            for campo in ("avaliacoes", "ponto_forte", "ponto_atencao", "preco"):
                if not resumo.get(campo, "").strip():
                    errors.append(f"{rel}: resumo sem {campo}")
            para_quem = resumo.get("para_quem", "").strip()
            if not para_quem:
                for campo in ("util_para", "atencao_de"):
                    if not resumo.get(campo, "").strip():
                        errors.append(f"{rel}: resumo sem {campo}")
            # Os quatro tópicos, somados, ficam entre 50 e 80 palavras.
            n = sum(len(re.findall(r"\S+", resumo.get(campo, ""))) for campo in TOPICOS_RESUMO)
            if n < 50 or n > 80:
                errors.append(f"{rel}: os 4 tópicos têm {n} palavras (esperado 50–80)")
        fontes = bloco_mapa(fm, "fontes")
        if not fontes or not fontes.get("coleta", "").strip():
            errors.append(f"{rel}: sem fontes")
        html_path = html_do_post(root, post)
        if html_path is None or not html_path.exists():
            errors.append(f"{rel}: HTML do relatório ausente")
            continue
        html = html_path.read_text(encoding="utf-8")
        secao = re.search(r'<section class="resumo"[^>]*>.*?</section>', html, re.S)
        if not secao:
            errors.append(f"{rel}: HTML sem a seção Resumo")
            continue
        miolo = secao.group(0)
        cursor = 0
        for rotulo in ROTULOS_RESUMO:
            pos = miolo.find(rotulo, cursor)
            if pos < 0:
                errors.append(f"{rel}: rótulo '{rotulo}' ausente ou fora de ordem")
                cursor = len(miolo)
            else:
                cursor = pos + len(rotulo)
        para_quem = (resumo or {}).get("para_quem", "").strip()
        if para_quem:
            if para_quem not in miolo:
                errors.append(f"{rel}: HTML do Resumo sem para_quem")
        else:
            for linha in ("Útil para quem", "Pede atenção de quem"):
                if linha not in miolo:
                    errors.append(f"{rel}: falta a linha '{linha}'")


def itens_lista(fm: str, chave: str) -> int:
    linhas = fm.splitlines()
    dentro = False
    n = 0
    for linha in linhas:
        if re.match(rf"^{re.escape(chave)}:\s*$", linha):
            dentro = True
            continue
        if not dentro:
            continue
        if re.match(r"^[^\s]", linha):
            break
        if re.match(r"^  -(\s|$)", linha):
            n += 1
    return n


def limites_regua(fm: str) -> tuple[float, float] | None:
    bloco = bloco_mapa(fm, "regua_preco")
    if not bloco:
        return None

    def numero(chave: str) -> float | None:
        bruto = bloco.get(chave, "").strip()
        if not bruto:
            return None
        try:
            return float(bruto.replace(",", "."))
        except ValueError:
            return None

    minimo = numero("minimo")
    maximo = numero("maximo")
    if minimo is None or maximo is None:
        return None
    return minimo, maximo


def checagens_limites(root: Path, errors: list) -> None:
    """Régua só com faixa, tabela sem coluna vazia, Fontes sem equivalentes."""
    repo = Path(__file__).resolve().parent.parent
    for post in sorted((repo / "_posts").glob("*.md")):
        fm = front_matter(post.read_text(encoding="utf-8"))
        rel = post.relative_to(repo).as_posix()
        html_path = html_do_post(root, post)
        if html_path is None or not html_path.exists():
            continue
        html = html_path.read_text(encoding="utf-8")
        n_elogios = itens_lista(fm, "elogios")
        n_criticas = itens_lista(fm, "criticas")
        tem_elogios = "comentarios-elogios" in html
        tem_criticas = "comentarios-criticas" in html
        if n_elogios == 0 and n_criticas == 0:
            if 'class="comentarios"' in html:
                errors.append(f"{rel}: tabela de comentários sem citações")
        else:
            if (n_elogios > 0) != tem_elogios:
                errors.append(f"{rel}: coluna de elogios não acompanha o front matter")
            if (n_criticas > 0) != tem_criticas:
                errors.append(f"{rel}: coluna de críticas não acompanha o front matter")
            if (n_elogios == 0) != (n_criticas == 0) and "comentarios-uma" not in html:
                errors.append(f"{rel}: coluna única sem ocupar a largura")
            if n_elogios > 0 and n_criticas > 0 and "comentarios-uma" in html:
                errors.append(f"{rel}: tabela completa marcada como coluna única")
        limites = limites_regua(fm)
        tem_regua = 'class="regua"' in html
        tem_precos = parse_precos(fm) is not None
        sem_faixa = limites is None or abs(limites[0] - limites[1]) < 1e-9
        if tem_precos:
            if tem_regua:
                errors.append(f"{rel}: régua desenhada junto com a tabela de preços")
        else:
            if sem_faixa and tem_regua:
                errors.append(f"{rel}: régua desenhada sem faixa de preço")
            if not sem_faixa and not tem_regua:
                errors.append(f"{rel}: régua ausente apesar da faixa de preço")
        fontes = bloco_mapa(fm, "fontes")
        if fontes is not None:
            frase = "Para o preço, comparamos com"
            if fontes.get("equivalentes", "").strip():
                if frase not in html:
                    errors.append(f"{rel}: Fontes sem a frase dos equivalentes")
            elif frase in html:
                errors.append(f"{rel}: Fontes cita equivalentes vazios")


def legendas_ligadas() -> bool:
    repo = Path(__file__).resolve().parent.parent
    texto = (repo / "_config.yml").read_text(encoding="utf-8")
    miolo = re.search(r"(?m)^legendas_afiliado:\s*(\S+)", texto)
    if not miolo:
        return False
    return miolo.group(1).strip().lower() in {"true", "yes", "sim"}


def desaspa(valor: str) -> str:
    valor = valor.strip()
    if len(valor) >= 2 and valor[0] == valor[-1] and valor[0] in "\"'":
        valor = valor[1:-1]
    return valor.strip()


def bloco_linhas(fm: str, chave: str) -> list[str] | None:
    linhas = fm.splitlines()
    inicio = None
    for i, linha in enumerate(linhas):
        if re.match(rf"^{re.escape(chave)}:\s*$", linha):
            inicio = i
            break
    if inicio is None:
        return None
    bloco = []
    for linha in linhas[inicio + 1 :]:
        if re.match(r"^[A-Za-z0-9_]+:\s*", linha):
            break
        bloco.append(linha)
    return bloco


def reais(texto: str) -> float | None:
    bruto = desaspa(texto)
    bruto = re.sub(r"(?i)^r\$\s*", "", bruto).replace("\xa0", "").replace(" ", "")
    if not bruto:
        return None
    if "," in bruto:
        bruto = bruto.replace(".", "").replace(",", ".")
    try:
        return float(bruto)
    except ValueError:
        return None


def arredondar(valor: float) -> int:
    return int(Decimal(str(valor)).quantize(Decimal("1"), rounding=ROUND_HALF_UP))


def mapa_inline(texto: str) -> dict[str, str]:
    miolo = texto.strip()
    if miolo.startswith("{") and miolo.endswith("}"):
        miolo = miolo[1:-1]
    campos = {}
    for parte in miolo.split(","):
        if ":" not in parte:
            continue
        chave, valor = parte.split(":", 1)
        campos[chave.strip()] = desaspa(valor)
    return campos


def parse_atributos(fm: str) -> list[dict[str, str]] | None:
    linhas = bloco_linhas(fm, "atributos")
    if linhas is None:
        return None
    itens: list[dict[str, str]] = []
    atual: dict[str, str] | None = None
    for linha in linhas:
        if not linha.strip() or linha.strip().startswith("#"):
            continue
        novo = re.match(r"^  - (.*)$", linha)
        if novo:
            if atual:
                itens.append(atual)
            atual = {}
            resto = novo.group(1).strip()
            if resto and ":" in resto:
                chave, valor = resto.split(":", 1)
                atual[chave.strip()] = desaspa(valor)
            continue
        if atual is not None and linha.startswith("    ") and ":" in linha:
            chave, valor = linha.strip().split(":", 1)
            atual[chave.strip()] = desaspa(valor)
    if atual:
        itens.append(atual)
    return itens


def parse_precos(fm: str) -> dict | None:
    linhas = bloco_linhas(fm, "precos")
    if linhas is None:
        return None
    dados: dict = {
        "data_coleta": "",
        "unidade": "",
        "itens": [],
        "kpis": {},
    }
    secao = ""
    item: dict | None = None
    vs: dict[str, str] | None = None

    def guarda_item() -> None:
        nonlocal item
        if item:
            dados["itens"].append(item)
        item = None

    for linha in linhas:
        if not linha.strip() or linha.strip().startswith("#"):
            continue
        if re.match(r"^  data_coleta:\s*", linha):
            dados["data_coleta"] = desaspa(linha.split(":", 1)[1])
            continue
        if re.match(r"^  unidade:\s*", linha):
            dados["unidade"] = desaspa(linha.split(":", 1)[1])
            continue
        if re.match(r"^  itens:\s*$", linha):
            guarda_item()
            secao = "itens"
            vs = None
            continue
        if re.match(r"^  kpis:\s*$", linha):
            guarda_item()
            secao = "kpis"
            continue
        if secao == "itens" and re.match(r"^    - ", linha):
            guarda_item()
            item = {"analisado": False, "diferenca": ""}
            resto = linha.split("-", 1)[1].strip()
            if resto and ":" in resto:
                chave, valor = resto.split(":", 1)
                item[chave.strip()] = desaspa(valor)
            continue
        if secao == "itens" and item is not None and linha.startswith("      ") and ":" in linha:
            chave, valor = linha.strip().split(":", 1)
            if chave.strip() == "analisado":
                item["analisado"] = valor.strip().lower() in {"true", "yes", "sim"}
            else:
                item[chave.strip()] = desaspa(valor)
            continue
        if secao == "kpis" and re.match(r"^    vs_media:\s*", linha):
            resto = linha.split(":", 1)[1].strip()
            if resto:
                dados["kpis"]["vs_media"] = mapa_inline(resto)
                vs = None
            else:
                vs = {}
                dados["kpis"]["vs_media"] = vs
            continue
        if secao == "kpis" and vs is not None and linha.startswith("      ") and ":" in linha:
            chave, valor = linha.strip().split(":", 1)
            vs[chave.strip()] = desaspa(valor)
            continue
        if secao == "kpis" and re.match(r"^    [A-Za-z0-9_]+:\s*", linha):
            vs = None
            chave, valor = linha.strip().split(":", 1)
            dados["kpis"][chave.strip()] = desaspa(valor)
    guarda_item()
    return dados


def posicao_mais_caro(valores: list[float], indice: int) -> str:
    """1 + quantos itens têm por_unidade estritamente maior.

    Empate no mesmo preço divide a posição: dois itens a R$ 94,02,
    com só um mais caro, ficam ambos em "2º mais caro de N".
    """
    analisado = valores[indice]
    maiores = sum(1 for valor in valores if valor > analisado + 1e-9)
    return f"{maiores + 1}º mais caro de {len(valores)}"


def campo_simples(fm: str, chave: str) -> str:
    miolo = re.search(rf"(?m)^{re.escape(chave)}:\s*(.+?)\s*$", fm)
    if not miolo:
        return ""
    return desaspa(miolo.group(1))


def palavras_corpo(texto: str) -> int:
    """Conta as palavras do markdown depois do front matter."""
    corpo = texto
    if texto.startswith("---"):
        fim = texto.find("\n---", 3)
        if fim >= 0:
            corpo = texto[fim + 4 :]
    return len(re.findall(r"\S+", corpo))


def checagens_precos(root: Path, errors: list, avisos: list) -> None:
    """Atributos, tabela de preços e KPIs no formato v3.1."""
    for post in sorted((Path(__file__).resolve().parent.parent / "_posts").glob("*.md")):
        texto = post.read_text(encoding="utf-8")
        fm = front_matter(texto)
        rel = post.relative_to(Path(__file__).resolve().parent.parent).as_posix()
        html_path = html_do_post(root, post)
        if html_path is None or not html_path.exists():
            continue
        html = html_path.read_text(encoding="utf-8")
        atributos = parse_atributos(fm)
        if atributos is not None:
            if not 4 <= len(atributos) <= 6:
                errors.append(f"{rel}: {len(atributos)} atributos (esperado 4–6)")
            nota = campo_simples(fm, "atributos_nota")
            pede_nota = False
            for item in atributos:
                freq = item.get("frequencia", "").strip()
                if freq not in FREQUENCIAS:
                    errors.append(f"{rel}: frequência inválida ({freq!r})")
                if freq in FREQUENCIAS_COM_NOTA:
                    pede_nota = True
            if pede_nota and not nota:
                errors.append(
                    f"{rel}: atributos_nota ausente com frequência que exige a nota"
                )
            if "tabela-atributos" not in html:
                errors.append(f"{rel}: HTML sem a tabela de atributos")
            if nota and nota not in html:
                errors.append(f"{rel}: HTML sem atributos_nota")
            if not nota and "atributos_nota" in html:
                errors.append(f"{rel}: HTML mostra atributos_nota vazio")
        precos = parse_precos(fm)
        if precos is None:
            if 'class="tabela-precos"' in html:
                errors.append(f"{rel}: tabela de preços sem o campo precos")
            continue
        if re.search(r"https?://", "\n".join(bloco_linhas(fm, "precos") or [])):
            errors.append(f"{rel}: precos contém link")
        n_corpo = palavras_corpo(texto)
        if n_corpo < 250:
            avisos.append(f"{rel}: corpo com {n_corpo} palavras (abaixo de 250)")
        itens = precos["itens"]
        if not itens:
            errors.append(f"{rel}: precos sem itens")
            continue
        valores = []
        for item in itens:
            numero = reais(item.get("por_unidade", ""))
            if numero is None:
                errors.append(f"{rel}: por_unidade ilegível ({item.get('por_unidade', '')!r})")
                numero = 0.0
            valores.append(numero)
        for anterior, seguinte in zip(valores, valores[1:]):
            if seguinte > anterior + 1e-9:
                errors.append(f"{rel}: precos.itens fora da ordem do maior para o menor")
                break
        analisados = [i for i, item in enumerate(itens) if item.get("analisado")]
        if len(analisados) != 1:
            errors.append(f"{rel}: {len(analisados)} itens analisados (esperado 1)")
            continue
        indice = analisados[0]
        analisado = valores[indice]
        equivalentes = [valor for i, valor in enumerate(valores) if i != indice]
        kpis = precos["kpis"]
        preco_kpi = reais(str(kpis.get("preco_unidade", "")))
        if preco_kpi is None or abs(preco_kpi - analisado) > 0.001:
            errors.append(f"{rel}: kpis.preco_unidade não é o por_unidade do analisado")
        if len(equivalentes) < 3:
            if kpis.get("vs_media") or str(kpis.get("posicao", "")).strip():
                errors.append(f"{rel}: vs_media ou posicao com menos de 3 equivalentes")
            if "kpis-um" not in html:
                errors.append(f"{rel}: faixa de KPIs sem a classe kpis-um")
        else:
            media = sum(equivalentes) / len(equivalentes)
            if media == 0:
                errors.append(f"{rel}: média dos equivalentes é zero")
            else:
                diferenca = (analisado - media) / media * 100
                if abs(diferenca) <= LIMITE_NA_MEDIA:
                    direcao = "na media"
                    percentual = None
                elif diferenca > 0:
                    direcao = "acima"
                    percentual = arredondar(abs(diferenca))
                else:
                    direcao = "abaixo"
                    percentual = arredondar(abs(diferenca))
                vs = kpis.get("vs_media") or {}
                if not isinstance(vs, dict):
                    errors.append(f"{rel}: vs_media ausente")
                else:
                    lida = str(vs.get("direcao", "")).strip().lower().replace("é", "e")
                    if lida != direcao:
                        errors.append(
                            f"{rel}: vs_media.direcao {lida!r} (esperado {direcao!r})"
                        )
                    if percentual is not None:
                        try:
                            lido = int(float(str(vs.get("percentual", "")).replace(",", ".")))
                        except ValueError:
                            lido = None
                        if lido != percentual:
                            errors.append(
                                f"{rel}: vs_media.percentual {vs.get('percentual')!r} (esperado {percentual})"
                            )
            esperada = posicao_mais_caro(valores, indice)
            if str(kpis.get("posicao", "")).strip() != esperada:
                errors.append(
                    f"{rel}: posicao {kpis.get('posicao')!r} (esperado {esperada!r})"
                )
            if "kpis-um" in html:
                errors.append(f"{rel}: kpis-um com 3 ou mais equivalentes")
        tabela = re.search(r'<figure class="tabela-precos">.*?</figure>', html, re.S)
        if not tabela:
            errors.append(f"{rel}: HTML sem a tabela de preços")
        elif "<a " in tabela.group(0) or "<a>" in tabela.group(0):
            errors.append(f"{rel}: link dentro da tabela de preços")


def main(root: Path, v3: bool = False) -> int:
    files = sorted(root.rglob("*.html"))
    if not files:
        print("nenhum HTML em", root)
        return 1
    errors = []
    legendas = legendas_ligadas()
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
            elif "titulo-afiliado" in classes:
                if rel_attr != "sponsored nofollow noopener":
                    errors.append(f"{rel}: rel de titulo-afiliado {rel_attr!r} em {href}")
                if target != "_blank":
                    errors.append(f"{rel}: titulo-afiliado sem target=_blank em {href}")
                if not href.startswith("https://meli.la/"):
                    errors.append(f"{rel}: titulo-afiliado sem https://meli.la/ em {href}")
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
        n_listas = len(re.findall(r'class="radar-list"', text))
        n_notas = text.count("Links de afiliado")
        if legendas:
            if n_listas != n_notas:
                errors.append(
                    f"{rel}: {n_listas} listas de produtos e {n_notas} notas 'Links de afiliado'"
                )
        elif n_notas:
            errors.append(f"{rel}: nota 'Links de afiliado' com legendas desligadas")
        for block in parser.affiliate_blocks:
            legenda = block["text"]
            if "Ver no Mercado Livre" not in legenda:
                errors.append(f"{rel}: botão sem 'Ver no Mercado Livre'")
            tem_legenda = "Link de afiliado" in legenda and "indisponível" not in legenda
            if legendas and not block["in_list"] and not tem_legenda:
                errors.append(f"{rel}: botão sem a legenda 'Link de afiliado'")
            if not legendas and tem_legenda:
                errors.append(f"{rel}: legenda 'Link de afiliado' com legendas desligadas")
        if "/radar/" in "/" + rel or rel.startswith("radar/"):
            if DISCLOSURE not in text:
                errors.append(f"{rel}: post sem o aviso de transparência")
            if 'class="disclosure"' not in text:
                errors.append(f"{rel}: post sem aside de disclosure")
            else:
                disc = text.find('class="disclosure"')
                h1 = text.find("<h1")
                fontes = re.search(r"<h2[^>]*>\s*Fontes", text)
                if h1 != -1 and disc < h1:
                    errors.append(f"{rel}: aviso de transparência antes do título")
                if fontes is None or disc > fontes.start():
                    errors.append(
                        f"{rel}: aviso de transparência deve vir antes de Fontes"
                    )
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
    checagens_18(root, errors)
    checagens_limites(root, errors)
    avisos: list[str] = []
    checagens_precos(root, errors, avisos)
    if v3:
        checagens_v3(root, errors)
    if avisos:
        print("\n".join(f"aviso: {item}" for item in avisos))
    if errors:
        print("\n".join(errors))
        return 1
    print(f"ok: {len(files)} páginas")
    return 0


if __name__ == "__main__":
    args = [item for item in sys.argv[1:] if item != "--v3"]
    site = Path(args[0] if args else "_site")
    sys.exit(main(site, v3="--v3" in sys.argv[1:]))
