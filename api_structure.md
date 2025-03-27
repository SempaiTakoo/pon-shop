# Структура API

## Уровни доступа

- **Публичный** – Доступ без токена.
- **Авторизованный** – Требуется валидный JWT.
- **Автор** – Только создатель ресурса (например, поста).
- **Админ** – Пользователи с ролью `admin`.

## Users API

### GET users/

Возвращает список пользователей.

### GET users/<user_id>/

Возвращает данные о пользователе.

## Reviews API

### GET rewiews/

Возвращает список отзывов.

### GET reviews/<review_id>/

Возвращает данные об отзыве.

### GET users/<user_id>/reviews/

Возвращает список отзывов пользователя.

### GET users/<user_id>/rewiews/<review_id>/

Возвращает данные об отзыве пользователя.

## Wishlists API

### GET wishlists/

Возвращает список вишлистов.

### GET users/<user_id>/wishlist/

Возвращает вишлист пользователя.

## Payment methods API

### GET payment_methods/

Возвращает список методов оплаты.

### GET users/<user_id>/payment_methods/

Возвращает список методов оплаты пользователя.

### GET users/<user_id>/payment_methods/<payment_method_id>/

Возвращает данные о методе оплаты пользователя.

## Orders API

### GET orders/

Возвращает список заказов.

### GET orders/<order_id>/

Возвращает данные о заказе.

### GET users/<user_id>/orders/

Возвращает список заказов пользователя.

### GET users/<user_id>/orders/<order_id>/

Возвращает данные о заказе пользователя, включая товары из заказа.

## Products API

### GET products/

Возвращает список продуктов.

### GET products/<product_id>/

Возвращает данные о заказе.

### GET orders/<order_id>/products/

Возвращает список продуктов в заказе.

## Categories API

### GET categories/

Возвращает список категорий.

### GET categories/<category_id>/

Возвращает данные о категории.

## Analytics API

### GET analytics/

Возвращает список видов аналитики.

### GET users/<user_id>/analytics/<вид аналитики>...

Эти эндпоинты нужно доработать.
