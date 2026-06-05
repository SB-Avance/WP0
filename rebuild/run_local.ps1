# Helper script to run the rebuild FastAPI service locally with safe dummy env values.
# Run from repository root with the venv activated:
#   .venv\Scripts\Activate.ps1
#   .\rebuild\run_local.ps1

# Ensure PYTHONPATH includes the package source
$repoRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$srcPath = Join-Path $repoRoot 'src'

$env:PYTHONPATH = "$srcPath;$env:PYTHONPATH"

Write-Host "Starting FastAPI (uvicorn) on http://127.0.0.1:8000"
Write-Host "Using PYTHONPATH=$env:PYTHONPATH"

# Start the server (this blocks)
python -m uvicorn whatsapp_manager.main:app --reload --host 127.0.0.1 --port 8000
