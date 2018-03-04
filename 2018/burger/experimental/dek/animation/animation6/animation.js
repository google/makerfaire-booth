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
	{ transform: 'translateY(' + conveyorY + 'vh)', opacity: 1},
	{ transform: 'translateY(' + finalY + 'vh)', opacity: 1},
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

function create_animation4() {
    var element = document.getElementById("wrapper");

    var timings = {
	duration: 1000,
	iterations: 1,
	easing: "linear",
	direction: "normal",
	fill: "forwards",
    }
    var keyframes = [
	{ transform: 'translateX(0vh) translateY(50vh)'},
	{ transform: 'translateX(100vh) translateY(50vh)'},
    ];
    return new KeyframeEffect(element, keyframes, timings);
}

$(window).ready(function() {
    var animation = [
	["crown", 0, -40, 16, 50],
	["lettuce", 1000, -45, 13, 47],
	["tomato", 2000, -50, 10, 44],
	["cheese", 3000, -55, 7, 41],
	["patty", 4000, -60, 4, 38],
	["heel", 5000, -65, 1, 35],
    ];
    var group1 = create_group(animation, create_animation1);
    var group3 = create_group(animation, create_animation3);
    var group4 = create_animation4();

    var sequence = new SequenceEffect([
	group1,
	group4,
	group3,
    ]);
    var player = new Animation(sequence, document.timeline);
    player.play();
});
