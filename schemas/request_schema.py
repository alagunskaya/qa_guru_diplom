CREATE_PRODUCT_REQUEST_SCHEMA = {
    "type": "object",
    "required": ["title", "price", "description", "category", "image"],
    "properties": {
        "title": {"type": "string"},
        "price": {"type": "number"},
        "description": {"type": "string"},
        "category": {"type": "string"},
        "image": {"type": "string", "format": "uri"},
    }
}

CREATE_CART_REQUEST_SCHEMA = {
    "type": "object",
    "required": ["userId", "products"],
    "properties": {
        "userId": {"type": "integer"},
        "products": {
            "type": "array",
            "items": {
                "type": "object",
                "required": ["productId", "quantity"],
                "properties": {
                    "productId": {"type": "integer"},
                    "quantity": {"type": "integer"}
                }
            }
        }
    }
}
