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

function pocet_zaznamov_stillage($db){
	
		$result = pg_query($db, 'SELECT * FROM "Stillage" ORDER BY "last_sync" DESC');
		$array = pg_fetch_all($result);
		$number = pg_num_rows($result);
		return $number;
}


function posuvanie_strany($db,$aktualna_strana){
		$number = pocet_zaznamov_stillage($db);
		$strana = 1;
		echo '<nav aria-label="Page navigation example"><ul class="pagination">';
		if($aktualna_strana >1){
		echo  '<li class="page-item"><a class="page-link" href="?strana=' . $aktualna_strana-1 . '">Previous</a></li>';
		}
		for ($k = 0 ; $k < ceil($number / 20); $k++){ 
				if($aktualna_strana == $strana){
		echo  '<li class="page-item active"><a class="page-link" href="?strana=' . $strana . '">' . $strana . '</a></li>';
		}
		else {
		echo '<li class="page-item"><a class="page-link" href="?strana=' . $strana . '">' . $strana . '</a></li>'; 
		}
		$strana++;
		}
		echo '<li class="page-item"><a class="page-link" href="?strana=' . $aktualna_strana+1 . '">Next</a></li></ul></nav>';
}



function vypis_audit($db,$aktualna_strana){
	$ofset = $aktualna_strana -1;
	$ofset = $ofset * 20;
	$limiter = 20;
	if ($db) {
		$result = pg_query($db, 'SELECT * FROM "Stillage" ORDER BY "last_sync" DESC LIMIT ' . $limiter . ' OFFSET ' . $ofset . '');
		if (!$result) {
			echo "An error occurred.\n";
			exit;
		}

		$array = pg_fetch_all($result);
			echo "<table class='table'><tr><th scope='col'>Meno</th><th scope='col'>Číslo užívateľa</th><th scope='col'>Naposledy upravené</th><th scope='col'>Export</th></tr>";
			$number = pocet_zaznamov_stillage($db);
			foreach($array as $item) {
			//Ziskanie SPZ
			$ajdi_SPZ = "'".$item['id']."'";
			$query_SPZ = 'SELECT
				"Vehicle"."SPZ"
				FROM "Stillage"
				JOIN "Shipment"
				  ON "Shipment_id" = "Shipment".id
				JOIN "Vehicle"
				  ON "Vehicle_id" = "Vehicle".id WHERE "Stillage".id = ' . $ajdi_SPZ . ' ';
				$result_SPZ = pg_query($db,$query_SPZ) or die('Error message: ' . pg_last_error());
				$row_SPZ = pg_fetch_row($result_SPZ);
			//Ziskanie Customera
			$ajdi_customer = "'".$item['id']."'";
			$query_customer = 'SELECT
				"Customer"."Name"
				FROM "Stillage"
				JOIN "Shipment"
				  ON "Shipment_id" = "Shipment".id
				JOIN "Customer"
				  ON "Customer_id" = "Customer".id WHERE "Stillage".id = ' . $ajdi_customer . ' ';
				$result_customer = pg_query($db,$query_customer) or die('Error message: ' . pg_last_error());
				$row_customer = pg_fetch_row($result_customer);
			//Ziskanie Usera
			$ajdi_user = "'".$item['id']."'";
			$query_user = 'SELECT
				"User"."code",
				"User"."Name",
				"User"."Last_name"
				FROM "Stillage"
				JOIN "Shipment"
				  ON "Shipment_id" = "Shipment".id
				JOIN "User"
				  ON "User_code" = "User".code WHERE "Stillage".id = ' . $ajdi_user . ' ';
				$result_user = pg_query($db,$query_user) or die('Error message: ' . pg_last_error());
				$row_user = pg_fetch_row($result_user);
			//Ziskanie Stillage_type_Name
			$ajdi_stillage_type = "'".$item['id']."'";
			$query_stillage_type = 'SELECT
				"Stillage_type"."Name"
				FROM "Stillage"
				JOIN "Stillage_type"
				  ON "Stillage_Type_id" = "Stillage_type".id WHERE "Stillage".id = ' . $ajdi_stillage_type . ' ';
				$result_stillage_type = pg_query($db,$query_stillage_type) or die('Error message: ' . pg_last_error());
				$row_stillage_type = pg_fetch_row($result_stillage_type);
			echo"<tr>";
			echo '<td>' . $row_user[1] . ' ' . $row_user[2] . '</td>';
			echo "<td>{$row_user[0]}</td>";
			echo "<td>{$item['last_sync']}</td>";
			echo"<td><button type='button' style='border: none;background-color: #ffffff;' data-bs-toggle='modal' data-bs-target='#modal{$item['id']}'>Export</button></td>";
			
			echo'<div class="modal fade" id="modal' . $item['id'] . '" tabindex="-1" role="dialog" aria-labelledby="vockoLabel" aria-hidden="true" data-bs-backdrop="static" data-bs-keyboard="false"><div class="modal-dialog" role="document"><div class="modal-content"><div class="modal-header"><h5 class="modal-title" id="fcLabel">' . $item['id'] . '</h5><button type="button" class="close" data-bs-dismiss="modal" aria-label="Close"><span aria-hidden="true">&times;</span></button></div><div class="modal-body">';
			
			        //Obsah v okne
		echo '				
					<form target="_blank" action="export.php" method="POST">

			<input type="checkbox" id="shipment_ajdi" name="shipment_ajdi" value="Shipment ID: ' . $number . '">
			<label for="shipment_ajdi">Shipment ID</label><br>
			

			<input type="checkbox" id="Plate_NO" name="Plate_NO" value="Plate_NO: ' . $row_SPZ[0] . '">
			<label for="Plate_NO">Plate_NO</label><br>
			
			<input type="checkbox" id="Customer" name="Customer" value="Customer: ' . $row_customer[0] . '">
			<label for="Customer">Customer</label><br>
			
			<input type="checkbox" id="User" name="User" value="User: ' . $row_user[1] . ' ' . $row_user[2] . ' ( ' . $row_user[0] . ' )">
			<label for="User">User</label><br>

			<input type="checkbox" id="time_start" name="time_start" value="Date Time start: ' . $item['Date_time_start'] . '">
			<label for="time_start"> time_start</label><br>

			<input type="checkbox" id="time_end" name="time_end" value="Date Time end: ' . $item['Date_time_end'] . '">
			<label for="time_end"> time_end</label><br>
			
						<input type="checkbox" id="time_close" name="time_close" value="Date Time Close: DOIMPLEMENTOVAŤ!(zatial by mohol byť last_sync)">
			<label for="time_close"> time_close</label><br>
			
			
			<input type="checkbox" id="Type" name="Type" value="Type: ' . $row_stillage_type[0] . '">
			<label for="Type">Type</label><br>
			


			<input type="checkbox" id="Stillage_number" name="Stillage_number" value="Stillage No: ' . $item['Stillage_number'] . '">
			<label for="Stillage_number"> Stillage_number</label><br>

			<input type="checkbox" id="Stillage_Number_on_Header" name="Stillage_Number_on_Header" value="Stillage_header: ' . $item['Stillage_Number_on_Header'] . '">
			<label for="Stillage_Number_on_Header"> Stillage_Number_on_Header</label><br>

			<input type="checkbox" id="First_scan_product" name="First_scan_product" value="First-Product: ' . $item['First_scan_product'] . '">
			<label for="First_scan_product"> First_scan_product</label><br>

			<input type="checkbox" id="Last_scan_product" name="Last_scan_product" value="Last-Product' . $item['Last_scan_product'] . '">
			<label for="Last_scan_product"> Last_scan_product</label><br>

			<input type="checkbox" id="JLR_Header_NO" name="JLR_Header_NO" value="JLR... : ' . $item['JLR_Header_NO'] . '">
			<label for="JLR_Header_NO"> JLR_Header_NO</label><br>

			<input type="checkbox" id="Carriage" name="Carriage" value="Carriage ... : ' . $item['Carriage_L_JLR_H'] . '">
			<label for="Carriage"> Carriage</label><br>

			<input type="checkbox" id="Check" name="Check" value="Check: ' . $item['_Check'] . '">
			<label for="Check"> Check</label><br>

			<input type="checkbox" id="First_scan_TLS" name="First_scan_TLS" value="TLS: ' . $item['First_scan_TLS_code'] . '">
			<label for="First_scan_TLS"> First_scan_TLS</label><br>

			<input type="checkbox" id="Last_scan_TLS" name="Last_scan_TLS" value="TLS_stop: ' . $item['Last_scan_TLS_code'] . '">
			<label for="First_scan_TLS"> Last_scan_TLS</label><br>

			<input type="checkbox" id="TLS_Range_start" name="TLS_Range_start" value="TLS_Range_start: ' . $item['TLS_range_start'] . '">
			<label for="TLS_Range_start"> TLS_Range_start</label><br>

			<input type="checkbox" id="TLS_Range_stop" name="TLS_Range_stop" value="TLS_range_stop: ' . $item['TLS_range_stop'] . '">
			<label for="TLS_Range_stop"> TLS_Range_stop</label><br>

			<input type="checkbox" id="Note" name="Note" value="Poznámka: ' . $item['Note'] . '">
			<label for="Note"> Note</label><br>

			<br><br>
				<input type="submit" value="Generuj" />
			</form>
		
		';

		
		
		
      echo '</div><div class="modal-footer"><button type="button" class="btn-primary"data-bs-dismiss="modal">Zavrieť</button></div></div></div></div>';	
			
			
			
			
			
			
			
			
			
			
			
			
			
			
			echo"</tr>";
			$number--;
			}
			echo "</table>";
	
	} else {
	return false;
}
}
?>
