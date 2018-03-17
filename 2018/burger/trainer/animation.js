
function create_animation1(element_name, data) {
    var element = document.getElementById(element_name);
    var body = document.getElementsByTagName("BODY")[0];
    width = body.getBoundingClientRect().width;
    height = body.getBoundingClientRect().height;

    var timings = {
	duration: 1000,
	iterations: 1,
	easing: "linear",
	direction: "normal",
	fill: "forwards",
	delay: data.delay,
    }

    var keyframes = [
	{ transform: 'translateX(' + (width/2 - 128) + 'px) translateY(' + data.initialY + ')', opacity: 1},
	{ transform: 'translateX(' + (width/2 - 128) + 'px) translateY(' + data.conveyorY + ')', opacity: 1},
    ];
    return new KeyframeEffect(element, keyframes, timings);
}

function create_animation2(element_name, data) {
    var element = document.getElementById(element_name);
    var body = document.getElementsByTagName("BODY")[0];
    width = body.getBoundingClientRect().width;
    height = body.getBoundingClientRect().height;

    var timings = {
	duration: 1000,
	iterations: 1,
	easing: "linear",
	direction: "normal",
	fill: "forwards",
    }

    var dest = data.dest == 'left' ? 0 : width-256;
    var keyframes = [
	{ transform: 'translateX(' + (width/2 - 128) + 'px) translateY(' + data.conveyorY + ')', opacity: 1},
	{ transform: 'translateX(' + dest + 'px) translateY(' + data.conveyorY + ')', opacity: 1},
    ];
    return new KeyframeEffect(element, keyframes, timings);
}

function create_animation3(element_name, data) {
    var element = document.getElementById(element_name);
    var body = document.getElementsByTagName("BODY")[0];
    width = body.getBoundingClientRect().width;
    height = body.getBoundingClientRect().height;

    var timings = {
	duration: 1000,
	iterations: 1,
	easing: "linear",
	direction: "normal",
	fill: "forwards",
    }
    var dest = data.dest == 'left' ? 0 : width-256;
    var keyframes = [
	{ transform: 'translateX(' + dest + 'px) translateY(' + data.conveyorY + ')', opacity: 1},
	{ transform: 'translateX(' + dest + 'px) translateY(' + data.finalY + ')', opacity: 1},
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

function create_chute() {
    var svgNS = 'http://www.w3.org/2000/svg';
    var chute = document.createElementNS(svgNS, "svg");
    chute.setAttributeNS(null, 'id', 'chute');
    var chuteline1 = document.createElementNS(svgNS, 'line');
    chuteline1.setAttributeNS(null, 'id', 'chuteline1');
    chuteline1.setAttributeNS(null, 'style', 'stroke:rgb(255,0,0);stroke-width:2');
    chute.appendChild(chuteline1);
    var chuteline2 = document.createElementNS(svgNS, 'line');
    chuteline2.setAttributeNS(null, 'id', 'chuteline2');
    chuteline2.setAttributeNS(null, 'style', 'stroke:rgb(255,0,0);stroke-width:2');
    chute.appendChild(chuteline2);
    document.body.appendChild(chute);
    
    var width = chute.getBoundingClientRect().width;
    var height = chute.getBoundingClientRect().height;
    chuteline1.setAttributeNS(null, 'x1', width/2 - 128);
    chuteline1.setAttributeNS(null, 'y1', 0);
    chuteline1.setAttributeNS(null, 'x2', width/2 - 128);
    chuteline1.setAttributeNS(null, 'y2', height);
    chuteline2.setAttributeNS(null, 'x1', width/2 + 128);
    chuteline2.setAttributeNS(null, 'y1', 0);
    chuteline2.setAttributeNS(null, 'x2', width/2 + 128);
    chuteline2.setAttributeNS(null, 'y2', height);
}

var leftBurger = null;
var rightBurger = null;

function start_animation() {
    var layers = [ 'crown', 'crown', 'crown', 'lettuce', 'tomato', 'cheese', 'patty', 'heel' ];
    var wrapper = create_burger(layers);
    document.body.appendChild(wrapper);
    var baseInitialY = -300;
    var baseConveyorY = 420;
    var baseFinalY = 1000;
    var animation = [];
    var dest;
    // use leftBurger and rightBurger to determine if we need to make a random choice;
    if (leftBurger == null && rightBurger == null) {
	if (Math.random() < 0.5) {
	    dest = 'left';
	} else {
	    dest = 'right';
	}
    } else if (leftBurger == null) {
	dest = 'left'; 
    } else if (rightBurger == null) {
	dest = 'right';
    } else {
	console.log("Can't start animation yet.");
	return;
    }
    for (i = 0; i < 8; i++) {
	animation.push(["layer" + (7-i+1), {
	    delay: i*1000,
	    initialY: (baseInitialY - i * 50) + 'px',
	    conveyorY: (baseConveyorY - i * 50) + 'px',
	    finalY: (baseFinalY - i * 50) + 'px',
	    dest: dest
	}]);
    }
    var group1 = create_group(animation, create_animation1);
    var group2 = create_group(animation, create_animation2);

    var sequence = new SequenceEffect([
    	group1,
    	group2,
    ]);
    
    var player = new Animation(sequence, document.timeline);
    player.onfinish = wait_for_keypress(animation, dest, wrapper);
    player.play();
}

function after_keypress(animation, keydownHandler, dest, wrapper) {
    var group = create_group(animation, create_animation3);
    var player = new Animation(group, document.timeline);
    document.removeEventListener('keydown', keydownHandler);
    player.onfinish = function() {
	if (dest == 'left') {
	    leftBurger = null;
	} else if (dest == 'right') {
	    rightBurger = null;
	}
	wrapper.remove();
    }
    player.play();
}

function wait_for_keypress(animation, dest, wrapper) {
    start_animation();
    var yesCode, noCode;
    if (dest == 'left') {
	leftBurger = wrapper;
	yesCode = "Z".charCodeAt(0);
	noCode = "X".charCodeAt(0);
    } else if (dest == 'right') {
	rightBurger = wrapper;
	yesCode = "N".charCodeAt(0);
	noCode = "M".charCodeAt(0);
    } else {
	console.log("Unexpected dest:" + dest);
	return;
    }
    function keydownHandler(e) {
	if (e.keyCode == yesCode || e.keyCode == noCode) {
	    after_keypress(animation, this.keydownHandler, dest, wrapper);
	}
    }
    document.addEventListener('keydown', keydownHandler, false);
}

$(window).ready(function() {
    create_chute();
    var layers = [ 'crown', 'crown', 'crown', 'lettuce', 'tomato', 'cheese', 'patty', 'heel' ];
    start_animation();
});
