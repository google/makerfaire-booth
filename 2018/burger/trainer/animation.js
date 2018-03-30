const MAX_BURGERS = 6;
const BURGER_LAYER_SPACING = 20;
const BASE_INITIAL_Y = -300;
const BASE_FINAL_Y = 2000;


const layers_enum = Object.freeze({
    0: "empty",
    1: "topbun",
    2: "lettuce",
    3: "tomato",
    4: "cheese",
    5: "patty",
    6: "bottombun"
});
const valid_burgers = [
    [0,0,0,1,5,6],
    [0,0,1,2,5,6],
    [0,0,1,3,5,6],
    [0,0,1,4,5,6],
    [0,0,1,5,2,6],
    [0,0,1,5,3,6],
    [0,0,1,5,4,6],
    [0,0,1,5,5,6],
    [0,1,2,2,5,6],
    [0,1,2,3,5,6],
    [0,1,2,4,5,6],
    [0,1,2,5,2,6],
    [0,1,2,5,3,6],
    [0,1,2,5,4,6],
    [0,1,2,5,5,6],
    [0,1,3,2,5,6],
    [0,1,3,3,5,6],
    [0,1,3,4,5,6],
    [0,1,3,5,2,6],
    [0,1,3,5,3,6],
    [0,1,3,5,4,6],
    [0,1,3,5,5,6],
    [0,1,4,2,5,6],
    [0,1,4,3,5,6],
    [0,1,4,4,5,6],
    [0,1,4,5,2,6],
    [0,1,4,5,3,6],
    [0,1,4,5,4,6],
    [0,1,4,5,5,6],
    [0,1,5,2,2,6],
    [0,1,5,2,3,6],
    [0,1,5,2,4,6],
    [0,1,5,2,5,6],
    [0,1,5,3,2,6],
    [0,1,5,3,3,6],
    [0,1,5,3,4,6],
    [0,1,5,3,5,6],
    [0,1,5,4,2,6],
    [0,1,5,4,3,6],
    [0,1,5,4,4,6],
    [0,1,5,4,5,6],
    [0,1,5,5,2,6],
    [0,1,5,5,3,6],
    [0,1,5,5,4,6],
    [0,1,5,5,5,6],
    [1,2,2,2,5,6],
    [1,2,2,3,5,6],
    [1,2,2,4,5,6],
    [1,2,2,5,2,6],
    [1,2,2,5,3,6],
    [1,2,2,5,4,6],
    [1,2,2,5,5,6],
    [1,2,3,2,5,6],
    [1,2,3,3,5,6],
    [1,2,3,4,5,6],
    [1,2,3,5,2,6],
    [1,2,3,5,3,6],
    [1,2,3,5,4,6],
    [1,2,3,5,5,6],
    [1,2,4,2,5,6],
    [1,2,4,3,5,6],
    [1,2,4,4,5,6],
    [1,2,4,5,2,6],
    [1,2,4,5,3,6],
    [1,2,4,5,4,6],
    [1,2,4,5,5,6],
    [1,2,5,2,2,6],
    [1,2,5,2,3,6],
    [1,2,5,2,4,6],
    [1,2,5,2,5,6],
    [1,2,5,3,2,6],
    [1,2,5,3,3,6],
    [1,2,5,3,4,6],
    [1,2,5,3,5,6],
    [1,2,5,4,2,6],
    [1,2,5,4,3,6],
    [1,2,5,4,4,6],
    [1,2,5,4,5,6],
    [1,2,5,5,2,6],
    [1,2,5,5,3,6],
    [1,2,5,5,4,6],
    [1,2,5,5,5,6],
    [1,3,2,2,5,6],
    [1,3,2,3,5,6],
    [1,3,2,4,5,6],
    [1,3,2,5,2,6],
    [1,3,2,5,3,6],
    [1,3,2,5,4,6],
    [1,3,2,5,5,6],
    [1,3,3,2,5,6],
    [1,3,3,3,5,6],
    [1,3,3,4,5,6],
    [1,3,3,5,2,6],
    [1,3,3,5,3,6],
    [1,3,3,5,4,6],
    [1,3,3,5,5,6],
    [1,3,4,2,5,6],
    [1,3,4,3,5,6],
    [1,3,4,4,5,6],
    [1,3,4,5,2,6],
    [1,3,4,5,3,6],
    [1,3,4,5,4,6],
    [1,3,4,5,5,6],
    [1,3,5,2,2,6],
    [1,3,5,2,3,6],
    [1,3,5,2,4,6],
    [1,3,5,2,5,6],
    [1,3,5,3,2,6],
    [1,3,5,3,3,6],
    [1,3,5,3,4,6],
    [1,3,5,3,5,6],
    [1,3,5,4,2,6],
    [1,3,5,4,3,6],
    [1,3,5,4,4,6],
    [1,3,5,4,5,6],
    [1,3,5,5,2,6],
    [1,3,5,5,3,6],
    [1,3,5,5,4,6],
    [1,3,5,5,5,6],
    [1,4,2,2,5,6],
    [1,4,2,3,5,6],
    [1,4,2,4,5,6],
    [1,4,2,5,2,6],
    [1,4,2,5,3,6],
    [1,4,2,5,4,6],
    [1,4,2,5,5,6],
    [1,4,3,2,5,6],
    [1,4,3,3,5,6],
    [1,4,3,4,5,6],
    [1,4,3,5,2,6],
    [1,4,3,5,3,6],
    [1,4,3,5,4,6],
    [1,4,3,5,5,6],
    [1,4,4,2,5,6],
    [1,4,4,3,5,6],
    [1,4,4,4,5,6],
    [1,4,4,5,2,6],
    [1,4,4,5,3,6],
    [1,4,4,5,4,6],
    [1,4,4,5,5,6],
    [1,4,5,2,2,6],
    [1,4,5,2,3,6],
    [1,4,5,2,4,6],
    [1,4,5,2,5,6],
    [1,4,5,3,2,6],
    [1,4,5,3,3,6],
    [1,4,5,3,4,6],
    [1,4,5,3,5,6],
    [1,4,5,4,2,6],
    [1,4,5,4,3,6],
    [1,4,5,4,4,6],
    [1,4,5,4,5,6],
    [1,4,5,5,2,6],
    [1,4,5,5,3,6],
    [1,4,5,5,4,6],
    [1,4,5,5,5,6],
    [1,5,2,2,2,6],
    [1,5,2,2,3,6],
    [1,5,2,2,4,6],
    [1,5,2,2,5,6],
    [1,5,2,3,2,6],
    [1,5,2,3,3,6],
    [1,5,2,3,4,6],
    [1,5,2,3,5,6],
    [1,5,2,4,2,6],
    [1,5,2,4,3,6],
    [1,5,2,4,4,6],
    [1,5,2,4,5,6],
    [1,5,2,5,2,6],
    [1,5,2,5,3,6],
    [1,5,2,5,4,6],
    [1,5,2,5,5,6],
    [1,5,3,2,2,6],
    [1,5,3,2,3,6],
    [1,5,3,2,4,6],
    [1,5,3,2,5,6],
    [1,5,3,3,2,6],
    [1,5,3,3,3,6],
    [1,5,3,3,4,6],
    [1,5,3,3,5,6],
    [1,5,3,4,2,6],
    [1,5,3,4,3,6],
    [1,5,3,4,4,6],
    [1,5,3,4,5,6],
    [1,5,3,5,2,6],
    [1,5,3,5,3,6],
    [1,5,3,5,4,6],
    [1,5,3,5,5,6],
    [1,5,4,2,2,6],
    [1,5,4,2,3,6],
    [1,5,4,2,4,6],
    [1,5,4,2,5,6],
    [1,5,4,3,2,6],
    [1,5,4,3,3,6],
    [1,5,4,3,4,6],
    [1,5,4,3,5,6],
    [1,5,4,4,2,6],
    [1,5,4,4,3,6],
    [1,5,4,4,4,6],
    [1,5,4,4,5,6],
    [1,5,4,5,2,6],
    [1,5,4,5,3,6],
    [1,5,4,5,4,6],
    [1,5,4,5,5,6],
    [1,5,5,2,2,6],
    [1,5,5,2,3,6],
    [1,5,5,2,4,6],
    [1,5,5,2,5,6],
    [1,5,5,3,2,6],
    [1,5,5,3,3,6],
    [1,5,5,3,4,6],
    [1,5,5,3,5,6],
    [1,5,5,4,2,6],
    [1,5,5,4,3,6],
    [1,5,5,4,4,6],
    [1,5,5,4,5,6],
    [1,5,5,5,2,6],
    [1,5,5,5,3,6],
    [1,5,5,5,4,6],
    [1,5,5,5,5,6]
];



