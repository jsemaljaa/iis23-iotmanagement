from re import compile as recompile
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


class PwdValidator:
    pin_regex = recompile('[a-zA-Z0-9]{1,10}')

    def validate(self, password, user=None):
        if not self.pin_regex.fullmatch(password):
            raise ValidationError(
                _('Password should have 1 to 10 symbols, digits and letters only'),
                code='pwd',
            )
