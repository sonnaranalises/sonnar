# Sonnar Análises

Site do Radar do dia. Slogan: **Detectando boas escolhas**.

Análises de produto em português, com links de afiliado do Mercado Livre identificados. Não é anúncio com pressa: o texto pode criticar o produto, não ataca marca, e quem decide é quem lê.

Endereço previsto: <https://sonnaranalises.github.io/sonnar/>

As cores seguem o brand book v1.2: Electric Teal `#00AEBB`, Warm Ivory `#EBE4D3`, Ink Black `#031211`. O sinal do favicon usa essa paleta. O brand book diz que a arte do logotipo não está no documento; quando a arte oficial existir, troque `assets/favicon.svg`, `assets/favicon-32.png`, `assets/apple-touch-icon.png` e `assets/og.png`.

## Nova análise

Cada Radar do dia é um arquivo em `_posts`.

1. Copie `modelos/radar-do-dia.md` para `_posts/AAAA-MM-DD-nome-curto.md`.
2. Preencha o cabeçalho. O texto depois do segundo `---` é a apresentação do produto.
3. Use quatro complementos, só com nome, preço e link. Sem análise neles.
4. Links de afiliado: endereço `https` completo do Mercado Livre, sem encurtador. O botão é sempre "Ver no Mercado Livre", com a legenda "Link de afiliado" embaixo. O topo da página traz o aviso de transparência.
5. Data, hora e fonte da consulta vão nos campos `rating_source`, `rating_checked`, `price_checked` e, no histórico, `price_history.source`, `source_url` e `checked_on`. Eles aparecem em nota sob a seção e no rodapé Fontes. Não escreva isso no parágrafo.
6. Deixe `example: true` enquanto for teste. Passe para `example: false` só quando preço, nota e comentários forem reais. Com `example: true` a página avisa que os dados são fictícios e não entra no sitemap.

Regras do texto: linguagem direta; qualidade e preço em separado; conclusão sem recomendação de compra; dado não confirmado não entra; crítica ao produto, não à marca.

O arquivo `_posts/2026-11-07-exemplo-bateria-portatil.md` é um exemplo de formato. Pode apagar quando a primeira análise real entrar.

## Ver no computador

É preciso Ruby 3.

```bash
gem install jekyll:4.3.4 webrick:1.8.2 kramdown-parser-gfm:1.1.0
jekyll serve --baseurl /sonnar
```

Abra <http://127.0.0.1:4000/sonnar/>.

O `baseurl` em `_config.yml` é `/sonnar`. Se o site passar a morar na raiz de um domínio, deixe `baseurl: ""`.

## Publicar

O workflow `.github/workflows/pages.yml` gera o site e envia ao GitHub Pages a cada push na branch `main`.

Quem administra o repositório precisa ligar o Pages uma vez:

1. Abra o repositório no GitHub.
2. Vá em **Settings → Pages**.
3. Em **Build and deployment**, no campo **Source**, escolha **GitHub Actions**.
4. Salve, se o GitHub pedir.
5. Abra a aba **Actions** e acompanhe o workflow **Publicar o site**.

Se o workflow tiver falhado antes dessa opção existir, use **Re-run** depois de salvá-la. Se Actions estiver desligado no repositório, em **Settings → Actions → General** permita actions e volte ao passo 2.

Não escolha ao mesmo tempo **Deploy from a branch**: a publicação deste repositório é a do workflow.

Quando o deploy termina, o site fica em <https://sonnaranalises.github.io/sonnar/>.

Não há JavaScript, analytics nem cookies do projeto. As fontes (Michroma no logotipo, Space Grotesk nos títulos, Inter no texto, IBM Plex Mono nos dados) estão em `assets/fonts/`, sob a licença OFL, em `assets/fonts/licenses/`.
