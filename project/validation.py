class ValidationException(Exception):
    pass


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


class Validation:
    """
    Check that a JSON object matches the schema we give it
    """
    schema = {}

    def validate(self, data):
        validation_results = {
            key: rule.validate(data.get(key, None))
            for (key, rule)
            in self.schema.items()
        }
        if any(item is not None for item in validation_results.values()):
            raise ValidationException(validation_results)


class ActionValidation(Validation):
    """
    An action object, sent from Supervisor to Machine
    """

    schema = {
        "action": IsNonEmptyString()
    }
