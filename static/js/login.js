document.addEventListener('DOMContentLoaded', () => {

    /* ===== Blob Mengikuti Cursor (parallax halus) ===== */

    const blobs = document.querySelectorAll('.blob');

    document.addEventListener('mousemove', (e) => {
        const x = (e.clientX / window.innerWidth - 0.5) * 2;
        const y = (e.clientY / window.innerHeight - 0.5) * 2;

        blobs.forEach((blob, i) => {
            const strength = (i + 1) * 12;
            blob.style.transform = `translate(${x * strength}px, ${y * strength}px)`;
        });
    });

    /* ===== Ripple Effect pada Tombol Login ===== */

    const btn = document.querySelector('.login-card .btn');

    if (btn) {
        btn.addEventListener('click', function (e) {
            const rect = this.getBoundingClientRect();
            const ripple = document.createElement('span');
            const size = Math.max(rect.width, rect.height) * 1.6;

            ripple.className = 'btn-ripple';
            ripple.style.width = ripple.style.height = size + 'px';
            ripple.style.left = (e.clientX - rect.left - size / 2) + 'px';
            ripple.style.top = (e.clientY - rect.top - size / 2) + 'px';

            this.appendChild(ripple);

            setTimeout(() => ripple.remove(), 600);
        });
    }

    /* ===== Toggle Password dengan Animasi Blink ===== */

    const togglePassword = document.getElementById('togglePassword');
    const passwordInput = document.getElementById('password');
    const eyeIcon = document.getElementById('eyeIcon');

    if (togglePassword && passwordInput && eyeIcon) {
        togglePassword.addEventListener('click', () => {
            eyeIcon.classList.add('blinking');

            setTimeout(() => {
                const isPassword = passwordInput.type === 'password';
                passwordInput.type = isPassword ? 'text' : 'password';
                eyeIcon.classList.toggle('showing', isPassword);
            }, 175);

            setTimeout(() => {
                eyeIcon.classList.remove('blinking');
            }, 350);
        });
    }
});