<#
  HOKO social auto-poster — Windows setup (run once on the PC, in PowerShell from the repo root):

      powershell -ExecutionPolicy Bypass -File tools\social\install-tasks.ps1

  Creates two Task Scheduler jobs for the current user:
    "HOKO Social Runner"  every 15 min   python -m tools.social run
    "HOKO Social Topup"   daily 23:00    python -m tools.social topup --render
  Disables the old "HOKO publish" job (content/youtube publish) so IG / YT aren't posted twice.
  Sets the PC to never sleep / hibernate on mains power (the runner must be awake at the slots).
  Prints which env keys are missing (names only, never values). Keys are read from User environment
  variables — set them with:  [Environment]::SetEnvironmentVariable('KEY','value','User')
#>
param(
  [string]$Python = 'python',
  [string]$Repo = (Resolve-Path (Join-Path $PSScriptRoot '..\..')).Path
)
$ErrorActionPreference = 'Stop'

$keys = 'META_PAGE_TOKEN','IG_BUSINESS_ID','FB_PAGE_ID','YT_CLIENT_ID','YT_CLIENT_SECRET','YT_REFRESH_TOKEN',
        'PINTEREST_TOKEN','PINTEREST_BOARD_ID','DISCORD_WEBHOOK_PICKUPS','DISCORD_WEBHOOK_TIKTOK_QUEUE',
        'TIKTOK_ENABLED','TIKTOK_CLIENT_KEY','TIKTOK_CLIENT_SECRET','TIKTOK_REFRESH_TOKEN',
        'SHOPIFY_STORE','SHOPIFY_ADMIN_TOKEN'
Write-Host "Env keys (User scope):"
foreach ($k in $keys) {
  $v = [Environment]::GetEnvironmentVariable($k, 'User')
  if ([string]::IsNullOrEmpty($v)) { Write-Host ("  {0,-30} MISSING" -f $k) -ForegroundColor Yellow }
  else { Write-Host ("  {0,-30} set" -f $k) }
}

# Python deps the poster needs (requests; tzdata for Australia/Melbourne on Windows)
& $Python -m pip install --quiet --upgrade requests tzdata
if ($LASTEXITCODE -ne 0) { throw "pip install failed" }

New-Item -ItemType Directory -Force -Path (Join-Path $Repo 'data') | Out-Null
$logFile = Join-Path $Repo 'data\social-runner.log'

function New-HokoAction([string]$cliArgs) {
  $cmd = "cd /d `"$Repo`" && `"$Python`" -m tools.social $cliArgs >> `"$logFile`" 2>&1"
  New-ScheduledTaskAction -Execute 'cmd.exe' -Argument "/c $cmd" -WorkingDirectory $Repo
}

$settings = New-ScheduledTaskSettingsSet -StartWhenAvailable -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries `
  -WakeToRun -MultipleInstances IgnoreNew -ExecutionTimeLimit (New-TimeSpan -Hours 2)
$principal = New-ScheduledTaskPrincipal -UserId "$env:USERDOMAIN\$env:USERNAME" -LogonType Interactive -RunLevel Limited

$start = (Get-Date).Date.AddHours((Get-Date).Hour).AddMinutes([math]::Ceiling((Get-Date).Minute / 15) * 15)
$runnerTrigger = New-ScheduledTaskTrigger -Once -At $start -RepetitionInterval (New-TimeSpan -Minutes 15)
Register-ScheduledTask -TaskName 'HOKO Social Runner' -Action (New-HokoAction 'run') -Trigger $runnerTrigger `
  -Settings $settings -Principal $principal -Description 'Posts / schedules due social items (tools/social)' -Force | Out-Null

$topupTrigger = New-ScheduledTaskTrigger -Daily -At '23:00'
Register-ScheduledTask -TaskName 'HOKO Social Topup' -Action (New-HokoAction 'topup --render') -Trigger $topupTrigger `
  -Settings $settings -Principal $principal -Description 'Keeps content/social-queue.json 14 days ahead + renders clips' -Force | Out-Null

# old single-post job from content/youtube would double-post IG + YT
if (Get-ScheduledTask -TaskName 'HOKO publish' -ErrorAction SilentlyContinue) {
  Disable-ScheduledTask -TaskName 'HOKO publish' | Out-Null
  Write-Host 'Disabled old task "HOKO publish" (replaced by HOKO Social Runner).'
}

# never sleep on mains power
powercfg /change standby-timeout-ac 0
powercfg /change hibernate-timeout-ac 0
powercfg /change monitor-timeout-ac 30

Get-ScheduledTask -TaskName 'HOKO Social*' | Select-Object TaskName, State | Format-Table -AutoSize
Write-Host "Logs: $logFile   ·   post log: data\social-post-log.csv"
Write-Host "Test without posting:  $Python -m tools.social dry-run"
