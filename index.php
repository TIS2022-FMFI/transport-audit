<?php
error_reporting(E_ERROR | E_WARNING | E_PARSE | E_NOTICE);
session_start();
include('db.php');
include('funkcie.php');
require('fpdf/fpdf.php');
$pdf = new FPDF();

if( isset($_SESSION['prihlasovacie_meno'])&& vrat_uzivatela_web($db,$_SESSION['prihlasovacie_meno'])[4]==999 ){
		echo "Účet expirovaný";
		session_unset();
		session_destroy();
}
?>



 
<?php
if(isset($_GET['strana'])) {
    $aktualna_strana = $_GET['strana'];
}
else {
	$aktualna_strana = 1;
}
$chyby = array();
if (isset($_POST['odhlas'])){
		vloz_log($db,101,"Odhlásenie",$_SESSION['prihlasovacie_meno']);
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
over_pouzivatela($db, $_POST["prihlasmeno"], $_POST["heslo"] )==true && vrat_uzivatela_web($db,$_POST["prihlasmeno"])[4]!=999 ){
	$pouzivatel = over_pouzivatela($db, $_POST["prihlasmeno"], $_POST["heslo"] );
	//print_r($pouzivatel);
	$_SESSION['prihlasovacie_meno'] = $pouzivatel[1] ;
	vloz_log($db,100,"Prihlásenie",$_SESSION['prihlasovacie_meno']);
}
if (isset($_SESSION['prihlasovacie_meno'])){
	//vloz_log($mysqli,$_SESSION['prihlasovacie_meno'],"Návšteva indexu ako prihlásený");
	navigacia('Exporty');
	
	
  


?>

<section>


<div class="row">
    <div class="col-4 d-flex">
        <?php vypis_audit($db2,$aktualna_strana); ?>
    </div>
</div>
		
				
	<?php posuvanie_strany($db2,$aktualna_strana); ?>			

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