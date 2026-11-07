# Sonnar Análises — guia vivo da marca · v2

Atualizado em 07/11/2026 (Brasília). Este guia substitui o PDF de rascunho e as orientações visuais anteriores. Nome: **Sonnar Análises**, sempre com dois Ns e acento. Slogan: **Te ajudando a detectar boas escolhas**.

## Identidade e propósito

Organizamos informações reais sobre produtos, opiniões de compradores e histórico de preço. Não simulamos experiência pessoal, não recomendamos a compra e não criamos urgência. A primeira versão usa links de afiliado do Mercado Livre. Produto e preço são analisados separadamente; uma crítica nunca vira ataque à marca.

No site e no texto institucional, usar o nome completo. No topo das artes, usar apenas **SONNAR**. O título do relatório apresenta o quadro: **Radar do dia · Análise Sonnar**. O subtítulo identifica o produto e sua categoria. O slogan fica no rodapé da página: **Sonnar Análises — Te ajudando a detectar boas escolhas**; não ocupa a área de título do relatório.

## Paleta e contraste

| Cor | Hex | Papel |
|---|---|---|
| Floral White | #fffcf2 | Fundo principal do site e texto claro nas artes escuras |
| Silver | #ccc5b9 | Bordas, divisórias, fundo da caixa de transparência; legendas sobre fundo escuro |
| Charcoal Brown | #403d39 | Texto secundário sobre fundo claro; fundo do cabeçalho/rodapé com texto Floral White |
| Carbon Black | #252422 | Texto principal; fundo das artes; texto dos botões Paprika |
| Spicy Paprika | #eb5e28 | Sinal do logo, botões, faixas de destaque e números em contexto acessível |

Não sobra teal, marfim ou preto da paleta antiga em CSS, SVG, favicons, imagens de compartilhamento e peças novas. Cores originais das embalagens nas fotos não são recoloridas.

Exigir WCAG AA: texto Carbon Black sobre Paprika; texto Carbon Black sobre fundo Silver na transparência. Sobre Floral White, Paprika não serve para texto pequeno: usar faixa Paprika com texto Carbon Black, sublinhado ou outro destaque que preserve o contraste. Números grandes/bold só podem ser Paprika quando atingirem contraste de 3:1. Legendas Silver são para fundo escuro; em fundo claro, usar Charcoal Brown.

## Tipografia

- Michroma: logotipo e títulos de marca.
- Space Grotesk: títulos editoriais e nomes de produto.
- Inter: texto e interface.
- IBM Plex Mono: preços, notas, contagens e volumes.

Manter fontes locais e licenças OFL. Não usar Orbitron como substituta.

## Logotipo

A marca aprovada é o S de ondas de sonar, com o ponto em Spicy Paprika `#eb5e28` e o campo em Carbon Black `#252422`. As ondas são Floral White; a onda interna é um cinza mais baixo. O arquivo completo traz o ícone e a palavra **sonnar** em minúsculas, na mesma cor clara.

Arquivos no repositório, em `assets/brand/`:

- `sonnar-icone-perfil-1024.png` — só o ícone, 1024 px.
- `sonnar-logo-completa-1024.png` — ícone e a palavra sonnar, 1024 px.
- Favicons gerados a partir do ícone: `favicon.ico`, 32 px, 180 px (apple-touch), 192 px e 512 px.

No cabeçalho do site, o ícone fica ao lado do nome Sonnar Análises, entre 28 e 36 px. O cabeçalho é escuro (Charcoal Brown), então o ícone entra com o próprio fundo Carbon Black, em cantos levemente arredondados. Em fundo claro, o ícone precisa de um tile ou círculo Carbon Black para o S claro não sumir.

A imagem padrão de Open Graph e Twitter, quando o post não tem imagem própria, é a logo completa centralizada em campo Carbon Black (`assets/og.png`). Não redesenhar as ondas nem trocar a cor do ponto.

## Site e bloco de produtos

Logo abaixo da transparência, o bloco **Produtos no radar do dia** tem cinco linhas compactas: nome com categoria, preço, botão pequeno **Ver no Mercado Livre** e legenda **Link de afiliado**. Não criar cartões grandes, descrições, fotos ou parágrafos separados nesse bloco. A meta é cerca de um terço da altura anterior em tela equivalente. Em celular, permitir duas linhas por item sem rolagem horizontal nem texto minúsculo.

O começo da análise dá destaque conjunto a **4,9/5** e **122.968 opiniões**. Usar cor também para preço e características-chave, sem depender apenas de negrito nem apenas de cor para transmitir significado.

