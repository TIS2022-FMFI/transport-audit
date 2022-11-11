<?php
date_default_timezone_set('Europe/Bratislava');
error_reporting(E_ALL ^ E_NOTICE);  
?>


<?php


/* kontroluje meno (meno a heslo v SHA256 "formáte")
vráti riadok s použivatelom ak existuje, ak nie vráti false
*/
function over_pouzivatela($db, $username, $pass) {
	if ($db) {
		$pass = hash('sha256', $pass);
		$sql = "SELECT * FROM users WHERE username=$1 AND password=$2" ;  // definuj dopyt
		$result = pg_prepare($db, "prihlasenie", $sql);
		//pg_get_result($db);
		$result = pg_execute($db, "prihlasenie", array($username, $pass));
		pg_send_query($db,"DEALLOCATE prihlasenie");
		//$result = pg_get_result($db);
//		echo "sql = $sql <br>";
		if ($result && (pg_num_rows($result) > 0)) {  // vykonaj dopyt
			// dopyt sa podarilo vykonať
			$row = pg_fetch_row($result,0);
			pg_free_result($result);
			return $row;
		} else {
			// dopyt sa NEpodarilo vykonať, resp. používateľ neexistuje!
			//echo "Kombinácia mena a hesla je nesprávna";
			return false;
		}
	} else {
		// NEpodarilo sa spojiť s databázovým serverom!
		return false;
	}
}
?>
