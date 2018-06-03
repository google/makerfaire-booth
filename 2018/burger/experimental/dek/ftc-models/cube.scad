width = 1;
height = 1;
depth = 1;
offset = 0.02;
cubewidth = (width-2*offset)/3.15;
difference() {
    cube([width,depth,height]);
    union() {
        translate([offset,0.0,offset]) cube([cubewidth,0.9,0.3]);
        translate([offset+cubewidth+offset,0.0,offset]) cube([cubewidth,0.9,0.3]);
        translate([offset+cubewidth+offset+cubewidth+offset,0.0,offset]) cube([cubewidth,0.9,0.3]);

        translate([offset,0.0,offset+cubewidth+offset]) cube([cubewidth,0.9,0.3]);
        translate([offset+cubewidth+offset,0.0,offset+cubewidth+offset]) cube([cubewidth,0.9,0.3]);
        translate([offset+cubewidth+offset+cubewidth+offset,0.0,offset+cubewidth+offset]) cube([cubewidth,0.9,0.3]);

        translate([offset,0.0,offset+cubewidth+offset+cubewidth+offset]) cube([cubewidth,0.9,0.3]);
        translate([offset+cubewidth+offset,0.0,offset+cubewidth+offset+cubewidth+offset]) cube([cubewidth,0.9,0.3]);
        translate([offset+cubewidth+offset+cubewidth+offset,0.0,offset+cubewidth+offset+cubewidth+offset]) cube([cubewidth,0.9,0.3]);
    }
}