function create_random_layers() {
    var layers = [];
    var empty_layers = Math.floor(Math.random() * (MAX_BURGERS-1));
    for (i = 0; i < empty_layers; i++) {
	layers.push("empty");
    }
    for (i = empty_layers; i < MAX_BURGERS; i++) {
	layers.push(layers_enum[Math.floor(Math.random() * 6)+1]);
    }
    return layers;
}


function create_valid_layers() {
    var layers_idx = valid_burgers[Math.floor(Math.random() * valid_burgers.length)];
    var layers = [];
    for (i = 0; i < layers_idx.length; i++) {
	layers.push(layers_enum[layers_idx[i]]);
    }
    return layers;
}

function create_chute(name, center_x, height) {
    var svgNS = 'http://www.w3.org/2000/svg';
    var chute = document.createElementNS(svgNS, "svg");
    chute.setAttributeNS(null, 'id', 'chute_' + name);
    chute.setAttributeNS(null, 'class', 'chute');
    document.body.appendChild(chute);

    var SIZE=Math.floor(128);
    var chuteline1 = document.createElementNS(svgNS, 'line');
    chuteline1.setAttributeNS(null, 'class', 'chuteline');
    chuteline1.setAttributeNS(null, 'style', 'stroke:rgb(255,0,0);stroke-width:5');
    chuteline1.setAttributeNS(null, 'x1', center_x - SIZE);
    chuteline1.setAttributeNS(null, 'y1', 0);
    chuteline1.setAttributeNS(null, 'x2', center_x - SIZE);
    chuteline1.setAttributeNS(null, 'y2', height);
    chute.appendChild(chuteline1);

    var chuteline2 = document.createElementNS(svgNS, 'line');
    chuteline2.setAttributeNS(null, 'class', 'chuteline');
    chuteline2.setAttributeNS(null, 'style', 'stroke:rgb(255,0,0);stroke-width:5');
    chuteline2.setAttributeNS(null, 'x1', center_x + SIZE);
    chuteline2.setAttributeNS(null, 'y1', 0);
    chuteline2.setAttributeNS(null, 'x2', center_x + SIZE);
    chuteline2.setAttributeNS(null, 'y2', height);
    chute.appendChild(chuteline2);
}

