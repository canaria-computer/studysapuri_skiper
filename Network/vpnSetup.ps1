$vpnNmae = "vpn Gate - L2TP"

# confirm
Write-Host "Do you want to start VPN Gate (https://www.vpngate.net/ja/) setup?"

do{
    $isConfirm = Read-Host "Yes/No"
} while(-not ($isConfirm  -in @("yes","no")))

if($isConfirm -eq "no"){
    exit
}

Add-VpnConnection -Name $vpnNmae -ServerAddress "public-vpn-116.opengw.net" -TunnelType L2tp -EncryptionLevel Maximum -L2tpPsk "vpn" -RememberCredential -Force
rasdial.exe $vpnNmae "vpn" "vpn"

Read-Host "If your computer is using Proxy and you are having trouble with VPN, turn it off."
