const MAX_BURGERS = 6;
const BURGER_LAYER_SPACING = 80;
const BASE_INITIAL_Y = -300;
const BASE_FINAL_Y = 600;
const BASE_ELEVATOR_FINAL_Y = 0;
const BASE_CONVEYOR_Y = 710;
const X_TARGET = 570;

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

    var keyframes = [
	{ transform: 'translateX(' + X_TARGET + 'px) translateY(' + data.initialY + ')', opacity: 1},
	{ transform: 'translateX(' + X_TARGET + 'px) translateY(' + data.conveyorY + ')', opacity: 1},
    ];
    return new KeyframeEffect(element, keyframes, timings);
}

function create_layer_height_offsets(spacing=BURGER_LAYER_SPACING) {
    var body = document.getElementsByTagName('body')[0];
    var width = body.getBoundingClientRect().width;
    var height = body.getBoundingClientRect().height;
    var baseConveyorY = BASE_CONVEYOR_Y;
    var animation = [];
    for (i = 0; i < MAX_BURGERS + 2; i++) {
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
        var keyframes = [
	{ transform: 'translateX(' + X_TARGET + 'px) translateY(' + data.conveyorY + ')', opacity: 1},
	{ transform: 'translateX(' + X_TARGET + 'px) translateY(' + data.finalY + ')', opacity: 1},
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
        var keyframes = [
	{ transform: 'translateX(' + X_TARGET + 'px) translateY(' + data.conveyorY + ')', opacity: 1},
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

    
    var keyframes = [
	{ transform: 'translateX(' + X_TARGET + 'px) translateY(' + data1.conveyorY + ')', opacity: 1},
	{ transform: 'translateX(' + X_TARGET + 'px) translateY(' + data2.conveyorY + ')', opacity: 1},
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

function updateStatus(request) {
    document.getElementById("fp").innerHTML = request.response["fp"];
    document.getElementById("tp").innerHTML = request.response["tp"];
    document.getElementById("tn").innerHTML = request.response["tn"];
    document.getElementById("fn").innerHTML = request.response["fn"];
    document.getElementById("iterations").innerHTML = request.response["n_iter"];
    document.getElementById("accuracy").innerHTML = (request.response["accuracy"] * 100.).toFixed(2);
    document.getElementById("burger_precision").innerHTML = request.response["p"][1].toFixed();
    document.getElementById("notburger_precision").innerHTML = request.response["p"][1].toFixed(2);
    document.getElementById("burger_recall").innerHTML = request.response["p"][0].toFixed(2);
    document.getElementById("notburger_recall").innerHTML = request.response["p"][0].toFixed(2);
}

function requestStatus() {
    var request = new XMLHttpRequest();
    request.onreadystatechange = function() {
	if(request.readyState === 4) {
	    if(request.status === 200) {
		updateStatus(request);
	    }
	}
    }
    
    request.responseType = 'json';
    request.open('GET', '/validate');
    request.send();
}

function vote(wrapper, choice) {
    var request = new XMLHttpRequest();

    burger = element_to_burger(wrapper);
    
    request.onreadystatechange = function() {
	if(request.readyState === 4) {
	    if(request.status === 200) {
		console.log("celebration!");
		requestStatus();
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
    requestStatus();
    start_burger_drop_animation();
};
