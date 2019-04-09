-- Exported from QuickDBD: https://www.quickdatatabasediagrams.com/
-- NOTE! If you have used non-SQL datatypes in your design, you will have to change these here.


CREATE TABLE `User` (
    `ID` int  NOT NULL ,
    `USERNAME` string  NOT NULL ,
    `EMAIL` string  NOT NULL ,
    `PASSWORD` string  NOT NULL ,
    PRIMARY KEY (
        `ID`
    ),
    CONSTRAINT `uc_User_USERNAME` UNIQUE (
        `USERNAME`
    ),
    CONSTRAINT `uc_User_EMAIL` UNIQUE (
        `EMAIL`
    ),
    CONSTRAINT `uc_User_PASSWORD` UNIQUE (
        `PASSWORD`
    )
);

CREATE TABLE `USERTESTS` (
    `ID` int  NOT NULL ,
    `TITLE` string  NOT NULL ,
    `DATE_POSTED` datetime  NOT NULL ,
    `CONTENT` text  NOT NULL ,
    `USER_ID` int  NOT NULL ,
    PRIMARY KEY (
        `ID`
    )
);

ALTER TABLE `USERTESTS` ADD CONSTRAINT `fk_USERTESTS_TITLE` FOREIGN KEY(`TITLE`)
REFERENCES `User` (`USERNAME`);

