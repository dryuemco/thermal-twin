# Propagate the MOD11A1 QC_Day screening rule through the downstream chain.
#
# WHY TWO ARMS AND NOT ONE
# The frozen outputs were produced on another machine by another operator. If
# the screened arm were compared straight against them, the contrast would mix
# the screening effect with every difference the rerun itself introduces. So
# BOTH arms are rebuilt here, from the same staged inputs, with the same code
# and the same pinned environment, and only the MODIS input differs between
# them. Arm A is additionally compared against the frozen numbers, but that
# comparison is reported as a diagnostic, not used as a gate: if the rerun
# drifts, the A-vs-B contrast is still internally valid and the drift is a
# fact worth reporting on its own.
#
# ARM A  unscreened MODIS (as exported for this region) -> step7 -> step8
# ARM B  screened MODIS (QC_Day bits + 3-observation minimum, -9999 nodata)
#        -> step7 -> step8
#
# step7c is not staged: it is a step7 OUTPUT and both arms regenerate it, and
# it is 2.7 GB of the 4.2 GB tree.
#
# WHY THIS SCRIPT NOW REFUSES TO RUN BY DEFAULT
# It stages inputs into repo\outputs, which CLAUDE.md declares read-only and
# which is not under version control. On 2026-08-14 a run of this script
# overwrote Mugla's canonical step8a modelling dataset; the frozen export
# survived only as an accidental nested copy, and Section 4.4 of the paper had
# to be re-run once the divergence was found (see paper/A1_sensitivity.md,
# "The data-provenance correction"). The overwrite was silent because the
# staging step uses -Force with -ErrorAction SilentlyContinue.
#
# Pass -AllowRepoWrites to proceed. The script then snapshots any step8a
# parquet it is about to replace, so the frozen version is recoverable.
#
# Usage: run_qc_propagation.ps1 <experiment_id> [-AllowRepoWrites]

param([Parameter(Mandatory = $true)][string]$Region,
      [switch]$AllowRepoWrites)

$ErrorActionPreference = "Continue"
$Root = "C:\Users\CORSAIR\projects\thermal-twin"
$Py   = "$Root\.venv-step10\Scripts\python.exe"
$Scr  = "C:\Users\CORSAIR\AppData\Local\Temp\claude\C--Users-CORSAIR-projects-thermal-twin\76ff7460-fb05-4162-9093-1e83fcc5b416\scratchpad"
$Wrap = "$Scr\run_with_project.py"
$Src  = "$Root\drive_new\experiments\$Region"
$Dst  = "$Root\repo\outputs\experiments\$Region"
$Work = "$Scr\qc_work\$Region"

New-Item -ItemType Directory -Force -Path $Work | Out-Null

function Say($m) { Write-Output ("=== [{0}] {1}" -f $Region, $m) }

if (-not $AllowRepoWrites) {
    Write-Output "REFUSING TO RUN: this script writes into $Dst, inside the read-only repo/ tree."
    Write-Output "A previous run overwrote a canonical step8a parquet there and the paper had to be"
    Write-Output "re-run. Re-invoke with -AllowRepoWrites if that is genuinely what you want."
    exit 1
}

# Snapshot anything we are about to replace, so a frozen export is recoverable.
$Snap = "$Scr\qc_repo_snapshot\$Region"
Get-ChildItem "$Dst" -Recurse -Filter "step8a_500m_modeling_dataset.parquet" -ErrorAction SilentlyContinue |
    ForEach-Object {
        $rel = $_.FullName.Substring($Dst.Length).TrimStart([char]92)
        $to  = Join-Path $Snap $rel
        New-Item -ItemType Directory -Force -Path (Split-Path $to) | Out-Null
        Copy-Item $_.FullName $to -Force
        Say ("snapshotted {0}" -f $rel)
    }

# ---------------------------------------------------------------- 1. stage --
Say "1/7 staging inputs (step7c excluded, it is regenerated)"
New-Item -ItemType Directory -Force -Path $Dst | Out-Null
Get-ChildItem $Src -Directory | Where-Object { $_.Name -ne 'step7c' } | ForEach-Object {
    Copy-Item $_.FullName (Join-Path $Dst $_.Name) -Recurse -Force -ErrorAction SilentlyContinue
}
Get-ChildItem $Src -File | ForEach-Object {
    Copy-Item $_.FullName (Join-Path $Dst $_.Name) -Force -ErrorAction SilentlyContinue
}
$mb = "{0:N0}" -f ((Get-ChildItem $Dst -Recurse -File | Measure-Object Length -Sum).Sum / 1MB)
Say "staged $mb MB"

