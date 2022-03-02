$AutomateClientName = "%clientname%"
$AutomateClientName = $AutomateClientName.Trim()
$AutomateLocationName = "%locationname%"
$AutomateLocationName = $AutomateLocationName.Trim()

$ForceInstall = '@ForceInstall@'

$path = "%TEMP%"

If (!(Test-Path -Path $path)) {
    New-Item -Path $path -ItemType Directory -Force | Out-Null
}



$RMM_API_KEY = ""

$RMM_API_URL_BASE = "https://www.am.remote.management/api/"

$clientList = @{}
$siteList = @{}

#Check for agent and exit if already installed, unless ForceInstall=1

$ChkAgent = Get-ChildItem -Path HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall, HKLM:\SOFTWARE\Wow6432Node\Microsoft\Windows\CurrentVersion\Uninstall |
Get-ItemProperty | Where-Object { $_.DisplayName -match "Advanced Monitoring Agent" } #checks for existing Agent install
        
if (($ChkAgent) -and !$ForceInstall) {   
    Write-Output "RMM Agent is already installed, set ForceInstall to 1 to ignore this check"
    Exit 1001
}


$Parameters = @{
    apikey  = $RMM_API_KEY
    service = "list_clients"
}

$xmlresponse = Invoke-RestMethod -Uri $RMM_API_URL_BASE -Body $Parameters -Method Get

$xmlresponse.result.items.client | ForEach-Object {

    $clientList.Add($_.name.innertext.Trim(), $_.clientid)
}

$specificClientID = $ClientList.$AutomateClientName

$Parameters = @{
    apikey   = $RMM_API_KEY
    service  = "list_sites"
    clientid = $specificClientID
}

$xmlresponse = Invoke-RestMethod -Uri $RMM_API_URL_BASE -Body $Parameters -Method Get

$xmlresponse.result.items.site | ForEach-Object {

    $siteList.Add($_.name.innertext, $_.siteid)
}

$specificSiteID = $SiteList.$AutomateLocationName

Write-Output "$AutomateClientName has ID $specificClientID in RMM and site $AutomateLocationName has ID $specificSiteID"

$Parameters = @{
    apikey        = $RMM_API_KEY
    service       = "get_site_installation_package"
    endcustomerid = $specificClientID
    siteid        = $specificSiteID
    os            = "windows"
    type          = "remote_worker"
}

Invoke-RestMethod -Uri $RMM_API_URL_BASE -Body $Parameters -Method Get -Outfile "$path\$specificSiteID.zip"

Write-Output "Downloaded installer for $AutomateClientName site $AutomateLocationName to $path\$specificSiteID.zip"

# Expand-Archive requires PS 5.0 or later
#Expand-Archive -Path "$path\$specificSiteID.zip" -DestinationPath "$path\$specificSiteID"

# Unzip for older PS versions

New-Item -ItemType directory -Path "$path\$specificSiteID" -Force

$shell = New-Object -ComObject Shell.Application
$zip = $shell.Namespace("$path\$specificSiteID.zip")
$items = $zip.items()
$shell.Namespace("$path\$specificSiteID").CopyHere($items, 1556)


Write-Output "Expanded ZIP archive"

if ($ForceInstall -eq 2){
    Remove-Item -Recurse -Force "C:\Program Files (x86)\Advanced Monitoring Agent\"
    Write-Output "Removed existing agent install path"
}

$installerEXE = Get-ChildItem "$path\$specificSiteID\"
$installerEXE = "$path\$specificSiteID\$InstallerEXE"
                    
$AgentInstall = (Start-Process -FilePath "$installerEXE" -PassThru -Wait).ExitCode
$AgentInstall

if ($AgentInstall -ne "0") {
    Write-Output "There was an error installing the RMM Agent"
    Exit 1002
}
Else {
    Write-Output "RMM Agent Installed Successfully"
    Exit 0
}


