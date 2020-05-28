var express = require("express"),
    uuid = require('uuid'),
    bodyParser = require('body-parser'),
    app = express(),
    server = require("http").createServer(app),
    path = require("path"),
    port = 80,
//    spawn = require("child_process").spawn,
    io = require('socket.io')(server);


const sessionId = uuid.v4();

/** ---STARTING SERVER--- **/
    server.listen(port);
    console.log(Date.now() + " : Server running on http://localhost:"+port+"/");
/** --------------------- **/

/** --- CLIENT LOCATION **/

// Parse JSON bodies (as sent by API clients)
app.use(bodyParser.urlencoded({     // to support URL-encoded bodies
  extended: true
})); 
app.use(bodyParser.json() ); // to support JSON-encoded bodies
app.use(express.static(path.join(__dirname, 'public')));


let python_socket;
let responseArray = []

app.post('/chat', function(req, res) {
  let query = req.body.tekst;
  console.log(query)
  
  python_socket.emit('message', query);
  responseArray.push(res);
  
  //res.send({res: result, time: hours+":"+minutes});
});


io.on('connection', function(socket){
  console.log('a user connected');
  python_socket = socket;
  /*socket.on('python-message', function( fromPython ) {
    socket.emit('message', fromPython );
    console.log(fromPython);
  });*/

  python_socket.on('categories', function( fromPython ) {
    console.log(fromPython);
  });

  python_socket.on('nonPrediction', function( fromPython ){
    /*executeQuery(projectId, sessionId, fromPython, languageCode).then((result) => {
      
      let date = new Date();
      let hours = date.getHours();
      let minutes = date.getMinutes();

      console.log("Hei hei");
      res = responseArray.pop();
      res.send({res: result, time: hours+":"+minutes});

    }).catch((err) => {
      console.log(err);
    });;*/
  });

  python_socket.on('prediction', function( fromPython ) {
    /*executeQuery(projectId, sessionId, fromPython[0] + " " + fromPython[1], languageCode).then((result) => {
      
      let date = new Date();
      let hours = date.getHours();
      let minutes = date.getMinutes();

      console.log("Hei hei");
      res = responseArray.pop();
      res.send({res: result, time: hours+":"+minutes});

    }).catch((err) => {
      console.log(err);
    });;*/
  });
});
