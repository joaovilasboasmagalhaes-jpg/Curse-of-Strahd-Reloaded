param(
    [Parameter(ValueFromRemainingArguments = $true)]
    [string[]]$Arguments
)

$ErrorActionPreference = 'Stop'
$runtime = 'C:\Program Files\Foundry Virtual Tabletop\Foundry Virtual Tabletop.exe'
if (-not (Test-Path -LiteralPath $runtime)) {
    throw "Foundry runtime not found: $runtime. Run assets.cjs with a compatible Node runtime instead."
}
$previous = $env:ELECTRON_RUN_AS_NODE
try {
    $env:ELECTRON_RUN_AS_NODE = '1'
    & $runtime (Join-Path $PSScriptRoot 'assets.cjs') @Arguments | Out-Host
    if ($LASTEXITCODE -ne 0) { throw "Asset command failed with exit code $LASTEXITCODE" }
}
finally {
    $env:ELECTRON_RUN_AS_NODE = $previous
}
