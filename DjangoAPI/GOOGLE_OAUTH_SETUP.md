# Налаштування входу через Google OAuth

## Крок 1: Створення проекту в Google Cloud Console

1. Перейдіть на [Google Cloud Console](https://console.cloud.google.com/)
2. Створіть новий проект або оберіть існуючий
3. У верхньому меню оберіть свій проект

## Крок 2: Налаштування OAuth consent screen

1. У лівому меню перейдіть до **APIs & Services** → **OAuth consent screen**
2. Оберіть **External** (для тестування) або **Internal** (для внутрішнього використання)
3. Натисніть **Create**
4. Заповніть обов'язкові поля:
   - **App name**: Django MVT App
   - **User support email**: ваша email адреса
   - **Developer contact information**: ваша email адреса
5. Натисніть **Save and Continue**
6. На сторінці **Scopes** натисніть **Add or Remove Scopes**
7. Оберіть:
   - `.../auth/userinfo.email`
   - `.../auth/userinfo.profile`
8. Натисніть **Update** → **Save and Continue**
9. На сторінці **Test users** (якщо обрали External):
   - Додайте свою email адресу для тестування
   - Натисніть **Save and Continue**

## Крок 3: Створення OAuth 2.0 Client ID

1. У лівому меню перейдіть до **APIs & Services** → **Credentials**
2. Натисніть **+ Create Credentials** → **OAuth client ID**
3. Оберіть **Application type**: **Web application**
4. Введіть назву: `Django MVT Web Client`
5. У розділі **Authorized redirect URIs** додайте:
   ```
   http://localhost:8000/accounts/google/login/callback/
   http://127.0.0.1:8000/accounts/google/login/callback/
   ```
   
   Для production також додайте:
   ```
   https://yourdomain.com/accounts/google/login/callback/
   ```

6. Натисніть **Create**
7. Скопіюйте **Client ID** та **Client Secret**

## Крок 4: Налаштування змінних середовища

1. Створіть файл `.env` в корені проекту (якщо його ще немає):
   ```bash
   touch .env
   ```

2. Додайте наступні змінні в `.env`:
   ```env
   # Google OAuth
   GOOGLE_CLIENT_ID=your-client-id-here.apps.googleusercontent.com
   GOOGLE_CLIENT_SECRET=your-client-secret-here
   ```

3. Переконайтеся, що `.env` додано в `.gitignore`:
   ```
   .env
   ```

## Крок 5: Застосування міграцій

Запустіть міграції для створення необхідних таблиць django-allauth:

```bash
python3 manage.py migrate
```

## Крок 6: Налаштування Social Application в Django Admin

1. Запустіть сервер розробки:
   ```bash
   python3 manage.py runserver
   ```

2. Перейдіть до Django Admin: http://127.0.0.1:8000/admin/

3. Увійдіть як суперкористувач (якщо немає, створіть: `python3 manage.py createsuperuser`)

4. У розділі **Sites** переконайтеся, що існує сайт з доменом:
   - Domain name: `127.0.0.1:8000` або `localhost:8000`
   - Display name: `Django MVT`
   
5. У розділі **Social Applications** натисніть **Add Social Application**

6. Заповніть поля:
   - **Provider**: Google
   - **Name**: Google OAuth
   - **Client id**: ваш Client ID з Google Console
   - **Secret key**: ваш Client Secret з Google Console
   - **Sites**: оберіть ваш сайт (перемістіть з "Available sites" в "Chosen sites")

7. Натисніть **Save**

## Крок 7: Тестування

1. Перейдіть на сторінку входу: http://127.0.0.1:8000/login/
2. Натисніть кнопку **"Увійти через Google"**
3. Виберіть Google акаунт
4. Підтвердіть доступ до email та профілю
5. Після успішної авторизації вас буде перенаправлено на головну сторінку

## Крок 8: Налаштування для Production

Для production середовища:

1. Оновіть **Authorized redirect URIs** у Google Console:
   ```
   https://yourdomain.com/accounts/google/login/callback/
   ```

2. Оновіть Site в Django Admin:
   - Domain name: `yourdomain.com`
   - Display name: `Your App Name`

3. Встановіть змінні середовища на сервері:
   ```env
   GOOGLE_CLIENT_ID=your-production-client-id
   GOOGLE_CLIENT_SECRET=your-production-client-secret
   ```

4. Переконайтеся, що `DEBUG=False` і `ALLOWED_HOSTS` містить ваш домен

## Додаткові налаштування

### Автоматичне заповнення профілю

Якщо ви хочете автоматично заповнювати профіль користувача даними з Google:

```python
# users/signals.py або де ви обробляєте сигнали

from allauth.socialaccount.signals import pre_social_login
from django.dispatch import receiver

@receiver(pre_social_login)
def populate_profile(sender, request, sociallogin, **kwargs):
    if sociallogin.account.provider == 'google':
        user = sociallogin.user
        if sociallogin.account.extra_data:
            # Отримайте дані з Google
            user.email = sociallogin.account.extra_data.get('email', '')
            # Додайте інші поля за потреби
```

### Налаштування кнопки Google

Стилі для кнопки Google вже додані в шаблоні `login.html`. Ви можете змінити стилі в `static/css/registration.css`.

## Troubleshooting

### Помилка: "redirect_uri_mismatch"
- Переконайтеся, що URL в **Authorized redirect URIs** точно співпадає з URL, який використовується
- Перевірте, чи використовуєте `http://` або `https://`
- Перевірте порт (8000)

### Помилка: "Social application not configured"
- Переконайтеся, що ви створили Social Application в Django Admin
- Перевірте, чи правильно вказано Client ID та Secret
- Переконайтеся, що сайт додано до Social Application

### Користувач не створюється автоматично
- Перевірте налаштування `SOCIALACCOUNT_AUTO_SIGNUP = True` в settings.py
- Перевірте, чи email підтверджено в Google акаунті

## Корисні посилання

- [Django-allauth документація](https://django-allauth.readthedocs.io/)
- [Google OAuth 2.0](https://developers.google.com/identity/protocols/oauth2)
- [Google Cloud Console](https://console.cloud.google.com/)
