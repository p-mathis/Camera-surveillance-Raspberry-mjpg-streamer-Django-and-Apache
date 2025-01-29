'''Script qui vérifie si la WiFi est connectée ; si elle ne l'est pas : la connecte
Au préalable il faut être sur qu'un réseau est joignable et s'assurer que les commandes ip link down et up sont fonctionnelles'''

import subprocess

# Test de ping pour savoir si wifi connectée
site = 'www.google.fr'
ping = f'ping -c1 {site}'
pingReturn = subprocess.run(ping, shell=True, stdout=subprocess.PIPE).stdout

if pingReturn:
    # si ping donne réponse
    print("wifi fonctionne déjà")
else:
    # sinon remettre la wifi
    print("wifi va se remettre")
    wifiUp = "sudo ip link set wlan0 up"
    subprocess.run(wifiUp, shell=True)
    print("done")

