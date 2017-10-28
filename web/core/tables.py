import django_tables2 as tables
from django.utils.html import format_html


class PhoneNumberColumn(tables.Column):
    def render(self, value, record):
        return format_html('<a href="tel:{}">{}</a>', value, value)
