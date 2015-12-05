var io = require("socket.io").listen(8008);
//var io = require("/var/www/PGraduacion/NodeJS/node_modules/socket.io/node_modules/socket.io-client/socket.io").listen(8008);

var querystring = require("querystring");
var http = require("http");

io.sockets.on("connection", function(socket){

	socket.on("LlamarCliente", function(data){
		var values = querystring.stringify(data);
		var options = {
			hostname: "localhost",
			port: "80",
			//port: "8000",
			path: "/NodeJS/LlamarCliente/",
			method: "POST",
			headers: {
				"Content-Type": "application/x-www-form-urlencoded",
				"Content-Length": values.length
			}
		};
		var req = http.request(options, function(res){
			res.setEncoding("utf8");
			res.on("data", function(data){
				io.sockets.emit("LlamarClienteRes", data);
			});
		});
		req.write(values);
		req.end();
	});

	socket.on("RellamarCliente", function(data){
		var values = querystring.stringify(data);
		var options = {
			hostname: "localhost",
			port: "80",
			//port: "8000",
			path: "/NodeJS/RellamarCliente/",
			method: "POST",
			headers: {
				"Content-Type": "application/x-www-form-urlencoded",
				"Content-Length": values.length
			}
		};
		var req = http.request(options, function(res){
			res.setEncoding("utf8");
			res.on("data", function(data){
				io.sockets.emit("RellamarClienteRes", data);
			});
		});
		req.write(values);
		req.end();
	});

});
