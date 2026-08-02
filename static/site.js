(() => {
  const recipeGrid = document.querySelector("#recipeGrid");

  if (recipeGrid) {
    const cards = [...recipeGrid.querySelectorAll(".recipe-card")];
    const searchInput = document.querySelector("#searchInput");
    const filterButtons = [...document.querySelectorAll("[data-filter]")];
    const resultSummary = document.querySelector("#resultSummary");
    const clearFilters = document.querySelector("#clearFilters");
    const emptyState = document.querySelector("#emptyState");
    const emptyClear = document.querySelector("#emptyClear");
    const randomButton = document.querySelector("#randomBtn");
    const filterPanel = document.querySelector("#filterPanel");
    const filterToggle = document.querySelector("#filterToggle");
    const filterRow = document.querySelector("#filterOptions");
    const mobileLayout = window.matchMedia("(max-width: 600px)");
    const initialTag = new URLSearchParams(window.location.search).get("tag")?.trim().toLowerCase();
    let activeFilter = "all";

    const setFilterPanelOpen = (isOpen) => {
      if (!filterPanel || !filterToggle) return;
      const open = !mobileLayout.matches || isOpen;
      filterPanel.classList.toggle("is-open", open);
      filterToggle.setAttribute("aria-expanded", String(open));
    };

    const syncFilterPanel = () => {
      setFilterPanelOpen(Boolean(initialTag));
    };

    if (initialTag && !filterButtons.some((button) => button.dataset.filter === initialTag)) {
      const activeTagButton = document.createElement("button");
      activeTagButton.className = "filter-chip is-active";
      activeTagButton.type = "button";
      activeTagButton.dataset.filter = initialTag;
      activeTagButton.setAttribute("aria-pressed", "true");
      activeTagButton.textContent = initialTag;
      filterRow.append(activeTagButton);
      filterButtons.push(activeTagButton);
    }

    filterToggle?.addEventListener("click", () => {
      if (!mobileLayout.matches) return;
      setFilterPanelOpen(!filterPanel.classList.contains("is-open"));
    });

    if (typeof mobileLayout.addEventListener === "function") {
      mobileLayout.addEventListener("change", syncFilterPanel);
    } else {
      mobileLayout.addListener(syncFilterPanel);
    }

    syncFilterPanel();

    const setActiveFilter = (filter, updateUrl = false) => {
      activeFilter = filter || "all";
      filterButtons.forEach((filterButton) => {
        const isActive = filterButton.dataset.filter === activeFilter;
        filterButton.classList.toggle("is-active", isActive);
        filterButton.setAttribute("aria-pressed", String(isActive));
      });

      if (updateUrl) {
        const url = new URL(window.location.href);
        if (activeFilter === "all") {
          url.searchParams.delete("tag");
        } else {
          url.searchParams.set("tag", activeFilter);
        }
        window.history.replaceState({}, "", url);
      }
    };

    const updateResults = () => {
      const query = searchInput.value.trim().toLowerCase();
      let visibleCount = 0;

      cards.forEach((card) => {
        const matchesQuery = !query || card.dataset.search.includes(query);
        const tags = card.dataset.tags.split("|").filter(Boolean);
        const matchesFilter = activeFilter === "all" || tags.includes(activeFilter);
        const isVisible = matchesQuery && matchesFilter;

        card.hidden = !isVisible;
        if (isVisible) visibleCount += 1;
      });

      resultSummary.replaceChildren(document.createTextNode("showing "));
      const countElement = document.createElement("strong");
      countElement.textContent = String(visibleCount);
      resultSummary.append(countElement);
      resultSummary.append(document.createTextNode(` ${visibleCount === 1 ? "recipe" : "recipes"}`));
      if (activeFilter !== "all") {
        resultSummary.append(document.createTextNode(` tagged ${activeFilter}`));
      }
      emptyState.hidden = visibleCount !== 0;
      clearFilters.hidden = !query && activeFilter === "all";
      randomButton.disabled = visibleCount === 0;
    };

    searchInput.addEventListener("input", updateResults);

    filterButtons.forEach((button) => {
      button.addEventListener("click", () => {
        const nextFilter = button.dataset.filter === activeFilter ? "all" : button.dataset.filter;
        setActiveFilter(nextFilter, true);
        updateResults();
      });
    });

    const resetFilters = () => {
      searchInput.value = "";
      setActiveFilter("all", true);
      updateResults();
      searchInput.focus();
    };

    clearFilters.addEventListener("click", resetFilters);
    emptyClear.addEventListener("click", resetFilters);

    randomButton.addEventListener("click", () => {
      const visibleCards = cards.filter((card) => !card.hidden);
      if (!visibleCards.length) return;
      const randomCard = visibleCards[Math.floor(Math.random() * visibleCards.length)];
      window.location.href = randomCard.querySelector("a").href;
    });

    setActiveFilter(initialTag);
    updateResults();
  }

  const recipeId = document.body.dataset.recipeId;
  const ingredients = [...document.querySelectorAll("[data-ingredient-index]")];

  if (recipeId && ingredients.length) {
    const storageKey = `noras-kitchen:checked:${recipeId}`;

    const readChecked = () => {
      try {
        return JSON.parse(window.localStorage.getItem(storageKey) || "[]");
      } catch (_error) {
        return [];
      }
    };

    const saveChecked = () => {
      const checked = ingredients
        .filter((ingredient) => ingredient.checked)
        .map((ingredient) => ingredient.dataset.ingredientIndex);
      try {
        window.localStorage.setItem(storageKey, JSON.stringify(checked));
      } catch (_error) {
        // Checklist still works for the current page if storage is unavailable.
      }
    };

    const checked = readChecked();
    ingredients.forEach((ingredient) => {
      ingredient.checked = checked.includes(ingredient.dataset.ingredientIndex);
      ingredient.addEventListener("change", saveChecked);
    });

    document.querySelector('[data-action="reset-checklist"]')?.addEventListener("click", () => {
      ingredients.forEach((ingredient) => {
        ingredient.checked = false;
      });
      try {
        window.localStorage.removeItem(storageKey);
      } catch (_error) {
        // No action needed when storage is unavailable.
      }
    });
  }

  document.querySelector('[data-action="print"]')?.addEventListener("click", () => {
    window.print();
  });

  const shareButton = document.querySelector('[data-action="share"]');
  if (shareButton) {
    const canCopy = navigator.clipboard && typeof navigator.clipboard.writeText === "function";
    if (!navigator.share && !canCopy) {
      shareButton.hidden = true;
    } else {
      shareButton.addEventListener("click", async () => {
        try {
          if (navigator.share) {
            await navigator.share({ title: document.title, url: window.location.href });
          } else if (canCopy) {
            await navigator.clipboard.writeText(window.location.href);
            shareButton.innerHTML = "link copied <span aria-hidden=\"true\">✓</span>";
            window.setTimeout(() => {
              shareButton.innerHTML = "share recipe <span aria-hidden=\"true\">↗</span>";
            }, 1800);
          }
        } catch (_error) {
          // User cancelled native share or clipboard was unavailable.
        }
      });
    }
  }
})();
