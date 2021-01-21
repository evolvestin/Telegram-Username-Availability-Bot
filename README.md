# Telegram-Username-Availability-Bot

Когда задается имя пользователя, происходит валидация.

## Список существующих ответов на валидацию имени пользователя Telegram
- Only 0-9, a-z, and underscores allowed.
- Sorry, this link is already occupied.
- Sorry, this link is too short.
- This link is available.
- This link is invalid.

## Причины ошибок валидации и ответы на неё
- когда два подчеркивания или начинается с цифры - This link is invalid
- когда не подходят символы - Only 0-9, a-z, and underscores allowed.

## Последовательность валидации
Сначала валидация подходящих символов, а потом уже длины.
