$(window).ready(function() {
  var container = document.getElementById('battery_container');
  container.addEventListener("load", function(event) {
    var battery =  container.contentDocument;
    var chargeBar =  battery.querySelector('.charge .bar');

    var green = "#8DC63F";
    var yellow = "#F9ED32";
    var red = "#F15A29";

    var player = chargeBar.animate([
      {
	width: "0",
	fill: red,
	offset: 0
      },
      {
	fill: yellow,
	offset: 3/4
      },
      {
	width: "240px",
	fill: green,
	offset: 1
      }
    ], {
      duration: 3000,
      iterations: Infinity,
      easing: "ease-in"
    });
  }, true);

});
