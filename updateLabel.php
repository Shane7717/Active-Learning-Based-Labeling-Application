<?php
	error_reporting(E_ALL);
	ini_set('display_errors', 1);
	
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
	
	$choice = $_POST["choice"];
	$text = $_POST["textarea"];
	$slashes_text = addslashes($text);
	
	if ($text == "") {
		echo "<script language=\"JavaScript\">\r\n";
		echo " alert(\"Sorry, you haven't choose any text to label. Please start randomly labeling.\");\r\n";
		echo " location.replace(\"uploadDatasets.php\");\r\n"; 
		echo "</script>";
		exit;
	}
	if ($choice == "") {
		echo "<script language=\"JavaScript\">\r\n";
		echo " alert(\"Sorry, you haven't labeled the text. Please give the text a label.\");\r\n";
		echo " location.replace(\"uploadDatasets.php\");\r\n"; 
		echo "</script>";
		exit;
	}
	
	//check information
	$sql = "SELECT * FROM tempdata WHERE (content='$slashes_text')";
	$result = $conn->query($sql);
	
	if ($result->num_rows != 0) {
		// same text has already been saved in the table
		echo "<script language=\"JavaScript\">\r\n";
		echo " alert(\"You have already labeled this text. Please choose another one to label.\");\r\n";
		echo " location.replace(\"uploadDatasets.php\");\r\n"; 
		echo "</script>";
		exit;
		
	} else {
		// no same text has been saved in the table
//		if ($choice == "negative") {
//			$sql = "INSERT INTO tempdata(content, label) VALUES ('$slashes_text', 0)";
//			mysqli_query($conn, $sql);
//		}
//		if ($choice == "positive") {
//			$sql = "INSERT INTO tempdata(content, label) VALUES ('$slashes_text', 1)";
//			mysqli_query($conn, $sql);
//		}
		$sql = "INSERT INTO tempdata(content, label) VALUES ('$slashes_text', $choice)";
		mysqli_query($conn, $sql);

		
		echo "<script language=\"JavaScript\">\r\n";
		echo " alert(\"Labeled successfully! You can continue to do labeling.\");\r\n";
		echo " location.replace(\"uploadDatasets.php\");\r\n";
		echo "</script>";
		exit;
	}

?>