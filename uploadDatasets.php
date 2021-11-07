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
//		echo "...Connected successfully...";
	}
	
	
	function showRandomText() {

		// Get the total number of the datasets
		global $conn, $sql;
		$sql = "SELECT count(*) FROM maindata";
		$result = mysqli_query($conn, $sql);
		$rows = mysqli_fetch_row($result);
		$rowcount = $rows[0];	// this will get 1000 for example
		
		$randomID = mt_rand(1, $rowcount);
		$sql = "SELECT * FROM maindata WHERE (id='$randomID')";
		$result = mysqli_query($conn, $sql);
		$res = mysqli_fetch_assoc($result);
		$content = $res['content'];
		$slashes_content = addslashes($content);
		
		return $slashes_content;
	}
	
	function showProgress() {
		global $conn, $sql;
		$sql = "SELECT * FROM tempdata";
		$result = $conn->query($sql);
		$labeled = $result->num_rows;
		
		$sql = "SELECT * FROM maindata";
		$result = $conn->query($sql);
		$total = $result->num_rows;
		
		$content = "You have labeled ".$labeled." out of ".$total." texts.";
		return $content;
	}
?>


<!DOCTYPE html>
<html>
	<head>
		<meta charset="UTF-8">
		<title>Upload Datasets</title>
		<style type = "text/css">
			body {
				background: url("images/plainBackground.jpeg");
				background-size: cover;
			}
			.relative{
				position: relative;
				left: 25%;
			}
			.buttonStyle1{
				position: relative;
				left: 36%;
				background-color: #0099CC; /* Blue */
				color: white;
				padding: 8px 16px;
				text-align: center;
				text-decoration: none;
				display: inline-block;
				font-size: 15px;
				font-weight: 600;
				border: none;
				transition-duration: 0.4s;
				box-shadow: 0 4px 8px 0 rgba(0,0,0,0.1), 0 6px 20px 0 rgba(0,0,0,0.19);
			}
			.buttonStyle1:hover{
				background-color: #009999;
				color: white;
				cursor: pointer;
				box-shadow: 0 12px 16px 0 rgba(0,0,0,0.24), 0 17px 50px 0 rgba(0,0,0,0.19);
				font-weight: 900;
			}
			.buttonStyle2{
				background-color: #FFFFF0; 
				border: 2.5px solid #4CAF50;
				color: black;
				padding: 6px 12px;
				text-align: center;
				text-decoration: none;
				display: inline-block;
				font-size: 12px;
				margin: 4px 2px;
				transition-duration: 0.4s;
				font-weight: 600;
				position: relative;
				left: 25%;
			}
			.buttonStyle2:hover{
				background-color: #4CAF50;
				color: white;
				cursor: pointer;
				font-weight: 900;
			}
			.textareaStyle{
				border:0;
				border-radius:5px;
				background-color:#FFFFF0;
				resize: none;
			}

			
		</style>
		
		<script type = "text/javascript">
						
			function show() {
				var content = "<?php echo showRandomText()?>";
				document.getElementById("textarea").innerText = content;
			}
			
			function showProgress() {
				var content = "<?php echo showProgress()?>";
				document.getElementById("progress").innerText = content;
			}
				
		</script>
				
	</head>
	<body onload="showProgress()">
		
		<!-- multipart/form-data ensures that form data is going to be encoded as MIME data -->
		<div><form action="upload.php" method="POST" enctype="multipart/form-data">
			
			<br><code style="background-color: #FFFFF0; font-size: x-large; font-weight: bold;" >Please upload your data zip file:</code><br><br><br>
			
			
				<code style="background-color: #FFFFF0;"> Select a zip file to upload: </code>
				
				<!-- name of the input fields are going to be used in our php script-->
				&nbsp;&nbsp;&nbsp;<input type="file" name="file" id="file">
				
				<br><br> 
				
				<input type="submit" class="buttonStyle1" style="left:0%" name="submit" value="Upload" >
				
		</form></div><br><br>
		
		<button type="button" class = "buttonStyle2" onclick="show();"> Start Randomly Labeling </button>&nbsp;&nbsp;
		<button type="button" class = "buttonStyle2" onclick="location.reload()"> Refresh </button><br>
				
		&nbsp;<code class="relative" style="background-color: #FFFFF0; color: green;" id="progress"></code>
		<form name = "label_form"; action = "updateLabel.php"; method = "POST"; style = "font-weight: bold;" class="relative">
			<label><textarea readonly="readonly" class="textareaStyle" name = "textarea" rows="18" cols="80" id="textarea"></textarea></label>
			<br>

			<input type = "text" name = "choice" 
				style="width:60px;height:24px;font-weight:900;text-align:center;border-radius:3px;border:1;background-color:#FFFFF0;"
				oninput="value = value.replace(/[^\d]/g,'')">
			<input type = "Submit" class="buttonStyle2" value = "Submit Label >>" style="left:1%" required = "true"/>
		</form><br>
		
		<code class="relative" style="background-color: #FFFFF0; color: blue;">If you think you have labeled enough data, you could click the button below.</code>
		<br><br>
		<button type="button" class = "buttonStyle1"><a href="http://127.0.0.1:8002/">Jump to Generate the Classifier</a></button>
		
		
	</body>
</html>