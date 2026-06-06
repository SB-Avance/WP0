$root='C:\VS\BIN'
$proposal=Join-Path $root 'archive\AUTO_MOVE_LIST.md'
if(-not(Test-Path $proposal)){ Write-Error 'No AUTO_MOVE_LIST.md found'; exit 2 }
$lines=Get-Content $proposal -Encoding utf8 | Where-Object { $_ -match '^\s*-\s+' }
if(-not $lines){ Write-Output 'No items found in AUTO_MOVE_LIST.md'; exit 0 }
$timestamp=Get-Date -Format 'yyyyMMdd_HHmmss'
$destRoot=Join-Path $root ('archive\' + $timestamp)
foreach($l in $lines){
    $it = ($l -replace '^\s*-\s+','').Trim()
    $src = Join-Path $root $it
    if(Test-Path $src){
        $dest = Join-Path $destRoot $it
        $destDir = Split-Path $dest -Parent
        if(-not (Test-Path $destDir)){ New-Item -ItemType Directory -Path $destDir -Force | Out-Null }
        Move-Item -Path $src -Destination $dest -Force
        Write-Output "Moved: $src -> $dest"
    } else {
        Write-Warning "Not found: $src"
    }
}
Write-Output "Done. Destination: $destRoot"
