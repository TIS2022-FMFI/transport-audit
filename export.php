<?php
require('fpdf/fpdf.php');

function filter_html($value){
    $value = mb_convert_encoding($value, 'ISO-8859-1', 'UTF-8');
    return $value;
}


$pdf = new FPDF();
$pdf->AddPage();
$pdf->SetFont('Arial','B',16);

$pdf->Cell(40,10,'Hello World!');
$pdf->Ln(20);


foreach( $_POST as $stuff ) {
		         $pdf->Cell(20,10,filter_html($stuff));
				$pdf->Ln(20);
}

$pdf->Output();

?>