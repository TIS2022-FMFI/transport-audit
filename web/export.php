<?php
define('FPDF_FONTPATH',"fpdf/font/");
require('fpdf/tfpdf.php');

$pdf = new tFPDF();
$pdf->AddPage();

$pdf->AddFont('DejaVu','','DejaVuSansCondensed.ttf',true);
$pdf->SetFont('Arial','B',16);


$pdf->Cell(100,10,'Nadpis');
$pdf->Ln(20);

$pdf->SetFont('DejaVu','',12);

foreach( $_POST as $stuff ) {
		         $pdf->Cell(20,10,$stuff);
				$pdf->Ln(20);
}

$pdf->Output();

?>