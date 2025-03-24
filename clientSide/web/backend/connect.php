<?php 
// Goal of this is to handle all of the connection oriented tasks for the database 

function connect(){
    //Goal make a connection that will be useable to add info into the database
    $db = 'localhost:3306';
    $user = 'engradmin';
    $pass = 'temp1234';
    $name = 'engrDisp';

    $link = new mysqli($db, $user, $pass, $name);

    if($link->connect_error){
        // Couldn't make the connection 
        echo "Failed to connect";
    }else{
        echo "connected";
    }
    return $link;
}
#connect();

//Main Functions here 
function addInfo($id, $timeDelay, $imgName, $imgPath, $imgAdded, $imgDeploy, $imgRetire, $imgActive){
    // Goal is to make adding info to the local sql database (images)
    $link = connect();

    if($link){
        //Valid link can continue 
        //Making and binding tghe link
        $sql=$link->prepare("INSERT INTO dispTable (dispTable_id, dispTable_Delay, dispTable_Name, dispTable_Path, dispTable_Added, dispTable_Deploy, dispTable_Retire, dispTable_Active) VALUES (?,?, ?, ?, ?, ?, ?,?)");
        $sql->bind_param("iisssssi", $id, $timeDelay, $imgName, $imgPath, $imgAdded, $imgDeploy, $imgRetire, $imgActive);

        if($sql->execute()){
            //Success 
            echo "Success";
        }else{
            //Error need to log
            echo "Failed to do addInfo";
        }
        //Clean up processes
        $sql->close();
        $link->close();

    }else{
        //Throw up error here
    }
    return;
}
#addInfo($id, $imgName, $imgPath, $imgAdded, $imgDeploy, $imgRetire, $imgActive)
addInfo(1, 10,"test4.img","/home/cjkenned/engrDisp/clientSide/images/","2025-01-25","2025-01-25","2026-01-26",1);

function getInfo(){
    //Goal of the function is to display all of the data needed for the webpage
    $link=connect();

    if($link){
        //Success need to now pull all of the data 

    }else{
        //Failure need to throw an error 

    }
}
#getInfo();

//Builder functions here 
function changeStatus($imgName, $newStatus){
    //Goal is to update the boolean flag in the database

    $link=connect();

    if($link && ($newStatus == 0 || $newStatus == 1)){
        $sql=$link->prepare("update dispTable set dispTable_Active = ? where dispTable_Name = ?");
        $sql->bind_param("is", $newStatus,$imgName);

        if($sql->execute()){
            //Success
        }else{
            //Failed
        }

        $sql->close();
    }else{
        //Failed to get link
    }
    $link->close();
    
}

function changeEndDate($imgName, $newTime){
    //Goal is to change the end date of an image 

    $link=connect();

    if($link){
        $sql=$link->prepare("update dispTable set dispTable_Retire = ? where dispTable_Name = ?");
        $sql->bind_param("ss", $newTime, $imgName);

        if($sql->execute()){
            //Success
        }else{
            //Failed
        }

        $sql->close();
    }else{
        //Failed to get the link
    }

    $link->close();
}

function changeStartDate($imgName, $newTime){
    //Goal is to change the end date of an image 

    $link=connect();

    if($link){
        $sql=$link->prepare("update dispTable set dispTable_Deploy = ? where dispTable_Name = ?");
        $sql->bind_param("ss", $newTime, $imgName);

        if($sql->execute()){
            //Success
        }else{
            //Failed
        }

        $sql->close();
    }else{
        //Failed to get the link
    }

    $link->close();
}

function changeName($oldName, $newName){
    //Goal is to change the img name and set the new filepath 

    $link=connect();

    if($link && (strlen($newName) <= 255) ){
        //Need to make a temp copy of the file before this just incase
        $newPath = "TEMP";

        $sql=$link->prepare("update dispTable set dispTable_Name = ?, dispTable_Path = ? where dispTable_Name =?");
        $sql->bind_param("sss", $newName, $newPath, $oldName);
        if($sql->execute()){
            //Success need to delete old file now 
        }else{
            //Failed 
        }
        $sql->close();
    }elseif($link){
        //Failed to make the link
    }elseif(strlen($newName) <= 255){
        //Name too long
    }
    $link->close();
}


?>