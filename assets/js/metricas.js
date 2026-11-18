(function () {
  var cfg = window.SONNAR_METRICAS || {};
  if (!cfg.url || !cfg.key) return;
  // Só mede no site publicado (não mede build local nem pré-visualização).
  if (location.hostname !== cfg.host) return;
  // Respeita "não rastrear" e o Global Privacy Control.
  if (navigator.doNotTrack === "1" || navigator.globalPrivacyControl === true) return;

  function device() {
    var w = window.innerWidth || document.documentElement.clientWidth || 0;
    return w < 768 ? "mobile" : (w < 1200 ? "tablet" : "desktop");
  }
  function referrerHost() {
    try {
      if (!document.referrer) return null;
      var h = new URL(document.referrer).hostname;
      return h === location.hostname ? "interno" : h.slice(0, 200);
    } catch (e) { return null; }
  }
  function tema() {
    return document.documentElement.getAttribute("data-tema") === "escuro" ? "escuro" : "claro";
  }
  function send(table, row) {
    try {
      fetch(cfg.url.replace(/\/+$/, "") + "/rest/v1/" + table, {
        method: "POST",
        keepalive: true,
        headers: {
          apikey: cfg.key,
          Authorization: "Bearer " + cfg.key,
          "Content-Type": "application/json",
          Prefer: "return=minimal"
        },
        body: JSON.stringify(row)
      }).catch(function () {});
    } catch (e) {}
  }

  var pagina = location.pathname.slice(0, 300);
  var slug = cfg.slug || null;

  // 1) Visita: uma por carregamento de página.
  send("eventos", { tipo: "visita", pagina: pagina, post_slug: slug, referrer: referrerHost(), device: device(), tema: tema() });

  // 2) Leitura até a conclusão: uma vez por carregamento, quando 40% da seção aparece na tela.
  var concl = document.querySelector(".conclusion");
  if (concl && "IntersectionObserver" in window) {
    var io = new IntersectionObserver(function (entries) {
      for (var i = 0; i < entries.length; i++) {
        if (entries[i].isIntersecting) {
          send("eventos", { tipo: "leu_conclusao", pagina: pagina, post_slug: slug, referrer: referrerHost(), device: device(), tema: tema() });
          io.disconnect();
          break;
        }
      }
    }, { threshold: 0.4 });
    io.observe(concl);
  }

  // 3) Clique no botão de afiliado ou no link do título.
  // A tabela cliques só grava local se ele estiver nesta lista.
  // Hoje o banco aceita lista, lateral, fim, resumo e titulo.
  // Um data-local desconhecido é registrado como 'lista'.
  // Se o banco ganhar outro valor, basta incluí-lo aqui.
  var LOCAIS_OK = ["lista", "lateral", "fim", "resumo", "titulo"];
  document.addEventListener("click", function (ev) {
    var a = ev.target && ev.target.closest ? ev.target.closest("a.affiliate-link, a.titulo-afiliado") : null;
    if (!a || !slug) return;
    var href = a.getAttribute("href") || "";
    if (!/^https:\/\/meli\.la\/[A-Za-z0-9]{4,20}$/.test(href)) return;
    var pos = parseInt(a.getAttribute("data-posicao"), 10);
    if (!(pos >= 1 && pos <= 5)) return;
    var local = a.getAttribute("data-local") || "lista";
    if (a.closest(".col-direita") && (window.innerWidth || 0) >= 1200) local = "lateral";
    if (LOCAIS_OK.indexOf(local) < 0) local = "lista";
    send("cliques", {
      post_slug: slug,
      posicao: pos,
      produto: (a.getAttribute("data-produto") || "").slice(0, 200) || null,
      destino: href,
      local: local,
      pagina: pagina,
      referrer: referrerHost(),
      device: device()
    });
  }, true);
})();
