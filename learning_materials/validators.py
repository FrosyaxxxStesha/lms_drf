import re
from rest_framework.serializers import ValidationError


class NoMatchRegexValidator:
    """
    Валидатор, проверяющий, что указанные поля не
    совпадают с регулярным выражением,
    в противном случае - возвращает совпавшие строки в полях
    """
    message = None
    regex = None
    restricted_strings_in_message = True
    rs_message_sep = ", "

    def __init__(self, *, fields=None):
        self.fields = fields

    def get_message(self):
        if self.message is None:
            raise NotImplementedError("Определите поле message или переопределите метод get_message")
        return self.message

    def get_regex(self):
        if self.regex is None:
            raise NotImplementedError("Определите поле regex или переопределите метод get_regex")
        return self.regex

    def __call__(self, value):
        restricted_strings = []
        regex = self.get_regex()

        for field_name in self.fields:
            field = value.get(field_name, "")
            restricted_strings.extend(regex.findall(field))

        if restricted_strings:
            message = self.get_message()

            if self.restricted_strings_in_message:
                formatted_rs = self.rs_message_sep.join(restricted_strings)
                response = message + formatted_rs
                raise ValidationError(response)

            raise ValidationError(message)


class YoutubeLinkOnlyValidator(NoMatchRegexValidator):
    """
    Валидатор для проверки отсутствия ссылок на все
    ресурсы, кроме youtube
    """
    message = "Ссылка на недопустимые ресурсы: "
    regex = re.compile(r"\b(?!https?://(?:www\.)?youtube\.com)https?://(?:www\.)?\S+\b")
