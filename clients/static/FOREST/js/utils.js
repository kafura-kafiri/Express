var inside = function (point, vs) {
    // ray-casting algorithm based on
    // http://www.ecse.rpi.edu/Homepages/wrf/Research/Short_Notes/pnpoly.html

    var x = point[0], y = point[1];

    var inside = false;
    for (var i = 0, j = vs.length - 1; i < vs.length; j = i++) {
        var xi = vs[i][0], yi = vs[i][1];
        var xj = vs[j][0], yj = vs[j][1];

        var intersect = ((yi > y) != (yj > y))
            && (x < (xj - xi) * (y - yi) / (yj - yi) + xi);
        if (intersect) inside = !inside;
    }

    return inside;
};

var distance = function (v, u) {
    var x = Math.pow(Math.abs(v[0] - u[0]), 2);
    var y = Math.pow(Math.abs(v[1] - u[1]), 2);
    return Math.sqrt(x + y);
};


var generate = function (r) {
    var p = [
        frame[0][0] + Math.random() * (frame[1][0] - frame[0][0]),
        frame[0][1] + Math.random() * (frame[1][1] - frame[0][1])
    ];
    if (inside(p, border)) {
        return p;
    } else return generate(r)
};

var arrow = function (r) {
    var v = generate(r);
    while (true) {
        u = generate(r);
        if (true) {
            return [v, u];
        }
    }
};
