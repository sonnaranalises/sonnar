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
affiliate_label: "Página do anúncio"
# Endereço https completo. Sem encurtador. Sem exemplo.com numa análise real.
affiliate_url: "https://www.mercadolivre.com.br/..."
# Vazio se não houver nota. Use ponto: 4.2 vira 4,2 na página.
rating_score:
rating_count: "0 avaliações na fonte, consultadas em AAAA-MM-DD"
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
  Se o preço do dia parece alto, coerente ou baixo. Separe isso da qualidade. Sem conselho de compra.
price_history:
  source: "FarejaPreço"
  source_url: "https://..."
  text: |
    O que a série mostra, com a fonte citada. Apague o bloco price_history inteiro se não houver série.
comparisons:
  - name: "Produto parecido, outra marca"
    note: |
      O que muda em relação ao destaque, sem eleger vencedor.
  - name: "Outro produto parecido, outra marca"
    note: |
      Segunda comparação curta.
conclusion: |
  Fecho neutro. Sem recomendação de compra. Qualidade e preço continuam separados.
complements:
  - name: "Complemento 1"
    price: "R$ 0,00"
    label: "Página do anúncio"
    url: "https://www.mercadolivre.com.br/..."
  - name: "Complemento 2"
    price: "R$ 0,00"
    label: "Página do anúncio"
    url: "https://www.mercadolivre.com.br/..."
  - name: "Complemento 3"
    price: "R$ 0,00"
    label: "Página do anúncio"
    url: "https://www.mercadolivre.com.br/..."
  - name: "Complemento 4"
    price: "R$ 0,00"
    label: "Página do anúncio"
    url: "https://www.mercadolivre.com.br/..."
---

Apresentação do produto em Markdown. Diga o que ele é e para que serve, sem copiar o anúncio.

Não use convite de compra, urgência ou ataque a marca. Dado não confirmado não entra.
