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
	navigacia('Nahraj report');
	
	
if (isset($_FILES['file'])){  
	


$ch = curl_init();
curl_setopt($ch, CURLOPT_URL, $target_url);
curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
curl_setopt($ch, CURLOPT_POST, true);
$tmpfile = $_FILES['file']['tmp_name'];
$filename = basename($_FILES['file']['name']);
$data = array(
    'file'      => curl_file_create($tmpfile, $_FILES['file']['type'], $filename),
    'api-heslo'         => $API_PASSWD
);

curl_setopt($ch, CURLOPT_POSTFIELDS, $data);
$output = curl_exec($ch);
$info = curl_getinfo($ch);

if (curl_errno($ch)) { 
   print curl_error($ch); 
} 

curl_close($ch);

$curlresponse = json_decode($output, true);



	echo '<div class="modal fade" id="onload" tabindex="-1"">
  <div class="modal-dialog">
    <div class="modal-content">
      <div class="modal-header">
        <h5 class="modal-title">Správa</h5>
        <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
      </div>
      <div class="modal-body">';
        if($curlresponse=='200'){
			echo '<p>Export úspešne nahraný.</p>';
			vloz_log($db,109,"Update reportu úspešný",$_SESSION['prihlasovacie_meno']);
		}
		        if($curlresponse=='400'){
			echo '<p>Súbor nemá prípomu .csv.</p>';
			vloz_log($db,107,"Zlý formát reportu",$_SESSION['prihlasovacie_meno']);
		}
		        if($curlresponse=='401'){
			echo '<p>Webová verzia aplikácie nemá v súbore db.php správne nastavené api heslo.</p>';
			vloz_log($db,107,"Zlý api-key pri nahrávaní reportu",$_SESSION['prihlasovacie_meno']);
		}
		echo '
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


?>

<section>


<div class="row">

         <form method = "post" enctype="multipart/form-data">  
        <input type="file" accept=".csv" name="file" required>  
		</br>
		</br>
        <button type="submit" class="btn btn-primary">Nahrať</button> 
    </form>  

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
