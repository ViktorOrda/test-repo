var http = require('http');
var fs = require('fs');
var qs = require('querystring');
var redis = require('redis');

var client = redis.createClient(6379, 'redis');

client.on('connect', function() {
    console.log('Redis client connected');
});

client.on('error', function (err) {
    console.log('Something went wrong ' + err);
});


http.createServer(function (req, res) {
  if (req.method === 'GET' && req.url === '/') {
        res.writeHead(200, {'Content-Type': 'text/html'});
        fs.readFile ('index.html', function(err, data) {
                res.write(data);
                res.end();
                }
        );
  }
  else if (req.method === 'GET' && req.url === '/status') {
        res.writeHead(200, {'Content-Type': 'application/json'});
        var answer = { endpoint: req.url, clientIP: req.connection.remoteAddress };
        res.write(JSON.stringify(answer));
        res.end();
  }
  else if (req.method === 'GET' && req.url === '/item') {
        res.writeHead(200, {'Content-Type': 'application/json'});
        var dict = {};
	client.keys('*', function(err, reply) {
         	var keys = reply;
		var processItems = async function(x) {
			if (x === keys.length) {
				await res.end(JSON.stringify(dict)); 
				return;
			}
			var value = keys[x];
			client.get(value, function(err, reply) {
				dict[value]=reply;
				processItems(x+1);
			});
		}
		processItems(0);
	});
  }
  else if (req.method === 'POST' && req.url === '/item') {
		var postData = '';
        req.on('data', function(content) {
                postData += content;
                if (postData.length > 1e6) {
                        request.connection.destroy();
                }
        });
        req.on('end', function() {
                var payload = qs.parse(postData);
                res.writeHead(200, {'Content-Type': 'text/plain'});
		client.set(payload.key, payload.value);
		res.write('New item added!');
		res.end();
	});
}
else {
	res.statusCode = 404;
	res.end();
 }
}).listen(80);
