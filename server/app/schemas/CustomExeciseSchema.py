customExerciseSchema = {
    "type": "object",
    "properties": {
        "name": {"type": "string"},
        "description": {"type": "string"},
        "category": {"type": "string"},
        "equipment": {"type": "string"},
        "muscle": {"type": "string"},
        "secondary_muscle": {"type": "string"},
        "video": {"type": "string"},
        "image": {"type": "string"},
    },
    "required": ["name", "muscle"]
}
