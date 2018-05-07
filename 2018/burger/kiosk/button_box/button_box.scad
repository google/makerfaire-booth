/* A simple console-shaped box, using the overly complicated finger library at hand.
 *
 * Post-processing:
 *
 * 1. some table saw or belt sanding is required on the front and
 *    back pieces (specifically, their top and rear faces need to match the
 *    gPanelAngle below).  It would look prettier if you hand-sand/file the
 *    rear tabs of the top piece, but that can't be easily automated.
 * 2. Chamfer the top of the button holes, and remove the large plastic flange
 *    on the buttons.  (They don't work with 12mm thickness otherwise.)  The
 *    alternative is to include a pocket on the underside.
 */

gMaterialThick = 12.0;
gBitSize = 3.4;
gPanelAngle = 15;
gInsideWidth = 520;
gInsideDepth = 170;
gInsideHeightFront = 40;
gInsideHeightBack = tan(gPanelAngle) * (gInsideDepth + gMaterialThick*2) + gInsideHeightFront;
gTopDepth = (gInsideDepth+gMaterialThick*2)/cos(gPanelAngle);

t = gInsideWidth+gMaterialThick*2;
gFrontTabs = [[0, 0], [1, t/7], [0, t*2/7], [1, t*3/7]];
gFrontCornerTabs = [[0,0], [1, 10], [0, 30], [1, gInsideHeightFront]];
gBackCornerTabs = [[0,0], [1, 30], [0, gInsideHeightBack-30], [1, gInsideHeightBack]];
gSideTabs = [[1, 0], [0, gTopDepth/3], [1, 2*gTopDepth/3], [0, gTopDepth+gMaterialThick]];
gLowerSideTabs = [[0, 0], [1, gMaterialThick+gInsideDepth/3], [0, gMaterialThick+2*gInsideDepth/3], [1, gInsideDepth+gMaterialThick*2]];

include <joinery.scad>

$fn=32;

module F(h, ev) {
  translate([-gInsideWidth/2,0]) difference() {
    union() {
      square([gInsideWidth, h]);
      translate([-gMaterialThick,h])
        generic_finger_positive(gMaterialThick*1.25, gBitSize, mirror_events(gFrontTabs, gInsideWidth+gMaterialThick*2));
      translate([-gMaterialThick,0]) scale([1,-1])
        generic_finger_positive(gMaterialThick, gBitSize, mirror_events(gFrontTabs, gInsideWidth+gMaterialThick*2));
      rotate([0,0,90]) generic_finger_positive(gMaterialThick, gBitSize, ev);
      translate([gInsideWidth,0]) scale([-1,1])
        rotate([0,0,90]) generic_finger_positive(gMaterialThick, gBitSize, ev);
    }
    translate([-gMaterialThick,h])
      generic_finger_negative(gMaterialThick, gBitSize, mirror_events(gFrontTabs, gInsideWidth+gMaterialThick*2), hole=false);
    translate([-gMaterialThick,0]) scale([1,-1])
      generic_finger_negative(gMaterialThick, gBitSize, mirror_events(gFrontTabs, gInsideWidth+gMaterialThick*2));
    rotate([0,0,90]) generic_finger_negative(gMaterialThick, gBitSize, ev);
    translate([gInsideWidth,0]) scale([-1,1])
      rotate([0,0,90]) generic_finger_negative(gMaterialThick, gBitSize, ev);
  }
}

module Front() {
  F(gInsideHeightFront, gFrontCornerTabs);
}

module Back() {
  F(gInsideHeightBack, gBackCornerTabs);
}

module Side() {
  difference() {
    union() {
      difference() {
        union() {
          translate([gMaterialThick,0]) square([gInsideDepth+gMaterialThick,gInsideHeightBack]);
	  translate([gInsideDepth+gMaterialThick*2,gInsideHeightBack]) square([gMaterialThick, gMaterialThick]);
	}
        translate([0,gInsideHeightFront+0.1]) rotate([0,0,gPanelAngle]) square([1000,1000]);
      }
      translate([0,gInsideHeightFront])
        rotate([0,0,gPanelAngle])
        generic_finger_positive(gMaterialThick, gBitSize, gSideTabs);
      scale([1,-1])
        generic_finger_positive(gMaterialThick, gBitSize, gLowerSideTabs);
      translate([gMaterialThick, 0])
        rotate([0,0,90]) generic_finger_positive(gMaterialThick, gBitSize, negate_events(gFrontCornerTabs));
      translate([gInsideDepth+gMaterialThick*2, 0])
        scale([-1,1]) rotate([0,0,90]) generic_finger_positive(gMaterialThick, gBitSize, negate_events(gBackCornerTabs));
    }
    translate([0,gInsideHeightFront])
      rotate([0,0,gPanelAngle])
      generic_finger_negative(gMaterialThick, gBitSize, gSideTabs, hole=false);
    scale([1,-1])
      generic_finger_negative(gMaterialThick, gBitSize, gLowerSideTabs);
    translate([gMaterialThick, 0])
      rotate([0,0,90]) generic_finger_negative(gMaterialThick, gBitSize, negate_events(gFrontCornerTabs), hole=false);
    translate([gInsideDepth+gMaterialThick*2, 0])
      scale([-1,1]) rotate([0,0,90]) generic_finger_negative(gMaterialThick, gBitSize, negate_events(gBackCornerTabs), hole=false);
  }
  // fixup front
  translate([0,gInsideHeightFront]) square([20,10]);
  // fixup back
  translate([gInsideDepth+gMaterialThick*2-gBitSize,gInsideHeightBack]) square([10,10]);
}

