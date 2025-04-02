# Détection et Suivi de Véhicules dans une Vidéo

Ce projet utilise OpenCV et Tkinter pour développer une application graphique permettant de charger une vidéo, sélectionner une région d'intérêt (ROI), définir des critères de détection de véhicules, et sauvegarder les résultats sous forme d'images.

## Fonctionnalités

- Chargement de vidéo(s) via une interface graphique.
- Sélection interactive de la **zone d'intérêt (ROI)**.
- Définition de la taille minimale des objets à détecter pour éviter les faux positifs.
- Détection de véhicules basée sur le soustracteur de fond (Background Subtractor).
- Sauvegarde des images des véhicules détectés avec horodatage.
- Visualisation optionnelle de la vidéo annotée en temps réel.

## Prérequis

### Ouvrir un terminal

- **Sur Linux** :  
  Ouvrez un terminal en appuyant sur `Ctrl + Alt + T` ou en recherchant "Terminal" dans vos applications.

- **Sur Windows** :  
  Ouvrez l'invite de commandes (CMD) ou PowerShell en appuyant sur `Win + R`, puis tapez `cmd` ou `powershell` et appuyez sur `Entrée`.

Assurez-vous d'avoir installé les éléments suivants :

### Python 3.7 ou plus
- Pour vérifier si Python est installé, exécutez l'une des commandes suivantes dans un terminal :

  ```bash
  python --version
  ```
  ou
  ```bash
  python3 --version
  ```
  
  Si une version >= 3.7 est affichée, Python est correctement installé.

- Si Python n'est pas installé, téléchargez-le depuis [python.org](https://www.python.org/downloads/) et suivez les instructions d'installation. Vous pouvez ensuite vérifier qu'il est bien installé en tapant la commande ci-dessus.

### Git
- Pour vérifier si Git est installé, exécutez la commande suivante dans un terminal :

  ```bash
  git --version
  ```
  
  Si une version est affichée, Git est correctement installé.
- Si Git n'est pas installé, téléchargez-le depuis [git-scm.com](https://git-scm.com/) et suivez les instructions d'installation. Vous pouvez ensuite vérifier qu'il est bien installé en tapant la commande ci-dessus.

### Bibliothèques Python
- OpenCV (`cv2`)
- Tkinter (inclus dans Python pour Windows/Mac)
- PIL (via `Pillow`)
- tqdm
- numpy

Vous pouvez installer les dépendances en tapant :

```bash
pip install opencv-python pillow tqdm numpy
```

ou

```bash
pip3 install opencv-python pillow tqdm numpy
```

## Installation

### Étape 1 : Ouvrir un terminal  

Si votre terminal est **déjà ouvert**, vous pouvez passer cette étape.  

- **Sur Linux** :  
  Ouvrez un terminal en appuyant sur `Ctrl + Alt + T` ou en recherchant "Terminal" dans vos applications.  

- **Sur Windows** :  
  Ouvrez l'invite de commandes (CMD) ou PowerShell en appuyant sur `Win + R`, puis tapez `cmd` ou `powershell`, puis appuyez sur `Entrée`.

### Étape 2 : Se déplacer dans le répertoire Bureau

- **Sur Linux** :  
  Une fois le terminal ouvert, tapez la commande suivante pour vous déplacer sur votre bureau :
  ```bash
  cd Bureau
  ```

- **Sur Windows** :  
  Dans l'invite de commandes ou PowerShell, tapez la commande suivante pour vous déplacer dans le répertoire Bureau :
  ```bash
  cd Desktop
  ```

### Étape 3 : Cloner le projet

Une fois sur le Bureau, clonez le dépôt du projet en tapant :

```bash
git clone https://github.com/cucu-la-tortue/car-detect.git
```

### Étape 4 : Fermer le terminal

Vous pouvez maintenant fermer le terminal en tapant la commande suivante ou en fermant simplement la fenêtre du terminal :

  ```bash
  exit
  ```

## Instructions d'utilisation

1. **Chargement des vidéos** : Allez sur votre Bureau, puis dans le répertoire `car-detect`. Créez dans ce répertoire un dossier `Videos`. Dans ce dossier, copiez-collez la ou les vidéo(s) à traiter.
2. **Lancer l'application** : Allez sur votre Bureau, double-cliquez sur le dossier `car-detect`, et double-cliquez sur le script `main.py`.
3. **Charger une ou des vidéo(s)** : Cliquez sur le bouton **"Charger Vidéos"** pour sélectionner une ou plusieurs vidéos.  
⚠ **Important :** Si vous sélectionnez plusieurs vidéos, **assurez-vous de les choisir dans le bon ordre**, car elles seront traitées successivement comme une seule séquence. **La même zone de traitement sera appliquée à toutes les vidéos sélectionnées.**
4. **Visualiser la première frame** : Cliquez sur **"Visualiser l'horodatage initial"** pour afficher la première image et sélectionner le moment de départ.
5. **Sélectionner la zone d'intérêt** :
    - Appuyez sur le bouton correspondant.
    - Déplacez-vous (si vous le souhaitez) dans la vidéo avec les touches `Q/D` ou les flèches.
    - Dessinez une zone avec la souris et validez avec `V`.
6. **Définir la taille minimale de véhicule** : Suivez la même procédure pour définir la taille des véhicules à détecter.  
⚠ **Attention :** Il est recommandé de **sélectionner une taille nettement inférieure à la plus petite voiture que vous souhaitez détecter**. Une zone trop large risque d'ignorer certains véhicules !
7. **Lancer la détection** : Cliquez sur le bouton pour détecter et sauvegarder les images des véhicules détectés.
8. **Consulter les images** : Une fois la ou les vidéo(s) traitée(s), vous pouvez fermer la fenêtre et aller consulter les résultats. Les images sont sauvegardés dans un répertoire du même nom que la vidéo.

## Structure du projet

```
├── detection_utils.py       # Fonctions utilitaires pour la détection
├── config.py                # Paramètres globaux
├── main.py                  # Script principal avec interface Tkinter
└── README.md                # Documentation
```

## Paramètres importants

Certains paramètres peuvent être ajustés dans le fichier `config.py` :

- **`iou_threshold`** : Seuil pour l'Intersection over Union (IoU), utilisé pour suivre les objets.
- **`frame_interval`** : Intervalle entre les frames traitées.
- **`max_inactive_frames`** : Nombre maximum de frames pendant lesquelles une voiture peut rester inactive avant d’être supprimée.

## Avertissements

- La détection repose sur le soustracteur de fond et peut être affectée par des changements soudains dans l'éclairage.
- Lorsque la couleur de la voiture est trop proche de la couleur du fond (par exemple de la route), elle peut ne pas être détectée.
- La taille minimale de véhicule doit être soigneusement définie pour éviter les faux positifs. **Attention** : de nuit, veillez à sélectionner une taille de voiture plus petite, voire même sélectionner la taille d'un phare (car le programme aura du mal à détecter la voiture en entier).

## Licence

Ce projet est sous licence [MIT](LICENSE).

