# Sonnar Análises · guia vivo da marca, v3

Atualizado em 18/11/2026 (horário de Brasília). É o resumo do **brand book v2.0** (PDF oficial) e substitui o `docs/BRAND.md` v2. Se houver conflito, vale o PDF.

- **Nome e slogan:** Sonnar Análises, sempre com dois Ns. O slogan "Te ajudando a detectar boas escolhas" fica no rodapé.
- **Regra nº 1: SINCERIDADE.** O relatório analisa, pelo consumidor, os dados de um produto. É baseado em dados concretos e sinceros, não em opinião. Ele dá direção, mas nunca diz "compre", "não perca" ou "escolhemos".

## Paleta: só 4 cores

| Cor | Hex | Papel |
|---|---|---|
| Carbon Black | #1A1B1F | Texto no tema claro; fundo no tema escuro; cabeçalho e rodapé |
| Cerulean | #367588 | Títulos, destaques, sublinhados, faixas, botões; links e números no tema claro |
| White | #FBFDFF | Fundo no tema claro e nas artes; texto no tema escuro; cartão das fotos |
| Pacific Blue | #5BA3B8 | Texto pequeno, links e números sobre fundo escuro. Não usar em texto sobre fundo claro (2,8:1) |

**Neutros:** só como transparências dessas cores.

- Texto secundário: Carbon a 72% (#595A5E).
- Fios: Carbon a 12% (#E0E2E4).
- Caixas: Cerulean a 8% (#EBF2F5).
- No tema escuro: White a 70% e White a 14%, e Pacific a 8%.

## Tipografia

- **Michroma:** só no logo e na palavra SONNAR.
- **Space Grotesk:** títulos.
- **Inter:** texto.
- **IBM Plex Mono:** números.

## Logo

- Campo em #1A1B1F, ondas em #FBFDFF, onda interna em White a 70% e ponto em #5BA3B8.
- No cabeçalho, a marca `.site-header .logo-mark` mede `calc(35px * 1.05)`, isto é, 36,75 px. O ícone do rodapé não muda.
- Arquivos em `assets/brand/`.

## Fotos

- Foto real do anúncio, com o fundo original, sobre um cartão #FBFDFF com cantos de 12 px.
- Moldura de 16 × 16rem, ou de 20 × 15rem para foto horizontal.
- Nunca alterar o produto.

## Relatório

A página do relatório fica nesta ordem:

1. Produtos no radar, com miniatura (lateral no desktop; topo no celular).
2. Título linkado, subtítulo, data e categoria.
3. Resumo, lido do front matter `resumo:`.
4. Foto e apresentação.
5. Especificações.
6. Notas e avaliações.
7. Tabela 3 + 3 de comentários.
8. Preço, com régua e 5 posições.
9. Conclusão.
10. Transparência.
11. Fontes e observações, em 0,8 rem, com a linha de IA.
12. Feedback.

O título do produto é um link de afiliado discreto (classe `titulo-afiliado`, cor do título, sublinhado só no hover e no foco). O botão do Resumo usa o mesmo destino, com a legenda "Link de afiliado".

O padrão completo está em `regras-relatorio-v2.md`.

## Categorias

Os slugs ficam em `_data/categorias.yml`. A categoria é diferente do tema do dia. Em 16/11/2026, com o OK do Vinícius, entrou também a categoria provisória `moda` (Moda e acessórios): roupas, calçados e acessórios de vestir. Ela fica sem relatório até o primeiro post dessa categoria.

## Artes

- Fundo claro.
- O tema do dia exato, em Cerulean.
- Preço em Cerulean.
- O carimbo "Preço em DD/MM, HHhMM".
- Sem riscado, sem % e sem urgência.
- Formatos:
  - Instagram: 5 imagens de 1080 × 1350.
  - X: 4 imagens.
  - Mais a arte de 1600 × 900.

## Redes

O post é uma carta de apresentação, com 2 ou 3 hashtags mais #Sonnar.

**[Pendente]** O aviso de publicidade nos posts, conforme o CONAR e os termos do afiliado do ML.

## Site

- Modo noturno.
- Coluna de 45rem.
- Lateral esquerda com as últimas análises.
- Lateral direita do relatório com os 5 produtos.
- Home: um card, o Radar do dia (o mais recente), com data e tema acima do card. Sem o kicker "Radar de hoje".
- Home, lateral direita: busca no navegador e categorias em acordeão (`details`/`summary`, fechado por padrão).
- No celular, a home fica Radar, busca e categorias, depois Últimas análises.
- Menu do celular: Privacidade sai do cabeçalho em telas de até 40 rem e continua no rodapé. Até 32 rem, os links do menu têm pelo menos 0,875 rem e área de toque de 44 px; se não couber numa linha, o menu quebra abaixo da logo.
- Sobre com a Transparência incluída.
- Medição sem cookies. O que se digita na busca não é enviado nem registrado.

## Mudanças de 18/11/2026

- Resumo no relatório, a partir de `resumo:`, com o botão "Ver no Mercado Livre" em 0,8 rem.
- Título do produto como link de afiliado (`titulo-afiliado`).
- Kicker da home: "Radar do dia", com data e tema acima do card.
- Busca local (`busca.json`) e categorias em acordeão na lateral direita da home.
- Menu do celular sem Privacidade no cabeçalho, com toque de 44 px e quebra de linha quando não cabe.
- Fontes em 0,8 rem (`12,8 px` com a raiz em 16 px), nos dois temas.
- Logo do cabeçalho mantida em 36,75 px.
