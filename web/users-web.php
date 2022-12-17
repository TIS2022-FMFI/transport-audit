<?php
session_start();
include('db.php');
include('funkcie.php');
require('fpdf/fpdf.php');
$pdf = new FPDF();
navigacia('Užívatelia-web',$db2);

?>



 
<?php
if (isset($_POST['meno']) && isset($_POST['username']) && isset($_POST['heslo']) && isset($_POST['rola'])  && isset($_POST['ano'])    ){
	//vloz_log($mysqli,$_SESSION['prihlasovacie_meno'],"odhlasenie");
	if(pridaj_uzivatela_web($db,$_POST['meno'],$_POST['username'],$_POST['rola'],$_POST['heslo']) ){
	echo '<div class="modal fade" id="onload" tabindex="-1"">
  <div class="modal-dialog">
    <div class="modal-content">
      <div class="modal-header">
        <h5 class="modal-title">'. $_POST['meno'] .'</h5>
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

if (isset($_POST['meno']) && isset($_POST['username']) && isset($_POST['heslo']) && isset($_POST['rola'])  && isset($_POST['id'])    ){
	//vloz_log($mysqli,$_SESSION['prihlasovacie_meno'],"odhlasenie");
	if(update_uzivatela_web($db,$_POST['meno'],$_POST['username'],$_POST['rola'],$_POST['id'],$_POST['heslo']) ){
	echo '<div class="modal fade" id="onload" tabindex="-1"">
  <div class="modal-dialog">
    <div class="modal-content">
      <div class="modal-header">
        <h5 class="modal-title">'. $_POST['meno'] .'</h5>
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
       <?php  vypis_uzivatelov_web($db);?>
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
