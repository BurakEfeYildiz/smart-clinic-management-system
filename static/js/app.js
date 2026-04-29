function showNotImplementedMessage() {
  const toast = document.getElementById("notImplementedToast");
  if (!toast) return;

  toast.classList.add("visible");
  window.clearTimeout(window.notImplementedTimer);
  window.notImplementedTimer = window.setTimeout(() => {
    toast.classList.remove("visible");
  }, 2600);
}

document.querySelectorAll("[data-not-implemented]").forEach((element) => {
  element.addEventListener("click", (event) => {
    event.preventDefault();
    showNotImplementedMessage();
  });
});

const roleSelect = document.querySelector("[data-role-select]");
if (roleSelect) {
  const rolePanels = document.querySelectorAll("[data-role-panel]");
  const roleInputs = document.querySelectorAll("[data-role-required]");
  const phoneInput = document.getElementById("phone");

  const syncRolePanels = () => {
    const role = roleSelect.value;

    rolePanels.forEach((panel) => {
      const isActive = panel.dataset.rolePanel === role;
      panel.hidden = !isActive;
      panel.style.display = isActive ? "grid" : "none";
    });

    roleInputs.forEach((input) => {
      input.required = input.dataset.roleRequired === role;
    });

    if (phoneInput) {
      phoneInput.required = role === "patient" || role === "secretary";
    }
  };

  roleSelect.addEventListener("change", syncRolePanels);
  syncRolePanels();
}
