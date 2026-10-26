CART_SCHEMA = {
    "type": "object",
    "required": ["id", "userId", "date", "products"],
    "properties": {
        "id": {"type": "integer"},
        "userId": {"type": "integer"},
        "date": {"type": "string", "format": "date-time"},
        "products": {
            "type": "array",
            "minItems": 1,
            "items": {
                "type": "object",
                "required": ["productId", "quantity"],
                "properties": {
                    "productId": {"type": "integer"},
                    "quantity": {"type": "integer", "minimum": 1}
                }
            }
        }
    }
}

CARTS_LIST_SCHEMA = {
    "type": "array",
    "items": CART_SCHEMA,
    "minItems": 1,
}

CART_CREATE_SCHEMA = {
    "type": "object",
    "required": ["id", "userId", "products"],
    "properties": {
        "id": {"type": "integer"},
        "userId": {"type": "integer"},
        "date": {"type": "string", "format": "date-time"},  # необязательное поле
        "products": {
            "type": "array",
            "minItems": 1,
            "items": {
                "type": "object",
                "required": ["productId", "quantity"],
                "properties": {
                    "productId": {"type": "integer"},
                    "quantity": {"type": "integer", "minimum": 1}
                }
            }
        }
    }
}