module Top() {
  w=gInsideWidth;
  h=gTopDepth;
  ev = negate_events(mirror_events(gFrontTabs, w+gMaterialThick*2));
  side_ev = negate_events(gSideTabs);
  sp = 120;
  difference() {
    union() {
      translate([-w/2,gMaterialThick]) square([w,h-gMaterialThick]);
      scale([1,-1]) translate([-w/2-gMaterialThick,-gMaterialThick])
        generic_finger_positive(gMaterialThick, gBitSize, ev);
      translate([-w/2-gMaterialThick,h])
        generic_finger_positive(gMaterialThick, gBitSize, ev);
      for(x_scale=[1,-1]) scale([x_scale,1])
        translate([-w/2,0]) rotate([0,0,90]) generic_finger_positive(gMaterialThick, gBitSize, side_ev);
    }
    scale([1,-1]) translate([-w/2-gMaterialThick,-gMaterialThick])
      generic_finger_negative(gMaterialThick, gBitSize, ev);
    translate([-w/2-gMaterialThick,h])
      generic_finger_negative(gMaterialThick, gBitSize, ev);
    for(x_scale=[1,-1]) scale([x_scale,1])
      translate([-w/2,0]) rotate([0,0,90]) generic_finger_negative(gMaterialThick, gBitSize, side_ev);

    // button holes
    for(x=[sp/2, 3*sp/2, -sp/2, -3*sp/2]) translate([x,h/2]) circle(d=24,$fn=128);
  }
}

module Bottom() {
  // Note this is not quite symmetrical in Y!
  ev = negate_events(mirror_events(gFrontTabs, gInsideWidth+gMaterialThick*2));
  side_ev = negate_events(gLowerSideTabs);
  difference() {
    union() {
      square([gInsideWidth,gInsideDepth+gMaterialThick], center=true);
      translate([-gInsideWidth/2-gMaterialThick,0]) for(y_scale=[1,-1]) scale([1,y_scale])
        translate([0,(gInsideDepth+gMaterialThick)/2]) generic_finger_positive(gMaterialThick, gBitSize, ev);
      for(x_scale=[1,-1]) scale([x_scale,1])
        translate([-gInsideWidth/2,-(gInsideDepth+gMaterialThick*3)/2])
        rotate([0,0,90]) generic_finger_positive(gMaterialThick, gBitSize, side_ev);
    }
    translate([-gInsideWidth/2-gMaterialThick,0]) for(y_scale=[1,-1]) scale([1,y_scale])
      translate([0,(gInsideDepth+gMaterialThick)/2]) generic_finger_negative(gMaterialThick, gBitSize, ev, hole=false);
    for(x_scale=[1,-1]) scale([x_scale,1])
      translate([-gInsideWidth/2,-(gInsideDepth+gMaterialThick*3)/2])
      rotate([0,0,90]) generic_finger_negative(gMaterialThick, gBitSize, side_ev, hole=false);
  }
  // patch up hole
  for(x_scale=[1,-1]) scale([x_scale,1])
    translate([gInsideWidth/2-gBitSize,gInsideDepth/2]) square([10,10]);
}

// Hard-coded numbers, change if piece sizes change.
module CutPlan1() {
  translate([0,0]) Top();
  translate([0,-gInsideHeightFront-8-gMaterialThick]) Front();
}

module CutPlan2() {
  Back();
  translate([0,-120]) Bottom();
}

module CutPlan3() {
  Side();
  translate([215,0]) Side();
}

module AllCutPlans() {
  rotate([0,0,90]) CutPlan1();
  translate([184,0]) rotate([0,0,90]) CutPlan2();
  translate([-20,290]) CutPlan3();
}

module All() {
  rotate([90,0,0]) linear_extrude(height=gMaterialThick) Front();
  translate([0,gInsideDepth+gMaterialThick*2,0]) rotate([90,0,0]) linear_extrude(height=gMaterialThick) Back();
  for(x_scale=[1,-1]) scale([x_scale,1,1])
    translate([gInsideWidth/2,-gMaterialThick,0]) rotate([90,0,90])
    linear_extrude(height=gMaterialThick) Side();
  translate([0,-gMaterialThick,gInsideHeightFront])
    rotate([gPanelAngle,0,0]) linear_extrude(height=gMaterialThick) Top();
  translate([0,(gInsideDepth+gMaterialThick)/2,-gMaterialThick]) linear_extrude(height=gMaterialThick) Bottom();
}

All();
//AllCutPlans();
//Bottom();
//Side();
//Top();
//Front();
