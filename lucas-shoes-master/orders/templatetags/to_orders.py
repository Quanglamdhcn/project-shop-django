from django import template
import re

register = template.Library()

phone = re.compile(r"(\d{3})")

@register.filter
def to_phone(value):
	return ' '.join(phone.split(str(value)))