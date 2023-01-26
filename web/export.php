<?php
 define('FPDF_FONTPATH',"fpdf/font/");
 include 'fpdf/fpdf.php';
 include 'fpdf/exfpdf.php';
 include 'fpdf/easyTable.php';
 require('db.php');
 error_reporting(E_ERROR | E_WARNING | E_PARSE | E_NOTICE);

function secure_iterable($var)
{
    return is_iterable($var) ? $var : array();
}
 function dekoduj($text){
	 return iconv('UTF-8//IGNORE', 'ISO-8859-2//IGNORE', $text);
 }
 
 $pdf=new exFPDF();
 $pdf->AddPage(); 
 $pdf->SetMargins(3, 3 , 3); 
 $pdf->AddFont('FontUTF8','','NotoSerif-Regular.php'); 
 $pdf->AddFont('FontUTF8','B','NotoSerif-Bold.php'); 
 $pdf->AddFont('FontUTF8','BI','NotoSerif-BoldItalic.php'); 
 $pdf->AddFont('FontUTF8','I','NotoSerif-Italic.php'); 
  $pdf->SetFont('FontUTF8','',10);

 $table1=new easyTable($pdf, 1);
 $table1->easyCell(dekoduj('LEAR Stillage Label Audit'), 'font-size:20; font-style:B; font-color:#00bfff;align:C;');
 //$table1->easyCell('', 'img:Pics/fpdf.png, w80; align:R;');
 $table1->printRow();

$shipment_info = "";
if( isset($_POST['shipment_ajdi']) ){
	$shipment_info .= "<b>Shipment ID:</b> {$_POST['shipment_ajdi']}\n";
}
if( isset($_POST['Plate_NO']) ){
	$shipment_info .= "<b>Plate NO.:</b> {$_POST['Plate_NO']}\n";
}
if( isset($_POST['Customer']) ){
	$customer_unicode = dekoduj($_POST['Customer']);
	$shipment_info .= "<b>Customer:</b> {$customer_unicode}\n";
}
if( isset($_POST['User']) ){
	$user_unicode = dekoduj($_POST['User']);
	$shipment_info .= "<b>User:</b> {$user_unicode}\n";
}

if( isset($_POST['time_close_s']) ){
	$shipment_info .= "<b>Date Time close:</b> {$_POST['time_close_s']}\n";
}

 $table1->rowStyle('font-size:12;');
 $table1->easyCell($shipment_info);
 $table1->printRow();



 $table1->endTable(5);

//====================================================================

$products=array(
'Consectetur adipiscing elit. Nam quis tincidunt mi', 
'Vitae pulvinar tortor. Integer quis mattis lorem. Quisque maximus ut ipsum aliquet mattis.', 
'Sed in tristique enim. Vivamus malesuada, sapien non consequat tempus, 
risus mauris ornare risus, in varius urna est quis enim.', 
'Suspendisse nec fermentum orci, ut feugiat felis.', 
'Phasellus molestie urna nisi, nec
imperdiet orci pretium vel. Donec vehicula tellus nisl, nec commodo diam posuere eu.',
'Interdum et malesuada fames ac ante ipsum primis in faucibus. Nunc in libero non',
'velit consectetur facilisis tincidunt non justo.',
'Pellentesque', 
'Scelerisque nec nibh a sollicitudin.', 
'Nullam porttitor nulla est, nec semper felis mattis sit amet.',
'Donec', 'fringilla congue felis, ornare', 'tempus velit congue at.', 
);

 		$shipmentz = pg_query($db2, 'SELECT * FROM "Stillage" WHERE "Shipment_id" = ' . $_POST['shipment_id_r'] . '');
		$shipmentz_array = pg_fetch_all($shipmentz);

$pocet_riadockov = 0;
foreach($_POST as $postik_1) {
	if($postik_1=='1'){
		$pocet_riadockov++;
	}
}

 $table=new easyTable($pdf, $pocet_riadockov,'align:C;border:1; border-color:#a1a1a1; ');

 $table->rowStyle('align:C;valign:M;bgcolor:#000000; font-color:#ffffff; font-style:B;font-size:7;');
 if( isset($_POST['Type']) ){
 $table->easyCell('Typ stillage');
}
if( isset($_POST['Stillage_number']) ){
 $table->easyCell(dekoduj('Číslo stillage'));
}

if( isset($_POST['First_scan_TLS']) ){
 $table->easyCell(dekoduj('Prvá pozícia vo vozíku TLS'));
}
if( isset($_POST['Last_scan_TLS']) ){
 $table->easyCell(dekoduj('Posledná pozícia vo vozíku TLS'));
}

