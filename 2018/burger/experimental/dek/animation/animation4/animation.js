function create_animation1(element_name, delay, initialY, conveyorY, finalY) {
  var element = document.getElementById(element_name);

  var timings = {
    duration: 1000,
    iterations: 1,
    easing: "linear",
    direction: "normal",
    fill: "forwards",
    delay: delay,
  }
  var keyframes = [
    { transform: 'translateY(' + initialY + 'vh)', opacity: 1},
    { transform: 'translateY(' + conveyorY + 'vh)', opacity: 1},
  ];
  return new KeyframeEffect(element, keyframes, timings);
}



function create_animation2(element_name, delay, initialY, conveyorY, finalY) {
  var element = document.getElementById(element_name);

  var timings = {
    duration: 2000,
    iterations: 1,
    easing: "linear",
    direction: "normal",
    fill: "forwards",
  }
  var keyframes = [
    { transform: 'translateY(' + conveyorY + 'vh) translateX(0vh)', opacity: 1},
    { transform: 'translateY(' + conveyorY + 'vh) translateX(100vh)', opacity: 1},
  ];
  return new KeyframeEffect(element, keyframes, timings);
}

function create_animation3(element_name, delay, initialY, conveyorY, finalY) {
  var element = document.getElementById(element_name);

  var timings = {
    duration: 1000,
    iterations: 1,
    easing: "linear",
    direction: "normal",
    fill: "forwards",
  }
  var keyframes = [
    { transform: 'translateY(' + conveyorY + 'vh) translateX(100vh)', opacity: 1},
    { transform: 'translateY(' + finalY + 'vh) translateX(100vh)', opacity: 1},
  ];
  return new KeyframeEffect(element, keyframes, timings);
}

function create_group(animation, f) {
  var kEffects = [];
  for (let a of animation) {
    var kf = f(a[0], a[1], a[2], a[3], a[4]);
    kEffects.push(kf);
  }
  var group = new GroupEffect(kEffects);
  return group;
}

$(window).ready(function() {
  var animation = [
    ["crown", 0, 0, 50, 125],
    ["lettuce", 1000, -5, 45, 120],
    ["tomato", 2000, -10, 40, 115],
    ["cheese", 3000, -15, 35, 110],
    ["patty", 4000, -20, 30, 105],
    ["heel", 5000, -25, 25, 100],
  ];
  var group1 = create_group(animation, create_animation1);
  var group2 = create_group(animation, create_animation2);
  var group3 = create_group(animation, create_animation3);

  var sequence = new SequenceEffect([group1, group2, group3]);
  var player = new Animation(sequence, document.timeline);
  player.play();
});
