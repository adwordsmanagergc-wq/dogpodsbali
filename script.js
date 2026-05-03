// Dharma's Dog Pods — interactive bits

const WA_NUMBER = "6281808029595";

function waLink(message) {
  return `https://wa.me/${WA_NUMBER}?text=${encodeURIComponent(message)}`;
}

// ---- Mobile nav toggle ----
document.addEventListener("DOMContentLoaded", () => {
  const toggle = document.querySelector(".nav-toggle");
  const menu = document.querySelector(".nav-menu");
  if (toggle && menu) {
    toggle.addEventListener("click", () => {
      const expanded = toggle.getAttribute("aria-expanded") === "true";
      toggle.setAttribute("aria-expanded", String(!expanded));
      menu.classList.toggle("hidden");
    });
  }

  // ---- Gallery lightbox ----
  const lightbox = document.getElementById("lightbox");
  if (lightbox) {
    const lightboxImg = lightbox.querySelector("img");
    const closeBtn = lightbox.querySelector("button.close");

    document.querySelectorAll(".gallery-item").forEach((el) => {
      el.addEventListener("click", () => {
        const img = el.querySelector("img");
        if (!img) return;
        lightboxImg.src = img.src;
        lightboxImg.alt = img.alt;
        lightbox.classList.add("open");
        lightbox.setAttribute("aria-hidden", "false");
      });
      el.addEventListener("keydown", (e) => {
        if (e.key === "Enter" || e.key === " ") {
          e.preventDefault();
          el.click();
        }
      });
    });

    const closeLightbox = () => {
      lightbox.classList.remove("open");
      lightbox.setAttribute("aria-hidden", "true");
      lightboxImg.src = "";
    };
    if (closeBtn) closeBtn.addEventListener("click", closeLightbox);
    lightbox.addEventListener("click", (e) => {
      if (e.target === lightbox) closeLightbox();
    });
    document.addEventListener("keydown", (e) => {
      if (e.key === "Escape" && lightbox.classList.contains("open")) closeLightbox();
    });
  }

  // ---- Contact form -> WhatsApp deep link ----
  const form = document.getElementById("contact-form");
  if (form) {
    form.addEventListener("submit", (e) => {
      e.preventDefault();
      const data = new FormData(form);
      const name = (data.get("name") || "").toString().trim();
      const bike = (data.get("bike") || "").toString().trim();
      const dog = (data.get("dog") || "").toString().trim();
      const msg  = (data.get("message") || "").toString().trim();

      const lines = [
        `Hi Dharma, I'd like a quote for a custom dog pod.`,
        name ? `Name: ${name}` : null,
        bike ? `Bike: ${bike}` : null,
        dog  ? `Dog size: ${dog}` : null,
        msg  ? `Notes: ${msg}` : null,
      ].filter(Boolean);

      window.open(waLink(lines.join("\n")), "_blank", "noopener");
    });
  }

  // ---- Hero slideshow ----
  document.querySelectorAll(".hero-slideshow").forEach((show) => {
    const slides = show.querySelectorAll(".hero-slide");
    if (slides.length < 2) return;
    const interval = parseInt(show.dataset.interval || "4000", 10);
    let i = 0;
    setInterval(() => {
      slides[i].classList.remove("is-active");
      i = (i + 1) % slides.length;
      slides[i].classList.add("is-active");
    }, interval);
  });

  // ---- Year in footer ----
  const yearEl = document.getElementById("year");
  if (yearEl) yearEl.textContent = new Date().getFullYear();
});
