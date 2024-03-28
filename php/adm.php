<?php

require "bd.php";

$data = $_POST['data'];
$tgid = $_POST['tgid'];
$username = $_POST['username'];
$name = $_POST['name'];

mysqli_set_charset($link, "utf8mb4");

if ($data == "admins")
{
	$result = mysqli_query($link, "SELECT * FROM AdminsFeedback WHERE status NOT LIKE 'user'");
	$row = mysqli_fetch_all($result, MYSQLI_ASSOC);
	echo json_encode($row);
}
elseif ($data == "god")
{
	$result = mysqli_query($link, "SELECT * FROM AdminsFeedback WHERE status='god'");
	$row = mysqli_fetch_all($result, MYSQLI_ASSOC);
	echo json_encode($row);
}
elseif ($data == "user")
{
	$result = mysqli_query($link, "SELECT * FROM AdminsFeedback WHERE status='user'");
	$row = mysqli_fetch_all($result, MYSQLI_ASSOC);
	echo json_encode($row);
}
elseif ($data == "addadmin") 
{
	$result = mysqli_query($link, "INSERT INTO `AdminsFeedback` (`tgid`, `status`) VALUES ('{$tgid}', 'admin')");
} 
elseif ($data == "update") 
{
	$result = mysqli_query($link, "UPDATE `AdminsFeedback` SET `name`='{$name}', `username`='{$username}' WHERE `tgid`='{$tgid}'");
} 
elseif ($data == "delete") 
{
	$result = mysqli_query($link, "DELETE FROM `AdminsFeedback` WHERE `tgid`='{$tgid}'");
} 
elseif ($data == "adduser") 
{
	$result = mysqli_query($link, "INSERT INTO `AdminsFeedback` (`tgid`, `name`, `username`, `status`) VALUES ('{$tgid}','{$name}','{$username}', 'user') ");
} 
elseif ($data == "find") 
{
	$result = mysqli_query($link, "SELECT * FROM  AdminsFeedback WHERE tgid='{$tgid}'");
	$row = mysqli_fetch_all($result, MYSQLI_ASSOC);
	echo json_encode($row);
}
elseif ($data == "block") 
{
	$result = mysqli_query($link, "UPDATE `AdminsFeedback` SET `ban`='ban' WHERE `tgid`='{$tgid}'");
}
elseif ($data == "checkblock")
{
	$result = mysqli_query($link, "SELECT * FROM AdminsFeedback WHERE tgid='{$tgid}' AND ban='ban' ");
	$row = mysqli_fetch_all($result, MYSQLI_ASSOC);
	echo json_encode($row);
}
elseif ($data == "allblock")
{
	$result = mysqli_query($link, "SELECT * FROM AdminsFeedback WHERE ban='ban' ");
	$row = mysqli_fetch_all($result, MYSQLI_ASSOC);
	echo json_encode($row);
}
elseif ($data == "delblock")
{
	$result = mysqli_query($link, "UPDATE `AdminsFeedback` SET `ban`='' WHERE `tgid`='{$tgid}'");
}

?>
