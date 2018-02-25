# API
1. [Example](#example)
2. [Example2](#example2)
3. [Third Example](#third-example)

## Stack Holders
1. Applicator: # this user is a customer who needs a delivery or pickup or both.
2. Porter: # this user has a vehicle and moves for our sake
3. Operator: 
4. Company: (ZoodFood | SnappBox)
5. Dev
6. Admin
## Collections
1. Users
    1. types
        * Porter, Applicator, Operator, Dev, SuperUser
    2. schema:
        ```
        {
            "username": username,
            "password": password,
            "first_name": first_name,
            "last_name": last_name,
            "cellphone": cellphone,
            "salt": "",
            "privileges": {},
            "bank": {
                "name": "",
                "account": "",
                "fee_per_order": "",
                "fixed_salary": ""
            },
            "detail": {
                "probation": "",
                "melli_code": "",
                "birth_date": "",
                "sheba": ""
            }
        }
        ```
2. Orders
    1. types
        * PickUp, Delivery, Both, None
    2. schema:
        ```
        {
            'item': {
                'id': '$str',
                "detail": "",
                "#": [],
                'volume': '$int',
            },
            'applicator': {
                'id': '#username',
                'phone': '$str',
            },
            'map': {
                'src': ['$num', '$num', "*str"],
                'dst': ['$num', '$num', "*str"]
            },
            'type': '$int',
            "status": "$int",
            "delay": "*int",
            #  "trip_id": "",
            #  "porter": ""
        }
        ```
    3. __foreign key to: (USER, TRIP, )__
3. Locations:
    1. schema:
        ```
        {
            'item': {
                'id': '$str',
                "detail": "",
                "#": [],
                'volume': '$int',
            },
            'applicator': {
                'id': '#username',
                'phone': '$str',
            },
            'map': {
                'src': ['$num', '$num', "*str"],
                'dst': ['$num', '$num', "*str"]
            },
            'type': '$int',
            "status": "$int",
            "delay": "*int",
            #  "trip_id": "",
            #  "porter": ""
        }
        ```
    2. __foreign key to: (USER, )__
4. Trips:
    1. schema:
        ```
        {
            'item': {
                'id': '$str',
                "detail": "",
                "#": [],
                'volume': '$int',
            },
            'applicator': {
                'id': '#username',
                'phone': '$str',
            },
            'map': {
                'src': ['$num', '$num', "*str"],
                'dst': ['$num', '$num', "*str"]
            },
            'type': '$int',
            "status": "$int",
            "delay": "*int",
            #  "trip_id": "",
            #  "porter": ""
        }
        ```
    2. __foreign key to: (USER, )__
5. Vehicles:
    
6. Histories:

## END POINTS
### Authentication

1. [signup](POST /signup)
2. [get key](POST /key)
3. [log out](POST /logout)

### Users

1. [create user](POST /users/)
2. [get user](GET /users/<_id>/)
3. [delete user](DELETE /users/<_id>/)
4. [add-privilege](POST /users/<_id>)
5. [set-status](POST /@status:<{status}>)
6. [set-shift](POST /@shift:<{shift}>=<{head}>,<{tail}>)
7. [frees](POST /frees/)

### Orders

1. [create order](POST /users/)
2. [get order](GET /users/<_id>/)
3. [delete order](DELETE /users/<_id>/)
4. [unassigned](POST /unassigned)
5. [history-back](POST /history-back:<{days}>)

### Trips

1. [create trip](POST /trips/)
2. [get trip](GET /trips/<_id>/)
3. [delete trip](DELETE /trips/<_id>/)
4. [ack](POST /<{_id}>/<{ack}>)

### Locations

1. [send-location](POST /trips/)

### Vehicles

1. [create vehicle](POST /trips/)
2. [get vehicle](GET /trips/<_id>/)
3. [delete vehicle](DELETE /trips/<_id>/)

