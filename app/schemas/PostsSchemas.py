postsSchema:dict = {
  "type": "object",
  "properties": {
    "title": {"type": "string"},
    "content": {"type": "string"},
    "training_id": {"type": "object"},
  },
  "required": ["title", "content", "training_id"]
}

updatePostsSchema:dict = {
  "type": "object",
  "properties": {
    "title": {"type": "string"},
    "content": {"type": "string"},
    "training_id": {"type": "object"},
    "likes": {"type": "integer"},
    "comments": {"type": "array"},
  },
  "required": ["title", "content", "training_id", "likes", "comments"]
}