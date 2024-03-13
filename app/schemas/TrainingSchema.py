trainingSchema:dict = {
    "type": "object",
    "properties": {
        "date": { "type": "string", "format": "date-time" },
        "duration": { "type": "integer" },
        "volume": { "type": "integer" },
        "reps": { "type": "integer" },
        "sets": { "type": "integer" },
        "exercises": { "type": "array", "items": { "type": "object", "properties": {
            "_id": { "type": "object" },
            "sets": { "type": "array", "items": { "type": "object", "properties": {
                "reps": { "type": "integer" },
                "weight": { "type": "integer" }
            } } }
        } } },
        "image": { "type": "string" },
        "description": { "type": "string" },
        "visibility": { "type": "boolean" },
    },
    "required": ["user", "training_program", "date", "duration", "volume", "exercises"]
}