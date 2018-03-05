function create_animation0(wrapper) {
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
    return new KeyframeEffect(wrapper, keyframes, timings);
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

function create_animation2(wrapper) {
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
    return new KeyframeEffect(wrapper, keyframes, timings);
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

$(window).load(function() {
    // var wrapper = document.getElementById("wrapper");
    // document.body.appendChild(wrapper);
    // var elements = [ 'crown', 'lettuce', 'tomato', 'cheese', 'patty', 'heel' ]
    // for (i = 0; i < elements.length; i++) {
    // 	var svg = document.createElementNS(document.documentElement.namespaceURI, "svg");
    // 	svg.setAttribute('id', 'layer' + (i+1).toString());
    // 	svg.setAttribute('class', elements[i]);
    // 	var use = document.createElement('use');
    // 	use.setAttribute('href', 'element.svg#path')
    // 	svg.appendChild(use);
    // 	wrapper.appendChild(svg);
    // }

    var wrapper = document.getElementById("wrapper");
    var animation = [
    	["layer1", {delay: 0, initialY: -40, conveyorY: 16, finalY: 70}],
    	["layer2", {delay:1000, initialY:-45, conveyorY: 13, finalY: 67}],
    	["layer3", {delay:2000, initialY:-50, conveyorY: 10, finalY: 64}],
    	["layer4", {delay:3000, initialY:-55, conveyorY: 7, finalY: 61}],
    	["layer5", {delay:4000, initialY: -60, conveyorY: 4, finalY: 58}],
    	["layer6", {delay:5000, initialY: -65, conveyorY: 1, finalY: 55}],
    ];
    var group0 = create_animation0(wrapper);
    var group1 = create_group(animation, create_animation1);
    var group2 = create_animation2(wrapper);
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

