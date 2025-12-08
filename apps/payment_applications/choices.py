from django.db.models import TextChoices


class CurrencyChoices(TextChoices):
    RUB = 'RUB', 'Российский рубль'
    USD = 'USD', 'Доллар США'
    EUR = 'EUR', 'Евро'
    CNY = 'CNY', 'Китайский юань'


class PaymentApplicationStatus(TextChoices):
    NEW = 'NEW', 'Новая'
    APPROVED = 'APPROVED', 'Одобрена'
    REJECTED = 'REJECTED', 'Отклонена'
    PAID = 'PAID', 'Выплачена'
