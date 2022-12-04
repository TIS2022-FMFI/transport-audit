<?php

require('fpdf/fpdf.php');

$pdf = new FPDF();
$pdf->AddPage();
$pdf->SetFont('Arial','B',16);

$pdf->Cell(40,10,'Hello World!');
$pdf->Ln(20);
if (isset($_POST['time_start'])){
	$pdf->Cell(20,10,$_POST['time_start']);
	$pdf->Ln(20);
}
$pdf->Output();

?>