var ractive = new Ractive({
    target: '#generator',
    template: '#template',
    data: {greeting: 'Hello', name: 'world'}
});

function initMap() {

    var uluru = {
        lat: 35.7018391,
        lng: 51.3670471,
    };
    var map = new google.maps.Map(document.getElementById('map'), {
        zoom: 12,
        center: uluru
    });

    for (var i = 0; i < border.length; i++) {
        circle(border[i], 1 * 150, map, '#ff0');
    }

    polygon(border, map, '#d79a42');

    for(var i=0;i<porters.length;i++) {
        porters[i] = new Porter(
            circle(generate(), 150, map, '#00f'),
            porters[i][0], porters[i][1]
        );
        porters[i].get_key();
        porters[i].send_location();
    }

    var applicator_key = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6InNoYWhpbiIsInByaXZpbGVnZXMiOnsiYXBwbGljYXRvciI6IiJ9fQ.KIpobCKJYLmmQJ8-KPWL1J7tdTWNHwOXA1XdSRs3UlQ'
    for(var i=0;i<2;i++) {
        var o = new Order(map);
        o.push(applicator_key);  // (-) o.show();
    }

    $('#button').click(function () {
        o = new Order(map);
        $.post('http://localhost:5000', data = o.order, function (response) {
            o.show();
        });
    });
}