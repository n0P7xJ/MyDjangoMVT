document.addEventListener('DOMContentLoaded', function() {
    const registerForm = document.getElementById('register-form');
    const loadingOverlay = document.getElementById('loading-overlay');

    if (!registerForm) return;

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

    registerForm.addEventListener('submit', function(e) {
        e.preventDefault();
        showLoading();

        const formDataObj = collectFormData(registerForm);

        setTimeout(() => {
            registerForm.submit();
        }, 500);
    });
});
