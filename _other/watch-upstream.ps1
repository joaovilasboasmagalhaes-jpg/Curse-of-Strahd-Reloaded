$ErrorActionPreference = 'Stop'

$repository = Split-Path -Parent $PSScriptRoot
$stateFile = Join-Path (Join-Path $repository '.git') 'upstream-main-seen'

Push-Location $repository
try {
    git fetch --quiet upstream main
    $currentCommit = (git rev-parse refs/remotes/upstream/main).Trim()
    $previousCommit = if (Test-Path $stateFile) { (Get-Content $stateFile -Raw).Trim() } else { '' }

    Set-Content -Path $stateFile -Value $currentCommit -NoNewline

    if ($previousCommit -and $previousCommit -ne $currentCommit) {
        Add-Type -AssemblyName System.Windows.Forms
        [System.Windows.Forms.MessageBox]::Show(
            "The original Curse of Strahd Reloaded repository has changes on main.`n`nRun 'git log HEAD..upstream/main' to review them.",
            'Upstream changes available',
            [System.Windows.Forms.MessageBoxButtons]::OK,
            [System.Windows.Forms.MessageBoxIcon]::Information
        ) | Out-Null
    }
}
finally {
    Pop-Location
}