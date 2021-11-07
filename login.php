<?php
	error_reporting(E_ALL);
	ini_set('display_errors', 1);
	
	$loginname = $_POST["name"];
	$pwd = $_POST["password"];
	
	//****confidential information*******
	$servername = "localhost";
	$username = "root";
	$password = "root";
	$dbname = "easyLabeler";
	
	$conn = new mysqli($servername, $username, $password, $dbname);
	if ($conn->connect_error) {
		die("Connection failed: " . $conn->connect_error);
	} else {
		echo "...Connected successfully...";
	}

	//check information
	$sql = "SELECT * FROM users WHERE (username='$loginname') AND (password='$pwd')";
	$result = $conn->query($sql);
	if ($result->num_rows != 0) {
		//jump to the specific location
		echo "<script language=\"JavaScript\">\r\n";
		echo " alert(\"Login successfully!\");\r\n";
		echo " location.replace(\"uploadDatasets.php\");\r\n"; 
		echo "</script>";
		exit;
	} else {
		echo "<script language=\"JavaScript\">\r\n";
		echo " alert(\"Wrong username or password. Login Failed!\");\r\n";
		echo " location.replace(\"index.html\");\r\n"; 
		echo "</script>";
		exit;
	}
?>
