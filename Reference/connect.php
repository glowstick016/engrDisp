
<?php
//Include Statements 
require_once "log.php";
require_once "goat.php";


function addInfo($username, $email, $pass, $admin, $rights){
/* Database credentials. Assuming you are running MySQL
server with default setting (user 'root' with no password) */

	list($pass,$salt) = salty($pass,$username,1);

	$DB_SERVER = 'localhost:3306';
	$DB_USERNAME = 'GlowWeb';
	$DB_PASSWORD = 'JbLr+KSswbEpo1FF';
	$DB_NAME = 'GlowWeb';

	/* Attempt to connect to MySQL database */
	$link = new mysqli($DB_SERVER, $DB_USERNAME, $DB_PASSWORD, $DB_NAME);
 
	// Check connection
	if($link ->connect_error){
		die("ERROR: Could not connect. " . mysqli_connect_error());
		logs("ERROR: Could not connect" . mysqli_connect_error());
		echo "Couldn't connect";
	}
	

	//User Info
	$sql=$link->prepare("INSERT INTO Users (Usr, EMAIL, Password, Admin, Rights) values (?,?,?,?,?)");

	//Bind Params
	$sql->bind_param("sssii",$username,$email,$pass,$admin,$rights);
	if($sql->execute()){
		//echo "New user added successfully";
		logs("Added $username waiting approval");
	} else {
		echo "Error: " . $sql . "<br>" . $link->error;
		logs("Error: " . $sql . "<br>" . $link->error);
	}

	$link->close();
	addSalt($username,$salt);
}

function connect(){
	    $DB_SERVER = 'localhost:3306';
		$DB_USERNAME = 'GlowWeb';
		$DB_PASSWORD = 'JbLr+KSswbEpo1FF';
		$DB_NAME = 'GlowWeb';

		/* Attempt to connect to MySQL database */
		$link = new mysqli($DB_SERVER, $DB_USERNAME, $DB_PASSWORD, $DB_NAME);

		// Check connection
		if($link ->connect_error){
			die("ERROR: Could not connect. " . mysqli_connect_error());
			logs("ERROR: Could not connect" . mysqli_connect_error());			
		}
		return $link;
}

function getRights($usr){
	
	$link=connect();

	$sql=$link->prepare("select Rights from Users where Usr = ?");

	if($sql){
		$sql->bind_param("s",$usr);
		$sql->execute();

		$sql->bind_result($tmp);
        	$sql->fetch();
		$sql->close();


        	$rights = $tmp;
		//echo $rights . "\n";
	}else{
		logs("Error getting $usr rights");
		$rights = NULL;
	}
	return $rights;
}

function getAdmin($usr){
	

	$link=connect();

        $sql=$link->prepare("select Admin from Users where Usr = ?");

	if($sql){
        	$sql->bind_param("s",$usr);
        	$sql->execute();

	        $sql->bind_result($tmp);
		$sql->fetch();
		$sql->close();


        	$admin = $tmp;
	
		//echo $admin . "\n";
        	return $admin;
	}else{
		logs("Error getting $usr admin status");
		return NULL;
	}
}

function giveAdmin($usr){
	$link=connect();

	$sql=$link->prepare("update Users set Admin = 1 where Usr = ?");

	if($sql){
		$sql->bind_param("s",$usr);

		$sql->execute();
		$sql->close();
		//echo "Added $usr as an admin\n";
		logs("Added $usr as admin");
	}else{
		logs("Error added $usr as admin");
	}
	return;
}

function changeRights($usr, $rights){
	$link=connect();
	
	$sql=$link->prepare("update Users set Rights = ? where Usr = ?");

	if($sql){
		$sql->bind_param("is", $rights, $usr);

		$sql->execute();
		$sql->close();
		//echo "Change $usr rights to $rights \n";
		logs("Change $usr rights to $rights \n");
	}else{
		logs("Error changing $usr rights");
	}
	return;
}

function changeEmail($usr, $email){
	$link=connect();

	$sql=$link->prepare("update Users set EMAIL = ? where Usr = ?");

	if($sql){
		$sql->bind_param("ss",$email,$usr);

		$sql->execute();
		$sql->close();

		echo "Change $usr email to $email";
		logs("Change $usr email to $email");
	}else{
		logs("Failed to change $usr email to $email");
	}
	return;
}

function removeUser($usr){
	$link=connect();

	$sql=$link->prepare("delete from Users where Usr = ?");

	if($sql){
		$sql->bind_param("s",$usr);

		$sql->execute();
		$sql->close();
			
		echo "Removed $usr";
	        logs("Removed $usr");
	}else{
		logs("Failed to remove $usr");
	}
	return;
}

function get2FA($usr){
	$link=connect();

	$sql=$link->prepare("select Phone from Users where Usr = ?");

	if($sql){
		$sql->bind_param("s",$usr);

		$sql->execute();
		$sql->bind_result($tmp);
		$sql->fetch();
		$sql->close();

		$phone = $tmp;
		return $phone;
	}else{
		logs("Failed to fetch $usr phone number");
		return NULL;
	}
}

function getSalt($usr){
	$link = connect();

	$sql=$link->prepare("select Salt from Users where Usr = ?");


	if($sql){
		$sql->bind_param("s",$usr);

		$sql->execute();
		$sql->bind_result($tmp);
		$sql->fetch();
		$sql->close();
		
		$salt = $tmp;
		return $salt;
	}else{
		logs("Failed to fetch $usr salt");
		return NULL;
	}
}

function addSalt($usr,$salt){
	$link = connect();

	$sql=$link->prepare("update Users set Salt = ? where Usr = ?");

	if($sql){
		$sql->bind_param("ss", $salt, $usr);
		
		$sql->execute();
		$sql->close();
		logs("Added salt for $usr");	
	}else{
		logs("failed to add salt for $usr");
	}
	return;
}


function changePass($usr, $pass){
	$hash = salty($pass,$usr,0);
	$link = connect();

	$sql=$link->prepare("update Users set Password = ? where Usr = ?");

	if($sql){
		$sql->bind_param("ss", $hash, $usr);
		
		$sql->execute();
		$sql->close();
		logs("Changed password for $usr");	
	}else{
		logs("failed to change password for $usr");
	}
	return;
}


function change2FA($usr, $phone){
	$link = connect();

	$sql=$link->prepare("update Users set Phone = ? where Usr = ?");

	if($sql){
		$sql->bind_param("ss",$phone,$usr);

		$sql->execute();
		$sql->close();
		logs("Changed 2FA for $usr");
	}else{
		logs("Failed to change 2FA for $usr");
	}
	return;

}
//addInfo("cjkenned","cjkenned@udel.edu","scooby016!!",0,0);
//$usr = "cjkenned";
//addSalt($usr,"a3rjvdsi2i2");
//removeUser($usr);
//changePass($usr,"asa");
?>
