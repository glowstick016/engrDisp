create database if not exists engrDisp;

use engrDisp;

create table if not exists dispTable(
    dispTable_Name VARCHAR(255) NOT NULL primary key,
    dispTable_id int NOT NULL,
    dispTable_Path VARCHAR(255) NOT NULL,
    dispTable_Added DATETIME NOT NULL,
    dispTable_Deploy DATETIME, /* Format for data is 'YYYY-MM-DD HR:MIN:SEC*/
    dispTable_Retire DATETIME,
    dispTable_Active BOOLEAN NOT NULL,  /* Format for a boolean is as an int (1/0) */
    dispTable_Delay int NOT NULL
    dispTable_crtd_id VARCHAR(40),
    dispTable_crtd_dt DATE,
    dispTable_updt_id VARCHAR(40),
    dispTable_updt_dt DATE
)