from flask_wtf import FlaskForm
from wtforms import StringField, DecimalField, SelectField
from wtforms.validators import DataRequired, Length, NumberRange, ValidationError


def safe_characters(field_label: str, *, allow_empty: bool = False):
    """WTForms validator limiting input to a safe, predictable character set.

    This does not replace output escaping (templates still auto-escape), but helps
    prevent surprising inputs (HTML fragments, control chars, etc.).
    """

    def _validator(form, field):
        value = field.data
        if value is None:
            return
        value = str(value)
        if allow_empty and value.strip() == "":
            return

        # Allow letters/numbers (incl. diacritics via \w), spaces, and common punctuation.
        # Reject angle brackets explicitly to avoid HTML-looking inputs.
        import re

        if "<" in value or ">" in value:
            raise ValidationError(f"{field_label}: znaky < a > nejsou povolené.")

        pattern = re.compile(r"^[\w\s\-\.,:;!?()\[\]{}'\"+/\\%@#&]+$", re.UNICODE)
        if not pattern.match(value):
            raise ValidationError(
                f"{field_label}: obsahuje nepovolené znaky (povolena jsou písmena/čísla, mezery a běžná interpunkce)."
            )

    return _validator

class ProductForm(FlaskForm):
    name = StringField('Název', validators=[DataRequired(), Length(max=100), safe_characters('Název')])
    price = DecimalField('Cena', places=2, validators=[DataRequired(), NumberRange(min=0)])
    description = StringField('Popis', validators=[Length(max=200), safe_characters('Popis', allow_empty=True)])
    dph = SelectField('DPH', choices=[('0','0%'), ('15','15%')], coerce=int, default=15)


class DeleteForm(FlaskForm):
    """Empty form used only to provide CSRF protection for delete actions."""
    pass
