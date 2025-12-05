document.addEventListener('DOMContentLoaded', function() {
    const registerForm = document.getElementById('register-form');
    const loginForm = document.getElementById('login-form');
    const loadingOverlay = document.getElementById('loading-overlay');
    const recaptchaSiteKey = document.querySelector('[data-recaptcha-site-key]')?.getAttribute('data-recaptcha-site-key');

    function showLoading() {
        if (loadingOverlay) {
            loadingOverlay.style.display = 'flex';
        }
    }

    function hideLoading() {
        if (loadingOverlay) {
            loadingOverlay.style.display = 'none';
        }
    }

    function collectFormData(form) {
        const formData = new FormData(form);
        const dataObject = {};

        for (let [key, value] of formData.entries()) {
            dataObject[key] = value;
        }

        console.log('Зібрані дані:', dataObject);
        return dataObject;
    }

    // Handle form submission with Turnstile verification
    async function handleFormSubmit(form, e) {
        e.preventDefault();

        // If Turnstile is configured, wait for token
        if (recaptchaSiteKey && window.turnstile) {
            showLoading();
            try {
                // Get token from Turnstile widget
                const token = window.turnstile.getResponse();
                
                if (!token) {
                    hideLoading();
                    alert('Будь ласка, пройдіть перевірку безпеки.');
                    return;
                }
                
                const input = document.createElement('input');
                input.type = 'hidden';
                input.name = 'cf_turnstile_response';
                input.value = token;
                form.appendChild(input);
                
                setTimeout(() => {
                    form.submit();
                }, 300);
            } catch (err) {
                console.error('Turnstile error:', err);
                hideLoading();
                alert('Помилка перевірки безпеки. Спробуйте ще раз.');
            }
        } else {
            // Fallback if Turnstile not configured
            showLoading();
            const formDataObj = collectFormData(form);
            setTimeout(() => {
                form.submit();
            }, 300);
        }
    }

    if (registerForm) {
        registerForm.addEventListener('submit', function(e) {
            handleFormSubmit(registerForm, e);
        });
    }

    if (loginForm) {
        loginForm.addEventListener('submit', function(e) {
            handleFormSubmit(loginForm, e);
        });
    }
});
