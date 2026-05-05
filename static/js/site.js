(() => {
    const root = document.documentElement;

    /* ================= THEME ================= */
    const savedTheme = localStorage.getItem("barqon-theme");
    if (savedTheme === "dark") {
        root.classList.add("theme-dark");
    }

    const syncThemeLabels = () => {
        const isDark = root.classList.contains("theme-dark");
        document.querySelectorAll("[data-theme-icon]").forEach((icon) => {
            icon.textContent = isDark ? "☀️" : "🌙";
        });
    };

    document.querySelectorAll("[data-theme-toggle]").forEach((button) => {
        button.addEventListener("click", () => {
            root.classList.toggle("theme-dark");
            localStorage.setItem(
                "barqon-theme",
                root.classList.contains("theme-dark") ? "dark" : "light"
            );
            syncThemeLabels();
        });
    });

    syncThemeLabels();

    /* ================= MENU ================= */
    document.querySelectorAll("[data-menu-toggle]").forEach((button) => {
        button.addEventListener("click", () => {
            const target = document.querySelector(button.dataset.menuToggle);
            if (!target) return;
            target.classList.toggle("is-open");
            button.setAttribute("aria-expanded", target.classList.contains("is-open"));
        });
    });

    /* ================= FORMATTER ================= */
    const pkrFormatter = new Intl.NumberFormat("en-PK", {
        style: "currency",
        currency: "PKR",
        maximumFractionDigits: 0,
    });

    /* ================= COUNTERS ================= */
    document.querySelectorAll("[data-count-to]").forEach((counter) => {
        const target = Number(counter.dataset.countTo) || 0;
        let current = 0;
        const step = Math.max(Math.ceil(target / 80), 1);

        const tick = () => {
            current = Math.min(current + step, target);
            counter.textContent = current.toLocaleString("en-PK");
            if (current < target) requestAnimationFrame(tick);
        };

        tick();
    });

    /* ================= SOLAR CALCULATOR ================= */
    const calculator = document.querySelector("[data-solar-calculator]");
    if (calculator) {
        const billInput = calculator.querySelector("[data-bill-input]");
        const tariffInput = calculator.querySelector("[data-tariff-input]");
        const lightsInput = calculator.querySelector("[data-load-lights]");
        const fansInput = calculator.querySelector("[data-load-fans]");
        const acCountInput = calculator.querySelector("[data-load-ac-count]");
        const fridgeInput = calculator.querySelector("[data-load-fridge]");
        const motorHpInput = calculator.querySelector("[data-load-motor-hp]");
        const otherInput = calculator.querySelector("[data-load-other]");
        const acConfigs = calculator.querySelector("[data-ac-configs]");

        const sizeOutput = calculator.querySelector("[data-result-size]");
        const costOutput = calculator.querySelector("[data-result-cost]");
        const savingsOutput = calculator.querySelector("[data-result-savings]");
        const roiOutput = calculator.querySelector("[data-result-roi]");
        const loadOutput = calculator.querySelector("[data-result-load]");
        const dailyOutput = calculator.querySelector("[data-result-daily]");
        const batteryOutput = calculator.querySelector("[data-result-battery]");
        const panelsOutput = calculator.querySelector("[data-result-panels]");

        const modeButtons = Array.from(document.querySelectorAll("[data-calc-mode]"));
        const panels = Array.from(document.querySelectorAll("[data-calc-panel]"));

        let activeMode = "bill";

        const numberValue = (input, fallback = 0) =>
            Math.max(Number(input?.value) || fallback, 0);

        const syncAcConfigs = () => {
            if (!acConfigs || !acCountInput) return;

            const count = Math.min(Math.max(parseInt(acCountInput.value || "0"), 0), 8);

            acConfigs.innerHTML = "";

            for (let i = 0; i < count; i++) {
                const card = document.createElement("div");
                card.className = "ac-config-card";

                card.innerHTML = `
                    <strong>AC ${i + 1}</strong>
                    <select data-ac-ton>
                        <option value="1200">1 Ton</option>
                        <option value="1800" selected>1.5 Ton</option>
                        <option value="2400">2 Ton</option>
                    </select>
                    <select data-ac-type>
                        <option value="0.72">Inverter</option>
                        <option value="1">Non-Inverter</option>
                    </select>
                `;

                acConfigs.appendChild(card);
            }
        };

        const getLoadWatts = () => {
            syncAcConfigs();

            const lights = numberValue(lightsInput) * 15;
            const fans = numberValue(fansInput) * 80;
            const fridge = numberValue(fridgeInput);
            const motors = numberValue(motorHpInput) * 746;
            const other = numberValue(otherInput);

            const acWatts = Array.from(acConfigs.querySelectorAll(".ac-config-card"))
                .reduce((sum, card) => {
                    const ton = numberValue(card.querySelector("[data-ac-ton]"));
                    const factor = numberValue(card.querySelector("[data-ac-type]"), 1);
                    return sum + ton * factor;
                }, 0);

            return lights + fans + fridge + motors + other + acWatts;
        };

        const updateSolarEstimate = () => {
            const tariff = Math.max(numberValue(tariffInput, 50), 1);

            let monthlyBill = numberValue(billInput);
            let monthlyUnits = monthlyBill / tariff;
            let dailyUnits = monthlyUnits / 30;

            let totalLoadWatts = 0;

            if (activeMode === "load") {
                totalLoadWatts = getLoadWatts();
                dailyUnits = (totalLoadWatts / 1000) * 6;
                monthlyUnits = dailyUnits * 30;
                monthlyBill = monthlyUnits * tariff;
            }

            const systemSize = Math.max(1, dailyUnits / 5.5);
            const cost = systemSize * 250000;
            const savings = monthlyBill * 0.7;
            const roi = savings ? cost / (savings * 12) : 0;

            sizeOutput.textContent = `${systemSize.toFixed(1)} kW`;
            costOutput.textContent = pkrFormatter.format(cost);
            savingsOutput.textContent = pkrFormatter.format(savings);
            roiOutput.textContent = `${roi.toFixed(1)} years`;
        };

        calculator.addEventListener("input", updateSolarEstimate);
        calculator.addEventListener("change", updateSolarEstimate);

        syncAcConfigs();
        updateSolarEstimate();
    }

    /* ================= BEFORE AFTER FIX ================= */
    document.querySelectorAll("[data-before-after]").forEach((slider) => {
        const input = slider.querySelector("input");
        if (!input) return;

        const update = () => {
            slider.style.setProperty("--split", `${input.value}%`);
        };

        input.addEventListener("input", update);
        update();
    });

    /* ================= SMART FORM (FIXED PROPERLY) ================= */
    function initSmartForm() {
        const form = document.getElementById("smart-assessment-form");
        if (!form) return;

        const steps = Array.from(form.querySelectorAll(".form-step"));
        const btnNext = document.getElementById("btn-next");
        const btnPrev = document.getElementById("btn-prev");

        let currentStep = 0;

        function showStep() {
            steps.forEach((s, i) => {
                s.style.display = i === currentStep ? "block" : "none";
            });
        }

        function validate() {
            const inputs = steps[currentStep].querySelectorAll("input, select");

            for (let input of inputs) {
                if (!input.checkValidity()) {
                    input.reportValidity();
                    return false;
                }
            }
            return true;
        }

        btnNext?.addEventListener("click", (e) => {
            e.preventDefault();

            if (!validate()) return;

            if (currentStep < steps.length - 1) {
                currentStep++;
                showStep();
            }
        });

        btnPrev?.addEventListener("click", (e) => {
            e.preventDefault();
            currentStep--;
            showStep();
        });

        showStep();
    }

    document.addEventListener("DOMContentLoaded", initSmartForm);

    /* ================= NAVBAR SHRINK ================= */
    const topbar = document.querySelector(".page-topbar");
    if (topbar) {
        const handleScroll = () => {
            if (window.scrollY > 20) {
                topbar.classList.add("is-scrolled");
            } else {
                topbar.classList.remove("is-scrolled");
            }
        };
        window.addEventListener("scroll", handleScroll, { passive: true });
        handleScroll();
    }

})();