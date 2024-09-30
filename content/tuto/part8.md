---
title: "Tutoriel : Partie 8 - Ajouter une caméra"
date: 2023-10-16T10:33:28+01:00
draft: false
---

## Position du problème
- D'autres caméras peuvent être installées en fonction :
    - du nombre de ports USB disponibles
    - de la puissance de la Raspberry
- Ceci nécessite la modification ou la création de plusieurs fichiers
- Les actions vont être les suivantes
    - Répertorier la nouvelle caméra
    - Modifier le fichier `configuration.ini`
    - Créer un dossier de stockage des photos de la nouvelle caméra
    - Modifier ou créer les scripts `python` qui gérent la nouvelle caméra
        - Créer le script de lancement
        - Modifier le script de suppression des photos
        - Modifier le script de stockage des photos
        - Modifier le cron
    - Créer la caméra dans la base de données
    - Modifier les fichiers `urls.py` et `views.py` de l'application `camera`
        - Modifier le fichier `urls.py`
        - Modifier le fichier `views.py`
            - modifier la fonction `historique`
            - modifier la fonction `parHeure`
            - ajouter la fonction `stream_3`
            - modifier la fonction `stream_AllCam`
    - Modifier ou créer les fichiers `html`
        - Créer le fichier `stream_3.html`
        - Modifier le fichier `base.html`
        - Modifier le fichier `historique.html`
        - Modifier le fichier `parHeure.html`
        - Modifier le fichier `stream_AllCam.html`
    - Modifier le fichier de configuration du serveur `apache2`
## Répertorier la caméra
- Dans le répertoire `/dev/v4l/by-id` répertorier l'identifiant de la nouvelle caméra USB
```sh
ls /dev/v4l/by-id
```
- Noter la valeur `index-O` de la nouvelle caméra
## Modifier le fichier&nbsp;*configuration.ini*
- Ouvrir le fichier config.ini en écriture  
```sh
sudo nano /etc/camera/configuration.ini
```
### Dans la section&nbsp;*\[hosts\]*
- Ajouter un proxy pour la nouvelle caméra
```sh
proxy_3=Rp3
```
### Dans la section&nbsp;*\[camera\]*
- Ajouter 
    - un nouveau port
    - le nom de la caméra
    - la résolution choisie
    - le nombre d'images secondes
- Par exemple : 
    - `cam_3_port=8083`
    - `cam_3_name=usb-046d_08ce_53892EC2-video-index0`
    - `cam_3_resol=640x480`
    - `cam_3_fps=5`

### Dans la section&nbsp;*\[paths\]*
- Ajouter un path pour la caméra
- Par exemple :
    - `pathCamera_3=Camera_3`

### Dans la section&nbsp;*\[frequences\]*
- Ajouter un temps d'attente pour le lancement de la caméra
- Par exemple :
    - `delay_run_Cam_3=100`
### Fichier final
- Le fichier ressemblera au fichier consultable [ici]({{< ref "/script/configuration_ini_4cam.md" >}} "configuration_ini_4cam")

