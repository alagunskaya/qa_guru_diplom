PRODUCT_SCHEMA = {
    "type": "object",
    "required": ["id", "title", "price", "description", "category", "image", "rating"],
    "properties": {
        "id": {"type": "integer"},
        "title": {"type": "string", "minLength": 1},
        "price": {"type": "number"},  # принимает и int, и float
        "description": {"type": "string"},
        "category": {"type": "string"},
        "image": {"type": "string", "format": "uri"},
        "rating": {
            "type": "object",
            "required": ["rate", "count"],
            "properties": {
                "rate": {"type": "number", "minimum": 0, "maximum": 5},
                "count": {"type": "integer", "minimum": 0}
            }
        }
    }
}

PRODUCTS_LIST_SCHEMA = {
    "type": "array",
    "items": PRODUCT_SCHEMA,
    "minItems": 1,
}

PRODUCT_CREATE_SCHEMA = {
    "type": "object",
    "required": ["id", "title", "price", "description", "category", "image"],
    "properties": {
        "id": {"type": "integer"},
        "title": {"type": "string", "minLength": 1},
        "price": {"type": "number"},
        "description": {"type": "string"},
        "category": {"type": "string"},
        "image": {"type": "string", "format": "uri"},
    }
}
