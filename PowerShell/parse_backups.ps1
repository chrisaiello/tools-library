$PSSBackupLogPath = 'C:\path\logs\Backup.log'

$MostRecentSuccess = 'none'
$MostRecentFailure = 'none'
$SuccessDateTime = [DateTime]'01/01/1999'
$FailureDateTime = [DateTime]'01/01/1999'
$InitialDate = [DateTime]'01/01/1999'
$CurrentDate = Get-Date
#write-host $CurrentDate.AddDays(-5)

$SuccessString = 'Scheduled backup completed successfully' #Strings to search for in the log file
$FailureString = 'Scheduled backup failed to execute'

$BackupListSuccess = New-Object System.Collections.ArrayList
$BackupListFailure = New-Object System.Collections.ArrayList

$dateFormat = 'yyyy-MM-dd HH:mm:ss'

$result = 'null'


foreach($line in Get-Content $PSSBackupLogPath){

    if($line -match $SuccessString){
        [void]$BackupListSuccess.Add($line) #Collect list of backup successes
        #write-host $line

    }elseIf($line -match $FailureString){ #Collect list of backup failures
        [void]$BackupListFailure.Add($line)
        #write-host $line
    }
}

if ($BackuplistSuccess.Count -ge 1){
    
    $MostRecentSuccess = $BackupListSuccess[$BackupListSuccess.Count-1]
    #write-host 'Most recent backup:' $MostRecentSuccess

    $SuccessDateTime =[Datetime]::ParseExact($MostRecentSuccess.Substring(0,19), $dateFormat, $null) #Convert string to DateTime object
    #write-host 'Most recent backup SUCCESS: '$SuccessDateTime
    
}
if ($BackupListFailure.Count -ge 1){

    $MostRecentFailure = $BackupListFailure[$BackupListFailure.Count-1]
    #write-host 'Most recent failure:' $MostRecentFailure

    $FailureDateTime =[Datetime]::ParseExact($MostRecentFailure.Substring(0,19), $dateFormat, $null)
    #write-host 'Most recent backup FAILURE: '$FailureDateTime
}
if ( ($BackupListSuccess.Count -lt 1) -AND ($BackupListFailure.Count -lt 1) ){
    #write-host 'There is no recent backup in the log'
    $result = '!FAILURE: There is no recent backup in the log'
    Write-Warning $result
    exit
}

if ( ($SuccessDateTime -ne $InitialDate) -OR ($FailureDateTime -ne $InitialDate) ){

    if ($FailureDateTime -gt $SuccessDateTime){

        if($SuccessDateTime -gt $CurrentDate.AddDays(-4)){
            $result = '!WARNING: There is a recent backup, ( '+$SuccessDateTime+' ) but the latest backup failed on: '+$FailureDateTime
            Write-Warning $result
            exit
        }
        $result = '!FAILURE: There has been a recent backup failure on: '+$FailureDateTime +"`nThe most recent successful backup was: "+$SuccessDateTime
        Write-Warning $result
        exit
    }
    elseif ($SuccessDateTime -gt $FailureDateTime){

        if($SuccessDateTime -gt $CurrentDate.AddDays(-4)){
            $result = '!SUCCESS: There has been a recent backup on: '+$SuccessDateTime
            Write-Output $result
            exit
        }
        elseif($SuccessDateTime -lt $CurrentDate.AddDays(-4)){
            $result = '!FAILURE: The backup is old, last backup was: '+$SuccessDateTime
            Write-Warning $result
            exit
        }

    }

}



