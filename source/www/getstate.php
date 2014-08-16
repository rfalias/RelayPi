<?php
//$state = readfile('/var/www/sensor/state');
//echo $state[0];
$url = "http://localhost:8080?state=get";
$curl = curl_init();
curl_setopt ($curl, CURLOPT_URL, $url);
curl_setopt($curl, CURLOPT_RETURNTRANSFER, 1);

$result = curl_exec ($curl);
curl_close ($curl);
$state = $result;

if ($state == "True")
{
	echo "On";
}
else if ($state == "False")
{
	echo "Off";
}
else
{
	echo "Unknown";
}
?>
