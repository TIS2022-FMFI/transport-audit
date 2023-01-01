<?php
date_default_timezone_set('Europe/Bratislava');
//error_reporting(E_ALL ^ E_NOTICE);  
error_reporting(0);
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

function navigacia($stranka,$db = NULL,$admin = 0){
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
		
		        <li class="nav-item dropdown">
          <a class="nav-link dropdown-toggle" href="#" role="button" data-bs-toggle="dropdown" aria-expanded="false">
            Logy
          </a>
          <ul class="dropdown-menu">
            <li><a class="dropdown-item" href="logy-web.php">Web</a></li>
            <li><hr class="dropdown-divider"></li>
			<li><a class="dropdown-item" href="logy-android.php">Android</a></li>
          </ul>
        </li>
		
      </ul>
				'.($stranka == "Užívatelia" && $admin !=0 ? '
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
				
								'.($stranka == "Užívatelia-web" ? '
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
						  <form action="users-web.php" method="post">
			<label>Meno: </label>
			<input type="text" name="meno" value="">
			<br>
			<label>Používateľské meno: </label>
			<input type="text" name="username" value="">
				<br>
				<label>Nové heslo: </label>
				<input type="text" name="heslo">
				<br>
				<label for="cars">Rola: </label>
				<select name="rola">
				  <option value="0">Operátor</option>
				  <option value="1">Administrátor</option>
				</select>
				<br>

			<input type="hidden"  name="ano" value="" />

						
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
				
				<form id="myform" method="post"><input type="hidden" id="odhlas" name="odhlas" value="odhlas">
				<button type="submit" class="btn btn-outline-success">Odhlásiť</button>
				</form>
			
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


function pridaj_uzivatela_web($db,$Name,$username,$User_Role,$passwd){

		//pg_get_result($db);
			  $data = array('real_name'=>$Name, 'username'=>$username, 'admin'=>$User_Role,'password'=>hash('sha256', $passwd));
			  $res = pg_insert($db, 'users', $data);
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

function update_uzivatela_web($db,$Name,$username,$User_Role,$id,$passwd){

		//pg_get_result($db);
		$date = date('Y-m-d H:i:s');
				if(strlen($passwd) > 0){		
			  $data = array('real_name'=>$Name, 'username'=>$username, 'admin'=>$User_Role,'password'=>hash('sha256', $passwd));
				}
				else{
					$data = array('real_name'=>$Name, 'username'=>$username, 'admin'=>$User_Role);
				}
			  $condition = array('id' => $id);
			  $res = pg_update($db, 'users', $data, $condition);
			  if ($res) {
				  //echo "Data is updated: $res\n";
				  return True;
			  } else {
				  return False;
			  }
}

function delete_uzivatela_web($db,$id){

		//pg_get_result($db);
		$deleted_value = 999; //Užívateľ s touto hodnotou sa považuje za zmazaného
			$data = array('admin'=>$deleted_value);
			  $condition = array('id' => $id);
			  $res = pg_update($db, 'users', $data, $condition);
			  if ($res) {
				  //echo "Data is updated: $res\n";
				  return True;
			  } else {
				  return False;
			  }
}

function vrat_uzivatela_web($db,$meno){
		if ($db) {
		$meno_str = "'".$meno."'";
		$result = pg_query($db, 'SELECT * FROM "users" where username=' . $meno_str . '');
		if (!$result) {
			echo "An error occurred.\n";
			exit;
		}

		return pg_fetch_row($result);
		}
}

function vypis_uzivatelov($db,$admin=0){
	if ($db) {
		$deleted_string = "'"."DELETED"."'";
		$result = pg_query($db, 'SELECT * FROM "User" WHERE doplnok is null or doplnok != ' . $deleted_string . ' ORDER BY "last_sync" DESC');
		if (!$result) {
			echo "An error occurred.\n";
			exit;
		}

		$array = pg_fetch_all($result);
			if($admin==1){
			echo "<table class='table'><tr><th scope='col'>Meno</th><th scope='col'>Rola</th><th scope='col'>Číslo užívateľa</th><th scope='col'>Naposledy upravené</th><th scope='col'>Upraviť</th><th scope='col'>QR kód</th></tr>";
			}
			else{
			echo "<table class='table'><tr><th scope='col'>Meno</th><th scope='col'>Rola</th><th scope='col'>Číslo užívateľa</th><th scope='col'>Naposledy upravené</th><th scope='col'>QR kód</th></tr>";
			}
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
			if($admin==1){
			echo"<td><button type='button' style='border: none;background-color: #ffffff;' data-bs-toggle='modal' data-bs-target='#modal{$item['code']}'>Uprav</button></td>";
			}
			echo"<td><button type='button' style='border: none;background-color: #ffffff;' data-bs-toggle='modal' data-bs-target='#modal{$item['code']}qr'>Zobraziť</button></td>";
			
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
			
			
			//qr code modal
					echo'<div class="modal fade" id="modal' . $item['code'] . 'qr" tabindex="-1" role="dialog" aria-labelledby="vockoLabel" aria-hidden="true" data-bs-backdrop="static" data-bs-keyboard="false"><div class="modal-dialog" role="document"><div class="modal-content"><div class="modal-header"><h5 class="modal-title" id="fcLabel">' . $item['Name']." ".$item['Last_name'] . '</h5><button type="button" class="close" data-bs-dismiss="modal" aria-label="Close"><span aria-hidden="true">&times;</span></button></div><div class="modal-body">';
			
			        //Obsah v okne
		echo '				
		<img src="qrcode.php?s=qr&d=' . $item['code'] . '&w=400&h=300">
		';

		
		
		
      echo '</div><div class="modal-footer"><button type="button" class="btn-primary"data-bs-dismiss="modal">Zavrieť</button></div></div></div></div>';
			
			
			
			
			
			
			
			
			
			
			
			
			
			echo"</tr>";
			}
			echo "</table>";
	
	} else {
	return false;
}
	
}

function vypis_uzivatelov_web($db){
	if ($db) {
		$result = pg_query($db, 'SELECT * FROM "users" where admin != 999');
		if (!$result) {
			echo "An error occurred.\n";
			exit;
		}

		$array = pg_fetch_all($result);
			echo "<table class='table'><tr><th scope='col'>Meno</th><th scope='col'>Prihlasovacie meno</th><th scope='col'>Admin</th><th scope='col'>Upraviť</th><th scope='col'>Zmazať</th></tr>";
			foreach($array as $item) {
				//získaj rolu
			
			
			echo"<tr>";
			echo '<td>' . $item['real_name'] . '</td>';
			echo "<td>{$item['username']}</td>";
			echo "<td>{$item['admin']}</td>";
			echo"<td><button type='button' style='border: none;background-color: #ffffff;' data-bs-toggle='modal' data-bs-target='#modal{$item['id']}'>Uprav</button></td>";
			echo"<td><button type='button' style='border: none;background-color: #ffffff;' data-bs-toggle='modal' data-bs-target='#modal{$item['id']}delete'>Zmaž</button></td>";
			
			echo'<div class="modal fade" id="modal' . $item['id'] . '" tabindex="-1" role="dialog" aria-labelledby="vockoLabel" aria-hidden="true" data-bs-backdrop="static" data-bs-keyboard="false"><div class="modal-dialog" role="document"><div class="modal-content"><div class="modal-header"><h5 class="modal-title" id="fcLabel">' . $item['real_name'] . '</h5><button type="button" class="close" data-bs-dismiss="modal" aria-label="Close"><span aria-hidden="true">&times;</span></button></div><div class="modal-body">';
			
			        //Obsah v okne
		echo '				
					<form action="" method="POST">
			<label>Meno: </label>
			<input type="text" name="meno" value="' . $item['real_name'] . '">
			<br>
			<label>Používateľské meno: </label>
			<input type="text" name="username" value="' . $item['username'] . '">
				<br>
				<label>Nové heslo: </label>
				<input type="text" name="heslo">
				<br>
				<label for="cars">Rola: </label>
				<select name="rola">
				  <option value="0" '.(($item['admin']=='0')?'selected="selected"':"").'>Operátor</option>
				  <option value="1" '.(($item['admin']=='1')?'selected="selected"':"").'>Administrátor</option>
				</select>
				<br>

			<input type="hidden"  name="id" value="' . $item['id'] . '" />
			<br><br>
				<input type="submit" value="Upraviť" />
			</form>
		';

		
		
		
      echo '</div><div class="modal-footer"><button type="button" class="btn-primary"data-bs-dismiss="modal">Zavrieť</button></div></div></div></div>';	
			
			
			//Modal delete
						echo'<div class="modal fade" id="modal' . $item['id'] . 'delete" tabindex="-1" role="dialog" aria-labelledby="vockoLabel" aria-hidden="true" data-bs-backdrop="static" data-bs-keyboard="false"><div class="modal-dialog" role="document"><div class="modal-content"><div class="modal-header"><h5 class="modal-title" id="fcLabel">' . $item['real_name'] . '</h5><button type="button" class="close" data-bs-dismiss="modal" aria-label="Close"><span aria-hidden="true">&times;</span></button></div><div class="modal-body">';
			
			        //Obsah v okne
		echo '				
					<form action="" method="POST">
				<h2>Naozaj chceš zmazať užívateľa ' . $item['real_name'] . ' ?</h2>

			<input type="hidden"  name="delete23" value="' . $item['id'] . '" />
			<input type="hidden"  name="meno32" value="' . $item['real_name'] . '" />
			<br><br>
				<input type="submit" value="Odstrániť" />
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
	
		$result = pg_query($db, 'SELECT * FROM "Shipment" ORDER BY "last_sync" DESC');
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
		$result = pg_query($db, 'SELECT * FROM "Shipment" ORDER BY "last_sync" DESC LIMIT ' . $limiter . ' OFFSET ' . $ofset . '');
		if (!$result) {
			echo "An error occurred.\n";
			exit;
		}

		$array = pg_fetch_all($result);
			echo "<table class='table'><tr><th scope='col'>Meno</th><th scope='col'>Číslo užívateľa</th><th scope='col'>Naposledy upravené</th><th scope='col'>Export</th></tr>";
			$number = pocet_zaznamov_stillage($db);
			foreach($array as $item) {
				$id_string = "'".$item['id']."'";
			//Ziskanie SPZ
						$query_spz = 'SELECT
				"Vehicle"."SPZ"
				FROM "Shipment"
				JOIN "Vehicle"
				  ON "Vehicle_id" = "Vehicle".id WHERE "Shipment".id = ' . $id_string . ' ';
				$result_spz = pg_query($db,$query_spz) or die('Error message: ' . pg_last_error());
				$row_spz = pg_fetch_row($result_spz);


			//Ziskanie Usera
			
			$query_user = 'SELECT
				"User"."code",
				"User"."Name",
				"User"."Last_name"
				FROM "Shipment"
				JOIN "User"
				  ON "User_code" = "User".code WHERE "Shipment".id = ' . $id_string . ' ';
				$result_user = pg_query($db,$query_user) or die('Error message: ' . pg_last_error());
				$row_user = pg_fetch_row($result_user);
				
						//Ziskanie Customera
				$query_customer = 'SELECT
				"Customer"."Name"
				FROM "Shipment"
				JOIN "Customer"
				  ON "Customer_id" = "Customer".id WHERE "Shipment".id = ' . $id_string . ' ';
				$result_customer = pg_query($db,$query_customer) or die('Error message: ' . pg_last_error());
				$row_customer = pg_fetch_row($result_customer);


			echo"<tr>";
			echo '<td>' . $row_user[1] . ' ' . $row_user[2] . '</td>';
			echo "<td>{$row_user[0]}</td>";
			echo "<td>{$item['last_sync']}</td>";
			echo"<td><button type='button' style='border: none;background-color: #ffffff;' data-bs-toggle='modal' data-bs-target='#modal{$item['id']}'>Export</button></td>";
			
			echo'<div class="modal fade" id="modal' . $item['id'] . '" tabindex="-1" role="dialog" aria-labelledby="vockoLabel" aria-hidden="true" data-bs-backdrop="static" data-bs-keyboard="false"><div class="modal-dialog" role="document"><div class="modal-content"><div class="modal-header"><h5 class="modal-title" id="fcLabel">' . $item['id'] . '</h5><button type="button" class="close" data-bs-dismiss="modal" aria-label="Close"><span aria-hidden="true">&times;</span></button></div><div class="modal-body">';
			
			        //Obsah v okne
		echo '				
					<form target="_blank" action="export.php" method="POST" >';
					
						echo "<script type='text/javascript'>
	$('#select-all').click(function(event) {   
    if(this.checked) {
        // Iterate each checkbox
        $(':checkbox').each(function() {
            this.checked = true;                        
        });
    } else {
        $(':checkbox').each(function() {
            this.checked = false;                       
        });
    }
}); 
	</script><input type='checkbox' name='select-all' id='select-all' /><label for='select-all'>Označiť / odznačiť všetko</label><br><br>";
		echo'
			
			<input type="checkbox" id="shipment_ajdi" name="shipment_ajdi" value="' . $number . '">
			<label for="shipment_ajdi">Shipment ID</label><br>
			

			<input type="checkbox" id="Plate_NO" name="Plate_NO" value="' . $row_spz[0] . '">
			<label for="Plate number">Plate_NO</label><br>
			
			<input type="checkbox" id="Customer" name="Customer" value="' . $row_customer[0] . '">
			<label for="Customer">Customer</label><br>
			
			<input type="checkbox" id="User" name="User" value="' . $row_user[1] . ' ' . $row_user[2] . ' ( ' . $row_user[0] . ' )">
			<label for="User">User</label><br>
			
						<input type="checkbox" id="time_close_s" name="time_close_s" value="' . $item['Date_time_close'] . '">
			<label for="time_close_s">Time close</label><br>

			<input type="checkbox" id="time_start" name="time_start" value="1">
			<label for="time_start">(Stillage)Time start</label><br>

			<input type="checkbox" id="time_end" name="time_end" value="1">
			<label for="time_end">(Stillage)Time end</label><br>
			
			
			<input type="checkbox" id="Type" name="Type" value="1">
			<label for="Type">(Stillage)Type</label><br>
			


			<input type="checkbox" id="Stillage_number" name="Stillage_number" value="1">
			<label for="Stillage_number">(Stillage)Stillage number</label><br>

			<input type="checkbox" id="Stillage_Number_on_Header" name="Stillage_Number_on_Header" value="1">
			<label for="Stillage_Number_on_Header">(Stillage)Stillage number on header</label><br>

			<input type="checkbox" id="First_scan_product" name="First_scan_product" value="1">
			<label for="First_scan_product">(Stillage)First scan product</label><br>

			<input type="checkbox" id="Last_scan_product" name="Last_scan_product" value="1">
			<label for="Last_scan_product">(Stillage)Last scan product</label><br>

			<input type="checkbox" id="JLR_Header_NO" name="JLR_Header_NO" value="1">
			<label for="JLR_Header_NO">(Stillage)JLR Header NO</label><br>

			<input type="checkbox" id="Carriage" name="Carriage" value="1">
			<label for="Carriage">(Stillage)Carriage</label><br>

			<input type="checkbox" id="Check" name="Check" value="1">
			<label for="Check">(Stillage)Check</label><br>

			<input type="checkbox" id="First_scan_TLS" name="First_scan_TLS" value="1">
			<label for="First_scan_TLS">(Stillage)First scan TLS</label><br>

			<input type="checkbox" id="Last_scan_TLS" name="Last_scan_TLS" value="1">
			<label for="First_scan_TLS">(Stillage)Last scan TLS</label><br>

			<input type="checkbox" id="TLS_Range_start" name="TLS_Range_start" value="1">
			<label for="TLS_Range_start">(Stillage)TLS Range start</label><br>

			<input type="checkbox" id="TLS_Range_stop" name="TLS_Range_stop" value="1">
			<label for="TLS_Range_stop">(Stillage)TLS range stop</label><br>

			<input type="checkbox" id="Note" name="Note" value="1">
			<label for="Note">(Stillage)Note</label><br>
			<input type="hidden" id="shipment_id_r" name="shipment_id_r" value="'.$id_string.'">
		
		';


	
		

echo '			<br><br>
				<input type="submit" value="Generuj" />
			</form>';
		
		
		
      echo '</div><div class="modal-footer"><button type="button" class="btn-primary"data-bs-dismiss="modal">Zavrieť</button></div></div></div></div>';	
			
			
			
			
			
			
			
			
			
			
			
			
			
			
			echo"</tr>";
			$number--;
			}
			echo "</table>";
	
	} else {
	return false;
}
}

//Logy-android
function pocet_zaznamov_logy($db,$android){
	
		$result = pg_query($db, 'SELECT * FROM "logy" where android = ' . $android .' ');
		$array = pg_fetch_all($result);
		$number = pg_num_rows($result);
		return $number;
}


function posuvanie_strany_logy($db,$aktualna_strana,$android){
		$number = pocet_zaznamov_logy($db,$android);
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

function vypis_logy_uzivatel_kod_chyby_option_as_str($db,$android_web,$prepinac) {
	// do premennej $row treba priradiť jednotlivé položky objednávky $id 
	if ($db) {
		$vysledok = "<option value=''>---</option>";
		$sql = 'SELECT * FROM "logy" where android=' . $android_web . ''; // definuj dopyt
		$result = pg_query($db,$sql);
		$array = pg_fetch_all($result);
		$duplicita = array();
			foreach($array as $item) {
				if($prepinac ==1 && in_array( $item['uzivatel'] ,$duplicita )==false ){
				$vysledok.= "<option value='{$item['uzivatel']}'>{$item['uzivatel']}</option>";
				array_push($duplicita, $item['uzivatel']);
				}
				elseif($prepinac !=1 && in_array( $item['kod_chyby'] ,$duplicita )==false){
					$vysledok.= "<option value='{$item['kod_chyby']}'>{$item['kod_chyby']}</option>";
					array_push($duplicita, $item['kod_chyby']);
				}

			}
			return $vysledok;
		} else {
			// dopyt sa NEpodarilo vykonať!
			echo '<p class="chyba">NEpodarilo sa získať údaje z databázy</p>' . $mysqli->error ;
		}
	}


function vloz_log($db,$code,$message,$user){

		//pg_get_result($db);
		$date = date('Y-m-d H:i:s');
			  $data = array('kod_chyby'=>$code, 'chyba'=>$message, 'uzivatel'=>$user, 'android'=>0, 'doplnok'=>$date);
			  $res = pg_insert($db, 'logy', $data);
			  if ($res) {
				  //echo "Data is updated: $res\n";
				  return True;
			  } else {
				  return False;
			  }
}


function vypis_logy_android($db,$aktualna_strana,$uzivatel,$kod_chyby,$android){
	$ofset = $aktualna_strana -1;
	$ofset = $ofset * 20;
	$limiter = 20;
	if ($db) {
		if($uzivatel !="" && $kod_chyby!=-1){
			$uzivatel_str = "'".$uzivatel."'";
			$result = pg_query($db, 'SELECT * FROM "logy" WHERE android = ' . $android .' and uzivatel= ' . $uzivatel_str . ' and kod_chyby = ' . $kod_chyby . '  ORDER BY doplnok::timestamp DESC');
		}
		elseif($uzivatel !=""){
			$uzivatel_str = "'".$uzivatel."'";
			$result = pg_query($db, 'SELECT * FROM "logy" WHERE android = ' . $android .' and uzivatel= ' . $uzivatel_str . ' ORDER BY doplnok::timestamp DESC');
		}
		elseif($kod_chyby!=-1){
			$result = pg_query($db, 'SELECT * FROM "logy" WHERE android = ' . $android .' and kod_chyby = ' . $kod_chyby . '  ORDER BY doplnok::timestamp DESC');
		}
		else{
		$result = pg_query($db, 'SELECT * FROM "logy" WHERE android = ' . $android .' ORDER BY doplnok::timestamp DESC LIMIT ' . $limiter . ' OFFSET ' . $ofset . '');
		}
		if (!$result) {
			echo "An error occurred.\n";
			exit;
		}

		$array = pg_fetch_all($result);
			echo "<table class='table'><tr><th scope='col'>Číslo užívateľa</th><th scope='col'>Kód záznamu</th><th scope='col'>Timestamp</th><th scope='col'>Záznam</th></tr>";
			foreach($array as $item) {
				$id_string = "'".$item['id']."'";
			echo"<tr>";
			echo "<td>{$item['uzivatel']}</td>";
			echo "<td>{$item['kod_chyby']}</td>";
			echo "<td>{$item['doplnok']}</td>";
			echo"<td><button type='button' style='border: none;background-color: #ffffff;' data-bs-toggle='modal' data-bs-target='#modal{$item['id']}'>Zobraziť</button></td>";
			
			echo'<div class="modal fade" id="modal' . $item['id'] . '" tabindex="-1" role="dialog" aria-labelledby="vockoLabel" aria-hidden="true" data-bs-backdrop="static" data-bs-keyboard="false"><div class="modal-dialog" role="document"><div class="modal-content"><div class="modal-header"><h5 class="modal-title" id="fcLabel">' . $item['kod_chyby'] . '</h5><button type="button" class="close" data-bs-dismiss="modal" aria-label="Close"><span aria-hidden="true">&times;</span></button></div><div class="modal-body">';
			
			        //Obsah v okne
		echo $item['chyba'];			

      echo '</div><div class="modal-footer"><button type="button" class="btn-primary"data-bs-dismiss="modal">Zavrieť</button></div></div></div></div>';	

			
			echo"</tr>";
			}
			echo "</table>";
	
	} else {
	return false;
}
}

?>
