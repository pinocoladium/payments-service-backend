from django.core.validators import RegexValidator


def digit_length_validator(length: int) -> RegexValidator:
    return RegexValidator(
        regex=rf"^\d{{{length}}}$",
        message=f"Значение должно содержать ровно {length} цифр",
    )


inn_validator = RegexValidator(
    regex=r'^(\d{10}|\d{12})$',
    message='ИНН должен состоять либо из 10, либо из 12 цифр',
)
