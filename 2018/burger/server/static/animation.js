const MAX_BURGERS = 6;
const BURGER_LAYER_SPACING = 40;
const BASE_INITIAL_Y = -300;
const BASE_FINAL_Y = 2000;
const BASE_ELEVATOR_FINAL_Y = 0;


const layers_enum = Object.freeze({
    0: "empty",
    1: "topbun",
    2: "lettuce",
    3: "tomato",
    4: "cheese",
    5: "patty",
    6: "bottombun"
});

const layer_names_enum = Object.freeze({
    "empty":0,
    "topbun":1,
    "lettuce":2,
    "tomato":3,
    "cheese":4,
    "patty":5,
    "bottombun":6
});

function create_chute(center_x, height) {
    var svgNS = 'http://www.w3.org/2000/svg';
    var chute = document.createElementNS(svgNS, "svg");
    chute.setAttributeNS(null, 'id', 'chute');
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

function create_animation_burger_drop(element_name, data, wrapper) {
    var element = wrapper.children.namedItem(element_name);
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

    var target = 256;

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
	    elevatorFinalY: (BASE_ELEVATOR_FINAL_Y - i * spacing) + 'px',
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

function create_burger(layers) {
    var svgNS = 'http://www.w3.org/2000/svg';
    var wrapper = document.createElement("div");
    wrapper.setAttribute('class', "wrapper");
    wrapper.setAttribute('id', 'chute');
    for (i = 0; i < layers.length; i++) {
    	var svg = document.createElementNS(svgNS, "svg");
    	svg.setAttributeNS(null, 'viewBox', '0 0 71.25 40');
    	svg.setAttributeNS(null, 'id', 'layer' + (i+1).toString());
    	svg.setAttributeNS(null, 'class', layers[i]);
	if (layers[i] != 'empty') {
    	    var use = document.createElementNS(svgNS, 'use');
	    var href = '/static/assets/' + layers[i] + '.svg#g10';
    	    use.setAttributeNS(null, 'href', href);
    	    svg.appendChild(use);
	}
    	wrapper.appendChild(svg);
    }
    return wrapper;
}

function layer_idx_to_layers(layers_idx) {
    var layers = [];
    for (i = 0; i < layers_idx.length; i++) {
	layers.push(layers_enum[layers_idx[i]]);
    }
    return layers;

}
function burger_drop_animation(layers) {
    console.log("Create burger", layers);
    var wrapper = create_burger(layers);
    document.body.appendChild(wrapper);

    var burgerOffsets = create_layer_height_offsets();
    var kEffects = [];
    for (let bf of burgerOffsets) {
	var kf = create_animation_burger_drop(bf[0], bf[1], wrapper);
	kEffects.push(kf);
    }
    var group = new GroupEffect(kEffects);
    var player = new Animation(group, document.timeline);
    player.onfinish = function() {
	wait_for_keypress(wrapper);
    }
    player.play();
}

function start_burger_drop_animation() {
    var request = new XMLHttpRequest();
    request.onreadystatechange = function() {
	if(request.readyState === 4) {
	    if(request.status === 200) {
		var layers_idx;
		layers_idx = request.response["burger"];
	    } else {
		console.log("sadness!", request.status, request.statusText);
		layers_idx = [1,2,3,4,5,6];
	    }
	    burger_drop_animation(layer_idx_to_layers(layers_idx));
	}
	
    }
    request.responseType = 'json';
    request.open('GET', '/burger');
    request.send();
}

function create_animation_trash_burger(element_name, data, wrapper) {
    var element = wrapper.children.namedItem(element_name);
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
    var target = 256;
    var keyframes = [
	{ transform: 'translateX(' + target + 'px) translateY(' + data.conveyorY + ')', opacity: 1},
	{ transform: 'translateX(' + target + 'px) translateY(' + data.finalY + ')', opacity: 1},
    ];
    return new KeyframeEffect(element, keyframes, timings);
}

function create_animation_convey_burger_to_middle(element_name, data, wrapper) {
    var element = wrapper.children.namedItem(element_name);
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
    var target = 256;
    var keyframes = [
	{ transform: 'translateX(' + target + 'px) translateY(' + data.conveyorY + ')', opacity: 1},
	{ transform: 'translateX(' + width/2 + 'px) translateY(' + data.conveyorY + ')', opacity: 1},
    ];
    return new KeyframeEffect(element, keyframes, timings);
}


function create_animation_smoosh_burger(element_name, data1, data2, wrapper) {
    var element = wrapper.children.namedItem(element_name);
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

    var target = 256;

    var keyframes = [
	{ transform: 'translateX(' + target + 'px) translateY(' + data1.conveyorY + ')', opacity: 1},
	{ transform: 'translateX(' + target + 'px) translateY(' + data2.conveyorY + ')', opacity: 1},
    ];
    return new KeyframeEffect(element, keyframes, timings);
}

function start_animation_convey_burger_to_middle(wrapper) {
    var burgerOffsets2 = create_layer_height_offsets(BURGER_LAYER_SPACING/2);
    var kEffects = [];
    for (let bf of burgerOffsets2) {
	var kf = create_animation_convey_burger_to_middle(bf[0], bf[1], wrapper);
	kEffects.push(kf);
    }
    var group = new GroupEffect(kEffects);
    var player = new Animation(group, document.timeline);
    player.onfinish = function() {
	wrapper.setAttribute('id', 'elevator');
	start_burger_elevator_animation(wrapper);
	start_burger_drop_animation();
    }
    player.play();
}

function create_animation_elevator(element_name, data, wrapper) {
    var element = wrapper.children.namedItem(element_name);
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
    var keyframes = [
	{ transform: 'translateX(' + width/2 + 'px) translateY(' + data.conveyorY + ')', opacity: 1},
	{ transform: 'translateX(' + width/2 + 'px) translateY(' + data.elevatorFinalY + ')', opacity: 1},
    ];
    return new KeyframeEffect(element, keyframes, timings);
}

function start_burger_elevator_animation(wrapper) {
    var burgerOffsets2 = create_layer_height_offsets(BURGER_LAYER_SPACING/2);
    var kEffects = [];
    for (let bf of burgerOffsets2) {
	var kf = create_animation_elevator(bf[0], bf[1], wrapper);
	kEffects.push(kf);
    }
    var group = new GroupEffect(kEffects);
    var player = new Animation(group, document.timeline);
    player.onfinish = function() {
	wrapper.remove();
    }
    player.play();
}

function start_animation_smoosh_burger(wrapper) {
    var burgerOffsets = create_layer_height_offsets();
    var burgerOffsets2 = create_layer_height_offsets(BURGER_LAYER_SPACING/2);
    var kEffects = [];
    for (i = 0; i < burgerOffsets.length; i++) {
	var kf = create_animation_smoosh_burger(burgerOffsets[i][0], burgerOffsets[i][1], burgerOffsets2[i][1], wrapper);
	kEffects.push(kf);
    }
    var group = new GroupEffect(kEffects);

    var player = new Animation(group, document.timeline);
    player.onfinish = function() {
	start_animation_convey_burger_to_middle(wrapper);
    }
    player.play();
}

function start_animation_trash_burger(wrapper) {
    var burgerOffsets = create_layer_height_offsets();
    var kEffects = [];
    for (let bf of burgerOffsets) {
	var kf = create_animation_trash_burger(bf[0], bf[1], wrapper);
	kEffects.push(kf);
    }
    var group = new GroupEffect(kEffects);
    var player = new Animation(group, document.timeline);
    player.onfinish = function() {
    	wrapper.remove();
    	start_burger_drop_animation();
    }
    player.play();
}

function element_to_burger(wrapper) {
    var burger = [];
    for (let node of wrapper.childNodes) {
	burger.push(layer_names_enum[node.getAttribute('class')])
    }
    return burger.join('');
}

function vote(wrapper, choice) {
    var request = new XMLHttpRequest();

    burger = element_to_burger(wrapper);
    
    request.onreadystatechange = function() {
	if(request.readyState === 4) {
	    if(request.status === 200) {
		console.log("celebration!");
		var request2 = new XMLHttpRequest();
		request2.onreadystatechange = function() {
		    if(request2.readyState === 4) {
			if(request2.status === 200) {
			    console.log("validation!");
			    document.getElementById("status").innerHTML = JSON.stringify(request2.response);
			}
		    }
		}
		
		request2.responseType = 'json';
		request2.open('GET', '/validate');
		request2.send();

	    } else {
		console.log("sadness!", request.status, request.statusText, request.responseText);
	    }
	}
    }
    request.responseType = 'json';
    request.open('GET', '/vote?burger=' + burger + '&vote=' + choice);
    request.send();
}

function after_keypress(wrapper, isBurger) {
    if (isBurger) {
	vote(wrapper, true);
	start_animation_smoosh_burger(wrapper);
    } else {
	vote(wrapper, false);
	start_animation_trash_burger(wrapper);
    }
}

function wait_for_keypress(wrapper) {
    var yesCode, noCode;
    function keydownHandler(e) {
	var yesCode = "Z".charCodeAt(0);
	var noCode = "X".charCodeAt(0);
	if (e.keyCode == yesCode || e.keyCode == noCode) {
	    document.removeEventListener('keydown', keydownHandler, false);
	    after_keypress(wrapper, e.keyCode == yesCode);
	}
    }
    document.addEventListener('keydown', keydownHandler, false);
}

const body = document.getElementsByTagName('body')[0];
body.onload = function() {
    var width = body.getBoundingClientRect().width;
    var height = body.getBoundingClientRect().height;
    create_conveyor(width, height-100);
    create_chute(256, height-100);
    start_burger_drop_animation();
};
