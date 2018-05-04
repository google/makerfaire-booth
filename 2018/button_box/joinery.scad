function negate_events(events) = [for(ev=events) [1-ev[0], ev[1]]];
// TODO symmetrical version, or one that does something specific with the new part

function offset_events(ev, symmetric_value) = [for(i=[0:len(ev)-1]) (i==0?ev[i]:i==len(events)-1?[ev[i][0], ev[i][1]+symmetric_value*2]:[ev[i][0], ev[i][1]+symmetric_value])];

function mirror_events(ev, width) = [for(i=[0:len(ev)*2-1]) (i<len(ev)?ev[i]:[1-ev[len(ev)-(i-len(ev)+1)][0], width-ev[len(ev)-(i-len(ev)+1)][1]])];

// first and last events define steady-state.
module generic_finger_positive(material_thickness, bit_size, events) {
  echo(events);
  for(i=[0:len(events)-1]) {
    if(events[i][0] == 1 && i < len(events)-1) { //begin notch
      translate([events[i][1], 0]) square([events[i+1][1]-events[i][1], material_thickness]);
    }
  }
}

module generic_finger_negative(material_thickness, bit_size, events, hole=true) {
  for(i=[0:len(events)-1]) {
    if((events[i][0] == 1) && i < len(events)-1) { // begin notch
      // can we always ignore last one, or need to know width?
      translate([events[i][1]-bit_size/2,0]) circle(d=bit_size);
      if(hole)
        translate([(events[i+1][1]+events[i][1])/2, material_thickness/2]) circle(d=bit_size);
    } else if(events[i][0] == 0 && i > 0) {
      translate([events[i][1]+bit_size/2,0]) circle(d=bit_size);
    }
  }
}
