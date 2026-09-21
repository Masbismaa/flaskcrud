document.addEventListener('DOMContentLoaded', () => {
    const statNumbers = document.querySelectorAll('.stat-content strong');

    statNumbers.forEach((el) => {
        const rawText = el.textContent.trim();
        const numericMatch = rawText.replace(/\./g, '').match(/-?\d+/);

        if (!numericMatch) return;

        const target = parseInt(numericMatch[0], 10);
        const prefix = rawText.slice(0, rawText.indexOf(numericMatch[0]));
        const duration = 900;
        const startTime = performance.now();

        function formatNumber(num) {
            return num.toLocaleString('id-ID');
        }

        function animate(now) {
            const progress = Math.min((now - startTime) / duration, 1);
            const eased = 1 - Math.pow(1 - progress, 3);
            const current = Math.round(eased * target);

            el.textContent = prefix + formatNumber(current);

            if (progress < 1) {
                requestAnimationFrame(animate);
            } else {
                el.textContent = rawText;
            }
        }

        requestAnimationFrame(animate);
    });
});