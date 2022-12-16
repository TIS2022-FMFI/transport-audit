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

function navigacia($stranka,$db = NULL){
	echo '<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/js/bootstrap.bundle.min.js" integrity="sha384-MrcW6ZMFYlzcLA8Nl+NtUVF0sA7MsXsP1UyJoMp4YLEuNSfAP+JcXn/tWtIaxVXM" crossorigin="anonymous"></script>
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-EVSTQN3/azprG1Anm3QDgpJLIm9Nao0Yz1ztcQTwFspd3yD65VohhpuuCOmLASjC" crossorigin="anonymous"> 
';
echo '<script src="https://code.jquery.com/jquery-3.6.0.min.js" integrity="sha256-/xUj+3OJU5yExlq6GSYGSHk7tPXikynS7ogEvDej/m4=" crossorigin="anonymous"></script>';
echo '<!doctype html>';
echo '<nav class="navbar navbar-expand-lg bg-light">
  <div class="container-fluid">
    <a class="navbar-brand" href="#">Gefco</a>
    <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
      <span class="navbar-toggler-icon"></span>
    </button>
    <div class="collapse navbar-collapse" id="navbarSupportedContent">
      <ul class="navbar-nav me-auto mb-2 mb-lg-0">
        <li class="nav-item">
          <a class="nav-link active" aria-current="page" href="index.php">Exporty</a>
        </li>

        <li class="nav-item dropdown">
          <a class="nav-link dropdown-toggle" href="#" role="button" data-bs-toggle="dropdown" aria-expanded="false">
            Užívatelia
          </a>
          <ul class="dropdown-menu">
            <li><a class="dropdown-item" href="users-web.php">Web</a></li>
            <li><hr class="dropdown-divider"></li>
			<li><a class="dropdown-item" href="users.php">Android</a></li>
          </ul>
        </li>
      </ul>
				'.($stranka == "Užívatelia" ? '
					<!-- Button trigger modal -->
					<button type="button" class="btn btn-outline-primary" data-bs-toggle="modal" data-bs-target="#exampleModal">
					  Pridať užívateľa
					</button>
					
					<!-- Modal -->
					<div class="modal fade" id="exampleModal" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true" data-bs-backdrop="static" data-bs-keyboard="false">
					  <div class="modal-dialog">
						<div class="modal-content">
						  <div class="modal-header">
							<h1 class="modal-title fs-5" id="exampleModalLabel">Pridať užívateľa</h1>
							<button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
						  </div>
						  <div class="modal-body">
						  <form action="users.php" method="post">
										<label>Meno: </label>
			<input type="text" name="meno_i">
			<br>
			<label>Priezvisko: </label>
			<input type="text" name="priezvisko_i">
				<br>
				<label>Rola: </label>
						<select name="rola_i">
						' .vypis_user_role_option_as_str($db,NULL) . '
						</select>
						
						  </div>
						  <div class="modal-footer">
							<button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
							<input type="submit" value="Send Request" />
							</form>
						  </div>
						</div>
					  </div>
					</div>
								
				': '').'
				<button class="btn btn-outline-success">
				<form id="myform" method="post"><input type="hidden" id="odhlas" name="odhlas" value="odhlas"></form>
				<a class="nav-link" onclick="document.getElementById("myform").submit();">Odhlásiť sa</a>
			
                </button>
    </div>
  </div>
</nav>';

}


function vrat_user_code_android($db){
		$sql = 'SELECT * FROM "User"'; // definuj dopyt
		$result = pg_query($db,$sql);
		$array = pg_fetch_all($result);
		$vysledok = array();
		foreach($array as $item){
			$vysledok[] = $item['code'];
		}
		return $vysledok;
}

function pridaj_uzivatela_android($db,$Name,$Last_name,$User_Role){
				  $min=10001;
				  $max=99999;
				  $kody = vrat_user_code_android($db);
				  while(true){
					  $cislo = rand($min,$max);
					  if(in_array($cislo,$kody)){

					  }
					  else{
						  //echo $cislo;
						  break;
					  }
					  
				  }
		//pg_get_result($db);
				$date = date('Y-m-d H:i:s');
			  $data = array('Name'=>$Name, 'Last_name'=>$Last_name, 'User_Role_id'=>$User_Role,'code'=>$cislo,'last_sync'=>$date);
			  $res = pg_insert($db, 'User', $data);
			  if ($res) {
				  //echo "Data is updated: $res\n";
				  return True;
			  } else {
				  return False;
			  }
}

function vypis_user_role_option($db,$id) {
	// do premennej $row treba priradiť jednotlivé položky objednávky $id 
	if ($db) {
		$sql = 'SELECT * FROM "User_Role"'; // definuj dopyt
		$result = pg_query($db,$sql);
		$array = pg_fetch_all($result);

			foreach($array as $item) {
					if($item['id'] == $id){
						echo "<option selected='selected' value='{$item['id']}'>{$item['name']}</option>";
					}
					else{
				echo "<option value='{$item['id']}'>{$item['name']}</option>";
					}

			}
		} else {
			// dopyt sa NEpodarilo vykonať!
			echo '<p class="chyba">NEpodarilo sa získať údaje z databázy</p>' . $mysqli->error ;
		}
	}


