<?php
require "bd.php";
$data = $_POST['data'];
$tgid = $_POST['tgid'];
$username = $_POST['username'];
$name = $_POST['name'];

if ($data == "addadmin")
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

?>
