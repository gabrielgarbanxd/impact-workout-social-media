userSchema:dict = {
    "type": "object",
    "properties": {
        "username": { "type": "string" },
        "email": { "type": "string", "format": "email" },
        "password": { "type": "string" },
        "name": { "type": "string" },
        "role": { "type": "integer" },
        "gender": { "type": "string" },
        "birthdate": { "type": "string", "format": "date-time" },
        "profile_picture": { "type": "string" },
        "bio": { "type": "string" },
        "links": { "type": "object" },
        "private": { "type": "boolean" },
        "vip": { "type": "boolean" },
        "followers": { "type": "array", "items": { "type": "object" } },
        "body_measures": { "type": "object" },
        "training_programs": { "type": "array", "items": { "type": "object" } },
        "following": { "type": "array", "items": { "type": "object" } }
    },
    "required": ["username", "email", "password", "name", "role", "gender", "birthdate", "profile_picture", "bio", "links", "private", "vip", "followers", "body_measures", "training_programs", "following"]
}