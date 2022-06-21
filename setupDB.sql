-- use master;

use sqlHeapTest;
ALTER DATABASE sqlHeapTest SET SINGLE_USER WITH ROLLBACK IMMEDIATE;

use [tempdb];
drop database sqlHeapTest;

create database sqlHeapTest;

use sqlHeapTest;

create table testTable (
    intColumn BIGINT,
    md5 VARCHAR(32),
    string VARCHAR(1000)
);


select count(*) from testTable;
