var Order = function (map) {
    this.o = arrow();
    this.order = {
        src: this.o[0],
        dst: this.o[1],
        item: {
            name: 'huli huli',
            volume: 5,
        }
    };

    this.show = function () {
        var vendor = rectangle(this.o[0], 150, map, '#00ba00');
        var applicator = triangle(this.o[1], 200, map, '#882292');
        var line = new google.maps.Polyline({
            path: [{
                lat: this.o[0][0],
                lng: this.o[0][1],
            }, {
                lat: this.o[1][0],
                lng: this.o[1][1],
            }],
            geodesic: true,
            strokeColor: '#FF0000',
            strokeOpacity: 1.0,
            strokeWeight: 2,
            map: map,
        });
    };

    this.push = function(key) {
        var o = this;
        $.post('/orders/',
            {
                key: key,
                'item.id': 'pesteh',
                'item.volume': 3,
                'applicator.phone': "'09133657623'",
                'map.src.0': 0,
                'map.src.1': 0,
                'map.dst.0': 1,
                'map.dst.1': 1,
                'type': 3,
                'status': 0,
            },
            function() {
                o.show();
                orders.push(this)
            });
    }
};