(function () {
  var root = document.querySelector("[data-reader-feedback]");
  if (!root) return;

  var form = root.querySelector(".reader-feedback-form");
  var thanks = root.querySelector(".reader-feedback-thanks");
  var error = root.querySelector(".reader-feedback-error");
  var button = form.querySelector("button[type='submit']");
  var storageKey = "sonnar-feedback:" + (root.getAttribute("data-post-url") || "");
  var sending = false;

  function showThanks() {
    document.documentElement.setAttribute("data-feedback-sent", "");
    if (thanks && typeof thanks.focus === "function") {
      thanks.focus();
    }
  }

  if (document.documentElement.hasAttribute("data-feedback-sent")) {
    return;
  }

  function setBusy(busy) {
    var controls = form.querySelectorAll("input, textarea, button");
    for (var i = 0; i < controls.length; i++) {
      controls[i].disabled = busy;
    }
    if (button) button.setAttribute("aria-busy", busy ? "true" : "false");
  }

  form.addEventListener("submit", function (event) {
    event.preventDefault();
    if (sending) return;
    if (error) error.hidden = true;
    if (!form.checkValidity()) {
      form.reportValidity();
      return;
    }

    var selected = form.querySelector("input[name='rating']:checked");
    var rating = selected ? Number(selected.value) : NaN;
    if (!Number.isInteger(rating) || rating < 1 || rating > 5) return;

    var commentField = form.querySelector("textarea[name='comment']");
    var comment = commentField ? commentField.value.replace(/^\s+|\s+$/g, "") : "";
    if (comment.length > 2000) comment = comment.slice(0, 2000);

    var title = root.getAttribute("data-post-title") || "";
    if (title.length > 300) title = title.slice(0, 300);

    var postUrl = root.getAttribute("data-post-url") || "";
    if (postUrl.length > 500) postUrl = postUrl.slice(0, 500);

    var userAgent = "";
    try {
      userAgent = String(navigator.userAgent || "").slice(0, 500);
    } catch (err) {
      userAgent = "";
    }

    var payload = {
      post_url: postUrl,
      post_title: title,
      rating: rating,
      comment: comment.length ? comment : null,
      user_agent: userAgent
    };

    var base = (root.getAttribute("data-supabase-url") || "").replace(/\/+$/, "");
    var anonKey = root.getAttribute("data-anon-key") || "";
    if (!base || !anonKey || !postUrl) {
      if (error) error.hidden = false;
      return;
    }

    sending = true;
    setBusy(true);

    fetch(base + "/rest/v1/feedbacks", {
      method: "POST",
      headers: {
        apikey: anonKey,
        Authorization: "Bearer " + anonKey,
        "Content-Type": "application/json",
        Prefer: "return=minimal"
      },
      body: JSON.stringify(payload)
    })
      .then(function (response) {
        if (!response || response.status !== 201) {
          throw new Error("status");
        }
        try {
          window.localStorage.setItem(storageKey, "1");
        } catch (err) {}
        showThanks();
      })
      .catch(function () {
        sending = false;
        setBusy(false);
        if (error) error.hidden = false;
      });
  });
})();