if( isset($_POST['JLR_Header_NO']) ){
 $table->easyCell('JLR Header NO');
}

if( isset($_POST['Stillage_Number_on_Header']) ){ 
 $table->easyCell('Carriage Label vs JLR Header stillage No.');//TOTO TU EŠTE ZREVIDOVAŤ !!!!
}

if( isset($_POST['time_start']) ){
 $table->easyCell('Date Time start');
}
if( isset($_POST['time_end']) ){
 $table->easyCell('Date Time end');
}


if( isset($_POST['First_scan_product']) ){
 $table->easyCell('First TLS in stillage scan');
}
if( isset($_POST['Last_scan_product']) ){
 $table->easyCell('Last TLS in stillage scan');
}

if( isset($_POST['Carriage']) ){
 $table->easyCell('Carriage'); // ČO je toto ?
}
if( isset($_POST['Check']) ){
 $table->easyCell('Check');
}

if( isset($_POST['TLS_Range_start']) ){
 $table->easyCell('TLS range start');
}
if( isset($_POST['TLS_Range_stop']) ){
 $table->easyCell('TLS range stop');
}
if( isset($_POST['Note']) ){
 $table->easyCell('Note');
}
 $table->printRow();
 $i = 0;
foreach(secure_iterable($shipmentz_array) as $item) {
    $bgcolor='';
    if($i%2)
    {
       $bgcolor='bgcolor:#ccf2ff;';
    }
    $table->rowStyle('valign:M;border:LR;paddingY:2;' . $bgcolor);
if( isset($_POST['Type']) ){
				$ajdi_stillage_type = "'".$item['id']."'";
			$query_stillage_type = 'SELECT
				"Stillage_type"."Name"
				FROM "Stillage"
				JOIN "Stillage_type"
				  ON "Stillage_Type_id" = "Stillage_type".id WHERE "Stillage".id = ' . $ajdi_stillage_type . ' ';
				$result_stillage_type = pg_query($db2,$query_stillage_type) or die('Error message: ' . pg_last_error());
				$row_stillage_type = pg_fetch_row($result_stillage_type);
				if($row_stillage_type != null) {
						$table->easyCell($row_stillage_type[0]);
				}
				else {
					$table->easyCell("");
				}
}
if( isset($_POST['Stillage_number']) ){
 $table->easyCell(dekoduj($item['Stillage_number']));
}

if( isset($_POST['First_scan_TLS']) ){
 $table->easyCell(dekoduj($item['First_scan_TLS_code']));
}
if( isset($_POST['Last_scan_TLS']) ){
 $table->easyCell(dekoduj($item['Last_scan_TLS_code']));
}

if( isset($_POST['JLR_Header_NO']) ){
 $table->easyCell(dekoduj($item['JLR_Header_NO']));
}

if( isset($_POST['Stillage_Number_on_Header']) ){ 
 $table->easyCell(dekoduj($item['Stillage_Number_on_Header']));//TOTO TU EŠTE ZREVIDOVAŤ !!!!
}

if( isset($_POST['time_start']) ){
 $table->easyCell(dekoduj($item['Date_time_start']));
}
if( isset($_POST['time_end']) ){
 $table->easyCell(dekoduj($item['Date_time_end']));
}


if( isset($_POST['First_scan_product']) ){
 $table->easyCell(dekoduj($item['First_scan_product']));
}
if( isset($_POST['Last_scan_product']) ){
 $table->easyCell(dekoduj($item['Last_scan_product']));
}

if( isset($_POST['Carriage']) ){
 $table->easyCell(dekoduj($item['Carriage_L_JLR_H'])); // ČO je toto ?
}
if( isset($_POST['Check']) ){
	$check_textik = dekoduj($item['_Check']);
	if($check_textik=="1"){
		$check_textik = "OK";
	}
	if($check_textik=="0"){
		$check_textik = "NOK";
	}
 $table->easyCell($check_textik);
}

if( isset($_POST['TLS_Range_start']) ){
 $table->easyCell(dekoduj($item['TLS_range_start']));
}
if( isset($_POST['TLS_Range_stop']) ){
 $table->easyCell(dekoduj($item['TLS_range_stop']));
}
if( isset($_POST['Note']) ){
 $table->easyCell(dekoduj($item['Note']));
}
    $table->printRow();
	$i++;
 }
 

 $table->endTable();


 $pdf->Output(); 



?>