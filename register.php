<?php
// This php file is used to send user account creation data to the database
	
    error_reporting(E_ALL);
    ini_set('display_errors', 1);
          
    $user_name = $_POST["username"];
    $email = $_POST["email"];
    $pwd = $_POST["pwd1"];

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
 	$sql = "SELECT * FROM users WHERE (username='$user_name')";
 	$result = $conn->query($sql);
	if ($result->num_rows != 0) {
		
		//jump to the specific location
		$sql = "DELETE FROM Users where username = '' ";
		mysqli_query($conn, $sql);
		echo "<script language=\"JavaScript\">\r\n";
		echo " alert(\"Sorry, the username has been used. Please change another username.\");\r\n";
		echo " location.replace(\"register.html\");\r\n"; 
		echo "</script>";
		exit;
	}
	else {
		$sql = "INSERT INTO users(username, password, email)
		VALUES ('$user_name', '$pwd','$email')";
		mysqli_query($conn, $sql);
		$sql = "DELETE FROM Users where username = '' ";
		mysqli_query($conn, $sql);
		
		//jump to the specific location
		echo "<script language=\"JavaScript\">\r\n";
		echo " alert(\"Register successfully!\");\r\n";
		echo " location.replace(\"index.html\");\r\n"; 
		echo "</script>";
		exit;
	}
	
	mysqli_close($conn);
?>
