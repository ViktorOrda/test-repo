var http = require('http');
var fs = require('fs');
var mysql = require('mysql');
var qs = require('querystring');

var DBhost = 'myinstance.cbkhb0ifzpmr.us-east-1.rds.amazonaws.com';
var username = 'admin';
var pass = '12345678';
var db = 'TempDB';

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
	var con = mysql.createConnection({
        	host: DBhost,
	        user: username,
	        password: pass,
        	database: db
	});
	con.connect(function(err) {
		if (err) throw err;
		con.query("SELECT * FROM Items", function (err, result, fields) {
                	if (err) throw err;
	                res.write(JSON.stringify(result));
        	        res.end();
        	});
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
		
		var con = mysql.createConnection({
 	               host: DBhost,
        	        user: username,
                	password: pass,
	                database: db
        	});

		con.connect(function(err) {
                if (err) throw err;
                con.query("INSERT INTO Items(name) VALUES ('" + payload.name +  "')", function (err, result, fields) {
                        if (err) throw err;
                        res.write('1 record was inserted!');
                        res.end();
                	});
        	});
                //var itemName = payload.name;
		//res.write(itemName);
		//res.end();
	});
  }
	
  //}

  else {
	res.statusCode = 404;
	res.end(); 
  }
}).listen(80);
