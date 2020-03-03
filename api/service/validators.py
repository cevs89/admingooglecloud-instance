from cerberus import Validator


class RegisterServiceValidator():
    """
    {
        "service":"Google Cloud",
        "machine":"name_machine",
        "project":"name_project",
        "zone":"zonce_instace",
        "instance":"nane_instance",
        "description":"descripcion_instance",
        "status":"status_initial"
    }
    """
    schema = {
        "service": {
            "type": "string",
            "required": True,
            "minlength": 6,
        },
        "machine": {
            "type": "string",
            "required": True,
            "minlength": 3,
        },
        "project": {
            "type": "string",
            "required": True,
            "minlength": 6,
        },
        "zone": {
            "type": "string",
            "required": True,
            "minlength": 4,
        },
        "instance": {
            "type": "string",
            "required": True,
            "minlength": 5,
        },
        "description": {
            "type": "string",
            "required": True,
            "minlength": 10,
            "maxlength": 255,
        },
        "status": {
            "type": "string",
            "required": True,
            "minlength": 5,
        },

    }

    def __init__(self, data):
        self.validator = Validator()
        self.data = data
        self.schema = self.__class__.schema

    def validate(self):
        return self.validator.validate(self.data, self.schema)

    def errors(self):
        return self.validator.errors
