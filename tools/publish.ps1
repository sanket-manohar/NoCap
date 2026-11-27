# One-time publish helper for Windows.   .\tools\publish.ps1 -User <github-username> -Email <email>
param([Parameter(Mandatory)][string]$User, [Parameter(Mandatory)][string]$Email)
$ErrorActionPreference = "Stop"
Set-Location (Split-Path $PSScriptRoot)
$Author = "Sanket Santosh Vidya Manohar"; $Slug = "$User/nocap"
$Version = "v" + ((Select-String -Path scanner/nocap.py -Pattern '^VERSION = "(.*)"').Matches[0].Groups[1].Value)
Get-ChildItem -Recurse -File | Where-Object { $_.FullName -notmatch '\\.git\\' -and $_.Name -notlike 'publish.*' } | ForEach-Object {
  $t = [IO.File]::ReadAllText($_.FullName)
  if ($t -match 'YOUR_GITHUB_USERNAME|YOUR_EMAIL') {
    [IO.File]::WriteAllText($_.FullName, ($t -replace 'YOUR_GITHUB_USERNAME', $User -replace 'YOUR_EMAIL', $Email))
  }
}
if (-not (Test-Path .git)) { git init -q -b main }
git config user.name $Author; git config user.email $Email
git add -A; git commit -q -m "feat: NoCap $Version — docs, security & compliance for AI-built apps"
git tag -a $Version -m "NoCap $Version"; git tag -f v1 | Out-Null
$manual = $true
if ((Get-Command gh -ErrorAction SilentlyContinue) -and ((gh auth status 2>&1) -and $LASTEXITCODE -eq 0)) {
  gh repo create $Slug --public --source . --remote origin --push --description "Your AI wrote the code. NoCap documents it, audits its security & checks compliance."
  if ($LASTEXITCODE -eq 0) { git push origin --tags; Write-Host "Live: https://github.com/$Slug" -ForegroundColor Green; $manual = $false }
}
if ($manual) {
  Write-Host "`nCreate an EMPTY public repo 'nocap' at https://github.com/new, then run:`n  git remote add origin https://github.com/$Slug.git`n  git push -u origin main`n  git push origin --tags" -ForegroundColor Green
}
