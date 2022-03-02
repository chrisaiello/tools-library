$current_name = $env:COMPUTERNAME

$invalid_name_regex="AA-.*-.*"

if($current_name -match $invalid_name_regex){

    $new_name=$current_name.Replace("AA-","AA")
    write-output "Name is $current_name, changing name to $new_name"
    
    $result = Rename-Computer -NewName $new_name -Force -PassThru

    write-output $Result


}else{
    write-output "Name is $current_name, not changing name"
}