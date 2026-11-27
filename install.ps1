# NoCap installer — Windows PowerShell 5.1+ / PowerShell 7+
#
#   irm https://raw.githubusercontent.com/sanket-manohar/nocap/main/install.ps1 | iex
#   .\install.ps1 -Target C:\code\myapp -Tools cursor,claude -CI
#   .\install.ps1 -Uninstall
param(
  [string]$Target = ".",
  [string]$Tools = "all",
  [switch]$CI,
  [switch]$Uninstall
)
$ErrorActionPreference = "Stop"
$Repo = if ($env:NOCAP_REPO) { $env:NOCAP_REPO } else { "sanket-manohar/nocap" }
$Ref = if ($env:NOCAP_REF) { $env:NOCAP_REF } else { "main" }
$Start = "<!-- nocap:start -->"; $End = "<!-- nocap:end -->"
$Target = (Resolve-Path $Target).Path

# ---- locate source ----
$Src = $null
if ($PSScriptRoot -and (Test-Path (Join-Path $PSScriptRoot "adapters/MANIFEST"))) { $Src = $PSScriptRoot }
else {
  $tmp = Join-Path ([IO.Path]::GetTempPath()) ("nocap-" + [guid]::NewGuid())
  New-Item -ItemType Directory -Path $tmp | Out-Null
  Write-Host "  > Downloading NoCap ($Repo@$Ref)..." -ForegroundColor Magenta
  $zip = Join-Path $tmp "vp.zip"
  Invoke-WebRequest "https://codeload.github.com/$Repo/zip/refs/heads/$Ref" -OutFile $zip -UseBasicParsing
  Expand-Archive $zip -DestinationPath $tmp
  $Src = (Get-ChildItem $tmp -Directory | Where-Object Name -like "nocap-*" | Select-Object -First 1).FullName
}

function Get-Tool($dest) {
  switch -Wildcard ($dest) {
    "AGENTS.md" { "generic" } "CLAUDE.md" { "claude" } ".claude/*" { "claude" } ".cursor/*" { "cursor" }
    ".github/copilot-instructions.md" { "copilot" } ".github/prompts/*" { "copilot" } ".windsurf/*" { "windsurf" }
    ".clinerules/*" { "cline" } ".roo/*" { "roo" } ".continue/*" { "continue" } "GEMINI.md" { "gemini" }
    ".junie/*" { "junie" } ".aider.conf.yml" { "aider" } default { "other" }
  }
}
function Test-Wanted($t) { $Tools -eq "all" -or ("," + $Tools + ",").Contains("," + $t + ",") }
function Remove-Block($file) {
  $out = @(); $skip = $false
  foreach ($l in Get-Content $file) { if ($l -eq $Start) { $skip = $true; continue }; if ($l -eq $End) { $skip = $false; continue }; if (-not $skip) { $out += $l } }
  Set-Content -Path $file -Value $out -Encoding UTF8
}
$manifest = Get-Content (Join-Path $Src "adapters/MANIFEST") | Where-Object { $_ -and -not $_.StartsWith("#") }

if ($Uninstall) {
  Remove-Item -Recurse -Force (Join-Path $Target ".nocap") -ErrorAction SilentlyContinue
  foreach ($line in $manifest) {
    $mode, $s, $d = $line -split " "; $f = Join-Path $Target $d
    if (-not (Test-Path $f)) { continue }
    if ($mode -eq "merge") { Remove-Block $f; if (-not ((Get-Content $f -Raw) -match '\S')) { Remove-Item $f } }
    elseif ($mode -eq "copy-if-missing") { if (Select-String -Path $f -Pattern "NoCap" -Quiet) { Remove-Item $f } }
    else { Remove-Item $f }
    $dir = Split-Path $f
    while ($dir -and ($dir -ne $Target) -and (Test-Path $dir) -and -not (Get-ChildItem $dir -Force)) { Remove-Item $dir; $dir = Split-Path $dir }
  }
  Write-Host "  NoCap removed." -ForegroundColor Green; return
}

Write-Host "`n  NoCap  installing into $Target`n" -ForegroundColor Magenta
$VP = Join-Path $Target ".nocap"
Remove-Item -Recurse -Force $VP -ErrorAction SilentlyContinue
New-Item -ItemType Directory -Force -Path (Join-Path $VP "scanner") | Out-Null
foreach ($d in "prompts", "templates", "checklists") { Copy-Item -Recurse (Join-Path $Src $d) $VP }
Copy-Item (Join-Path $Src "AGENTS.md"), (Join-Path $Src "MASTER_PROMPT.md"), (Join-Path $Src "TERMS.md"), (Join-Path $Src "LICENSE") $VP
Copy-Item (Join-Path $Src "scanner/nocap.py") (Join-Path $VP "scanner")
New-Item -ItemType File -Force -Path (Join-Path $VP ".nocap-toolkit") | Out-Null
Set-Content -Path (Join-Path $VP "vp.cmd") -Encoding ASCII -Value "@echo off`r`nwhere py >nul 2>nul && (py -3 `"%~dp0scanner\nocap.py`" %*) || (python `"%~dp0scanner\nocap.py`" %*)"
Write-Host "  > Toolkit      -> .nocap/"

foreach ($line in $manifest) {
  $mode, $s, $d = $line -split " "
  $t = Get-Tool $d; if (-not (Test-Wanted $t)) { continue }
  $f = Join-Path $Target $d; New-Item -ItemType Directory -Force -Path (Split-Path $f) | Out-Null
  $srcFile = Join-Path $Src $s
  switch ($mode) {
    "copy" { Copy-Item $srcFile $f -Force }
    "copy-if-missing" { if (-not (Test-Path $f)) { Copy-Item $srcFile $f } }
    "merge" {
      if (Test-Path $f) { Remove-Block $f }
      $block = @($Start) + (Get-Content $srcFile) + @($End)
      if ((Test-Path $f) -and (Get-Content $f)) { Add-Content $f "" }
      Add-Content -Path $f -Value $block -Encoding UTF8
    }
  }
  Write-Host ("  OK {0,-12} -> {1}" -f $t, $d) -ForegroundColor Green
}

if ($CI) {
  $wf = Join-Path $Target ".github/workflows"; New-Item -ItemType Directory -Force -Path $wf | Out-Null
  (Get-Content (Join-Path $Src "adapters/ci/nocap.yml")) -replace "sanket-manohar/nocap", $Repo | Set-Content (Join-Path $wf "nocap.yml")
  Write-Host "  > CI workflow  -> .github/workflows/nocap.yml"
}
$gi = Join-Path $Target ".gitignore"
if (-not ((Test-Path $gi) -and (Select-String -Path $gi -Pattern "nocap-results.json" -Quiet))) { Add-Content $gi "`n# NoCap`n.nocap-results.json" }

Write-Host "`n  NoCap installed!`n" -ForegroundColor Green
Write-Host "  Open your AI assistant and type:  nocap docs   |   nocap audit   |   nocap ship"
Write-Host "  Or run the scanner:               .nocap\vp`n"
Write-Host "  NoCap is a development aid. Final checks are your responsibility. See .nocap\TERMS.md`n" -ForegroundColor DarkGray
