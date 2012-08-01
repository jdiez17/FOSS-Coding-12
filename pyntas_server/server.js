var redis = require("redis"), client = redis.createClient();
var io = require("socket.io").listen(8082);

io.sockets.on("connection", function(socket) {
	client.on("message", function(channel, message) {
		message = JSON.parse(message);
		if(!message['location'])
			return;

		
		site = message['location']['letters'] + '-';
		if(message['location']['numbers'] < 10) {
			site += '0' + message['location']['numbers'];
		} else site += message['location']['numbers'];

		color = '#00ff00';

		pyntas_payload = {'user': 'Anonymous', 'site': site, 'message': message['message'], 'color': color};
		socket.emit('data', pyntas_payload);
	});
});

client.subscribe("euskalmap_channel");
