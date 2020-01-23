from collections import Sequence

from . import parser
from . import units


class ValidationError(ValueError):
    pass


def _numeric_validator(num_value, numeric_type, min_value, max_value):
    try:
        num_value = numeric_type(num_value)
    except (ValueError, TypeError):
        error_msg = "Cannot coerce {num_value} to {numeric_type}".format(
            num_value=num_value, numeric_type=numeric_type.__name__)
        raise ValidationError(error_msg)

    if min_value is not None and num_value < min_value:
        error_msg = 'Value {num_value} below minimum value {min_value}'.format(
            num_value=num_value, min_value=min_value)
        raise ValidationError(error_msg)

    if max_value is not None and num_value > max_value:
        error_msg = 'Value {num_value} above maximum value {max_value}'.format(
            num_value=num_value, max_value=max_value)
        raise ValidationError(error_msg)

    return num_value


def is_number(value=None, min_value=None, max_value=None):
    """
    Validate that value is a valid float.

    If min_value or max_value are provided, range checks are performed.
    """

    def validator(num_value):
        return _numeric_validator(num_value=num_value, numeric_type=float, min_value=min_value, max_value=max_value)

    if min_value is None and max_value is None:
        return validator(value)
    else:
        return validator


is_number.description = '<number>'


def is_integer(value=None, min_value=None, max_value=None):
    """
    Validate that value is a valid integer.

    If min_value or max_value are provided, range checks are performed.
    """

    def validator(num_value):
        return _numeric_validator(num_value=num_value, numeric_type=int, min_value=min_value, max_value=max_value)

    if min_value is None and max_value is None:
        return validator(value)
    else:
        return validator


is_integer.description = '<integer>'


def is_length(value):
    try:
        value = parser.units(value)
    except ValueError as error:
        raise ValidationError(str(error))

    return value


is_length.description = '<length>'


def is_percentage(value):
    try:
        value = parser.units(value)
    except ValueError as error:
        raise ValidationError(str(error))

    if not isinstance(value, units.Percent):
        error_msg = 'Value {value} is not a Percent unit'.format(value=value)
        raise ValidationError(error_msg)

    return value


is_percentage.description = '<percentage>'


def is_color(value):
    try:
        value = parser.color(value)
    except ValueError as error:
        raise ValidationError(str(error))

    return value


is_color.description = '<color>'


def is_border_spacing(value):
    """
    Check if value is corresponds to a border spacing.

    <length> <length>?

    Returns a tuple with horizontal and vertical spacing.
    """
    if isinstance(value, Sequence) and not isinstance(value, str):
        values = value
    elif isinstance(value, (int, float)):
        values = (value, )
    else:
        values = [x.strip() for x in value.split()]

    if len(values) == 1:
        try:
            horizontal = is_length(values[0])
            return (horizontal, )
        except ValueError as error:
            raise ValidationError(str(error))
    elif len(values) == 2:
        try:
            horizontal = is_length(values[0])
            vertical = is_length(values[1])
            return (horizontal, vertical)
        except ValueError as error:
            raise ValidationError(str(error))
    else:
        raise ValidationError('Should provide 1 or 2 <length> values!')


is_border_spacing.description = '<length> <length>?'