## Créer le dossier de stockage pour la caméra
- Par exemple :
```sh
sudo mkdir /var/www/stock/Camera_3
```
- Accorder les droits ad hoc
```sh
sudo chown -R pi /var/www/stock/Camera_3
```
## Ecrire et modifier les scripts python pour la caméra
### Le script de lancement
- Créer le script de lancement
```sh
nano ~/script/runCamera_3.py
```
- Ecrire dans ce fichier le même script que pour les fichiers des autres caméras, en adaptant les différentes variables
- Un exemple de fichier est disponible [ici]({{< ref "/script/runCamera_3_py_4cam.md" >}} "runCamera_3_py_4cam
")
### Modifier le fichier de suppression des photos 
- Ouvrir le fichier suppressFiles 
```sh
nano ~/script/suppressFiles.py
```
- Ajouter dans ce fichier le chemin relatif du fichier de stockage depuis le fichier `configuration.ini`
```python
pathCamera_3 = parser.get("paths", "pathCamera_3")
```
- Ajouter la commande de suppression des fichiers
```python
command_3 = ["find", f'{stock}/{pathCamera_3}', "-mtime", f'+{str(delay_delete)}', "-delete"]
```
- Ajouter le lancement de cette commande
```python
run(command_3)
```
- Le fichier ressemblera au fichier consultable [ici]({{< ref "/script/suppressFiles_py_4cam.md" >}} "suppressFiles_py_4cam
")
### Modifier le fichier de stockage des photos
- Ouvrir le fichier de stockage des photos
```sh
nano ~/script/getCamerasAndRegister.py
```
- Ajouter dans ce fichier le chemin relatif du fichier de stockage
```python
pathCamera_3 = parser.get("paths", "pathCamera_3")
```
- Ajouter le port de la caméra
```python
cam_3_port = parser.get("camera", "cam_3_port")
```
- Ajouter le chemin absolu du fichier de stockage
```python
path_3 = f'{stock}/{pathCamera_3}'
```
- Ajouter la commande de récupération et de copie des snapshots
```python
command_3 = 'wget http://{}:{}/?action=snapshot -O {}/{}.jpg'.format(host, cam_3_port, path_3, name)
```
- Modifier la commande générale `command` en ajoutant `command_3`
```python
command = '{} & {} & {} & {}'.format(command_1, command_2, command_py, command_3)
```
- Ajouter la commande de copie des images dans la base de données
```python
 c.execute("INSERT INTO {}_photo(date, appareil_id, name, path) VALUES (?, '4', ?, ?)".format(appli), (date, name, pathCamera_3))
```
- *La base de données numérote les caméras (`appareil_id`) par ordre de saisie*
- *La caméra surajoutée est, ici, la quatrième caméra, ce qui explique qu'elle a l'identifiant `4`*
- Le fichier de stockage ressemblera au fichier consultable [ici]({{< ref "/script/getCamerasAndRegister_py_4cam.md" >}} "getCamerasAndRegister_py_4cam
")

### Modifier le cron
- Le fichier de mise en route de la nouvelle caméra doit être lancé par le cron lors du démarrage de la raspberry
- Ouvrir le cron en édition
```sh
crontab -e
```
- Ajouter la ligne
```sh
@reboot python3 /home/pi/script/runCamera_3.py
```

## Créer la caméra dans la base de données
- **Se mettre en environnement virtuel**
```sh
source ~/folder/folder_venv/bin/activate
```
- Ouvrir la `console interactive` pour créer la caméra
```sh
(venv) python ~/folder/project/manage.py shell
```
- Vérifier le nombre actuel de caméras
```sh
>>> from camera.models import Appareil
>>> Appareil.objects.all()
<QuerySet [<Appareil: Cam_1>, <Appareil: Cam_2>, <Appareil: Cam_py>]>
```
- Créer la caméra
```sh
>>> c = Appareil(name="Cam_3")
>>> c.save()
```
- Vérifier la création de la caméra
```sh
>>> Appareil.objects.all()
<QuerySet [<Appareil: Cam_1>, <Appareil: Cam_2>, <Appareil: Cam_py>, <Appareil: Cam_3>]>
```
- La caméra est bien créée
- Quitter la console : `Crtl+D`
- On peut maintenant quitter l'environnement virtuel
```sh
(venv) deactivate
```
## Modifier les fichiers&nbsp;*urls*&nbsp;et&nbsp;*views*&nbsp;de Django
### Modifier le fichier&nbsp;*urls\.py*&nbsp;dans&nbsp;*\~\/folder\/project\/camera*
- Ouvrir le fichier
```sh
nano ~/folder/project/camera/urls.py
```
- Ajouter dans `urlpatterns` le `path` du stream de la nouvelle caméra
```python
path('stream_3/', views.stream_3, name="stream_3"),
```
- Le fichier modifié est consultable [ici]({{< ref "/script/urls_py_4cam.md" >}} "urls_py_4cam
")
### Modifier le fichier&nbsp;*views\.py*&nbsp;dans&nbsp;*\~\/folder\/project\/camera*
- Ouvrir le fichier
```sh
nano ~/folder/project/camera/views.py
```
- Ajouter les variables du fichier `configuration.ini` relatives à la nouvelle caméra
```python
cam_3_port = parser.get("camera", "cam_3_port")
Rp3 = parser.get("hosts", "proxy_3")
```
#### Modifier&nbsp;*def historique(request)*
- Ajouter chacune des lignes suivantes à la suite des lignes qui leur sont équivalentes

```python

latest_photo_list_3 = Photo.objects.filter(appareil=4).order_by('-date')[:display_nombre]

latest_photo_list_3_oneoutofN = []

for photo in latest_photo_list_3:      #pour ne sélectionner qu'une photo sur N
    if (photo.date - maintenant).seconds // hz_capture % hz_historique == 0:        
        latest_photo_list_3_oneoutofN.append(photo)
```
- Modifier la variable `min_length` en ajoutant la nouvelle caméra dans la liste
```python
min_length = min(len(latest_photo_list_1_oneoutofN), len(latest_photo_list_2_oneoutofN), len(latest_photo_list_py_oneoutofN), len(latest_photo_list_3_oneoutofN))
```
- Dans la dernière boucle `for` modifier la variable `new_group` en ajoutant la nouvelle caméra dans la liste 
```python
new_group = [latest_photo_list_1_oneoutofN[i], latest_photo_list_2_oneoutofN[i], latest_photo_list_py_oneoutofN[i], latest_photo_list_3_oneoutofN[i]] 
```
- Les dernières lignes de la fonction doivent ressembler à ceci
```python
    latest_photo_list_group = [] 
    for i in range(min_length):
        new_group = [latest_photo_list_1_oneoutofN[i], latest_photo_list_2_oneoutofN[i], latest_photo_list_py_oneoutofN[i], latest_photo_list_3_oneoutofN[i]] 
        latest_photo_list_group.extend(new_group)
    
    context = {
        'latest_photo_list_group': latest_photo_list_group,
    }  
```


#### Modifier&nbsp;*def parheure(request)*
- Ajouter la ligne suivante après `latest_photo_list_py ...`
```python
latest_photo_list_3 = Photo.objects.filter(appareil=4).order_by('-date')[:display_nombre]
```
- Modifier la valeur de `min_length ...` en ajoutant `len(latest_photo_list_3)`
```python
min_length = min(len(latest_photo_list_1), len(latest_photo_list_2), len(latest_photo_list_py), len(latest_photo_list_3))
```
- Modifier la boucle `for i in range(min_length):` en ajoutant la nouvelle caméra à la liste `new_group`
```python
new_group = [latest_photo_list_1[i], latest_photo_list_2[i], latest_photo_list_py[i], latest_photo_list_3[i]] 
```
- La boucle `for` doit donc ressembler à ceci
```python
for i in range(min_length):
    new_group = [latest_photo_list_1[i], latest_photo_list_2[i], latest_photo_list_py[i], latest_photo_list_3[i]] 
    latest_photo_list_group.extend(new_group)
```
- Dans la varaible `paginator` modifier éventuellement le nombre d'éléments par page en mettant, par exemple, `240` au lieu de `180` (*240 permet de visualiser les photos d'une heure complète si on prend une photo toutes les minutes*). 
```python
paginator = Paginator(latest_photo_list_group, 240)
```
#### Ajouter la fonction&nbsp;*stream_3*
- Après les trois fonctions `stream` ajouter :
```python
def stream_3(request):
    stream = ["/{}?action=stream".format(Rp3)]
    context = {
        'stream': stream,
    }
```
#### Modifier la fonction&nbsp;*stream_AllCam*
- Dans la liste `stream` ajouter `"/{}?action=stream".format(Rp3)`
```python
stream = ["/{}?action=stream".format(Rp1),"/{}?action=stream".format(Rp2),"/{}?action=stream".format(Rpi), "/{}?action=stream".format(Rp3)]
```
#### Fichier consultable
Le fichier `views.py` doit ressembler au fichier consultable [ici]({{< ref "/script/views_py_4cam.md" >}} "views_py_4cam
")
## Modifier les fichiers html (templates)
### Position du problème
- Nécessité de créer un fichier de streaming pour la nouvelle caméra : `stream_3.html`
- Modifier `base.html` pour ajouter la nouvelle caméra dans le menu 
- Modifier `historique.html` pour modifier le nombre d'éléments affichés par ligne
- Modifier `parHeure.html` pour modifier le nombre d'éléments affichés par ligne
- Modifier `stream_AllCam.html` pour ajouter la nouvelle caméra
- Toiletter divers fichiers `.html`
### Créer le ficher&nbsp;*stream_3.html*
- Créer le fichier en écriture
```sh
nano ~/folder/project/camera/templates/camera/stream_3.html
```
- Ecrire un contenu équivalent à celui des autres templates de streaming en :
    - modifiant le titre `<h2>`
    - adaptant l'attribut `alt` 
    - modifiant le texte de `<figcaption>`
    - modifiant le texte du bouton `<Direct n Caméras>`

- Un exemple de fichier est disponible [ici]({{< ref "/script/stream_3_html_4cam.md" >}} "stream_3_html_4cam")

### Modifier le fichier&nbsp;*base.html*
- Ouvrir le fichier en écriture
```sh
nano ~/folder/project/camera/templates/camera/base.html
```
- Repérer le bloc `{% block navebar %}` du `body`
- Dans ce bloc repérer la div `<div class="dropdown-content">`
- A la fin de cette div, après l'ancre vers la `Caméra 2` ajouter la ligne 
```html
<a href="/camera/stream_3/">Caméra 3</a>
```
- Un exemple de fichier est disponible [ici]({{< ref "/script/base_html_4cam.md" >}} "base_html_4cam
")

### Modifier le fichier&nbsp;*historique.html*
- Ouvrir le fichier en écriture
```sh
nano ~/folder/project/camera/templates/camera/historique.html
```
- Rechercher la ligne après la condition `{% else %}`
```html
{% if forloop.counter|divisibleby:"3" %}
```
- Remplacer cette valeur
    - soit par `4` ; vous afficherez les snapshots des 4 caméras sur une seule ligne
    - soit par `2` : dans ce cas on affiche 2 snapshots par ligne, ce qui est plus lisible sur un portable.
- Il est aussi possible de ne pas modifier cette valeur. Dans ce cas, 3 photos seront affichées par ligne, avec un décalage des caméras en passant d'une ligne à l'autre
- Un exemple de fichier est disponible [ici]({{< ref "/script/historique_html_4cam.md" >}} "historique_html_4cam
")

### Modifier le fichier&nbsp;*parHeure.html*
- Ouvrir le fichier en écriture
```sh
nano ~/folder/project/camera/templates/camera/parHeure.html
```
- Rechercher la ligne 
```html
{% if forloop.counter|divisibleby:"3" %}
```
- Remplacer cette valeur
    - soit par `4` ; vous afficherez les snapshots des 4 caméras sur une seule ligne
    - soit par `2` : dans ce cas on affiche 2 snapshots par ligne, ce qui est plus lisible sur un portable.
- Il est aussi possible de ne pas modifier le fichier. Dans ce cas, 3 photos seront affichées par ligne, avec un décalage des caméras en passant d'une ligne à l'autre
- Un exemple de fichier est disponible [ici]({{< ref "/script/parHeure_html_4cam.md" >}} "parHeure_html_4cam
")


### Modifier le fichier&nbsp;*stream_AllCam.html*
- Ouvrir le fichier en écriture
```sh
nano ~/folder/project/camera/templates/camera/stream_AllCam.html
```
- Modifier le titre dans la balise `<h1>` (`les 4 caméras en direct` par exemple)
- Ajouter le stream de la nouvelle caméra en ajoutant une balise `<td>` à la fin du fichier, avant la balise fermante de ligne (r pour row) `</tr>` qui précède la balise fermante du tableau `</table>`
```sh
<td>
    <a href="{% url 'stream_3' %}">        
        <img class="centre-image imgresponsive" src={{stream.3}} alt="Erreur sur la caméra 3" width="300" >                 
            <figcaption>CAMERA 3 : Streaming</figcaption>        
    </a>
</td>

```
- Si on laisse le fichier tel quel, les 4 caméras seront visibles sur la même ligne
- Cette lecture pouvant ne pas être très agréable, on peut créer une deuxième ligne : on aura ainsi deux caméras par ligne 
- Scinder le texte entre la balise ouvrante `<tr>` et la balise fermante `</tr>` en sélectionnant les deux premières cellules déterminées par les balises `<td>...</td>`
- Créer une deuxième ligne avec une balise `<tr>...</tr>`
- Y insérer la troisième cellule existante, délimitée par la troisième balise `<td>...</td>`
- Et ajouter la quatrième cellule comme définie plus haut
- Un exemple de fichier (*avec 2 caméras par ligne sur 2 lignes*) est disponible [ici]({{< ref "/script/stream_AllCam_html_4cam.md" >}} "stream_AllCam_html_4cam
")
### Toiletter divers fichiers&nbsp;*\.html*
- Un certain nombre de fichiers font référence à trois caméras et non quatre
- Il est possible de modifier le code `html` pour faire référence à quatre caméras
- Par exemple au niveau des `boutons` des fichiers de streaming (`stream_1.html, stream_2.html, stream_py.html`)
- Ces modificatins sont cosmétiques et non indispensables !
## Vérifier les éventuelles migrations de l'application&nbsp;*camera*
- A priori, aucune modification de `models.py` n'a eu lieu
- Il est cependant possible de vérifier qu'on n'a pas touché à cette partie de l'application `camera`
- Se mettre en environnement virtuel, puis vérifier les migrations
```sh
source ~/folder/folder_venv/bin/activate
(venv) python ~/folder/project/manage.py makemigrations
(venv) python ~/folder/project/manage.py migrate
```
## Modifier le fichier de configuration apache2 du site
### Modifier le fichier
- Ouvrir le fichier en écriture
```sh
sudo nano /etc/apache2/sites-available/project-camera.conf
```
- Après la balise fermante `</location>` du `VirtualHost *:443` chercher les lignes `ProxyPass` et `ProxyPassReverse`
- Ajouter les deux lignes
```sh
ProxyPass /Rp3 http://< localIP Raspberry >:8083/
ProxyPassReverse /Rp3 http://< localIP Raspberry >:8083/
```
- **Changer `<localIP>` par l'IP locale de la raspberry** (par exemple : `ProxyPass /Rp3 http://192.168.1.49:8083/`)
- Rajouter ces deux lignes également au niveau du `VirtualHost *:80`
- Si il a été nécessaire de créer un `Virtual Host` supplémentaire pour accéder au site depuis le réseau interne (`<VirtualHost *:54321>`) par exemple, ajouter les nouveaux `ProxyPass` et `ProxyPassReverse` au niveau de ce `Virtual Host`
- Un exemplaire de ce fichier est disponible [ici]({{< ref "/script/project-camera_conf_4cam.md" >}} "project-camera_conf_4cam
")
### Vérifier la syntaxe et relancer le serveur
- Vérifier la syntaxe 
```sh
sudo apache2ctl configtest
```
- Relancer le serveur
```sh
sudo systemctl restart apache2
```
## Relancer la raspberry
- Pour prendre en charge toutes les modifications, relancer la raspberry
```sh
sudo reboot
```
## Remarques sur les caméras
### Longueur du câble USB
- Il peut être nécessaire d'allonger le câble USB d'une caméra
- Si la longueur de la rallonge est courte, une rallonge simple peut suffire
- Sinon, il convient d'utiliser une rallonge avec **[répéteur actif](https://www.amazon.fr/s?k=usb+active+repeater+extension&rh=n%3A2908498031&__mk_fr_FR=%C3%85M%C3%85%C5%BD%C3%95%C3%91&ref=nb_sb_noss)**, de manière à amplifier le signal de la caméra
### Alimentation de plusieurs caméras
- Le nombre de ports USB de la Raspberry est limité
- Si on installe un grand nombre de caméras, il faut évidemment un [hub USB](https://fr.wikipedia.org/wiki/Hub_USB)
- Les caméras vont utiliser l'énergie fournie par la Raspberry pour fonctionner
- A terme, la puissance de celle-ci sera insuffisante
- Aussi est-il souhaitable de prévoir un **[hub avec alimentation externe](https://www.amazon.fr/s?k=hub+usb+alimentation+externe&adgrpid=57890976642&hvadid=601470758526&hvdev=c&hvlocphy=9109000&hvnetw=g&hvqmt=e&hvrand=17884128194425712080&hvtargid=kwd-298458767922&hydadcr=196_2608013&tag=googhydr0a8-21&ref=pd_sl_91g4ccd9d7_e)**
### Capacité du streaming
- Lorsque le nombre de caméras est élevé, il est possible que la Raspberry ne puisse pas bien afficher tous les flux des caméras ensemble
- Avec une Raspberry 3-B+, au delà de 4 caméras le flux en direct s'est essouflé
- Il convient alors de ne pas afficher tous les flux ensemble et de créer, par exemple, une première fonction de `views.py` qui affichera 4 caméras et une deuxième fonction qui affichera les 2 autres *(dans une hypothèse de 6 caméras)*
- Il faut bien sûr, dans ce cas, adapter `urls.py` et créer les fichiers `html` *ad hoc*
- Une alternative (possible, mais non testée) est d'utiliser une Raspberry plus puissante *(Pi-4 ou Pi-5 par exemple)*
- Il est également possible d'utiliser une deuxième Raspberry qui accueillera de nouvelles caméras et qui enverra les images à la Raspberry qui héberge le site Django : voir la [Partie 10]({{< ref "part10" >}})