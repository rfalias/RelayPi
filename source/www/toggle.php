<?php
$request = isset($_GET['req'])?$_GET['req']:null;

function SetState($value)
{
	$url = "http://192.168.2.113:8080?state=" . $value;
	$curl = curl_init();
	curl_setopt ($curl, CURLOPT_URL, $url);
	curl_setopt($curl, CURLOPT_RETURNTRANSFER, 1);

	$result = curl_exec ($curl);
	curl_close ($curl);
}

if (!isset($request))
{
	if (isset($_POST['On']))
	{
		$request = "1";
	}	

	if (isset($_POST['Off']))
	{
		$request = "0";
	}
}
if ($request == '1')
{
	SetState('1');
	//unlink('/var/www/sensor/1');
	//fopen('/var/www/sensor/1',w);
	//unlink('/var/www/sensor/1');
}
if ($request == '0')
{
	SetState(0);
	//unlink('/var/www/sensor/0');
	//fopen('/var/www/sensor/0',w);
	//unlink('/var/www/sensor/0');
}

?>

<html>
<head>
<script src="http://ajax.googleapis.com/ajax/libs/jquery/1.11.1/jquery.min.js"></script>

<script>


var state = '0'
function showHint() {
	
  var xmlhttp=new XMLHttpRequest();
  xmlhttp.onreadystatechange=function() {
    if (xmlhttp.readyState==4 && xmlhttp.status==200) {
      document.getElementById("txtHint").innerHTML=xmlhttp.responseText;
      state = xmlhttp.responseText;
    }
  }
  xmlhttp.open("GET","./getstate.php",true);
  xmlhttp.send();
}
showHint();
setInterval(showHint,1000);
function loadLog() {
	
  var xmlhttp=new XMLHttpRequest();
  xmlhttp.onreadystatechange=function() {
    if (xmlhttp.readyState==4 && xmlhttp.status==200) {
      document.getElementById("log").innerHTML=xmlhttp.responseText;
      state = xmlhttp.responseText;
    }
  }
  xmlhttp.open("GET","./sensorlog.php",true);
  xmlhttp.send();
}
loadLog();
setInterval(loadLog,3000);

</script>
<style type="text/css">
body{
background: #efefef;
}
.btn {
  background: #3498db;
  background-image: -webkit-linear-gradient(top, #3498db, #2980b9);
  background-image: -moz-linear-gradient(top, #3498db, #2980b9);
  background-image: -ms-linear-gradient(top, #3498db, #2980b9);
  background-image: -o-linear-gradient(top, #3498db, #2980b9);
  background-image: linear-gradient(to bottom, #3498db, #2980b9);
  font-family: Arial;
  color: #ffffff;
  font-size: 20px;
  padding: 10px 20px 10px 20px;
  text-decoration: none;
}

.btn:hover {
  background: #3cb0fd;
  background-image: -webkit-linear-gradient(top, #3cb0fd, #3498db);
  background-image: -moz-linear-gradient(top, #3cb0fd, #3498db);
  background-image: -ms-linear-gradient(top, #3cb0fd, #3498db);
  background-image: -o-linear-gradient(top, #3cb0fd, #3498db);
  background-image: linear-gradient(to bottom, #3cb0fd, #3498db);
  text-decoration: none;
}

.btn:disabled{
 
background: #3498db;
background-image: -webkit-linear-gradient(top, #ededed, #dfdfdf);
background-image: -moz-linear-gradient(top, #ededed, #dfdfdf);
background-image: -ms-linear-gradient(top, #ededed, #dfdfdf);
background-image: -o-linear-gradient(top, #ededed, #dfdfdf);
background-image: linear-gradient(to bottom, #ededed, #dfdfdf);
font-family: Arial;
color: #ffffff;
font-size: 20px;
padding: 10px 20px 10px 20px;
text-decoration: none;
}
h1 {
position: relative;
font-size: 50px;
margin-top: 0;
font-family: 'Myriad Pro', 'Myriad', helvetica, arial, sans-serif;
text-shadow: 2px 3px 3px #292929;
letter-spacing: -3px;
-webkit-text-stroke: 1px white;
}

.box{
width: 500px;
margin-left:auto;
margin-right:auto;
-moz-border-radius: 27px;
-webkit-border-radius: 27px;
border-radius: 27px;
/*IE 7 AND 8 DO NOT SUPPORT BORDER RADIUS*/
-moz-box-shadow: 0px 0px 1px #000000;
-webkit-box-shadow: 0px 0px 1px #000000;
box-shadow: 0px 0px 1px #000000;
/*IE 7 AND 8 DO NOT SUPPORT BLUR PROPERTY OF SHADOWS*/
padding-top:10px;
background:#dadada;
padding-bottom:10px;

}
.center{

width:500px;
text-align:center;
margin-left:auto;
margin-right:auto;
padding-top:15px;
}
#log{
margin-top:-10px;
text-align:center;
height:120px;
}
</style>
</head>
<body >
<div class="box">
<div class="center">
	<div style="float:left;margin-left:18%;"><h1>Relay State:<span id="txtHint"></span></h1></div>
	<div style="clear:both;"></div>
	<form action="toggle.php" method="post">
		<input class="btn" type="submit" name="On" value="On"></input>
		<input class="btn" type="submit" name="Off" value="Off"></input>
	</form>
</div>
</div>
<div class="center">
<div id="log" class="box"></div>
</div>
</body>
</html>