function create_conveyor(width, height) {
    var svgNS = 'http://www.w3.org/2000/svg';
    var conveyor = document.createElementNS(svgNS, "svg");
    conveyor.setAttributeNS(null, 'id', 'conveyor');
    conveyor.setAttributeNS(null, 'class', 'conveyor');
    document.body.appendChild(conveyor);
    var conveyorLine = document.createElementNS(svgNS, 'line');
    conveyorLine.setAttributeNS(null, 'class', 'chuteline');
    conveyorLine.setAttributeNS(null, 'style', 'stroke:rgb(255,0,0);stroke-width:5');
    conveyorLine.setAttributeNS(null, 'x1', 0);
    conveyorLine.setAttributeNS(null, 'y1', height);
    conveyorLine.setAttributeNS(null, 'x2', width);
    conveyorLine.setAttributeNS(null, 'y2', height);
    conveyor.appendChild(conveyorLine);
}

function create_animation1(element_name, data, wrapper) {
    var element = wrapper.children.namedItem(element_name);
    var side = wrapper.getAttribute('id');
    var body = document.getElementsByTagName("BODY")[0];
    var width = body.getBoundingClientRect().width;
    var height = body.getBoundingClientRect().height;

    var timings = {
	duration: 500,
	iterations: 1,
	easing: "linear",
	direction: "normal",
	fill: "forwards",
	delay: data.delay,
    }

    var target = side == 'left' ? 256 : width-256;

    var keyframes = [
	{ transform: 'translateX(' + target + 'px) translateY(' + data.initialY + ')', opacity: 1},
	{ transform: 'translateX(' + target + 'px) translateY(' + data.conveyorY + ')', opacity: 1},
    ];
    return new KeyframeEffect(element, keyframes, timings);
}

function create_layer_height_offsets(spacing=BURGER_LAYER_SPACING) {
    var body = document.getElementsByTagName('body')[0];
    var width = body.getBoundingClientRect().width;
    var height = body.getBoundingClientRect().height;
    var baseConveyorY = height-100-10;
    var animation = [];
    for (i = 0; i < 8; i++) {
	animation.push(["layer" + (MAX_BURGERS-i+1), {
	    delay: i*100,
	    initialY: (BASE_INITIAL_Y - i * spacing) + 'px',
	    conveyorY: (baseConveyorY - i * spacing) + 'px',
	    finalY: (BASE_FINAL_Y - i * spacing) + 'px',
	}]);
    }
    return animation;
}



function create_group(wrapper, f) {
    var burgerOffsets = create_layer_height_offsets();
    var kEffects = [];
    for (let bf of burgerOffsets) {
	var kf = f(bf[0], bf[1], wrapper);
	kEffects.push(kf);
    }
    var group = new GroupEffect(kEffects);
    return group;
}

