// wiffle ball

color([1,1,1]) {
    difference() {
        difference() {
            sphere(40, $fn=100); // baseball 72.64–74.68 mm
            sphere(38, $fn=100);
        }
        union() {
            holes();
            rotate([180,0,0]) holes();
        }
    }
}    
module holeObject() {
    translate([0,0,20]) {
        linear_extrude(height = 20) {
            rounded_ngon(2,13,5);
            }
        }
}

module holes() {
    union() {
        for (a = [ 0 : 45 : 360 ])
            rotate([0,50,a]) holeObject();
    }
}

module rounded_ngon(num, r, rounding = 0) {
  function v(a) = let (d = 360/num, v = floor((a+d/2)/d)*d) (r-rounding) * [cos(v), sin(v)];
  polygon([for (a=[0:360-1]) v(a) + rounding*[cos(a),sin(a)]]);
}
