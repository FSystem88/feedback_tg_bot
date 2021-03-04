<?php
require "bd.php";

$data = $_POST['data'];
$tgid = $_POST['tgid'];
$name = $_POST['name'];
$username = $_POST['username'];
$text = $_POST['text'];
$answer = $_POST['answer'];
$adminID = $_POST['adminID'];
$adminName = $_POST['adminName'];


if ($data == "new")
{
	$result = mysqli_query($link, "INSERT INTO `MessFeedback` (`tgid`, `name`, `username`, `text`, `status`) VALUES ('{$tgid}', '{$name}', '{$username}', '{$text}', '0') ");
}
elseif ($data == "count")
{
	$result = mysqli_query($link, "select count(*) from MessFeedback where status='0'");
	$r = mysqli_fetch_array($result);
	echo $r[0];
}
elseif ($data == "delete")
{
	$result = mysqli_query($link, "DELETE FROM `MessFeedback` WHERE `text`='{$text}' AND `tgid`='{$tgid}' ");
}
elseif ($data == "reply")
{
	$result = mysqli_query($link, " UPDATE `MessFeedback` SET `answer`='{$answer}', `status`='1', `adminID`='{$adminID}', `adminName`='{$adminName}' WHERE `text`='{$text}' AND `tgid`='{$tgid}' ");
}
elseif ( $data == "unread" )
{
	$result = mysqli_query($link, "SELECT * FROM MessFeedback WHERE status='0'");
	$row = mysqli_fetch_all($result, MYSQLI_ASSOC);
	echo json_encode($row);
}
elseif ( $data == "old" )
{
	$result = mysqli_query($link, "SELECT * FROM MessFeedback WHERE status='1'");
	$row = mysqli_fetch_all($result, MYSQLI_ASSOC);
	echo json_encode($row);
}

?>
