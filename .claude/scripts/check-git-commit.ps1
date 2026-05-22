# Runs before every Bash tool call.
# Warns if a git commit is attempted without an active session log.

try {
    $stdinContent = [System.Console]::In.ReadToEnd()
    $isCommit = $stdinContent -match '"git commit' -or $stdinContent -match "'git commit"

    if ($isCommit) {
        $logBase = "docs\workflow\logs"
        $hasActiveLog = $false

        if (Test-Path $logBase) {
            $logs = Get-ChildItem $logBase -Recurse -Filter "*.md" -ErrorAction SilentlyContinue
            $active = $logs | Where-Object {
                $content = Get-Content $_.FullName -Raw -ErrorAction SilentlyContinue
                $content -match "Statut:\s*in_progress"
            }
            $hasActiveLog = ($null -ne $active -and @($active).Count -gt 0)
        }

        if (-not $hasActiveLog) {
            Write-Host ""
            Write-Host "WORKFLOW : Aucun log de session actif."
            Write-Host "Creez d'abord un log : /start-task <type> <nom>"
            Write-Host ""
        }
    }
} catch {
    # Never block on hook errors
}
exit 0
