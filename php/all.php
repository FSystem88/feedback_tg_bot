<?php
require "bd.php";

$status = $_POST['status'];

if ( $status == "" )
{
	$result = mysqli_query($link, "select * from AdminsFeedback");
}
else
{
	$result = mysqli_query($link, "select * from AdminsFeedback where status='{$status}'");
}

$row = mysqli_fetch_all($result, MYSQLI_ASSOC);
echo json_encode($row);

?>
