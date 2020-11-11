#! /bin/bash
ip = "$1"
channelplan = "$2"
##app_File = "$3"
lbtEnabled = false
password = "Multitech_123"

if [!$1 !$2]
then
    echo "Please include the ip address and the channel plan of the conduit in the command line"
    exit 1
fi

echo "Preparing conduit on the ip address $ip"

echo "loggin in and preparing token."

####Comissioning mode
echo "Starting commissioning..."
curl -k "https://$ip/api/commissioning" 
##set username 
aas_ID=$(curl -k -X POST -H "Content-Type: json/apaas_IDplication" -d '{"username":"admin", "aasID": "", "aasAnswer":""}' https://$ip:443/api/commissioning | jq -r '.result.aasID' )
##set password
curl -k -X POST -H "Content-Type: json/application" -d '{"username":"admin", "aasID":"'"$password"'", "aasAnswer":"Admin123"}' https://$ip:443/api/commissioning 2>/dev/null &
##confirm password
curl -k -X POST -H "Content-Type: json/application" -d '{"username":"admin", "aasID":"'"$password"'", "aasAnswer":"Admin123"}' https://$ip:443/api/commissioning 2>/dev/null &
echo "-- comissioning Done--"
## end comminsioning..

#####change password

##login and save token
token=$(curl -k "https://$ip/api/login?username=admin&password=$password" | jq -r '.result.token' ) 
echo "recieved token: $token"
pwd = "MTCDT-"
lora_username="$pwd$(curl -k "https://$ip/api/system?token=$token" | jq -r '.result.deviceId')"
aas_ID=$(curl -k -X POST -H "Content-Type: json/application" -d '{"username":"admin", "aasID": ""}' https://$ip/api/command/passwd?token=$token1 |jq -r '.result.aasID')

curl -k -X POST -H "Content-Type: json/application" -d '{"username":"admin", "aasID": "'"$aas_ID"'", "aasAnswer":"'"$password"'"}' https://$ip/api/command/passwd?token=$token 2>/dev/null &
curl -k -X POST -H "Content-Type: json/application" -d '{"username":"admin", "aasID": "'"$aas_ID"'", "aasAnswer":"'"$password"'"}' https://$ip/api/command/passwd?token=$token 2>/dev/null &
curl -k -X POST -H "Content-Type: json/application" -d '{"username":"admin", "aasID": "'"$aas_ID"'", "aasAnswer":"'"$password"'"}' https://$ip/api/command/passwd?token=$token 2>/dev/null &
curl -k -X POST -H "Content-Type: json/application" -d '{"username":"admin", "aasID": "'"$aas_ID"'", "aasAnswer":"'"$lora_username"'"}' https://$ip/api/command/passwd?token=$token 2>/dev/null &
curl -k -X POST -H "Content-Type: json/application" -d '{"username":"admin", "aasID": "'"$aas_ID"'", "aasAnswer":"'"$lora_username"'"}' https://$ip/api/command/passwd?token=$token 2>/dev/null &
curl -k -X POST -H "Content-Type: json/application" -d '{"username":"admin", "aasID": "'"$aas_ID"'", "aasAnswer":"'"$lora_username"'"}' https://$ip/api/command/passwd?token=$token 2>/dev/null &
password = lora_username
##end change password



echo "get system info"
curl -k "https://$ip/api/system?token=$token1" 2>1&
device_id = $(curl -k "https://$ip/api/system?token=$token1" | jq -r '.result.deviceId')
lora_username ="MTCDT-$device_id"
export lora_username
case $channelplan in
as932-japan)
    channelplan = "AS923"
    lbtEnabled = true
    ;;
kr920)
    lbtEnabled = true
    ;;
esac
#####enable WiFi Accesspoint#####
echo "Enabling Wi-Fi-AP $lora_username"
`curl -kX PUT -H 'Content-Type: application/json' -d '{"ap":{"enabled":true,"security":{"algorithm":"TKIP","mode":"WPA2-PSK","psk":"'"$password"'"},"ssid":"'"$lora_username"'"}}' "https://$ip/api/wifi/?token=$token1}" 2>/dev/null &

echo "Enabling LoRa, setting join delay to 5, channel plan to $channelplan and lbtEnabled to $lbtEnabled"
curl -kX PUT -H "Content-Type: application/json" -d '{ "lora": { "enabled": true, "joinDelay":5, "channelPlan": "'"$channelplan"'", "lbtEnabled": "'"$lbtEnabled"'"} }' "https://$ip/api/loraNetwork?token=$token1" 2>/dev/null &

echo "setting the lora username and password to $lora_username"
curl -kX PUT -H "Content-Type: application/json" -d '{ "network":{ "public":1, "name": "'"$lora_username"'", "passphrase": "'"$lora_username"'"}" } }' "https://$ip/api/loraNetwork/?apply=now&token=#$token1}" 2>/dev/null &

echo "setting fsb to 1 $lora_username"
curl -kX PUT -H "Content-Type: application/json" -d '{ "lora":{"frequencySubBand":1} }' "https://$ip/api/loraNetwork/?apply=now&token=$token1" 2>/dev/null &

puts "get LoRa fsb, name, passphrase "
json = $(curl -k "https://${ip}/api/loraNetwork?token=$token1" 2>/dev/null &)
echo "Lora name:   $($json | jq -r '.result.network.name')"
echo "Lora passphrase:  $($json | jq -r '.result.network.passphrase')"
echo "Lora public  $($json | jq -r '.result.network.public')"
echo "Lora: fsb   $($json | jq -r '.result.lora.frequencysubBand')"
echo "Lora: enabled $($json | jq -r '.result.lora.enabled')"
echo "Lora: joinDelay $($json | jq -r '.result.lora.joinDelay')"
echo "Lora: channelplan $($json | jq -r '.result.lora.channelPlan')"
echo "Lora: lbtEnabled  $($json | jq -r '.result.lora.lbtEnabled')"

###Install python app to conduit
##curl -k -X POST -H "Content-Type: json/application" -d '{"info":{"fileName":"'"$app_File"'","fileSize":}}' $ip/api/command/app_pre_upload?token=$token1
##curl -i -k -b /tmp/headers --http1.0 -F file=@$app_File "https://$ip/api/command/app_upload?token=$token1"
##curl -k -X POST -H "Content-Type: json/application" -d '{"info":{"appId":"5a8f0828feab4f747f818781","appName":"Starterkit,"appFile":"'"$app_File"'"}}' https:$ip/api/command/app_install?token=$token1



echo "First time Setup"
curl -kX PUT -H 'Content-Type: application/json' -d '{ "firstTimeSetup": true }' "https://$ip/api/system?token=$token1" 2>1&
##save and apply changes
curl -k -X POST -d "" "https://#{ip}/api/command/save?token=$token1" 2>/dev/null &
echo "saving user defined defaults"
curl -k -X POST -d "" "https://$ip/api/command/save_oem?token=$token1" 2>/dev/null
sleep 5
echo "save and restart conduit"
curl -k -X POST -d "" "https://$ip/api/command/save_restart?token=$token1" 2>/dev/null
echo "waiting for reboot"
sleep 4m 45s
token1= ""
echo "verifying it rebooted ok"
while [!$token1]
do 
    token1 = $(curl -k "https://$ip/api/login?username=admin&password=$password" | jq -r '.result.token' ) 
    sleep 1
    echo "reboot ok" if $token1
done


