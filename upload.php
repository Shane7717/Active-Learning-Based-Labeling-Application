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
	
	// Getting user uploaded file
	$file = $_FILES['file'];
		
	// Saving file in uploads folder
	move_uploaded_file($file["tmp_name"], "uploads/" . $file["name"]);
	
	// Clear the table first
	$sql = "TRUNCATE maindata";
	mysqli_query($conn, $sql);
	
	$zip_handle = zip_open("uploads/data.zip");
	$counter = 0;
	
	while($zip_entry = zip_read($zip_handle))
		{
			$resource = zip_entry_open($zip_handle, $zip_entry, "rb"); 
			$file_name = zip_entry_name($zip_entry); 
			
			$check = substr($file_name, 0, 8);
			// if the file name starts with __MACOSX
			if (strcmp($check, "__MACOSX") == 0) {
				continue;
			}
			
			if ($resource == true)
				{
					// read zip content，maximum 60000 bytes
					$file_content = zip_entry_read($zip_entry, 60000); 
					echo("File Name: " . $file_name . " is opened Successfully. <br>"); 
					//$file_content = addslashes($file_content);
					echo($file_content); 
					echo("<br><br>"); 
					
					// without knowing the labels beforehand
					$file_content = addslashes($file_content);
					$sql = "INSERT INTO maindata(file_name, content, label) VALUES ('$file_name', '$file_content', -1)";
					mysqli_query($conn, $sql);
					
					$counter = $counter + 1;
					zip_entry_close($zip_entry); 
				}
			else
				echo("Failed to Open."); 
		}
		
	zip_close($zip_handle);
	
	//jump to the specific location
	echo "<script language=\"JavaScript\">\r\n";
	echo " alert(\"Data uploaded successfully!\");\r\n";
	echo " location.replace(\"uploadDatasets.php\");\r\n"; 
	echo "</script>";
	
	mysqli_close($conn);
//	exit;
?>