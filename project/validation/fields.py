from .exceptions import ValidationException


class ValidationField:
    """
    Validate an individual field
    """

    def validate(self, field):
        raise NotImplementedError()


class IsNonEmptyString(ValidationField):
    """
    Validate a field is a non-empty string
    """

    def validate(self, field):
        if not isinstance(field, str) or field == "":
            return "Field is not a valid non-empty string"
        return None


class IsList(ValidationField):
    def __init__(self, listItemValidator):
        super().__init__()
        self.listItemValidator = listItemValidator

    def validate(self, field):
        if not isinstance(field, list):
            return "Field is not a list"

        subvalidation = []
        for item in field:
            try:
                self.listItemValidator.validate(item)
                subvalidation.append(None)
            except ValidationException as e:
                subvalidation.append(e)

        if any(item is not None for item in subvalidation):
            return f"Field items malformed - {subvalidation}"

        return None
