var express = require('express');
var partials = require('express-partials');
var app = express();
var port = process.env.PORT || 4000;
var sys = require('sys')
var exec = require('child_process').exec;
var spawn = require('child_process').spawnSync;
function puts(error, stdout, stderr) { sys.puts(stdout) }
const execa = require('execa');

var execSync = require('child_process').execSync;
app.set('views', __dirname + '/views');
app.set('view engine', 'ejs');
app.use(partials());
app.use(express.static(__dirname + '/public'));

// Root page
app.get('/', 
function(req, res) {
  res.render('index');
});
app.get('/stream', 
function(req, res) {
  var link = req.query.link;
  var key = req.query.key;
  var cmd = "bash stream.sh " + key + " " + link +">/dev/null";  
  console.log(cmd);
  console.log("Đã Live Tắt trinh duyệt đi !! chờ tầm 3,4 p tự Live");
  exec(cmd,{
    maxBuffer: 1024*1024 //quick fix
    },puts);
//execa('sh',['stream.sh',key,link]).then(result => {
//	console.log(result.stdout);
	//=> 'unicorns'
//});
  //var proc = spawn('sh',['stream.sh',key,link,"&"]);
//spawn('sh',['stream.sh',key,link]);
//console.log('stdout here: \n' + proc.stdout);
 // exec(cmd, puts);
});
app.get('/streamedit',
function(req, res) {
var link = req.query.link;
  var key = req.query.key;
  var lach = req.query.lach;
 var cmd1 = "bash streamedit.sh " + key + " " + link +">/dev/null";  
  console.log("Đã Lach Tắt trinh duyệt đi !! chờ tầm 3,4 p tự Live");
  exec(cmd1,{
    maxBuffer: 1024*1024 //quick fix
    },puts);

});
app.get('/custom',
function(req, res) {
var link = req.query.link;
  var key = req.query.key;
  var lach = req.query.lach;
 var cmd1 = "bash" + key + " " + link +">/dev/null";  
  console.log("Đã Lach Tắt trinh duyệt đi !! chờ tầm 3,4 p tự Live");
  exec(cmd1,{
    maxBuffer: 1024*1024 //quick fix
    },puts);

});

app.get('/streamoff',
function(req, res) {
  var cmd = "pkill ffmpeg && pkill youtube-dl";
  exec(cmd, puts);
});
app.get('/host', 
function(req, res) {
  exec("bash stream.sh 468 https://www.youtube.com/watch?v=mn1nWOOMH9E", puts);
});
app.get('/view', 
function(req, res) {
  res.render('view');
});

app.listen(port);
console.log('Server is listening on ' + port);
