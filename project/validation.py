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


class Validation:
    """
    Check that a JSON object matches the schema we give it
    """

    schema = {}

    def validate(self, data):
        validation_results = {
            key: rule.validate(data.get(key, None))
            for (key, rule) in self.schema.items()
        }
        if any(item is not None for item in validation_results.values()):
            raise ValidationException(validation_results)


class ActionValidation(Validation):
    """
    An action object, sent from Supervisor to Machine
    """

    schema = {"action": IsNonEmptyString()}


class ActionChoicesValidation(Validation):
    """
    An action option that can be taken by the frontend
    """

    schema = {"id": IsNonEmptyString(), "label": IsNonEmptyString()}


class MachineReportValidation(Validation):
    """
    A machine report object, sent from Machine to Supervisor
    """

    schema = {
        "id": IsNonEmptyString(),
        "template": IsNonEmptyString(),
        "actions": IsList(ActionChoicesValidation()),
    }
