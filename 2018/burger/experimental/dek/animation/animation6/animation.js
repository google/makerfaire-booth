function create_animation0() {
    var element = document.getElementById("wrapper");

    var timings = {
	duration: 1000,
	iterations: 1,
	easing: "linear",
	direction: "normal",
	fill: "forwards",
    }
    var keyframes = [
	{ transform: 'translateX(90vh) translateY(50vh)'},
	{ transform: 'translateX(0vh) translateY(50vh'},
    ];
    return new KeyframeEffect(element, keyframes, timings);
}

function create_animation1(element_name, data) {
    var element = document.getElementById(element_name);

    var timings = {
	duration: 1000,
	iterations: 1,
	easing: "linear",
	direction: "normal",
	fill: "forwards",
	delay: data.delay,
    }
    var keyframes = [
	{ transform: 'translateY(' + data.initialY + 'vh)', opacity: 1},
	{ transform: 'translateY(' + data.conveyorY + 'vh)', opacity: 1},
    ];
    return new KeyframeEffect(element, keyframes, timings);
}

function create_animation3(element_name, data) {
    var element = document.getElementById(element_name);

    var timings = {
	duration: 1000,
	iterations: 1,
	easing: "linear",
	direction: "normal",
	fill: "forwards",
    }
    var keyframes = [
	{ transform: 'translateY(' + data.conveyorY + 'vh)', opacity: 1},
	{ transform: 'translateY(' + data.finalY + 'vh)', opacity: 1},
    ];
    return new KeyframeEffect(element, keyframes, timings);
}

function create_group(animation, f) {
    var kEffects = [];
    for (let a of animation) {
	var kf = f(a[0], a[1]);
	kEffects.push(kf);
    }
    var group = new GroupEffect(kEffects);
    return group;
}

function create_animation2() {
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
	{ transform: 'translateX(90vh) translateY(50vh'},
    ];
    return new KeyframeEffect(element, keyframes, timings);
}

$(window).ready(function() {
    var animation = [
	["crown", {delay: 0, initialY: -40, conveyorY: 16, finalY: 70}],
	["lettuce", {delay:1000, initialY:-45, conveyorY: 13, finalY: 67}],
	["tomato", {delay:2000, initialY:-50, conveyorY: 10, finalY: 64}],
	["cheese", {delay:3000, initialY:-55, conveyorY: 7, finalY: 61}],
	["patty", {delay:4000, initialY: -60, conveyorY: 4, finalY: 58}],
	["heel", {delay:5000, initialY: -65, conveyorY: 1, finalY: 55}],
    ];
    var group0 = create_animation0();
    var group1 = create_group(animation, create_animation1);
    var group2 = create_animation2();
    var group3 = create_group(animation, create_animation3);

    var sequence = new SequenceEffect([
	group0,
	group1,
	group2,
	group3,
    ]);
    var player = new Animation(sequence, document.timeline);
    player.play();
    
    player.onfinish = function() {
	player.play();
    };
});
