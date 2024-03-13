authEmailSchema: dict = {
    "type": "object",
    "properties": {
        "email": {"type": "string", "format": "email"},
        "password": {"type": "string"}
    },
    "required": ["email", "password"]
}

authUserNameSchema: dict = {
    "type": "object",
    "properties": {
        "username": {"type": "string"},
        "password": {"type": "string"}
    },
    "required": ["username", "password"]
}

authRegisterSchema: dict = {
    "type": "object",
    "properties": {
        "username": {"type": "string"},
        "email": {"type": "string", "format": "email"},
        "password": {"type": "string"},
        "name": {"type": "string"},
        "role": {"type": "integer", "enum": [1, 100]},
        "gender": {"type": "string", "enum": ["male", "female", "other"]}
    },
    "required": ["username", "email", "password"]
}