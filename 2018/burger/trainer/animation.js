function create_animation0(wrapper) {
    var timings = {
	duration: 1000,
	iterations: 1,
	easing: "linear",
	direction: "normal",
	fill: "forwards",
    }
    var keyframes = [
	{ transform: 'translateX(90vh) translateY(500px)'},
	{ transform: 'translateX(0vh) translateY(500px)'},
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
	{ transform: 'translateY(' + data.initialY + ')', opacity: 1},
	{ transform: 'translateY(' + data.conveyorY + ')', opacity: 1},
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
	{ transform: 'translateX(0vh) translateY(500px)'},
	{ transform: 'translateX(90vh) translateY(500px)'},
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
	{ transform: 'translateY(' + data.conveyorY + ')', opacity: 1},
	{ transform: 'translateY(' + data.finalY + ')', opacity: 1},
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

function create_burger(layers) {
    var svgNS = 'http://www.w3.org/2000/svg';
    var wrapper = document.createElement("div");
    wrapper.setAttribute('id', "wrapper");
    for (i = 0; i < layers.length; i++) {
    	var svg = document.createElementNS(svgNS, "svg");
    	svg.setAttributeNS(null, 'id', 'layer' + (i+1).toString());
    	svg.setAttributeNS(null, 'class', layers[i]);
    	var use = document.createElementNS(svgNS, 'use');
    	use.setAttributeNS(null, 'href', 'element.svg#shape')
    	svg.appendChild(use);
    	wrapper.appendChild(svg);
    }
    return wrapper;
}

function start_animation() {
    var layers = [ 'crown', 'crown', 'crown', 'lettuce', 'tomato', 'cheese', 'patty', 'heel' ];
    var wrapper = create_burger(layers);
    document.body.appendChild(wrapper);
    var animation = [
    	["layer8", {delay: 0, initialY: '-300px', conveyorY: '420px', finalY: '1000px'}],
    	["layer7", {delay:1000, initialY: '-350px', conveyorY: '370px', finalY: '950px'}],
    	["layer6", {delay:2000, initialY: '-400px', conveyorY: '320px', finalY: '900px'}],
    	["layer5", {delay:3000, initialY: '-450px', conveyorY: '270px', finalY: '850px'}],
    	["layer4", {delay:4000, initialY: '-500px', conveyorY: '220px', finalY: '800px'}],
    	["layer3", {delay:5000, initialY: '-550px', conveyorY: '170px', finalY: '750px'}],
    	["layer2", {delay:6000, initialY: '-600px', conveyorY: '120px', finalY: '700px'}],
    	["layer1", {delay:7000, initialY: '-650px', conveyorY: '70px', finalY: '650px'}],
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
	wrapper.remove();
	start_animation();
    }
}

$(window).load(function() {
    start_animation();
});

