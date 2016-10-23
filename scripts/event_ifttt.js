var http = require('http');
var express = require('express');

var app = express();
var bodyParser = require('body-parser');

var port = process.argv[2];
var result = {};

app.use(bodyParser.json());

// add post method to process request from ifttt
app.post('/action', function(req, res) {
        var response = req.body;
	//console.log(req);
	result.response = response;
	result.status = 200;
	result.response["end"] = "test";
        console.log('ifttt request received', response);
        res.send(result);
});

process.on('SIGINT', function() {
  console.log("\nGracefully shutting down from SIGINT (Ctrl+C)");

  process.exit();
});

// add post method to process request from ifttt
app.get('/action', function(req, res) {
      //  var response = req.body;
        //console.log(req);
        console.log('ifttt request received get method');
	var temResult = result;
	result = {};
	res.send(temResult);

//        res.send('Event processed by RPi');
});

// ------------------------------------------------------------------------
// Start Express App Server
//
//console.log(port);
app.listen(port);
console.log('RPi Server is listening on port', port);

