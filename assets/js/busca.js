(function () {
  // A busca roda no navegador. O que é digitado não é enviado nem registrado.
  var form = document.querySelector("form.busca");
  if (!form) return;
  var campo = form.querySelector(".busca-campo");
  var status = form.querySelector(".busca-status");
  var lista = form.querySelector(".busca-resultados");
  var url = form.getAttribute("data-busca-url");
  if (!campo || !status || !lista || !url) return;

  var meses = ["janeiro", "fevereiro", "março", "abril", "maio", "junho", "julho", "agosto", "setembro", "outubro", "novembro", "dezembro"];
  var itens = null;
  var pedido = null;

  function normalizar(s) {
    return String(s || "")
      .toLowerCase()
      .normalize("NFD")
      .replace(/[\u0300-\u036f]/g, "");
  }

  function textoDe(item) {
    var extra = "";
    var resumo = item.resumo;
    if (resumo && typeof resumo === "object") {
      extra = Object.keys(resumo).map(function (k) { return resumo[k]; }).join(" ");
    } else if (typeof resumo === "string") {
      extra = resumo;
    }
    return normalizar([
      item.title, item.subtitle, item.tema, item.tipo, item.categoria, item.summary, extra
    ].join(" "));
  }

  function dataPt(iso) {
    var partes = String(iso || "").split("-");
    if (partes.length !== 3) return "";
    var mes = meses[parseInt(partes[1], 10) - 1];
    if (!mes) return "";
    return parseInt(partes[2], 10) + " de " + mes + " de " + partes[0];
  }

  function urlOk(u) {
    return typeof u === "string" && u.charAt(0) === "/" && u.charAt(1) !== "/";
  }

  function limpar() {
    status.textContent = "";
    lista.textContent = "";
  }

  function noTitulo(item, palavras) {
    var t = normalizar(item.title);
    for (var i = 0; i < palavras.length; i++) {
      if (t.indexOf(palavras[i]) === -1) return false;
    }
    return true;
  }

  function mostrar(consulta) {
    var palavras = normalizar(consulta).split(/\s+/).filter(Boolean);
    lista.textContent = "";
    if (!palavras.length) {
      status.textContent = "";
      return;
    }
    var achados = itens.filter(function (item) {
      var texto = textoDe(item);
      for (var i = 0; i < palavras.length; i++) {
        if (texto.indexOf(palavras[i]) === -1) return false;
      }
      return urlOk(item.url);
    });
    achados.sort(function (a, b) {
      var at = noTitulo(a, palavras) ? 1 : 0;
      var bt = noTitulo(b, palavras) ? 1 : 0;
      if (at !== bt) return bt - at;
      if (a.date < b.date) return 1;
      if (a.date > b.date) return -1;
      return 0;
    });
    achados = achados.slice(0, 8);
    if (!achados.length) {
      status.textContent = "Nenhum relatório encontrado";
      return;
    }
    status.textContent = achados.length === 1 ? "1 resultado" : achados.length + " resultados";
    achados.forEach(function (item) {
      var li = document.createElement("li");
      var a = document.createElement("a");
      var titulo = document.createElement("span");
      var data = document.createElement("span");
      titulo.className = "busca-item-titulo";
      data.className = "busca-item-data";
      titulo.textContent = item.title || "";
      data.textContent = dataPt(item.date);
      a.setAttribute("href", item.url);
      a.appendChild(titulo);
      if (data.textContent) a.appendChild(data);
      li.appendChild(a);
      lista.appendChild(li);
    });
  }

  function carregar() {
    if (itens) return Promise.resolve(itens);
    if (pedido) return pedido;
    pedido = fetch(url, { headers: { Accept: "application/json" } })
      .then(function (resposta) {
        if (!resposta.ok) throw new Error("rede");
        return resposta.json();
      })
      .then(function (dados) {
        if (!Array.isArray(dados)) throw new Error("rede");
        itens = dados;
        return itens;
      })
      .catch(function () {
        pedido = null;
        status.textContent = "Não foi possível carregar a busca. Verifique a conexão e tente de novo.";
        lista.textContent = "";
        throw new Error("rede");
      });
    return pedido;
  }

  function agendar() {
    var consulta = campo.value;
    carregar().then(function () {
      if (campo.value !== consulta) return;
      mostrar(consulta);
    }).catch(function () {});
  }

  campo.addEventListener("focus", agendar);
  campo.addEventListener("input", agendar);
  campo.addEventListener("keydown", function (ev) {
    if (ev.key !== "Escape") return;
    campo.value = "";
    limpar();
  });
  form.addEventListener("submit", function (ev) {
    ev.preventDefault();
  });
})();
