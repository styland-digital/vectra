# Runs from project root after each Claude response.
# Checks docs/workflow/logs for an in_progress session log.

$logBase = "docs\workflow\logs"

if (-not (Test-Path $logBase)) { exit 0 }

$logs = Get-ChildItem $logBase -Recurse -Filter "*.md" -ErrorAction SilentlyContinue
$active = $logs | Where-Object {
    $content = Get-Content $_.FullName -Raw -ErrorAction SilentlyContinue
    $content -match "Statut:\s*in_progress"
}

Write-Host ""
if ($active) {
    $name = ($active | Select-Object -First 1).Name
    Write-Host ">>> LOG ACTIF : $name"
    Write-Host "    Mettez a jour le log et STATUS.md avant de terminer."
} else {
    Write-Host ">>> Aucun log de session actif."
    Write-Host "    Avant de coder : /start-task <type> <nom>"
    Write-Host "    Types : feature | component | api | agent | database | fix | test"
}
