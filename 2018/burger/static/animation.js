const MAX_BURGERS = 6;
const BURGER_LAYER_SPACING = 40;
const BASE_INITIAL_Y = -300;
const BASE_FINAL_Y = 1000;
const BASE_ELEVATOR_FINAL_Y = 0;
const BASE_CHUTE_Y = 450;
const BASE_CONVEYOR_Y = 870;
const X_TARGET = 905;
const TRASH_X_TARGET = 400;
const GOOD_X_TARGET = 1300;

const layers_enum = Object.freeze({
    0: "empty",
    1: "topbun",
    2: "lettuce",
    3: "tomato",
    4: "cheese",
    5: "patty",
    6: "bottombun",
    7: "banana",
    8: "book",
    9: "shoe",
});

const layer_names_enum = Object.freeze({
    "empty":0,
    "topbun":1,
    "lettuce":2,
    "tomato":3,
    "cheese":4,
    "patty":5,
    "bottombun":6,
    "banana":7,
    "book":8,
    "shoe":9,
});

function create_layer_height_offsets(spacing=BURGER_LAYER_SPACING) {
    var body = document.getElementsByTagName('body')[0];
    var width = body.getBoundingClientRect().width;
    var height = body.getBoundingClientRect().height;
    var animation = [];
    for (i = 0; i < MAX_BURGERS + 2; i++) {
	animation.push(["layer" + (MAX_BURGERS-i+1), {
	    delay: i*100,
	    initialY: (BASE_INITIAL_Y - i * spacing) + 'px',
	    chuteY: (BASE_CHUTE_Y - i * spacing) + 'px',
	    conveyorY: (BASE_CONVEYOR_Y - i * spacing) + 'px',
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

function create_burger(layers, class_, id) {
    var svgNS = 'http://www.w3.org/2000/svg';
    var wrapper = document.createElement("div");
    wrapper.setAttribute('class', class_);
    wrapper.setAttribute('id', id);
    for (i = 0; i < layers.length; i++) {
    	var svg = document.createElementNS(svgNS, "svg");
    	svg.setAttributeNS(null, 'viewBox', '0 0 71.25 40');
    	svg.setAttributeNS(null, 'id', 'layer' + (i+1).toString());
    	svg.setAttributeNS(null, 'class', layers[i]);
	if (layers[i] != 'empty') {
    	    var use = document.createElementNS(svgNS, 'use');
	    var href = '/assets/' + layers[i] + '.svg#g10';
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



function updateStatus(request) {
    document.getElementById("fp").innerHTML = request.response["fp"];
    document.getElementById("tp").innerHTML = request.response["tp"];
    document.getElementById("tn").innerHTML = request.response["tn"];
    document.getElementById("fn").innerHTML = request.response["fn"];
}

function element_to_burger(wrapper) {
    var burger = [];
    for (let node of wrapper.childNodes) {
	burger.push(layer_names_enum[node.getAttribute('class')])
    }
    return burger.join('');
}

function update_burgerrank(burgers) {
    var burgerstack = document.getElementById("burgerstack");
    burgerstack.innerHTML='';
    for(j = 0; j < Math.min(5, burgers.length); j++) {
	var key = burgers[j][0];
	var s = key.split('');
	var layers = [];
	for (i = 0; i < s.length; i++) {
	    layers.push(layers_enum[parseInt(s[i])]);
	}
	var wrapper = create_burger(layers, "burgerstack_wrapper", key);
	for (i = 0; i <  wrapper.children.length; i++) {
	    var node = wrapper.children[i];
	    var ty = j*150 + (i*BURGER_LAYER_SPACING)/3;
	    node.setAttribute('transform', 'translate(0 ' + ty + ')');
	    node.style.opacity = 1;
	}
	burgerstack.appendChild(wrapper);
    }
}

function request_burgerrank() {
    var request = new XMLHttpRequest();
    request.onreadystatechange = function() {
	if(request.readyState === 4) {
	    if(request.status === 200) {
		console.log("celebration!", request.response);
		var burgers = request.response["results"];
		update_burgerrank(burgers);
		updateStatus(request);
	    } else {
		console.log("sadness!", request.status, request.statusText, request.response);
	    }
	}
    }
    request.responseType = 'json';
    request.open('GET', 'http://' + window.location.hostname + ':8888/rank');
    request.send();
}

function vote(wrapper, choice) {
    var request = new XMLHttpRequest();

    burger = element_to_burger(wrapper);
    
    request.onreadystatechange = function() {
	if(request.readyState === 4) {
	    if(request.status === 200) {
		console.log("celebration!", request.response);
		request_burgerrank();
	    } else {
		console.log("sadness!", request.status, request.statusText, request.responseText);
	    }
	}
    }
    request.responseType = 'json';
    request.open('GET', 'http://' + window.location.hostname + ':8888/vote?burger=' + burger + '&vote=' + choice);
    request.send();
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
	{ transform: 'translateX(' + GOOD_X_TARGET + 'px) translateY(' + data.conveyorY + ')', opacity: 1},
	{ transform: 'translateX(' + GOOD_X_TARGET + 'px) translateY(' + data.elevatorFinalY + ')', opacity: 1},
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
	start_burger_drop_animation();
    }
    player.play();
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
	{ transform: 'translateX(' + GOOD_X_TARGET + 'px) translateY(' + data.conveyorY + ')', opacity: 1},
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
	start_burger_elevator_animation(wrapper);
    }
    player.play();
}

function create_animation_convey_burger_to_trash_2(element_name, data, wrapper) {
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
	    { transform: 'translateX(' + TRASH_X_TARGET + 'px) translateY(' + data.conveyorY + ')', opacity: 1},
	    { transform: 'translateX(' + TRASH_X_TARGET + 'px) translateY(' + data.finalY + ')', opacity: 1},
    ];
    return new KeyframeEffect(element, keyframes, timings);
}

function start_animation_convey_burger_to_trash_2(wrapper) {
    var burgerOffsets = create_layer_height_offsets(BURGER_LAYER_SPACING/2);
    var kEffects = [];
    for (let bf of burgerOffsets) {
	var kf = create_animation_convey_burger_to_trash_2(bf[0], bf[1], wrapper);
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

function create_animation_convey_burger_to_trash(element_name, data, wrapper) {
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
	{ transform: 'translateX(' + X_TARGET + 'px) translateY(' + data.conveyorY + ')', opacity: 1},
	{ transform: 'translateX(' + TRASH_X_TARGET + 'px) translateY(' + data.conveyorY + ')', opacity: 1},
    ];
    return new KeyframeEffect(element, keyframes, timings);
}

function start_animation_convey_burger_to_trash(wrapper) {
    var burgerOffsets = create_layer_height_offsets(BURGER_LAYER_SPACING/2);
    var kEffects = [];
    for (let bf of burgerOffsets) {
	var kf = create_animation_convey_burger_to_trash(bf[0], bf[1], wrapper);
	kEffects.push(kf);
    }
    var group = new GroupEffect(kEffects);
    var player = new Animation(group, document.timeline);
    player.onfinish = function() {
    	start_animation_convey_burger_to_trash_2(wrapper);
    }
    player.play();
}

function start_animation_convey_burger_to_fate(wrapper, isBurger) {
    if (isBurger) 
	start_animation_convey_burger_to_middle(wrapper);
    else 
	start_animation_convey_burger_to_trash(wrapper);
}

function create_burger_drop_to_conveyor_animation(element_name, data1, data2, wrapper) {
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
	{ transform: 'translateX(' + X_TARGET + 'px) translateY(' + data1.chuteY + ')', opacity: 1},
	{ transform: 'translateX(' + X_TARGET + 'px) translateY(' + data2.conveyorY + ')', opacity: 1},
    ];
    return new KeyframeEffect(element, keyframes, timings);
}
function start_burger_drop_to_conveyor_animation(wrapper, isBurger) {
    var burgerOffsets = create_layer_height_offsets();
    var burgerOffsets2 = create_layer_height_offsets(BURGER_LAYER_SPACING/2);
    var kEffects = [];
    for (i = 0; i < burgerOffsets.length; i++) {
	var kf = create_burger_drop_to_conveyor_animation(burgerOffsets[i][0], burgerOffsets[i][1], burgerOffsets2[i][1], wrapper);
	kEffects.push(kf);
    }
    var group = new GroupEffect(kEffects);
    var player = new Animation(group, document.timeline);
    player.onfinish = function() {
	start_animation_convey_burger_to_fate(wrapper, isBurger);
    }
    player.play();
}

function after_keypress(wrapper, isBurger) {
    vote(wrapper, isBurger);
    start_burger_drop_to_conveyor_animation(wrapper, isBurger);
}

const yesCode = "Z".charCodeAt(0);
const noCode = "X".charCodeAt(0);

function wait_for_keypress(wrapper) {
    function keydownHandler(e) {
	if (e.keyCode == yesCode || e.keyCode == noCode) {
	    document.removeEventListener('keydown', keydownHandler, false);
	    after_keypress(wrapper, e.keyCode == yesCode);
	}
    }
    document.addEventListener('keydown', keydownHandler, false);
}

function create_animation_burger_drop(element_name, data, wrapper) {
    var element = wrapper.children.namedItem(element_name);
    var body = document.getElementsByTagName("BODY")[0];
    var width = body.getBoundingClientRect().width;
    var height = body.getBoundingClientRect().height;

    var timings = {
	duration: 1000,
	iterations: 1,
	easing: "linear",
	direction: "normal",
	fill: "forwards",
	delay: data.delay,
    }

    var keyframes = [
	{ transform: 'translateX(' + X_TARGET + 'px) translateY(' + data.initialY + ')', opacity: 1},
	{ transform: 'translateX(' + X_TARGET + 'px) translateY(' + data.chuteY + ')', opacity: 1},
    ];
    return new KeyframeEffect(element, keyframes, timings);
}

function create_burger_drop_animation(layers) {
    console.log("Create burger", layers);
    var wrapper = create_burger(layers, "wrapper", "chute");
    document.body.insertBefore(wrapper, document.getElementById("burger_machine"));

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
	    create_burger_drop_animation(layer_idx_to_layers(layers_idx));
	}
	
    }
    request.responseType = 'json';
    request.open('GET', 'http://' + window.location.hostname + ':8888/burger');
    request.send();
}

const resetCode = "R".charCodeAt(0);

function invokeReset(e) {
	var request = new XMLHttpRequest();
	request.onreadystatechange = function() {
	    if(request.readyState === 4) {
		if(request.status === 200) {
		    location.reload();
		} else {
		    console.log("sadness!", request.status, request.statusText);
		}
	    }
	}
	request.responseType = 'json';
	request.open('GET', 'http://' + window.location.hostname + ':8888/reset');
	request.send();
}
function resetKeydownHandler(e) {
    if (e.keyCode == resetCode) {
	invokeReset();
    }
}

const body = document.getElementsByTagName('body')[0];
body.onload = function() {
    request_burgerrank();
    start_burger_drop_animation();
    document.addEventListener('keydown', resetKeydownHandler, false);
};