function create_burger(layers, side) {
    var svgNS = 'http://www.w3.org/2000/svg';
    var wrapper = document.createElement("div");
    wrapper.setAttribute('class', "wrapper");
    wrapper.setAttribute('id', side);
    for (i = 0; i < layers.length; i++) {
    	var svg = document.createElementNS(svgNS, "svg");
    	svg.setAttributeNS(null, 'id', 'layer' + (i+1).toString());
    	svg.setAttributeNS(null, 'class', layers[i]);
	if (layers[i] != 'empty') {
    	    var use = document.createElementNS(svgNS, 'use');
	    var href = '../assets/' + layers[i] + '.svg#g10';
    	    use.setAttributeNS(null, 'href', href);
    	    svg.appendChild(use);
	}
    	wrapper.appendChild(svg);
    }
    return wrapper;
}


function start_animation(side) {
    console.log("Animating a new burger in the hopper on side: " + side);
    if (Math.random() < 0.5) {
	var layers = create_random_layers();
    } else {
	var layers = create_valid_layers();
    }

    var burger = create_burger(layers, side);
    document.body.appendChild(burger);
    var group1 = create_group(burger, create_animation1);

    var player = new Animation(group1, document.timeline);
    player.onfinish = function() {
	wait_for_keypress(burger);
    }
    player.play();
}

function create_animation2(element_name, data, wrapper) {
    var element = wrapper.children.namedItem(element_name);
    var side = wrapper.getAttribute('id');
    var body = document.getElementsByTagName("BODY")[0];
    var width = body.getBoundingClientRect().width;
    var height = body.getBoundingClientRect().height;

    var timings = {
	duration: 500,
	iterations: 1,
	easing: "linear",
	direction: "normal",
	fill: "forwards",
    }

    var target = side == 'left' ? 256 : width-256;
    
    var keyframes = [
	{ transform: 'translateX(' + (width/2 - 128) + 'px) translateY(' + data.conveyorY + ')', opacity: 1},
	{ transform: 'translateX(' + target + 'px) translateY(' + data.conveyorY + ')', opacity: 1},
    ];
    return new KeyframeEffect(element, keyframes, timings);
}

function convey_burger(wrapper) {
    console.log("conveying burger if needed.");
    // use leftBurger and rightBurger to determine if we need to make a random choice;
    var side;
    var leftBurger = document.getElementById('left');
    var rightBurger = document.getElementById('right');
    if (leftBurger == null && rightBurger == null) {
	if (Math.random() < 0.5) {
	    side = 'left';
	} else {
	    side = 'right';
	}
    } else if (leftBurger == null) {
	side = 'left'; 
    } else if (rightBurger == null) {
	side = 'right';
    } else {
	console.log("Cannot convey burger.");
	return;
    }
    console.log("Chose conveyor side:", side);
    wrapper.setAttribute('id', side);

    var group2 = create_group(wrapper, create_animation2);
    var player = new Animation(group2, document.timeline);
    player.onfinish = function() {
	wait_for_keypress(wrapper);
    }
    player.play();
}

function create_animation3(element_name, data, wrapper) {
    var element = wrapper.children.namedItem(element_name);
    var side = wrapper.getAttribute('id');
    var body = document.getElementsByTagName("BODY")[0];
    width = body.getBoundingClientRect().width;
    height = body.getBoundingClientRect().height;

    var timings = {
	duration: 500,
	iterations: 1,
	easing: "linear",
	direction: "normal",
	fill: "forwards",
    }
    var target = side == 'left' ? 256 : width-256;
    var keyframes = [
	{ transform: 'translateX(' + target + 'px) translateY(' + data.conveyorY + ')', opacity: 1},
	{ transform: 'translateX(' + target + 'px) translateY(' + data.finalY + ')', opacity: 1},
    ];
    return new KeyframeEffect(element, keyframes, timings);
}

function create_animation4(element_name, data, wrapper) {
    var element = wrapper.children.namedItem(element_name);
    var side = wrapper.getAttribute('id');
    var body = document.getElementsByTagName("BODY")[0];
    width = body.getBoundingClientRect().width;
    height = body.getBoundingClientRect().height;

    var timings = {
	duration: 500,
	iterations: 1,
	easing: "linear",
	direction: "normal",
	fill: "forwards",
    }
    var target = side == 'left' ? 256 : width-256;
    var keyframes = [
	{ transform: 'translateX(' + target + 'px) translateY(' + data.conveyorY + ')', opacity: 1},
	{ transform: 'translateX(' + width/2 + 'px) translateY(' + data.conveyorY + ')', opacity: 1},
    ];
    return new KeyframeEffect(element, keyframes, timings);
}


