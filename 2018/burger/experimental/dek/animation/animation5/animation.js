function create_animation1(element_name) {
  var element = document.getElementById(element_name);

  var timings = {
    duration: 5000,
    iterations: 1,
    easing: "linear",
    direction: "normal",
    fill: "forwards",
  }
  var keyframes = [
    { transform: 'translateX(0) translateY(0vh)' },
    { transform: 'translateX(0) translateY(70vh)' },
    { transform: 'translateX(70vh) translateY(70vh)' },
  ];
  return new KeyframeEffect(element, keyframes, timings);
}

$(window).ready(function() {
  var kf = create_animation1("045");

  var player = new Animation(kf, document.timeline);
  player.play();
});
