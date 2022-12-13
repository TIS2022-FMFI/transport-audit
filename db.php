<?php

$db = pg_connect("host=server.nahovno.eu dbname=audit-preprav-web user=admin password=Verejne_zname_heslo_47");

if (!$db) {
    $error = error_get_last();
    echo "Connection failed. Error was: ". $error['message']. "\n";
} else {
    //echo "Connection succesful.\n";
}

$db2 = pg_connect("host=server.nahovno.eu dbname=audit-preprav user=admin password=Verejne_zname_heslo_47");

if (!$db2) {
    $error = error_get_last();
    echo "Connection failed. Error was: ". $error['message']. "\n";
} else {
    //echo "Connection succesful.\n";
}

?>