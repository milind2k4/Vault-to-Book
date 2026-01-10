<#
.SYNOPSIS
    Wrapper script for import_vault.py
.DESCRIPTION
    Runs the python import script with correctly passed arguments.
.EXAMPLE
    .\run_import.ps1
#>
param(
    [string]$Source = "E:\Obsidian\College\DBMS",

    [string]$Attachments = "E:\Obsidian\00 Attachments",

    [string]$Output = "DBMS",

    [switch]$Build = $true
)

$scriptPath = Join-Path $PSScriptRoot "import_vault.py"

# Build arguments list
$pyArgs = @()
$pyArgs += "--source", "$Source"
$pyArgs += "--attachments", "$Attachments"

if ($Output) {
    $pyArgs += "--output", "$Output"
}

if ($Build) {
    $pyArgs += "--build"
}

Write-Host "Running import_vault.py..." -ForegroundColor Cyan
python $scriptPath @pyArgs
