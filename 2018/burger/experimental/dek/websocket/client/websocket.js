var ws = new WebSocket("ws://gork:8888/websocket");
ws.onopen = function() {
    ws.send("Hello, world");
};
ws.onmessage = function (evt) {
    alert(evt.data);
};
