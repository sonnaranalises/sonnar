---
layout: post
# Deixe true enquanto os dados forem de teste. A página ganha o aviso de
# placeholder e sai do índice. Troque para false só com dados reais.
example: true
title: "Categoria Marca Modelo"
subtitle: "O que é, em poucas palavras, e para que serve."
date: 2026-11-16 12:00:00 -0300
summary: "Uma frase para a lista e para as redes."
description: "Descrição para buscadores, até cerca de 160 caracteres."
image: "/assets/img/radar/AAAA-MM-DD-slug.jpg"
image_alt: "Categoria Marca Modelo"
# image_formato: horizontal
# Só quando a foto for horizontal (largura ÷ altura acima de 1,3). Sem o campo, a moldura é quadrada.
categoria: eletroportateis
tipo: "Tipo do produto"
tema: "Tema do dia"
# Resumo lido do front matter (não do markdown). Os 4 tópicos, somados, ficam entre 50 e 80 palavras.
# util_para e atencao_de podem começar com "quem" ou não: o site não repete a palavra.
resumo:
  avaliacoes: "Nota, volume e o que esses números querem dizer."
  ponto_forte: "O elogio que mais se repete."
  ponto_atencao: "A crítica que mais se repete."
  preco: "Preço de agora e onde ele fica na faixa dos equivalentes."
  para_quem: "Um parágrafo, em duas ou três frases, no lugar de util_para e atencao_de."
# atributos (v3.2): de 4 a 6; em o_que_dizem, um retrato único que junta elogios e críticas.
# frequencia: "muitos citam" | "alguns citam" | "caso isolado"
# Sem atributos_nota. Se a amostra for filtrada (ex.: notas 1 a 3), a proporção fica dentro do próprio o_que_dizem.
  # Posts v3 sem para_quem ainda usam as duas linhas abaixo.
  # util_para: "quem busca o uso principal do produto."
  # atencao_de: "precisa do ponto que os dados não sustentam."
products:
  - name: "Produto em destaque, com categoria e marca"
    price: "R$ 0,00"
    url: "https://meli.la/XXXXXXXX"
    source_url: "https://www.mercadolivre.com.br/..."
    image: "/assets/img/radar/AAAA-MM-DD-slug.jpg"
    image_alt: "Produto em destaque, com categoria e marca"
  - name: "Complemento 2"
    price: "R$ 0,00"
    url: "https://meli.la/XXXXXXXX"
    source_url: "https://www.mercadolivre.com.br/..."
    image: "/assets/img/radar/AAAA-MM-DD-comp-2.jpg"
    image_alt: "Complemento 2"
  - name: "Complemento 3"
    price: "R$ 0,00"
    url: "https://meli.la/XXXXXXXX"
    source_url: "https://www.mercadolivre.com.br/..."
    image: "/assets/img/radar/AAAA-MM-DD-comp-3.jpg"
    image_alt: "Complemento 3"
  - name: "Complemento 4"
    price: "R$ 0,00"
    url: "https://meli.la/XXXXXXXX"
    source_url: "https://www.mercadolivre.com.br/..."
    image: "/assets/img/radar/AAAA-MM-DD-comp-4.jpg"
    image_alt: "Complemento 4"
  - name: "Complemento 5"
    price: "R$ 0,00"
    url: "https://meli.la/XXXXXXXX"
    source_url: "https://www.mercadolivre.com.br/..."
    image: "/assets/img/radar/AAAA-MM-DD-comp-5.jpg"
    image_alt: "Complemento 5"
elogios:
  - "Citação literal de elogio, até cerca de 200 caracteres."
criticas:
  - "Citação literal de crítica, até cerca de 200 caracteres."
# Se minimo e maximo forem iguais, a régua não é desenhada. Sem o bloco, também não.
regua_preco:
  produto: 0.00
  minimo: 0.00
  maximo: 0.00
  produto_txt: "R$ 0,00"
  minimo_txt: "R$ 0,00"
  maximo_txt: "R$ 0,00"
  unidade: "por unidade"
  posicao: "no meio da faixa"
fontes:
  coleta: "16/11/2026, até 12h00"
  # Se equivalentes estiver vazio ou ausente, a frase do preço some das Fontes.
  equivalentes: "produtos equivalentes da mesma categoria, porte parecido e nota parecida"
---

Apresentação em um parágrafo: nome com categoria e marca, o que o produto é, o que oferece e para quem faz sentido.

- **Rótulo:** valor, com a observação curta quando ela mudar a escolha.

## Notas e avaliações

Nota, volume, o que esses números querem dizer, e os parágrafos de elogio e de crítica. As citações literais não ficam neste texto.

<!-- tabela-comentarios -->

## Preço

Preço atual, critério dos equivalentes, mínimo, máximo e uma das cinco posições.

<!-- regua-preco -->

## Conclusão

Para quem os dados indicam que o produto serve, para quem não, e o ponto específico. O segundo parágrafo é o fecho prático.
