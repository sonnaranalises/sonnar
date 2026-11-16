(function () {
  var root = document.documentElement;
  var botao = document.querySelector("[data-tema-botao]");
  if (!botao) return;

  function aplicar(tema) {
    if (tema !== "claro" && tema !== "escuro") tema = "claro";
    root.setAttribute("data-tema", tema);
    botao.setAttribute("aria-pressed", tema === "escuro" ? "true" : "false");
    try {
      localStorage.setItem("sonnar-tema", tema);
    } catch (e) {}
  }

  aplicar(root.getAttribute("data-tema") === "escuro" ? "escuro" : "claro");

  botao.addEventListener("click", function () {
    aplicar(root.getAttribute("data-tema") === "escuro" ? "claro" : "escuro");
  });
})();
