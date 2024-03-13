trainingProgramSchema:dict = {
    "type": "object",
    "properties": {
        "name": { "type": "string" },
        "description": { "type": "string" },
        "avg_duration": { "type": "integer" },
        "avg_volume": { "type": "integer" },
        "avg_reps": { "type": "integer" },
        "avg_sets": { "type": "integer" },
        "exercises": { "type": "array", "items": { "type": "object", "properties": {
            "_id": { "type": "object" },
            "sets": { "type": "array", "items": { "type": "object", "properties": {
                "reps": { "type": "integer" },
                "weight": { "type": "integer" }
            } } }
        } } }
    },
    "required": ["name", "description", "avg_duration", "avg_volume", "avg_reps", "avg_sets", "exercises"]
}