$docxPath = (Resolve-Path "API_Monitoring_Project_Report.docx").Path
$pdfPath = [System.IO.Path]::ChangeExtension($docxPath, ".pdf")
$mergedPdfPath = (Resolve-Path "Report format pg-1-2(23-24) (1)-merged.pdf").Path

Write-Host "Opening Word COM..."
$word = New-Object -ComObject Word.Application
$word.Visible = $false
try {
    $doc = $word.Documents.Open($docxPath)
    $pageCount = $doc.ComputeStatistics(2) # 2 = wdStatisticPages
    Write-Host "Exact Page Count in Word: $pageCount"
    
    # Export to PDF (17 = wdFormatPDF)
    Write-Host "Exporting to PDF: $pdfPath"
    $doc.SaveAs([ref]$pdfPath, [ref]17)
    $doc.SaveAs([ref]$mergedPdfPath, [ref]17)
    Write-Host "Export completed successfully!"
    $doc.Close([ref]$false)
} catch {
    Write-Host "Error during Word automation: $_"
} finally {
    $word.Quit()
}
