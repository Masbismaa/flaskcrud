document.addEventListener('DOMContentLoaded', () => {

    /* ===== Blob Mengikuti Cursor (lerp — smooth & liquid) ===== */

    const blobs = Array.from(document.querySelectorAll('.blob')).map((el, i) => ({
        el,
        strength: (i + 1) * 14,
        targetX: 0,
        targetY: 0,
        currentX: 0,
        currentY: 0
    }));

    let mouseX = 0;
    let mouseY = 0;

    document.addEventListener('mousemove', (e) => {
        mouseX = (e.clientX / window.innerWidth - 0.5) * 2;
        mouseY = (e.clientY / window.innerHeight - 0.5) * 2;
    });

    function animateBlobs() {
        blobs.forEach((blob) => {
            blob.targetX = mouseX * blob.strength;
            blob.targetY = mouseY * blob.strength;

            blob.currentX += (blob.targetX - blob.currentX) * 0.06;
            blob.currentY += (blob.targetY - blob.currentY) * 0.06;

            blob.el.style.transform = `translate(${blob.currentX.toFixed(2)}px, ${blob.currentY.toFixed(2)}px)`;
        });

        requestAnimationFrame(animateBlobs);
    }

    requestAnimationFrame(animateBlobs);

    /* ===== Ripple Effect pada Tombol Login ===== */

    const btn = document.querySelector('.login-card .btn');

    if (btn) {
        btn.addEventListener('click', function (e) {
            const rect = this.getBoundingClientRect();
            const ripple = document.createElement('span');
            const size = Math.max(rect.width, rect.height) * 1.8;

            ripple.className = 'btn-ripple';
            ripple.style.width = ripple.style.height = size + 'px';
            ripple.style.left = (e.clientX - rect.left - size / 2) + 'px';
            ripple.style.top = (e.clientY - rect.top - size / 2) + 'px';

            this.appendChild(ripple);

            ripple.addEventListener('animationend', () => ripple.remove());
        });
    }

    /* ===== Toggle Password dengan Animasi Blink (lebih smooth) ===== */

    const togglePassword = document.getElementById('togglePassword');
    const passwordInput = document.getElementById('password');
    const eyeIcon = document.getElementById('eyeIcon');

    if (togglePassword && passwordInput && eyeIcon) {
        let isAnimating = false;

        togglePassword.addEventListener('click', () => {
            if (isAnimating) return;
            isAnimating = true;

            eyeIcon.classList.add('blinking');

            setTimeout(() => {
                const isPassword = passwordInput.type === 'password';
                passwordInput.type = isPassword ? 'text' : 'password';
                eyeIcon.classList.toggle('showing', isPassword);
            }, 220);

            setTimeout(() => {
                eyeIcon.classList.remove('blinking');
                isAnimating = false;
            }, 440);
        });
    }
});