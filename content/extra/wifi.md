---
title: "Wifi"
date: 2023-12-02T19:48:16+01:00
draft: false
---

## Connexion au WiFi
### Position du problème
- Si la Raspberry est connectée en WiFi et non en filaire, lors d'une panne de courant, la Raspberry se mettra en route **AVANT** que la WiFi ne soit disponible
- La Raspberry sera alors incapable de se connecter au WiFi
- Le logiciel sera opérationnel, avec prises de photos, stockage dans la base de données... Mais le site ne sera pas accessible
- La Raspberry ne sera même pas accessible en `ssh` et il ne sera donc pas possible de la rebooter à distance
- La seule solution est alors de débrancher la Raspberry et de la rebrancher pour qu'elle se connecte au WiFi au redémarrage
### Script de test de connexion
- Une solution est proposée par [dweeber](https://github.com/dweeber/WiFi_Check/blob/master/WiFi_Check)
- Dans cet esprit, on peut proposer un script python qui va tester la connexion WiFi régulièrement en lançant un [ping](https://fr.wikipedia.org/wiki/Ping_(logiciel))
- En absence de réponse, une commande lance la connexion WiFi
### Procédure
#### Vérifier le fichier&nbsp;*wpa_supplicant.conf*
- Voir [la page LinuxHint](https://linuxhint.com/connect-raspberry-pi-wifi-using-terminal/) et le [forum ArchiLinux](https://bbs.archlinux.org/viewtopic.php?pid=1324810#p1324810)
- Ouvrir le fichier  
```sh
sudo nano /etc/wpa_supplicant/wpa_supplicant.conf
```
- Si le contenu est du type 
```sh
ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
update_config=1
country=FR

network={
        ssid="<monReseau>"
        psk="<monMotDePasse>"
        key_mgmt=WPA-PSK
}
```
- Vérifier juste que le nom du réseau et le mot de passe sont corrects
- Sinon effacer le fichier et écrire les lignes précédentes en ajustant le nom de votre réseau et le mot de passe
- Sauvegarder si besoin et fermer
<!-- #### Blacklister&nbsp;*hp_wmi*
- Dans le terminal, **toujours en root**, taper
```sh
echo "blacklist hp_wmi" > /etc/modprobe.d/hp.conf
```

- Rebooter le système par `reboot`
- Une fois la Raspberry redémarrée et reconnectée en `ssh`
- Se remettre en *root* : `sudo su`
- Taper dans la ligne de commande
```sh
rfkill unblock all
```
- Quitter le mode superutilisateur : `Ctrl + D` -->
#### Ecrire le script de vérification/reconnexion de la WiFi
- Ouvrir le fichier *wifi.py* en écriture
```sh
nano ~/script/wifi.py
```
- Copier/coller le contenu suivant
```python
'''Script qui vérifie si la WiFi est connectée ; si elle ne l'est pas : la connecte
Au préalable il faut être sur qu'un réseau est joignable et s'assurer que les commandes ip link down et up sont fonctionnelles'''

import subprocess

site = 'www.google.fr'

ping = f'ping -c1 {site}'
pingReturn = subprocess.run(ping, shell=True, stdout=subprocess.PIPE).stdout

if pingReturn:
    print("wifi fonctionne déjà")
    pass
else:
    print("wifi va se remettre")
    wifiUp = "sudo rfkill unblock all && sudo ip link set wlan0 up"
    subprocess.run(wifiUp, shell=True)
    print("done")

```
- Sauvegarder et quitter : `Ctrl + O + X`
- Ouvrir le crontab : `crontab -e`
- Lancer le script *wifi.py* toutes les 5 minutes (par exemple) en ajoutant à la fin du `crontab`
```sh
*/5 * * * * python3 /home/pi/script/wifi.py
```
- Sauvegarder et quitter le `crontab`


