$h = Get-FileHash .\Network\vpnSetup.ps1 -Algorithm SHA256
$h.Hash > ./Network/vpnSetup.sha256.txt

$h = Get-FIleHash .\Network\vpnSetup.ps1 -Algorithm SHA512
$h.Hash > ./Network/vpnSetup.sha512.txt