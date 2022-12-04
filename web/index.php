<?php
session_start();
include('db.php');
include('funkcie.php');
require('fpdf/fpdf.php');
$pdf = new FPDF();
?>
<!doctype html>
<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/js/bootstrap.bundle.min.js" integrity="sha384-MrcW6ZMFYlzcLA8Nl+NtUVF0sA7MsXsP1UyJoMp4YLEuNSfAP+JcXn/tWtIaxVXM" crossorigin="anonymous"></script>
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-EVSTQN3/azprG1Anm3QDgpJLIm9Nao0Yz1ztcQTwFspd3yD65VohhpuuCOmLASjC" crossorigin="anonymous"> 
<section>


 
<?php
$chyby = array();
if (isset($_POST['odhlas'])){
	//vloz_log($mysqli,$_SESSION['prihlasovacie_meno'],"odhlasenie");
	session_unset();
	session_destroy();
}

if (isset($_POST[ "prihlasmeno"] ) && isset($_POST["heslo"] ) &&
over_pouzivatela($db, $_POST["prihlasmeno"], $_POST["heslo"] )==false ){
	//vloz_log($mysqli,$_POST[ "prihlasmeno"],"Kombinácia mena a hesla je nesprávna");
 echo "Kombinácia mena a hesla je nesprávna";
}



if (isset($_POST[ "prihlasmeno"] ) && isset($_POST["heslo"] ) &&
over_pouzivatela($db, $_POST["prihlasmeno"], $_POST["heslo"] )==true ){
	$pouzivatel = over_pouzivatela($db, $_POST["prihlasmeno"], $_POST["heslo"] );
	//print_r($pouzivatel);
	$_SESSION['prihlasovacie_meno'] = $pouzivatel[1] ;
	//vloz_log($mysqli,$_SESSION['prihlasovacie_meno'],"prihlasenie");
}
if (isset($_SESSION['prihlasovacie_meno'])){
	//vloz_log($mysqli,$_SESSION['prihlasovacie_meno'],"Návšteva indexu ako prihlásený");
	
	
  


?>
<div class="container tekst">
<section>
				<button>
				<form id="myform" method="post"><input type="hidden" id="odhlas" name="odhlas" value="odhlas"></form>
				<a class="nav-link" onclick="document.getElementById('myform').submit();">Odhlásiť sa</a>
			
                </button>
				<?php vypis_audit($db2); ?>
				
				
</div>
<?php

    }
  
	



else{

?>

<div class="container prihlas">
	<form method="post">
		<p>
		<span class="txt1">Prihlasovacie meno</span>
		<div class="wrap-input100 validate-input" data-validate="Username is required">		
		<input class="input100" name="prihlasmeno" type="text" size="30" maxlength="50" id="prihlasmeno" value="<?php if (isset($_POST["prihlasmeno"])) echo $_POST["prihlasmeno"]; ?>" >
		<span class="focus-input100"></span><br>
		</div>
		<span class="txt1">Heslo</span>
				<div class="wrap-input100 validate-input" data-validate="Username is required">		
		<input class="input100" name="heslo" type="password" size="30" maxlength="50" id="heslo"> 
		<span class="focus-input100"></span><br>
		</div>
		
		</p>
		<p>
			<input class="login100-form-btn" name="submit" type="submit" id="submit" value="Prihlásiť">
		</p>
			
	</form>
	<br>
</section>
</div>
<?php
}
?>
<?php
//include('pata.php'); do buducna
?>