## Regras editoriais

1. Não publicar números da amostra de comentários. A contagem total de opiniões do anúncio pode e deve aparecer.
2. Não julgar desconto ou preço de referência. Mostrar menor, média e maior do histórico e o preço do anúncio sem juízo sobre o desconto.
3. Fontes, datas e horários ficam em notas curtas com asterisco e tipo menor. Horários em Brasília.
4. Comparar por posicionamento, sem nomear concorrentes. Usar equivalentes reais e omitir comparações sem dados.
5. Fechar com convite gentil para avaliar as informações. Nunca escrever “a decisão é sua”.
6. Usar linguagem simples, frases curtas, sem “ND”, jargão desnecessário ou nomes de arquivos internos.
7. Transparência fica no topo do relatório: “Transparência: os links desta página são de afiliado. Se eles forem úteis pra você, a comissão ajuda a Sonnar a continuar no ar, sem custo adicional na sua compra e sem influenciar o que escrevemos.” Cada botão de afiliado recebe a legenda “Link de afiliado”. Nunca usar “#publi · Link de afiliado”.
8. Suspeitas de compradores são relatos, não fatos. Não insinuar falsificação a partir de queixas sobre lacre.
9. Não acrescentar sermões ou ressalvas genéricas como “nota alta não garante…” ou “são percepções… não comprovam tratamento…”.
10. Opiniões positivas e críticas são resumidas em parágrafos, seguidos de 1–3 citações literais, reais e anônimas por seção. Nunca inventar depoimentos.
11. Usar “Produtos no radar do dia”, não “Complementares”.
12. O acesso aos cinco produtos fica logo após a transparência. A legenda do Instagram aponta para o relatório no link da bio.
13. O título é o quadro da Sonnar Análises; o subtítulo é o produto com categoria correta, confirmada na fonte, não um nome comercial incompreensível.
14. Dar peso proporcional à avaliação geral. Nota e quantidade total aparecem cedo e com destaque; críticas seguem honestas sem dominar a síntese.
15. Aplicar a nova paleta a site, logo e redes. Destacar preço, nota e contagem com cor acessível.
16. Instruções internas não viram fechamento público. Remover “A comissão de afiliado não define a pauta nem o texto. Quem decide é quem lê.”; encerrar a página com a marca e o slogan no rodapé.
17. Páginas Radar, Sobre, Transparência e Privacidade usam linguagem humana. Não alegar ausência de cookies ou rastreamento além do que foi tecnicamente verificado. O radar só roda por comando. Enquanto houver revisão manual, publicar após essa revisão, sem pedir autorizações repetidas para as etapas já liberadas. Máximo de dois ciclos de correção.

## Artes

Instagram: cinco imagens 1080 × 1350, uma por produto, destaque primeiro. X: uma imagem 1600 × 900 do destaque. Todas levam SONNAR no topo, categoria, nome e preço. O destaque leva também nota e quantidade total de opiniões. Fotos reais do produto podem ser utilizadas sem alterar a embalagem; não inventar mockups ou simular uso. Se não houver foto de origem confirmada, usar composição tipográfica limpa.

Não incluir “Análises” no topo, data/hora de preço, “Link de afiliado”, “Mercado Livre”, “Loja oficial” ou marcas do marketplace. Não usar preço riscado, de/por, percentual de desconto, urgência ou recomendação de compra. Revisar cada PNG visualmente antes da entrega.

## Redes

X: nome com categoria; depois “Leia o nosso relatório para ver o que aparece nos elogios, nas críticas e no histórico de preço: [URL]”; 2–4 hashtags relevantes. Até 280 caracteres ponderados, links com 23. Publicar com a imagem, não apenas o link.

Instagram: destaque curto do produto e convite ao relatório no link da bio. Carrossel de cinco peças; 5–10 hashtags relevantes. Sem lista de preços, texto de transparência ou menção à loja do Mercado Livre. Hashtags ajudam a categorizar o conteúdo; não prometer alcance.

## Papéis e validação

A coordenação recebe o comando, distribui pesquisa, seleção, análise, redação, arte, revisão e publicação. Arte e pesquisa podem correr em paralelo; a redação usa a pesquisa; a revisão verifica dados, fontes, texto e arquivos finais. A publicação não altera o material validado. As responsabilidades dos nove papéis existentes são preservadas; as regras v2 acima prevalecem em qualquer conflito com documentos anteriores.
