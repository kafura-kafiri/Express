var circle = function (center, radius, map, color) {
    return new google.maps.Circle({
        strokeColor: color,
        strokeOpacity: 0.8,
        strokeWeight: 2,
        fillColor: color,
        fillOpacity: 0.35,
        map: map,
        center: {
            lat: center[0],
            lng: center[1]
        },
        radius: radius
    });
};

var rectangle = function (center, radius, map, color) {
    radius /= 100000;
    return new google.maps.Rectangle({
        strokeColor: color,
        strokeOpacity: 0.8,
        strokeWeight: 2,
        fillColor: color,
        fillOpacity: 0.35,
        map: map,
        bounds: {
            north: center[0] + radius,
            south: center[0] - radius,
            east: center[1] + radius,
            west: center[1] - radius,
        }
    });
};

var triangle = function (center, radius, map, color) {
    radius /= 100000;
    path = [
        {
            lat: center[0] + radius * 2 / 3,
            lng: center[1]
        }, {
            lat: center[0] - radius / 2,
            lng: center[1] + radius * Math.sqrt(3) / 2
        }, {
            lat: center[0] - radius / 2,
            lng: center[1] - radius * Math.sqrt(3) / 2
        }, {
            lat: center[0] + radius * 2 / 3,
            lng: center[1]
        }
    ];
    new google.maps.Polygon({
        paths: path,
        strokeColor: color,
        strokeOpacity: 0.8,
        strokeWeight: 2,
        fillColor: color,
        fillOpacity: 0.35,
        map: map,
    });
};

var polygon = function(paths, map, color) {
    var _paths = [];
    for(var i=0;i<paths.length;i++)
        _paths.push({lat: paths[i][0], lng: paths[i][1]});
    new google.maps.Polygon({
        paths: _paths,
        strokeColor: color,
        strokeOpacity: 0.8,
        strokeWeight: 1,
        fillColor: color,
        fillOpacity: 0.07,
        map: map,
    });
};
