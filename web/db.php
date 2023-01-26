<?php

$API_PASSWD='94bd18c7-91a4-4f79-b45a-7a59105631f4';

$db = pg_connect("host=127.0.0.1 dbname=wrp_audit_web user=app_wrp_audit_web password=lAM*c.mho`i;x^");

if (!$db) {
    $error = error_get_last();
    echo "Connection failed. Error was: ". $error['message']. "\n";
} else {
    //echo "Connection succesful.\n";
}
$heslo_db2 = 'J!i"wLJ0uQE_I/';
$db2 = pg_connect("host=127.0.0.1 dbname=wrp_audit user=app_wrp_audit password={$heslo_db2}");

if (!$db2) {
    $error = error_get_last();
    echo "Connection failed. Error was: ". $error['message']. "\n";
} else {
    //echo "Connection succesful.\n";
}

?>