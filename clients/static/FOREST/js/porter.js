function Porter(marker, username, password) {
    this.marker = marker;
    this.username = username;
    this.password = password;
    this.status = '';
    this.get_key = function() {
        var p = this;
        $.post('/key', {'username': p.username, 'password': p.password}, function(key) {
            p.key = key;
            console.log(key);
        }).fail(function(response) {
            alert('Error: ' + response.responseText);
        });
    };

    this._send_location = function() {
        if(this.key) {
            var c = this.marker.center;
            $.post('/locations/' + c.lat() + ',' + c.lng(), {'key': this.key});
            // this.marker.setCenter({lat: c.lat() + .0001, lng: c.lng() + .0001});
        }
    };

    this.send_location = function() {
        var p = this;
        setInterval(function() {
            p._send_location();
        }, 1000);
    };

    this.ack = function(_id, response, f) {
        $.post('/routes/{_id}/@ack:{response}'.format(_id, response), f);
    };

    this.route_request = function() {
        p = this;
        $.post('/users/route_request'.format(p.key), function(route) {
            p.ack(route, true, function() {
                this.routes.add(route);
            });
        });
    };

    this.status = function(route) {
        orders = route['orders'];
        for(var i=0;i<orders.length;i++) {
            status = orders[i]['action'];
            _id = orders[i]['_id'];
            $.post('/orders/{_id}/@status:{status}'.format(_id, status));
        }
    };

    this.move = function(t) {
        if(this.routes.length == 0)
            this.route_request();
        if(!this.move_permission || t == 0 || this.routes.length == 0)
            return
        var p = this.marker.folan;
        var r = this.routes[0];
        var steps = r['routes'][0]['legs'][0]['steps']
        if(steps.length == 0 || steps.length == 1) {
            route = this.routes.pop_back();
            this.status(route);
            this.move(t);
        }
        var step = steps[0];
        var next_step = steps[1];
        var wall = next_step['location'];
        var max_distance = 0;
        var speed = step['distance'] / step['duration'];
        var remain = 0;
        if (max_distance / speed < t) {
            remain = t - max_distance / speed;
            t = max_distance / speed;
        }
        var bearing = step['bearing'];
        var dLat = Math.sin(bearing / 180 * Math.pi) * speed * t;
        var dLng = Math.cos(bearing / 180 * Math.pi) * speed * t;
        this.marker.location = [p[0] + dLat, p[1] + dLng];
    }
}