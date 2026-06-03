<#
PowerShell setup script for development environment.
Run from repository root in PowerShell:
  .\rebuild\scripts\setup_dev.ps1
#>
Write-Host "Creating virtual environment .venv..."
python -m venv .venv
Write-Host "Activating virtual environment..."
. .\.venv\Scripts\Activate.ps1
Write-Host "Upgrading pip and installing dependencies..."
python -m pip install --upgrade pip
pip install -r rebuild/requirements.txt

if (Get-Command pre-commit -ErrorAction SilentlyContinue) {
    Write-Host "Installing pre-commit hooks..."
    pre-commit install
} else {
    Write-Host "pre-commit not found. Install it with 'pip install pre-commit'"
}

Write-Host "Done. Copy rebuild/.env.example to .env and fill the values."
