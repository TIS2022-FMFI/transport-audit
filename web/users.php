<?php
error_reporting(E_ERROR | E_WARNING | E_PARSE | E_NOTICE);
session_start();
include('db.php');
include('funkcie.php');
require('fpdf/fpdf.php');
$pdf = new FPDF();
if(isset($_SESSION['prihlasovacie_meno'])==false){
	    echo "<script> location.href='index.php'; </script>";
        exit;
}
if( isset($_SESSION['prihlasovacie_meno'])&& vrat_uzivatela_web($db,$_SESSION['prihlasovacie_meno'])[4]==999 ){
		echo "Účet expirovaný";
		session_unset();
		session_destroy();
}
if( isset($_SESSION['prihlasovacie_meno'])&& vrat_uzivatela_web($db,$_SESSION['prihlasovacie_meno'])[4]==1 ){
	navigacia('Užívatelia',$db2,1);
}
else{
navigacia('Užívatelia',$db2);
}
?>



 
<?php
if (isset($_POST['meno_i']) && isset($_POST['priezvisko_i']) && isset($_POST['rola_i'])   ){
	//vloz_log($mysqli,$_SESSION['prihlasovacie_meno'],"odhlasenie");
	if(pridaj_uzivatela_android($db2,$_POST['meno_i'],$_POST['priezvisko_i'],$_POST['rola_i'])){
		vloz_log($db,105,"Pridanie užívateľa: ".$_POST['meno_i']." ".$_POST['priezvisko_i']." ",$_SESSION['prihlasovacie_meno']);
	echo '<div class="modal fade" id="onload" tabindex="-1"">
  <div class="modal-dialog">
    <div class="modal-content">
      <div class="modal-header">
        <h5 class="modal-title">'. $_POST['meno_i']." ".$_POST['priezvisko_i'] .'</h5>
        <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
      </div>
      <div class="modal-body">
        <p>Užívateľ úspešne pridaný.</p>
      </div>
      <div class="modal-footer">
        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
      </div>
    </div>
  </div>
</div>';
echo "<script type='text/javascript'>
    window.onload = () => {
        $('#onload').modal('show');
    }
</script>";
	}
}

if (isset($_POST['meno']) && isset($_POST['priezvisko']) && isset($_POST['rola']) && isset($_POST['code'])  && isset($_POST['doplnok'])    ){
	//vloz_log($mysqli,$_SESSION['prihlasovacie_meno'],"odhlasenie");
	if(update_uzivatela_android($db2,$_POST['meno'],$_POST['priezvisko'],$_POST['rola'],$_POST['code'],$_POST['doplnok']) ){
		vloz_log($db,106,"Úprava užívateľa: ".$_POST['meno']." ".$_POST['priezvisko']." ".$_POST['code'],$_SESSION['prihlasovacie_meno']);
	echo '<div class="modal fade" id="onload" tabindex="-1"">
  <div class="modal-dialog">
    <div class="modal-content">
      <div class="modal-header">
        <h5 class="modal-title">'. $_POST['code'] .'</h5>
        <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
      </div>
      <div class="modal-body">
        <p>Užívateľ úspešne aktualizovaný.</p>
      </div>
      <div class="modal-footer">
        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
      </div>
    </div>
  </div>
</div>';
echo "<script type='text/javascript'>
    window.onload = () => {
        $('#onload').modal('show');
    }
</script>";
	}
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
over_pouzivatela($db, $_POST["prihlasmeno"], $_POST["heslo"] )==true ){
	$pouzivatel = over_pouzivatela($db, $_POST["prihlasmeno"], $_POST["heslo"] );
	//print_r($pouzivatel);
	$_SESSION['prihlasovacie_meno'] = $pouzivatel[1] ;
	//vloz_log($mysqli,$_SESSION['prihlasovacie_meno'],"prihlasenie");
}
if (isset($_SESSION['prihlasovacie_meno'])){
	//vloz_log($mysqli,$_SESSION['prihlasovacie_meno'],"Návšteva indexu ako prihlásený");
	
	
  


?>

<section>


<div class="row">
    <div class="col-4 d-flex">
       <?php  
	   if( isset($_SESSION['prihlasovacie_meno'])&& vrat_uzivatela_web($db,$_SESSION['prihlasovacie_meno'])[4]==1 ){
	vypis_uzivatelov($db2,1);
}
else{
vypis_uzivatelov($db2);
}
?>
    </div>
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