function create_animation5(element_name, data1, data2, wrapper) {
    var element = wrapper.children.namedItem(element_name);
    var side = wrapper.getAttribute('id');
    var body = document.getElementsByTagName("BODY")[0];
    var width = body.getBoundingClientRect().width;
    var height = body.getBoundingClientRect().height;

    var timings = {
	duration: 500,
	iterations: 1,
	easing: "linear",
	direction: "normal",
	fill: "forwards",
	delay: data1.delay,
    }

    var target = side == 'left' ? 256 : width-256;

    var keyframes = [
	{ transform: 'translateX(' + target + 'px) translateY(' + data1.conveyorY + ')', opacity: 1},
	{ transform: 'translateX(' + target + 'px) translateY(' + data2.conveyorY + ')', opacity: 1},
    ];
    return new KeyframeEffect(element, keyframes, timings);
}

function start_animation6(wrapper) {
    var burgerOffsets2 = create_layer_height_offsets(BURGER_LAYER_SPACING/2);
    var kEffects = [];
    for (let bf of burgerOffsets2) {
	var kf = create_animation4(bf[0], bf[1], wrapper);
	kEffects.push(kf);
    }
    var group = new GroupEffect(kEffects);
    var player = new Animation(group, document.timeline);
    player.onfinish = function() {
	var side = wrapper.getAttribute('id');
	wrapper.setAttribute('id', 'elevator');
	start_animation(side);
    }
    player.play();
}

function start_animation5(wrapper) {
    var burgerOffsets = create_layer_height_offsets();
    var burgerOffsets2 = create_layer_height_offsets(BURGER_LAYER_SPACING/2);
    var kEffects = [];
    for (i = 0; i < burgerOffsets.length; i++) {
	var kf = create_animation5(burgerOffsets[i][0], burgerOffsets[i][1], burgerOffsets2[i][1], wrapper);
	kEffects.push(kf);
    }
    var group = new GroupEffect(kEffects);

    var player = new Animation(group, document.timeline);
    player.onfinish = function() {
	start_animation6(wrapper);
    }
    player.play();
}

function start_animation7(wrapper) {
    var burgerOffsets = create_layer_height_offsets();
    var kEffects = [];
    for (let bf of burgerOffsets) {
	var kf = create_animation3(bf[0], bf[1], wrapper);
	kEffects.push(kf);
    }
    var group = new GroupEffect(kEffects);
    var player = new Animation(group, document.timeline);
    player.onfinish = function() {
	var side = wrapper.getAttribute('id');
    	wrapper.remove();
    	start_animation(side);
    }
    player.play();
}

function after_keypress(wrapper, isBurger) {
    console.log("after keypress for", wrapper);
    var side = wrapper.getAttribute('id');
    console.log("side is", side);
    console.log("isBurger is", isBurger);
    if (isBurger) {
	start_animation5(wrapper);
    } else {
	start_animation7(wrapper);
    }
}

function wait_for_keypress(wrapper) {
    console.log("wait for keypress for", wrapper);
    var yesCode, noCode;
    function keydownHandlerLeft(e) {
	var yesCode = "Z".charCodeAt(0);
	var noCode = "X".charCodeAt(0);
	console.log("keydownHandlerLeft waiting for", yesCode, noCode, "got", e.keyCode);
	if (e.keyCode == yesCode || e.keyCode == noCode) {
	    document.removeEventListener('keydown', keydownHandlerLeft, false);
	    after_keypress(wrapper, e.keyCode == yesCode);
	}
    }
    function keydownHandlerRight(e) {
	var yesCode = "M".charCodeAt(0);
	var noCode = "N".charCodeAt(0);
	console.log("keydownHandlerRight waiting for", yesCode, noCode, "got", e.keyCode);
	if (e.keyCode == yesCode || e.keyCode == noCode) {
	    document.removeEventListener('keydown', keydownHandlerRight, false);
	    after_keypress(wrapper, e.keyCode == yesCode);
	}
    }
    var side = wrapper.getAttribute('id');
    console.log("side is", side);
    if (side == 'left')
	document.addEventListener('keydown', keydownHandlerLeft, false);
    else if (side == 'right')
	document.addEventListener('keydown', keydownHandlerRight, false);
}

$(window).ready(function() {
    var body = document.getElementsByTagName('body')[0];
    var width = body.getBoundingClientRect().width;
    var height = body.getBoundingClientRect().height;
    create_conveyor(width, height-100);
    create_chute('left', 256, height-100);
    create_chute('right', width-256, height-100);
    start_animation('left');
    start_animation('right');
});
