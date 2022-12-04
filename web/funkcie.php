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

function vypis_audit($db){
	if ($db) {
		$result = pg_query($db, 'SELECT * FROM "Stillage" ORDER BY "last_sync" DESC');
		if (!$result) {
			echo "An error occurred.\n";
			exit;
		}

		$array = pg_fetch_all($result);
			echo "<table><tr><th>ID</th><th>Naposledy upravené</th><th>Export</th></tr>";
			$number = 1;
			foreach($array as $item) {
			echo"<tr>";
			echo "<td>{$item['id']}</td>";
			echo "<td>{$item['last_sync']}</td>";
			echo"<td><button type='button' style='border: none;background-color: #ffffff;' data-bs-toggle='modal' data-bs-target='#modal{$item['id']}'>Export</button></td>";
			
			echo'<div class="modal fade" id="modal' . $item['id'] . '" tabindex="-1" role="dialog" aria-labelledby="vockoLabel" aria-hidden="true" data-bs-backdrop="static" data-bs-keyboard="false"><div class="modal-dialog" role="document"><div class="modal-content"><div class="modal-header"><h5 class="modal-title" id="fcLabel">' . $item['id'] . '</h5><button type="button" class="close" data-bs-dismiss="modal" aria-label="Close"><span aria-hidden="true">&times;</span></button></div><div class="modal-body">';
			
			        //Obsah v okne
		echo '				
					<form target="_blank" action="export.php" method="POST">

			<input type="checkbox" id="time_start" name="time_start" value="' . $item['Date_time_start'] . '">
			<label for="time_start"> time_start</label><br>

			<input type="checkbox" id="time_end" name="time_end" value="time_end">
			<label for="time_end"> time_end</label><br>

			<input type="checkbox" id="Stillage_number" name="Stillage_number" value="Stillage_number">
			<label for="Stillage_number"> Stillage_number</label><br>

			<input type="checkbox" id="Stillage_number_on_Header" name="Stillage_number_on_Header" value="Stillage_number_on_Header">
			<label for="Stillage_number_on_Header"> Stillage_number_on_Header</label><br>

			<input type="checkbox" id="First_scan_product" name="First_scan_product" value="First_scan_product">
			<label for="First_scan_product"> First_scan_product</label><br>

			<input type="checkbox" id="Last_scan_product" name="Last_scan_product" value="Last_scan_product">
			<label for="Last_scan_product"> Last_scan_product</label><br>

			<input type="checkbox" id="JLR_Header_NO" name="JLR_Header_NO" value="JLR_Header_NO">
			<label for="JLR_Header_NO"> JLR_Header_NO</label><br>

			<input type="checkbox" id="Carriage" name="Carriage" value="Carriage">
			<label for="Carriage"> Carriage</label><br>

			<input type="checkbox" id="Check" name="Check" value="Check">
			<label for="Check"> Check</label><br>

			<input type="checkbox" id="First_scan_TLS" name="First_scan_TLS" value="First_scan_TLS">
			<label for="First_scan_TLS"> First_scan_TLS</label><br>

			<input type="checkbox" id="Last_scan_TLS" name="Last_scan_TLS" value="Last_scan_TLS">
			<label for="First_scan_TLS"> Last_scan_TLS</label><br>

			<input type="checkbox" id="TLS_Range_start" name="TLS_Range_start" value="TLS_Range_start">
			<label for="TLS_Range_start"> TLS_Range_start</label><br>

			<input type="checkbox" id="TLS_Range_stop" name="TLS_Range_stop" value="TLS_Range_stop">
			<label for="TLS_Range_stop"> TLS_Range_stop</label><br>

			<input type="checkbox" id="Note" name="Note" value="Note">
			<label for="Note"> Note</label><br>

			<br><br>
				<input type="submit" value="Submit" />
			</form>
		
		';

		
		
		
      echo '</div><div class="modal-footer"><button type="button" class="btn-primary"data-bs-dismiss="modal">Zavrieť</button></div></div></div></div>';	
			
			
			
			
			
			
			
			
			
			
			
			
			
			
			echo"</tr>";
			$number++;
			}
			echo "</table>";
	
	} else {
	return false;
}
}
?>