# Keep the unscreened MODIS so arm A can be restored after arm B overwrites it.
$ModisDir = "$Dst\data\modis"
$Keep     = "$Dst\data\modis_unscreened_frozen"
if (-not (Test-Path $Keep)) {
    Copy-Item $ModisDir $Keep -Recurse -Force
    Say "unscreened MODIS preserved at data/modis_unscreened_frozen"
}

Set-Location "$Root\repo"
$env:PYTHONPATH = "$Root\repo"

# ------------------------------------------------------------- 2. arm A ----
Say "2/7 ARM A: step7 downscaling from UNSCREENED MODIS"
Copy-Item "$Keep\*" $ModisDir -Force
& $Py -m scripts.run_step7_downscaling_only --experiment $Region --force 2>&1 |
    Select-String -Pattern "Traceback|ERROR|CRITICAL|tamamlan|completed|fused" | Select-Object -Last 6

Say "3/7 ARM A: step8 modeling"
& $Py -m scripts.run_step8_modeling --experiment $Region --force 2>&1 |
    Select-String -Pattern "Traceback|ERROR|CRITICAL|ROC|AUC|tamamlan" | Select-Object -Last 8

New-Item -ItemType Directory -Force -Path "$Work\armA" | Out-Null
foreach ($s in @('step8a', 'step8b', 'step8c', 'step8d', 'step8e')) {
    if (Test-Path "$Dst\$s") {
        Copy-Item "$Dst\$s" "$Work\armA\$s" -Recurse -Force -ErrorAction SilentlyContinue
    }
}
Copy-Item "$ModisDir\*" "$Work\armA\" -Force -ErrorAction SilentlyContinue
Say "ARM A outputs captured"

# ------------------------------------------------------------- 3. arm B ----
Say "4/7 ARM B: regenerating MODIS WITH QC screening (Earth Engine)"
& $Py $Wrap scripts.prepare_modis_for_step7 --experiment $Region --export --force 2>&1 |
    Select-String -Pattern "Traceback|ERROR|nodata|sentinel|valid_observation|indir|download|tamam" |
    Select-Object -Last 10

# Refuse to continue on a MODIS raster that is not actually the screened one.
$chk = & $Py -c @"
import rasterio, sys
p = r'$ModisDir\modis_lst_mean_celsius.tif'
with rasterio.open(p) as s:
    print('NODATA', s.nodata)
"@
Say "screened MODIS check -> $chk"
if ($chk -notmatch '-9999') {
    Say "ABORT: regenerated MODIS carries no -9999 nodata tag; arm B is not the screened chain"
    Set-Location $Root
    exit 1
}

Say "5/7 ARM B: step7 downscaling from SCREENED MODIS"
& $Py -m scripts.run_step7_downscaling_only --experiment $Region --force 2>&1 |
    Select-String -Pattern "Traceback|ERROR|CRITICAL|tamamlan|completed|fused" | Select-Object -Last 6

Say "6/7 ARM B: step8 modeling"
& $Py -m scripts.run_step8_modeling --experiment $Region --force 2>&1 |
    Select-String -Pattern "Traceback|ERROR|CRITICAL|ROC|AUC|tamamlan" | Select-Object -Last 8

New-Item -ItemType Directory -Force -Path "$Work\armB" | Out-Null
foreach ($s in @('step8a', 'step8b', 'step8c', 'step8d', 'step8e')) {
    if (Test-Path "$Dst\$s") {
        Copy-Item "$Dst\$s" "$Work\armB\$s" -Recurse -Force -ErrorAction SilentlyContinue
    }
}
Copy-Item "$ModisDir\*" "$Work\armB\" -Force -ErrorAction SilentlyContinue
Say "ARM B outputs captured"

Say "7/7 done. Arms are in $Work\armA and $Work\armB"
Set-Location $Root
