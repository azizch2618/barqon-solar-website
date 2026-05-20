/**
 * BARQON Enterprise UI — nav, lazy media, reduced motion
 */
(() => {
    const root = document.documentElement;
    const prefersReduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

    /* ── Fixed nav offset for page shell ── */
    const navWrapper = document.getElementById('navWrapper');
    const pageShell = document.querySelector('.page-shell');
    const topbar = document.querySelector('.bq-topbar');

    if (pageShell && topbar && window.innerWidth >= 1025) {
        pageShell.classList.add('has-topbar');
    }

    const syncNavScroll = () => {
        if (!navWrapper) return;
        navWrapper.classList.toggle('scrolled', window.scrollY > 40);
    };
    window.addEventListener('scroll', syncNavScroll, { passive: true });
    syncNavScroll();

    /* ── Mobile menu body lock ── */
    const mobileMenu = document.getElementById('mobileMenu');
    const navToggle = document.getElementById('navToggle');

    const setMenuOpen = (open) => {
        if (!mobileMenu) return;
        mobileMenu.classList.toggle('active', open);
        document.body.classList.toggle('bq-menu-open', open);
        if (navToggle) {
            const icon = navToggle.querySelector('i');
            if (icon) icon.setAttribute('data-lucide', open ? 'x' : 'menu');
            navToggle.setAttribute('aria-expanded', open ? 'true' : 'false');
            if (window.lucide) lucide.createIcons();
        }
    };

    if (typeof window.toggleMobileMenu === 'function') {
        const original = window.toggleMobileMenu;
        window.toggleMobileMenu = function bqToggleMobileMenu() {
            const willOpen = !mobileMenu?.classList.contains('active');
            original();
            document.body.classList.toggle('bq-menu-open', mobileMenu?.classList.contains('active'));
            if (navToggle) {
                navToggle.setAttribute('aria-expanded', mobileMenu?.classList.contains('active') ? 'true' : 'false');
            }
        };
    } else if (navToggle && mobileMenu) {
        navToggle.addEventListener('click', () => {
            setMenuOpen(!mobileMenu.classList.contains('active'));
        });
        document.getElementById('mobileMenuClose')?.addEventListener('click', () => setMenuOpen(false));
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape' && mobileMenu.classList.contains('active')) setMenuOpen(false);
        });
    }

    /* ── Lazy images ── */
    if ('IntersectionObserver' in window) {
        const lazyImages = document.querySelectorAll('img[loading="lazy"]:not([data-lazy-bound])');
        const io = new IntersectionObserver(
            (entries) => {
                entries.forEach((entry) => {
                    if (!entry.isIntersecting) return;
                    const img = entry.target;
                    img.dataset.lazyBound = '1';
                    if (img.dataset.src) {
                        img.src = img.dataset.src;
                        img.removeAttribute('data-src');
                    }
                    io.unobserve(img);
                });
            },
            { rootMargin: '120px' }
        );
        lazyImages.forEach((img) => io.observe(img));
    }

    /* ── Resize: topbar visibility ── */
    let resizeTimer;
    window.addEventListener(
        'resize',
        () => {
            clearTimeout(resizeTimer);
            resizeTimer = setTimeout(() => {
                if (!pageShell) return;
                if (window.innerWidth >= 1025 && topbar) {
                    pageShell.classList.add('has-topbar');
                } else {
                    pageShell.classList.remove('has-topbar');
                }
            }, 150);
        },
        { passive: true }
    );

    if (prefersReduced) {
        root.classList.add('bq-reduced-motion');
    }
})();
