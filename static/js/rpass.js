const newPassword = document.getElementById('newPassword');
    const confirmPassword = document.getElementById('confirmPassword');
    const strengthBar = document.getElementById('strengthBar');
    const strengthLabel = document.getElementById('strengthLabel');
    const matchLabel = document.getElementById('matchLabel');

    function checkStrength(value) {
        let score = 0;
        if (value.length >= 8) score++;
        if (/[A-Z]/.test(value)) score++;
        if (/[0-9]/.test(value)) score++;
        if (/[^A-Za-z0-9]/.test(value)) score++;
        return score;
    }

    newPassword.addEventListener('input', () => {
        const score = checkStrength(newPassword.value);
        const levels = [
            { width: '0%', color: '#e5e7eb', label: '' },
            { width: '25%', color: '#ef4444', label: 'Lemah' },
            { width: '50%', color: '#f59e0b', label: 'Sedang' },
            { width: '75%', color: '#3b82f6', label: 'Kuat' },
            { width: '100%', color: '#22c55e', label: 'Sangat Kuat' }
        ];
        const level = levels[score];
        strengthBar.style.width = level.width;
        strengthBar.style.background = level.color;
        strengthLabel.textContent = level.label;
        strengthLabel.style.color = level.color;
        checkMatch();
    });

    confirmPassword.addEventListener('input', checkMatch);

    function checkMatch() {
        if (!confirmPassword.value) {
            matchLabel.textContent = '\u00A0';
            confirmPassword.style.borderColor = '';
            return;
        }
        if (confirmPassword.value === newPassword.value) {
            matchLabel.textContent = '✓ Password cocok';
            matchLabel.style.color = '#22c55e';
            confirmPassword.style.borderColor = '#22c55e';
        } else {
            matchLabel.textContent = '✗ Password tidak cocok';
            matchLabel.style.color = '#ef4444';
            confirmPassword.style.borderColor = '#ef4444';
        }
    }