status = {
    '0': "init",
    '1': "ready",
    '2': "at",
    '3': "picked",
    '4': "delivered"
}

obj = {
    "crate": {},
    "transmitter": {

    },
    "receiver": {

    },
    "timeline": {
        "init": {
            "by": "",
            "at": "",
        }
    },
}

schema = {
    "crate": {
        "id": (".crate_id", "str"),
        "volume": ("$volume", "int"),
    },
    "transmitter": {
        "username": ("$transmitter_username", "str"),
        "phone": ("$transmitter_phone", "str"),
        "first_name": ("$transmitter_first_name", "str"),
        "last_name": ("$transmitter_last_name", "str"),
        "coordinates": [
            ("$transmitter_lat", "num"),
            ("$transmitter_lng", "num")
        ]
    },
    "receiver": {
        "username": ("$receiver_username", "str"),
        "phone": ("$receiver_phone", "str"),
        "first_name": ("$receiver_first_name", "str"),
        "last_name": ("$receiver_last_name", "str"),
        "coordinates": [
            ("$receiver_lat", "num"),
            ("$receiver_lng", "num")
        ]
    },
    "timeline": {
        "init": {
            "by": ("-username", "str")
        }
    }
}
