$(window).load(function() {
  var child1 = document.getElementById('child1');
  var child2 = document.getElementById('child2');
  var parent = document.getElementById('parent');

  var player1 = child1.animate([
    {
      transform: 'translateX(0px)'
    },
    {
      transform: 'translateX(280px)'
    }
  ], {
    duration: 3000,
    iterations: Infinity,
    easing: "ease-in-out",
    direction: "alternate",
    fill: "forwards",
  });

  var player2 = child2.animate([
    {
      transform: 'translateX(500px)'
    },
    {
      transform: 'translateX(0px)'
    }
  ], {
    duration: 3000,
    iterations: Infinity,
    easing: "ease-in-out",
    direction: "alternate",
    fill: "forwards",
  });

    var player3 = parent.animate([
    {
      transform: 'translateY(0px)'
    },
    {
      transform: 'translateY(280px)'
    }
  ], {
    duration: 3000,
    iterations: Infinity,
    easing: "ease-in-out",
    direction: "alternate",
    fill: "forwards",
  });

});
