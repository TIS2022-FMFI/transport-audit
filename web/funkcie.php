<?php
date_default_timezone_set('Europe/Bratislava');

?>


<?php


/* kontroluje meno (meno a heslo v SHA256 "formáte")
vráti riadok s použivatelom ak existuje, ak nie vráti false
*/
function over_pouzivatela($mysqli, $username, $pass) {
	if (!$mysqli->connect_errno) {
		$pass = hash('sha256', $pass);
		$sql = "SELECT * FROM users WHERE username=? AND password=?" ;  // definuj dopyt
		$stmt = $mysqli->prepare($sql);
		$stmt->bind_param("ss", $username,$pass);
		$stmt->execute();
//		echo "sql = $sql <br>";
		if (($result = $stmt->get_result()) && ($result->num_rows > 0)) {  // vykonaj dopyt
			// dopyt sa podarilo vykonať
			$row = $result->fetch_assoc();
			$result->free();
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
