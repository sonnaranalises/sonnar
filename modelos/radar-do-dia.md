---
layout: post
# Deixe true enquanto os dados forem de teste. A página ganha o aviso de
# placeholder e sai do índice de busca. Troque para false só com dados reais.
example: true
title: "Nome do produto"
# Não use data futura: o Jekyll esconde o post até esse horário.
date: 2026-11-07 00:10:00 -0300
summary: "Uma frase para a lista da home."
description: "Descrição para buscadores e redes, até cerca de 160 caracteres."
marketplace: "Mercado Livre"
price_caption: "Preço visto no anúncio"
price: "R$ 0,00"
# Endereço https completo. Sem encurtador. O botão é sempre "Ver no Mercado Livre".
affiliate_url: "https://www.mercadolivre.com.br/..."
# Vazio se não houver nota. Use ponto: 4.2 vira 4,2 na página.
rating_score:
rating_count: "0 avaliações"
# Fonte e data da consulta saem numa nota, não no parágrafo.
rating_source: "Página do anúncio no Mercado Livre"
rating_checked: "7 de novembro de 2026, 10:00"
# Quando o preço foi visto. Também vai para a nota e para o rodapé de fontes.
price_checked: "7 de novembro de 2026, 10:00"
# Imagem opcional, dentro do site, com texto alternativo obrigatório.
# image: /assets/posts/foto.jpg
# image_alt: "Descrição objetiva da imagem"
specs:
  - name: "Capacidade"
    value: ""
  - name: "Peso"
    value: ""
praise: |
  O elogio que mais se repete, em linguagem comum, sem identificar quem comentou.
complaints: |
  A reclamação que mais se repete, no mesmo peso do elogio. Crítica ao produto, não à marca.
price_reading: |
  Se o preço do dia parece alto, coerente ou baixo. Separe isso da qualidade. Sem conselho de compra. Sem data neste parágrafo.
price_history:
  source: "FarejaPreço"
  source_url: "https://..."
  checked_on: "7 de novembro de 2026, 10:00"
  text: |
    O que a série mostra, sem repetir a data. Apague o bloco price_history inteiro se não houver série.
comparisons:
  - name: "Produto parecido, outra marca"
    note: |
      O que muda em relação ao destaque, sem eleger vencedor.
  - name: "Outro produto parecido, outra marca"
    note: |
      Segunda comparação curta.
conclusion: |
  Fecho neutro. Sem recomendação de compra. Qualidade e preço continuam separados.
# Lista do topo, logo após a caixa de transparência: Produtos no radar do dia.
products:
  - name: "Produto 1"
    price: "**R$ 0,00**"
    url: "https://www.mercadolivre.com.br/..."
  - name: "Produto 2"
    price: "**R$ 0,00**"
    url: "https://www.mercadolivre.com.br/..."
  - name: "Produto 3"
    price: "**R$ 0,00**"
    url: "https://www.mercadolivre.com.br/..."
  - name: "Produto 4"
    price: "**R$ 0,00**"
    url: "https://www.mercadolivre.com.br/..."
  - name: "Produto 5"
    price: "**R$ 0,00**"
    url: "https://www.mercadolivre.com.br/..."
products_note: "Preços das ofertas principais: Mercado Livre, data e hora (Brasília)."
---

Apresentação do produto em Markdown. Diga o que ele é e para que serve, sem copiar o anúncio.

Não use convite de compra, urgência ou ataque a marca. Dado não confirmado não entra. Data, hora e fonte da consulta ficam nos campos de nota, não neste texto.
