<?php
require "bd.php";

$status = $_POST['status'];

if ($status == "admins") {
	$result = mysqli_query($link, "SELECT * FROM AdminsFeedback WHERE status NOT LIKE 'user'");
} elseif ($status == "god") {
	$result = mysqli_query($link, "SELECT * FROM AdminsFeedback WHERE status='god'");
} elseif ($status == "user") {
	$result = mysqli_query($link, "SELECT * FROM AdminsFeedback WHERE status='user'");
}

$row = mysqli_fetch_all($result, MYSQLI_ASSOC);
echo json_encode($row);
