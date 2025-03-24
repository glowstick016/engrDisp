create database if not exists engrDisp;

use engrDisp;

create table if not exists dispStatus(
    dispName varchar(255) NOT NULL,
    loc varchar(255),
    ping int,
    user varchar(255),
    api varchar(255), 
)