from .exceptions import ValidationException
from .fields import IsNonEmptyString, IsList


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