function vypis_user_role_option_as_str($db,$id) {
	// do premennej $row treba priradiť jednotlivé položky objednávky $id 
	if ($db) {
		$vysledok = "";
		$sql = 'SELECT * FROM "User_Role"'; // definuj dopyt
		$result = pg_query($db,$sql);
		$array = pg_fetch_all($result);

			foreach($array as $item) {
					if($item['id'] == $id){
						$vysledok.= "<option selected='selected' value='{$item['id']}'>{$item['name']}</option>";
					}
					else{
				$vysledok.= "<option value='{$item['id']}'>{$item['name']}</option>";
					}

			}
			return $vysledok;
		} else {
			// dopyt sa NEpodarilo vykonať!
			echo '<p class="chyba">NEpodarilo sa získať údaje z databázy</p>' . $mysqli->error ;
		}
	}





function update_uzivatela_android($db,$Name,$Last_name,$User_Role,$id,$doplnok){

		//pg_get_result($db);
		$date = date('Y-m-d H:i:s');
			  $data = array('Name'=>$Name, 'Last_name'=>$Last_name, 'User_Role_id'=>$User_Role,'doplnok'=>$doplnok,'last_sync'=>$date);
			  $condition = array('code' => $id);
			  $res = pg_update($db, 'User', $data, $condition);
			  if ($res) {
				  //echo "Data is updated: $res\n";
				  return True;
			  } else {
				  return False;
			  }
}

function vypis_uzivatelov($db){
	if ($db) {
		$result = pg_query($db, 'SELECT * FROM "User" ORDER BY "last_sync" DESC');
		if (!$result) {
			echo "An error occurred.\n";
			exit;
		}

		$array = pg_fetch_all($result);
			echo "<table class='table'><tr><th scope='col'>Meno</th><th scope='col'>Rola</th><th scope='col'>Číslo užívateľa</th><th scope='col'>Naposledy upravené</th><th scope='col'>Upraviť</th></tr>";
			foreach($array as $item) {
				//získaj rolu
			$code_string = "'".$item['code']."'";
			$query_user_role = 'SELECT
				"User_Role"."name"
				FROM "User"
				JOIN "User_Role"
				  ON "User_Role_id" = "User_Role".id WHERE "User".code = ' . $code_string . ' ';
				$result_user_role = pg_query($db,$query_user_role) or die('Error message: ' . pg_last_error());
				$row_user_role = pg_fetch_row($result_user_role);
			
			echo"<tr>";
			echo '<td>' . $item['Name'] . ' ' . $item['Last_name'] . '</td>';
			echo "<td>{$row_user_role[0]}</td>";
			echo "<td>{$item['code']}</td>";
			echo "<td>{$item['last_sync']}</td>";
			echo"<td><button type='button' style='border: none;background-color: #ffffff;' data-bs-toggle='modal' data-bs-target='#modal{$item['code']}'>Uprav</button></td>";
			
			echo'<div class="modal fade" id="modal' . $item['code'] . '" tabindex="-1" role="dialog" aria-labelledby="vockoLabel" aria-hidden="true" data-bs-backdrop="static" data-bs-keyboard="false"><div class="modal-dialog" role="document"><div class="modal-content"><div class="modal-header"><h5 class="modal-title" id="fcLabel">' . $item['code'] . '</h5><button type="button" class="close" data-bs-dismiss="modal" aria-label="Close"><span aria-hidden="true">&times;</span></button></div><div class="modal-body">';
			
			        //Obsah v okne
		echo '				
					<form action="" method="POST">
			<label>Meno: </label>
			<input type="text" name="meno" value="' . $item['Name'] . '">
			<br>
			<label>Priezvisko: </label>
			<input type="text" name="priezvisko" value="' . $item['Last_name'] . '">
				<br>
						<select name="rola">
						' ;
						vypis_user_role_option($db,$item['User_Role_id']);
		echo '
			</select>
			<br>
			<input type="hidden"  name="doplnok" value="' . $item['doplnok'] . '" />
			<input type="hidden"  name="code" value="' . $item['code'] . '" />
			<br><br>
				<input type="submit" value="Upraviť" />
			</form>
		';

		
		
		
      echo '</div><div class="modal-footer"><button type="button" class="btn-primary"data-bs-dismiss="modal">Zavrieť</button></div></div></div></div>';	
			
			
			
			
			
			
			
			
			
			
			
			
			
			
			echo"</tr>";
			}
			echo "</table>";
	
	} else {
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
		if($aktualna_strana <ceil($number / 20)){
		echo '<li class="page-item"><a class="page-link" href="?strana=' . $aktualna_strana+1 . '">Next</a></li></ul></nav>';
		}
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
