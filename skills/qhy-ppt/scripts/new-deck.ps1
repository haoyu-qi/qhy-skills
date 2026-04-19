param(
  [Parameter(Mandatory = $true, Position = 0)]
  [string]$Name,

  [Parameter(Position = 1)]
  [string]$Parent = "examples"
)

$ErrorActionPreference = "Stop"

$skillRoot = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
$template = Join-Path $skillRoot "assets\deck-starter.html"

if (-not (Test-Path -LiteralPath $template)) {
  throw "Template not found: $template"
}

$outDir = Join-Path $skillRoot $Parent
$outDir = Join-Path $outDir $Name

if (Test-Path -LiteralPath $outDir) {
  throw "Output already exists: $outDir"
}

New-Item -ItemType Directory -Path $outDir -Force | Out-Null
$target = Join-Path $outDir "index.html"
Copy-Item -LiteralPath $template -Destination $target

Write-Host "Created $target"
Write-Host ""
Write-Host "Next steps:"
Write-Host "  1. Replace placeholders in index.html"
Write-Host "  2. Open it in a browser and verify keyboard navigation"
Write-Host "  3. Render previews with scripts\render.ps1"
