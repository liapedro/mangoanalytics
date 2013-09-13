<?php

include_once("libs/misc.lib.php");
include_once("configs/default.conf.php");
include_once("libs/paloSantoACL.class.php");
include_once("libs/paloSantoDB.class.php");

session_name("elastixSession");
session_start();
$pDB  = new paloDB($arrConf["elastix_dsn"]["acl"]);
$pACL = new paloACL($pDB);
if(isset($_SESSION["elastix_user"]))
    $elastix_user = $_SESSION["elastix_user"];
else
    $elastix_user = "";
session_commit();
if($pACL->isUserAdministratorGroup($elastix_user)){

	$db = mysql_connect('localhost', 'nextor_tarificador', 'k4590NAEUI');
	#We save such credentials:

	$query = "INSERT INTO tarifica_elastixuser(name, permissions) VALUES('".$elastix_user."', 1)";
	$result = mysql_query($query);
	if(!$result){
		echo "Something went wrong while redirecting to Mango Analytics.";
		die();
	}
	$ip = $_SERVER["SERVER_ADDR"];
	$path = $_SERVER["PATH_INFO"];

	$loc_path = "http://".$ip.":8000".$path;
	header("Location: ".$loc_path);
}
?>