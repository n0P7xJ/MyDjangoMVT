/**
 * Main JavaScript - Основний скрипт для Django проекту
 * Включає ініціалізацію компонентів та глобальні функції
 */

document.addEventListener('DOMContentLoaded', function() {
    // Ініціалізація всіх компонентів
    initializeProject();
    
    function initializeProject() {
        // Ініціалізація Cropper.js для форм (якщо потрібно)
        initializeCropperComponents();
        
        // Додаткові ініціалізації
        setupGlobalFeatures();
    }
    
    /**
     * Ініціалізація Cropper.js компонентів
     */
    function initializeCropperComponents() {
        const registrationForm = document.getElementById('registrationForm');
        if (registrationForm) {
            // Ініціалізація буде оброблена окремим файлом registration-cropper.js
            console.log('Registration form detected - Cropper.js will be initialized');
        }
    }
    
    /**
     * Налаштування глобальних функцій
     */
    function setupGlobalFeatures() {
        // Налаштування тултіпів Bootstrap
        const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
        tooltipTriggerList.map(function(tooltipTriggerEl) {
            return new bootstrap.Tooltip(tooltipTriggerEl);
        });
        
        // Активні алерти автоматично зникають через 5 секунд
        setTimeout(() => {
            const alerts = document.querySelectorAll('.alert');
            alerts.forEach((alert) => {
                const bsAlert = new bootstrap.Alert(alert);
                setTimeout(() => {
                    bsAlert.close();
                }, 5000);
            });
        }, 100);
    }
    
    /**
     * Глобальний обробник помилок
     */
    window.onerror = function(message, source, lineno, colno, error) {
        console.error('Global JavaScript Error:', {
            message: message,
            source: source,
            lineno: lineno,
            colno: colno,
            error: error
        });
        
        // Показуємо користувачу дружнє повідомлення
        if (typeof showUserFriendlyError === 'function') {
            showUserFriendlyError('Виникла помилка. Спробуйте оновити сторінку.');
        }
    };
    
    /**
     * Показати дружнє повідомлення про помилку
     */
    function showUserFriendlyError(message) {
        const errorContainer = document.getElementById('error-container');
        if (errorContainer) {
            errorContainer.innerHTML = `
                <div class="alert alert-danger alert-dismissible fade show" role="alert">
                    <i class="fas fa-exclamation-triangle me-2"></i>
                    ${message}
                    <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
                </div>
            `;
        } else {
            console.error('Error: ' + message);
        }
    }
    
    /**
     * Логін/лог-аут обробники
     */
    const loginForm = document.getElementById('login-form');
    if (loginForm) {
        loginForm.addEventListener('submit', function(e) {
            const submitBtn = loginForm.querySelector('button[type="submit"]');
            const originalText = submitBtn.innerHTML;
            
            submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i> Увійдіть...';
            submitBtn.disabled = true;
            
            // Повернення тексту через 5 секунд якщо помилка
            setTimeout(() => {
                if (submitBtn.innerHTML !== originalText) {
                    submitBtn.innerHTML = originalText;
                    submitBtn.disabled = false;
                }
            }, 5000);
        });
    }
    
    /**
     * Налаштування локального сховища
     */
    function initLocalStorage() {
        // Збереження налаштувань теми (якщо реалізуєте)
        const savedTheme = localStorage.getItem('theme');
        if (savedTheme) {
            document.body.classList.add(savedTheme);
        }
    }
    
    // Ініціалізація локального сховища
    initLocalStorage();
    
    /**
     * Обробка сповіщень
     */
    function initNotifications() {
        const notifications = document.querySelectorAll('[data-notification]');
        notifications.forEach(notification => {
            const type = notification.dataset.notification;
            const duration = parseInt(notification.dataset.duration) || 5000;
            
            setTimeout(() => {
                if (notification) {
                    const bsAlert = new bootstrap.Alert(notification);
                    bsAlert.close();
                }
            }, duration);
        });
    }
    
    // Ініціалізація сповіщень
    initNotifications();
});

/**
 * Глобальні утиліти
 */
window.DjangoUtils = {
    // Форматування дат
    formatDate: function(date, format = 'uk-UA') {
        return new Intl.DateTimeFormat(format, {
            year: 'numeric',
            month: 'long',
            day: 'numeric'
        }).format(date);
    },
    
    // Валідне число
    isValidNumber: function(value) {
        return typeof value === 'number' && !isNaN(value);
    },
    
    // Форматування валюти
    formatCurrency: function(amount, currency = 'UAH') {
        return new Intl.NumberFormat('uk-UA', {
            style: 'currency',
            currency: currency
        }).format(amount);
    },
    
    // Копіювання в буфер обміну
    copyToClipboard: function(text) {
        navigator.clipboard.writeText(text).then(() => {
            // Показати тултип "Скопійовано!"
            console.log('Copied to clipboard:', text);
        }).catch(err => {
            console.error('Failed to copy:', err);
        });
    },
    
    // Анімований скрол
    smoothScrollTo: function(target, duration = 800) {
        const targetElement = document.querySelector(target);
        if (targetElement) {
            targetElement.scrollIntoView({
                behavior: 'smooth'
            });
        }
    }
};
