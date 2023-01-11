#BCP Rename script
#Used for customer to rename batch of BC files on monthly basis

$path = [INSERT PATH]
$files = Get-ChildItem -Path $path -File

foreach ($file in $files) {
    $newName = $file.Name.Substring($file.Name.LastIndexOf("-") + 1)
    Rename-Item -Path $file.FullName -NewName $newName
}
