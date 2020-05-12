PERMISSIONS_SCHEMA = {
    "groups": {
        "required": True,
        "type": "list",
        "schema": {
            "type": "dict",
            "schema": {
                "name": {"required": True, "type": "string"},
                "permissions": {
                    "required": False,
                    "type": "dict",
                    "keysrules": {"required": True, "type": "string"},
                    "valuesrules": {
                        "type": "list",
                        "schema": {
                            "required": True,
                            "type": "string",
                            "regex": "^[a-z0-9]+.[a-z0-9]+_[a-z0-9]+$",
                        },
                    },
                },
            },
        },
    }
}
