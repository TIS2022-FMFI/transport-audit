<?php
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
if(isset($_SESSION['prihlasovacie_meno']) && vrat_uzivatela_web($db,$_SESSION['prihlasovacie_meno'])[4]==0){
	    echo "<script> location.href='index.php'; </script>";
        exit;
}
navigacia('Logy web',$db2);

?>



 
<?php

if(isset($_SESSION['prihlasovacie_meno'])==false){
	    echo "<script> location.href='index.php'; </script>";
        exit;
}

if(isset($_GET['strana'])) {
    $aktualna_strana = $_GET['strana'];
}
else {
	$aktualna_strana = 1;
}
if(isset($_POST['uzivatel'])) {
    $uzivatel = $_POST['uzivatel'];
}
else {
	$uzivatel = "";
}
if(isset($_POST['kod_chyby']) && $_POST['kod_chyby']!="") {
    $kod_chyby = (int)$_POST['kod_chyby'];
}
else {
	$kod_chyby = -1;
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
	 <button type='button' style='border: none;background-color: #ffffff;' data-bs-toggle='modal' data-bs-target='#modalsort'>Vyhľadať</button>
			
	<div class="modal fade" id="modalsort" tabindex="-1" role="dialog" aria-labelledby="vockoLabel" aria-hidden="true" data-bs-backdrop="static" data-bs-keyboard="false"><div class="modal-dialog" role="document"><div class="modal-content"><div class="modal-header"><h5 class="modal-title" id="fcLabel">Search</h5><button type="button" class="close" data-bs-dismiss="modal" aria-label="Close"><span aria-hidden="true">&times;</span></button></div><div class="modal-body">
			
			<form action="" method="POST">
			<label>Užívateľ: </label>

				
						<select name="uzivatel">
						<?php
						echo vypis_logy_uzivatel_kod_chyby_option_as_str($db,0,1);
		?>	
			</select>
			<br>
						<label>Kód záznamu: </label>

				
						<select name="kod_chyby">
						<?php
						echo vypis_logy_uzivatel_kod_chyby_option_as_str($db,0,2);
		?>	
			</select>
			<br>

			<br>
				<input type="submit" value="Hľadať" />
			</form>        
		

      </div><div class="modal-footer"><button type="button" class="btn-primary"data-bs-dismiss="modal">Zavrieť</button></div></div></div></div>

<div class="row">
    <div class="col-4 d-flex">
        <?php vypis_logy_android($db,$aktualna_strana,$uzivatel,$kod_chyby,0); ?>
    </div>
</div>
		
				
	<?php if($uzivatel == "" && $kod_chyby == -1){posuvanie_strany_logy($db,$aktualna_strana,0);} ?>	
				
			

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
