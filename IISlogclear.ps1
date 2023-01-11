
#IIS LOG CLEAR
#used to clear IIS VMs of old logs

$LogPath = "C:\inetpub\logs\LogFiles"
$ErrLogPath = "C:\Windows\System32\LogFiles\HTTPERR"

$InstanceLogPath = "C:\inetpub\"

$maxDaystoKeep = -5

$instanceMaxDaystoKeep = -14

Set-Location -Path $LogPath

$itemsToDelete = Get-ChildItem $LogPath -Filter *.log -Recurse | Where LastWriteTime -lt ((get-date).AddDays($maxDaystoKeep))

Set-Location -Path $ErrLogPath
$errLogsToDelete = Get-ChildItem $ErrLogPath -Filter *.log -Recurse | Where LastWriteTime -lt ((get-date).AddDays($maxDaystoKeep))

Set-Location -Path $InstanceLogPath
$instanceLogsToDelete = Get-ChildItem $InstanceLogPath -Filter 'App_data' -Recurse | Where-Object {$_.PSIsContainer } | Get-ChildItem -Filter *.log* -Recurse | Where LastWriteTime -lt ((get-date).AddDays($instanceMaxDaystoKeep))
# IIS logs
If ($itemsToDelete.Count -gt 0){
ForEach ($item in $itemsToDelete){
Get-item $item.FullName | Remove-Item -Verbose
}

Write-Output "IIS Log Retention: Cleanup of log files older than $((get-date).AddDays($maxDaystoKeep)) completed..."
}
Else
{
Write-Output "IIS Log Retention: No items to be deleted today $($(Get-Date).DateTime)"
}

# HTTPERR logs

If ($errLogsToDelete.Count -gt 0){
ForEach ($item in $errLogsToDelete){
Get-item $item.FullName | Remove-Item -Verbose
}

Write-Output "Err Log Retention: Cleanup of log files older than $((get-date).AddDays($maxDaystoKeep)) completed..."
}
Else
{
Write-Output "Err Log Retention: No items to be deleted today $($(Get-Date).DateTime)"
}

# inetpub Instance Logs
If ($instanceLogsToDelete.Count -gt 0){
ForEach ($item in $instanceLogsToDelete){
Get-item $item.FullName | Remove-Item -Verbose
}
Write-Output "inetpub Log Retention: Cleanup of customer IIS log files older than $((get-date).AddDays($instanceMaxDaystoKeep)) completed..."
}
Else
{
Write-Output "inetpub Log Retention: No items to be deleted today $($(Get-Date).DateTime)"
}

Start-Sleep -Seconds 3




