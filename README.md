# Détection et Suivi de Véhicules dans une Vidéo

Ce projet utilise OpenCV et Tkinter pour développer une application graphique permettant de charger une vidéo, sélectionner une région d'intérêt (ROI), définir des critères de détection de véhicules, et sauvegarder les résultats sous forme d'images.

## Fonctionnalités

- Chargement d'une vidéo via une interface graphique.
- Sélection interactive de la **zone d'intérêt (ROI)**.
- Définition de la taille minimale des objets à détecter pour éviter les faux positifs.
- Détection de véhicules basée sur le soustracteur de fond (Background Subtractor).
- Sauvegarde des images des véhicules détectés avec horodatage.
- Visualisation optionnelle de la vidéo annotée en temps réel.

## Prérequis

Assurez-vous d'avoir installé les bibliothèques suivantes :

- Python >= 3.7
- OpenCV (`cv2`)
- Tkinter (inclus dans Python pour Windows/Mac)
- PIL (via `Pillow`)
- tqdm
- numpy

Vous pouvez installer les dépendances avec :

```bash
pip install opencv-python-headless pillow tqdm numpy
```

## Installation

1. Clonez ce dépôt sur votre machine locale :

   ```bash
   git clone https://github.com/cucu-la-tortue/car-detect.git
   cd car-detect
   ```

2. Placez vos vidéos dans le répertoire de travail, ou préparez un chemin d'accès valide.

3. Lancez le script principal :

   ```bash
   python3 main.py
   ```

## Instructions d'utilisation

1. **Lancer l'application** : Démarrez l'application en exécutant le script.
2. **Charger une vidéo** : Cliquez sur le bouton **"Charger Vidéo"** pour sélectionner une vidéo au format `.mp4`.
3. **Visualiser la première frame** : Cliquez sur **"Visualiser l'horodatage initial"** pour afficher la première image et sélectionner le moment de départ.
4. **Sélectionner la ROI** :
    - Appuyez sur le bouton correspondant.
    - Déplacez-vous dans les frames avec les touches `q/d` ou les flèches.
    - Dessinez une zone avec la souris et validez avec `v`.
5. **Définir la taille minimale de véhicule** : Suivez la même procédure pour définir la taille des véhicules à détecter.
6. **Lancer la détection** : Cliquez sur le bouton pour détecter et sauvegarder les images des véhicules détectés dans le répertoire `Cars`.

## Structure du projet

```
├── detection_utils.py       # Fonctions utilitaires pour la détection
├── config.py                # Paramètres globaux
├── votre_script.py          # Script principal avec interface Tkinter
├── Cars/                  # Répertoire pour les résultats
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
- La taille minimale de véhicule doit être soigneusement définie pour éviter les faux positifs. Attention: de nuit, veillez à sélectionner une taille de voiture plus petite (car le programme aura du mal à détecter la voiture en entier).

## Licence

Ce projet est sous licence [MIT](LICENSE).