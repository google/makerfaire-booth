function animation() {
  var crown = document.getElementById('crown');
  var lettuce = document.getElementById('lettuce');
  var tomato = document.getElementById('tomato');
  var cheese = document.getElementById('cheese');
  var patty = document.getElementById('patty');
  var heel = document.getElementById('heel');

  var timings = {
    duration: 3000,
    delay: 10,
    iterations: Infinity,
    easing: "ease-in-out",
    direction: "alternate",
    fill: "forwards",

  }
  var keyframes = [
    { transform: 'scale(1)' },
    { transform: 'scale(0.1) translateY(-100%)'},
  ];

  var kEffects = [
    new KeyframeEffect(crown, keyframes, timings),
    new KeyframeEffect(lettuce, keyframes, timings),
    new KeyframeEffect(tomato, keyframes, timings),
    new KeyframeEffect(cheese, keyframes, timings),
    new KeyframeEffect(patty, keyframes, timings),
    new KeyframeEffect(heel, keyframes, timings),
  ];

  var group = new GroupEffect(kEffects);
  var player = new Animation(group, document.timeline);

  return player;
}

function animation1() {
  var crown = document.getElementById('crown');
  var lettuce = document.getElementById('lettuce');
  var tomato = document.getElementById('tomato');
  var cheese = document.getElementById('cheese');
  var patty = document.getElementById('patty');
  var heel = document.getElementById('heel');

  var timings = {
    duration: 3000,
    delay: 10,
    iterations: 1,
    easing: "ease-in-out",
    direction: "alternate",
    fill: "forwards",

  }
  var keyframes = [
    { transform: 'scale(1)' },
    { transform: 'scale(0.1) translateY(-100%)'},
  ];

  var kEffects = [
    new KeyframeEffect(crown, keyframes, timings),
    new KeyframeEffect(lettuce, keyframes, timings),
    new KeyframeEffect(tomato, keyframes, timings),
    new KeyframeEffect(cheese, keyframes, timings),
    new KeyframeEffect(patty, keyframes, timings),
    new KeyframeEffect(heel, keyframes, timings),
  ];

  var group = new SequenceEffect(kEffects);
  var player = new Animation(group, document.timeline);

  return player;
}

function animation2() {
  var crown = document.getElementById('crown');
  var lettuce = document.getElementById('lettuce');
  var tomato = document.getElementById('tomato');
  var cheese = document.getElementById('cheese');
  var patty = document.getElementById('patty');
  var heel = document.getElementById('heel');

  var timings = {
    duration: 3000,
    delay: 10,
    iterations: 1,
    easing: "linear",
    direction: "normal",
    fill: "forwards",

  }
  var keyframes = [
    { transform: 'translateY(0)' },
    { transform: 'translateY(100%)'},
  ];

  var kEffects = [
    new KeyframeEffect(crown, keyframes, timings),
    new KeyframeEffect(lettuce, keyframes, timings),
    new KeyframeEffect(tomato, keyframes, timings),
    new KeyframeEffect(cheese, keyframes, timings),
    new KeyframeEffect(patty, keyframes, timings),
    new KeyframeEffect(heel, keyframes, timings),
  ];

  var group = new SequenceEffect(kEffects);

  var player = new Animation(group, document.timeline);

  return player;
}

function animation2() {
  var crown = document.getElementById('crown');
  var lettuce = document.getElementById('lettuce');
  var tomato = document.getElementById('tomato');
  var cheese = document.getElementById('cheese');
  var patty = document.getElementById('patty');
  var heel = document.getElementById('heel');

  var timings = {
    duration: 3000,
    delay: 10,
    iterations: 1,
    easing: "linear",
    direction: "normal",
    fill: "forwards",

  }
  var keyframes = [
    { transform: 'translateY(0)' },
    { transform: 'translateY(100%)'},
  ];

  var kEffects = [
    new KeyframeEffect(crown, keyframes, timings),
    new KeyframeEffect(lettuce, keyframes, timings),
    new KeyframeEffect(tomato, keyframes, timings),
    new KeyframeEffect(cheese, keyframes, timings),
    new KeyframeEffect(patty, keyframes, timings),
    new KeyframeEffect(heel, keyframes, timings),
  ];

  var group = new SequenceEffect(kEffects);
  var player = new Animation(group, document.timeline);

  return player;
}

$(window).ready(function() {
  player = animation2();
  player.play();
});
