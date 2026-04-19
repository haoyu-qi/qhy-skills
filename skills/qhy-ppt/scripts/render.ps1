param(
  [Parameter(Mandatory = $true, Position = 0)]
  [string]$File,

  [Parameter(Position = 1)]
  [string]$Count = "1",

  [Parameter(Position = 2)]
  [string]$OutDir
)

$ErrorActionPreference = "Stop"

function Resolve-BrowserPath {
  $candidates = @(
    "$env:ProgramFiles\Google\Chrome\Application\chrome.exe",
    "${env:ProgramFiles(x86)}\Google\Chrome\Application\chrome.exe",
    "$env:ProgramFiles\Microsoft\Edge\Application\msedge.exe",
    "${env:ProgramFiles(x86)}\Microsoft\Edge\Application\msedge.exe"
  )

  foreach ($candidate in $candidates) {
    if ($candidate -and (Test-Path -LiteralPath $candidate)) {
      return $candidate
    }
  }

  throw "Chrome/Edge not found. Install Google Chrome or Microsoft Edge first."
}

function Get-SlideCount {
  param([string]$HtmlPath)

  $content = Get-Content -Raw -Encoding UTF8 $HtmlPath
  $matches = [regex]::Matches($content, 'class\s*=\s*"[^"]*\bslide\b')
  if ($matches.Count -gt 0) {
    return $matches.Count
  }
  return 1
}

function Render-One {
  param(
    [string]$Browser,
    [string]$Url,
    [string]$Target
  )

  $targetDir = Split-Path -Parent $Target
  if ($targetDir -and -not (Test-Path -LiteralPath $targetDir)) {
    New-Item -ItemType Directory -Path $targetDir -Force | Out-Null
  }

  & $Browser `
    --headless=new `
    --disable-gpu `
    --hide-scrollbars `
    --disable-crash-reporter `
    --disable-features=Crashpad `
    --no-first-run `
    --window-size=1920,1080 `
    "--screenshot=$Target" `
    $Url | Out-Null

  Write-Host "Rendered $Target"
}

$resolvedFile = Resolve-Path -LiteralPath $File
$browser = Resolve-BrowserPath
$stem = [System.IO.Path]::GetFileNameWithoutExtension($resolvedFile)

if ($Count -eq "all") {
  $slideCount = Get-SlideCount -HtmlPath $resolvedFile
}
elseif ($Count -match '^\d+$') {
  $slideCount = [int]$Count
}
else {
  throw "Count must be a positive integer or 'all'."
}

if ($slideCount -lt 1) {
  $slideCount = 1
}

$fileUri = [System.Uri]::new($resolvedFile)

if (-not $OutDir) {
  if ($slideCount -eq 1) {
    $OutDir = Join-Path (Split-Path -Parent $resolvedFile) "$stem.png"
  }
  else {
    $OutDir = Join-Path (Split-Path -Parent $resolvedFile) "$stem-png"
  }
}

if ($slideCount -eq 1) {
  $singleTarget = $OutDir
  if ([System.IO.Path]::GetExtension($singleTarget) -ne ".png") {
    $singleTarget = Join-Path $singleTarget "$stem.png"
  }
  Render-One -Browser $browser -Url $fileUri.AbsoluteUri -Target $singleTarget
}
else {
  if (-not (Test-Path -LiteralPath $OutDir)) {
    New-Item -ItemType Directory -Path $OutDir -Force | Out-Null
  }

  for ($i = 1; $i -le $slideCount; $i++) {
    $url = "$($fileUri.AbsoluteUri)#/$i"
    $target = Join-Path $OutDir ("{0}_{1:d2}.png" -f $stem, $i)
    Render-One -Browser $browser -Url $url -Target $target
  }
}

Write-Host "Done: rendered $slideCount slide(s) from $resolvedFile"
