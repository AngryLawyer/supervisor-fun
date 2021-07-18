from unittest import TestCase
from project.validation import (
    ActionValidation,
    ActionChoicesValidation,
    ValidationException,
    MachineReportValidation,
)


class TestActionValidation(TestCase):
    def test_validates(self):
        ActionValidation().validate({"action": "hello"})

    def test_excepts(self):
        with self.assertRaises(ValidationException):
            ActionValidation().validate({})
        with self.assertRaises(ValidationException):
            ActionValidation().validate({"action": None})
        with self.assertRaises(ValidationException):
            ActionValidation().validate({"action": ""})


class TestActionChoicesValidation(TestCase):
    def test_validates(self):
        ActionChoicesValidation().validate({"id": "hello", "label": "Hello"})

    def test_excepts(self):
        with self.assertRaises(ValidationException):
            ActionChoicesValidation().validate({})
        with self.assertRaises(ValidationException):
            ActionChoicesValidation().validate({"id": None, "label": None})
        with self.assertRaises(ValidationException):
            ActionChoicesValidation().validate({"id": "", "label": ""})


class TestMachineReportValidation(TestCase):
    def test_validates(self):
        MachineReportValidation().validate(
            {
                "id": "blinker",
                "template": "light",
                "actions": [{"id": "hello", "label": "Hello"}],
            }
        )

    def test_excepts(self):
        with self.assertRaises(ValidationException):
            MachineReportValidation().validate({})
        with self.assertRaises(ValidationException):
            MachineReportValidation().validate(
                {
                    "id": "blinker",
                    "template": "light",
                    "actions": [{"id": None, "label": "Hello"}],
                }
            )
        with self.assertRaises(ValidationException):
            MachineReportValidation().validate(
                {
                    "id": "",
                    "template": "",
                    "actions": [{"id": "hello", "label": "Hello"}],
                }
            )
