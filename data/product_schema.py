single_product_schema = {
    "type": "object",
    "properties": {
        "responseCode": {"type": "integer"},
        "product": {
            "type": "object",
            "properties": {
                "id": {"type": "integer"},
                "name": {"type": "string"},
                "price": {"type": "string"},
                "category": {
                    "type": "object",
                    "properties": {
                        "usertype": {
                            "type": "object",
                            "properties": {
                                "usertype": {"type": "string"}
                            },
                            "required": ["usertype"]
                        },
                        "category": {"type": "string"}
                    },
                    "required": ["usertype", "category"]
                }
            },
            "required": ["id", "name", "price", "category"]
        }
    },
    "required": ["responseCode", "product"]
}
