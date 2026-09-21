document.addEventListener('DOMContentLoaded', () => {

    /* ===== 1. Sliding Pill Indicator ===== */

    const navLinks = document.getElementById('navLinks');
    const indicator = document.getElementById('navIndicator');
    const links = navLinks ? navLinks.querySelectorAll('a') : [];

    function moveIndicatorTo(el) {
        if (!el || !indicator) return;
        indicator.style.width = el.offsetWidth + 'px';
        indicator.style.left = el.offsetLeft + 'px';
        indicator.style.opacity = '1';
    }

    const activeLink = navLinks ? navLinks.querySelector('a.active') : null;

    if (activeLink) {
        indicator.style.transition = 'none';
        moveIndicatorTo(activeLink);
        requestAnimationFrame(() => {
            indicator.style.transition = 'left 0.3s ease, width 0.3s ease, opacity 0.2s ease';
        });
    }

    links.forEach((link) => {
        link.addEventListener('mouseenter', () => moveIndicatorTo(link));
    });

    if (navLinks) {
        navLinks.addEventListener('mouseleave', () => {
            if (activeLink) {
                moveIndicatorTo(activeLink);
            } else {
                indicator.style.opacity = '0';
            }
        });
    }

    /* ===== 2. Ripple Effect on Click ===== */

    links.forEach((link) => {
        link.addEventListener('click', function (e) {
            const rect = this.getBoundingClientRect();
            const ripple = document.createElement('span');
            const size = Math.max(rect.width, rect.height) * 1.4;

            ripple.className = 'nav-ripple';
            ripple.style.width = ripple.style.height = size + 'px';
            ripple.style.left = (e.clientX - rect.left - size / 2) + 'px';
            ripple.style.top = (e.clientY - rect.top - size / 2) + 'px';

            this.appendChild(ripple);

            setTimeout(() => ripple.remove(), 600);
        });
    });

    /* ===== 3. Navbar Shrink on Scroll ===== */

    const nav = document.querySelector('nav');

    if (nav) {
        window.addEventListener('scroll', () => {
            if (window.scrollY > 12) {
                nav.classList.add('scrolled');
            } else {
                nav.classList.remove('scrolled');
            }
        });
    }
});