import time
import threading
import cv2
import os
import sys
import numpy as np
import tkinter as tk

from tqdm import tqdm
from datetime import datetime, timedelta
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageTk
from detection_utils import *
from config import *



##### VIDEO UTILS =======================================================================================================================
def load_video(path_label):
    """Fonction pour ouvrir la boîte de dialogue et récupérer le chemin du fichier vidéo"""
    global video_queue

    # Ouvrir une boîte de dialogue pour sélectionner un fichier vidéo à partir du dossier courant
    current_directory = os.getcwd()
    video_paths = filedialog.askopenfilenames(
        initialdir=current_directory,
        filetypes=[("Fichiers Vidéo", "*.mp4 *.avi *.mov *.mkv")],
        title="Sélectionnez des vidéos"
    )
    if video_paths:
        video_queue = list(video_paths)   # Stocker les vidéos dans une liste
        
        # Afficher le nombre de vidéos sélectionnées
        path_label.config(text=f"{len(video_queue)} vidéo(s) sélectionnée(s)")



def display_first_frame(video_path):
    global frame_window

    # Créer une nouvelle fenêtre pour afficher la première frame
    frame_window = tk.Toplevel()
    frame_window.title("Première Frame")

    cap = cv2.VideoCapture(video_path)
    
    # Vérifier si la vidéo a été chargée correctement
    if not cap.isOpened():
        print("Erreur lors de l'ouverture de la vidéo.")
        return
    
    # Lire la première frame
    ret, frame = cap.read()
    if ret:
        # Convertir l'image en RGB (car OpenCV lit en BGR)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Redimensionner l'image pour qu'elle tienne dans la fenêtre
        window_width, window_height = 800, 600  # Taille maximale pour la fenêtre
        frame_height, frame_width = frame.shape[:2]

        scaling_factor = min(window_width / frame_width, window_height / frame_height)
        new_width = int(frame_width * scaling_factor)
        new_height = int(frame_height * scaling_factor)

        frame = cv2.resize(frame, (new_width, new_height))

        # Convertir l'image en format compatible avec Tkinter
        img = Image.fromarray(frame)
        img = ImageTk.PhotoImage(img)
        
        # Créer un label dans la nouvelle fenêtre pour afficher l'image
        img_label = tk.Label(frame_window, image=img)
        img_label.pack()

        # Garder une référence de l'image pour éviter que l'image ne soit détruite
        img_label.image = img
    
    cap.release()
    




def draw_rectangle(event, x, y, flags, param):
    """Fonction pour dessiner un rectangle"""
    global drawing, roi_x, roi_y, roi_w, roi_h, start_point, frame

    if event == cv2.EVENT_LBUTTONDOWN:
        # Démarre le tracé
        drawing = True
        start_point = (x, y)
        roi_x, roi_y = x, y

    elif event == cv2.EVENT_MOUSEMOVE:
        # Met à jour le rectangle pendant le déplacement de la souris
        if drawing:
            frame_copy = original_frame.copy()
            cv2.rectangle(frame_copy, start_point, (x, y), (255, 0, 0), 2)
            cv2.imshow("Frame", frame_copy)

    elif event == cv2.EVENT_LBUTTONUP:
        # Terminer le tracé
        drawing = False
        roi_w = abs(x - roi_x)
        roi_h = abs(y - roi_y)
        roi_x, roi_y = min(roi_x, x), min(roi_y, y)  # Assure que (x, y) sont les coordonnées en haut à gauche
        frame = original_frame.copy()
        cv2.rectangle(frame, (roi_x, roi_y), (roi_x + roi_w, roi_y + roi_h), (0, 255, 0), 2)
        cv2.imshow("Frame", frame)



def draw_rectangle_min_car(event, x, y, flags, param):
    """Fonction pour dessiner un rectangle"""
    global drawing, min_car_x, min_car_y, min_car_w, min_car_h, start_point, frame

    if event == cv2.EVENT_LBUTTONDOWN:
        # Démarre le tracé
        drawing = True
        start_point = (x, y)
        min_car_x, min_car_y = x, y

    elif event == cv2.EVENT_MOUSEMOVE:
        # Met à jour le rectangle pendant le déplacement de la souris
        if drawing:
            frame_copy = original_frame.copy()
            cv2.rectangle(frame_copy, start_point, (x, y), (255, 0, 0), 2)
            cv2.imshow("Frame", frame_copy)

    elif event == cv2.EVENT_LBUTTONUP:
        # Terminer le tracé
        drawing = False
        min_car_w = abs(x - min_car_x)
        min_car_h = abs(y - min_car_y)
        min_car_x, min_car_y = min(min_car_x, x), min(min_car_y, y)  # Assure que (x, y) sont les coordonnées en haut à gauche
        frame = original_frame.copy()
        cv2.rectangle(frame, (min_car_x, min_car_y), (min_car_x + min_car_w, min_car_y + min_car_h), (0, 255, 0), 2)
        cv2.imshow("Frame", frame)



def select_roi_from_video(video_path):
    """Fonction pour sélectionner la ROI dans une vidéo"""

    global roi_x, roi_y, roi_w, roi_h, frame, original_frame, current_frame_index

    # Ouvrir la vidéo
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print("Erreur d'ouverture de la vidéo")
        return None

    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))  # Nombre total de frames

    # Charger la première frame
    ret, frame = cap.read()
    if not ret:
        print("Erreur de lecture de la première frame")
        return None

    current_frame_index = 0
    original_frame = frame.copy()

    # Crée une fenêtre redimensionnable
    cv2.namedWindow("Frame", cv2.WINDOW_NORMAL)

    cv2.imshow("Frame", frame)

    # Assigner le callback pour la souris
    cv2.setMouseCallback("Frame", draw_rectangle)

    while True:
        key = cv2.waitKey(1) & 0xFF

        if key == 27 or cv2.getWindowProperty("Frame", cv2.WND_PROP_VISIBLE) < 1:  # Quitter (avec la touche esc ou en fermant manuellement la fenêtre)
            print("Sélection annulée.")
            break

        elif key == ord('v'):  # Valider
            if roi_w > 0 and roi_h > 0:  # Vérifier que la ROI est valide
                print(f"Zone d'intérêt validée : ({roi_x}, {roi_y}), largeur={roi_w}, hauteur={roi_h}")
                # Afficher le tic vert à côté du bouton
                roi_selected_label.config(text="OK", fg="green")
                break
            else:
                print("La sélection est invalide. Veuillez dessiner une ROI correcte.")
                show_error_about_roi_selection_button()

        elif key == ord('r'):  # Réinitialiser
            roi_x, roi_y, roi_w, roi_h = -1, -1, 0, 0
            frame = original_frame.copy()
            cv2.imshow("Frame", frame)
            print("Sélection réinitialisée.")

        elif key == 83 or key == ord('d'):  # Flèche droite ou touche D
            if current_frame_index < total_frames - 1:
                current_frame_index += 5
                cap.set(cv2.CAP_PROP_POS_FRAMES, current_frame_index)
                ret, frame = cap.read()
                if ret:
                    original_frame = frame.copy()
                    cv2.imshow("Frame", frame)

        elif key == 81 or key == ord('q'):  # Flèche gauche ou touche Q
            if current_frame_index > 0:
                current_frame_index -= 5
                cap.set(cv2.CAP_PROP_POS_FRAMES, current_frame_index)
                ret, frame = cap.read()
                if ret:
                    original_frame = frame.copy()
                    cv2.imshow("Frame", frame)

    # Fermer la fenêtre après validation ou annulation
    cap.release()
    cv2.destroyAllWindows()
    


def select_min_car_from_video(video_path):
    """Fonction pour sélectionner la ROI dans une vidéo"""

    global min_car_x, min_car_y, min_car_w, min_car_h, frame, original_frame, current_frame_index

    # Ouvrir la vidéo
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print("Erreur d'ouverture de la vidéo")
        return None

    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))  # Nombre total de frames

    # Charger la première frame
    ret, frame = cap.read()
    if not ret:
        print("Erreur de lecture de la première frame")
        return None

    current_frame_index = 0
    original_frame = frame.copy()

    # Crée une fenêtre redimensionnable
    cv2.namedWindow("Frame", cv2.WINDOW_NORMAL)

    cv2.imshow("Frame", frame)

    # Assigner le callback pour la souris
    cv2.setMouseCallback("Frame", draw_rectangle_min_car)

    while True:
        key = cv2.waitKey(1) & 0xFF

        if key == 27 or cv2.getWindowProperty("Frame", cv2.WND_PROP_VISIBLE) < 1:  # Quitter (avec la touche esc ou en fermant manuellement la fenêtre)
            print("Sélection annulée.")
            break

        elif key == ord('v'):  # Valider
            if min_car_w > 0 and min_car_h > 0:  # Vérifier que la ROI est valide
                print(f"Zone d'intérêt validée : ({min_car_x}, {min_car_y}), largeur={min_car_w}, hauteur={min_car_h}")
                # Afficher le tic vert à côté du bouton
                min_car_selected_label.config(text="OK", fg="green")
                break
            else:
                print("La sélection est invalide. Veuillez dessiner une ROI correcte.")
                show_error_about_min_car_button()

        elif key == ord('r'):  # Réinitialiser
            min_car_x, min_car_y, min_car_w, min_car_h = -1, -1, 0, 0
            frame = original_frame.copy()
            cv2.imshow("Frame", frame)
            print("Sélection réinitialisée.")

        elif key == 83 or key == ord('d'):  # Flèche droite ou touche D
            if current_frame_index < total_frames - 1:
                current_frame_index += 5
                cap.set(cv2.CAP_PROP_POS_FRAMES, current_frame_index)
                ret, frame = cap.read()
                if ret:
                    original_frame = frame.copy()
                    cv2.imshow("Frame", frame)

        elif key == 81 or key == ord('q'):  # Flèche gauche ou touche Q
            if current_frame_index > 0:
                current_frame_index -= 5
                cap.set(cv2.CAP_PROP_POS_FRAMES, current_frame_index)
                ret, frame = cap.read()
                if ret:
                    original_frame = frame.copy()
                    cv2.imshow("Frame", frame)

    # Fermer la fenêtre après validation ou annulation
    cap.release()
    cv2.destroyAllWindows()



def show_info_about_min_car_button():
    messagebox.showinfo("Information", 
                        "Ce bouton permet de dessiner la taille minimale des voitures à détecter, "
                        "afin d'éviter de détecter des mouvements trop petits (ex: piétons, branches qui bougent...)")

def show_info_about_roi_selection_button():
    messagebox.showinfo("Instructions", 
                        "- Utilisez les flèches gauche/droite ou les touches q/d pour changer de frame.\n"
                        "- Cliquez et faites glisser pour sélectionner une zone d'intérêt.\n"
                        "- Appuyez sur 'v' pour valider la sélection.\n"
                        "- Appuyez sur 'r' pour réinitialiser la sélection.\n"
                        "- Appuyez sur 'esc' pour quitter sans valider.")

def show_error_about_roi_selection_button():
    messagebox.showerror("Erreur", 
                        "La sélection est invalide. Veuillez sélectionner une zone de traitement correcte.")
    
def show_error_about_min_car_button():
    messagebox.showerror("Erreur", 
                        "La sélection est invalide. Veuillez sélectionner une zone correcte.")
    
def show_error_about_video():
    messagebox.showerror("Erreur", 
                        "Aucune vidéo n'a été chargée.")
    
def show_error_about_timestamp():
    messagebox.showerror("Erreur", 
                        "L'horodatage est invalide. Veuillez respecter le format demandé (JJ-MM-AAAA HH:MM:SS)")

def show_error_about_roi():
    messagebox.showerror("Erreur", 
                        "Veuillez sélectionner une zone de traitement.")

def show_error_about_min_car():
    messagebox.showerror("Erreur", 
                        "Veuillez sélectionner une taille minimale de voiture.")

def toggle_warning():
    """Affiche ou masque le message d'avertissement selon l'état de la checkbox"""
    if display_video.get():
        warning_label.pack(pady=5)
    else:
        warning_label.pack_forget()

def detect_and_save_frames(video_path, start_datetime, display_video, progress_bar, percentage_label, time_remaining_label):
    """Fonction pour détecter et sauvegarder les images"""
    global stop_processing
    stop_processing = False  # Réinitialiser le flag au démarrage

    try:
        assert video_path is not None, "Aucune vidéo chargée"
    except AssertionError:
        show_error_about_video()

    try:
        start_datetime = datetime.strptime(start_datetime, "%d-%m-%Y %H:%M:%S")
    except ValueError as e:
        show_error_about_timestamp()
    
    try:
        assert roi_w > 0 and roi_h > 0, "Aucune ROI sélectionnée"
    except AssertionError:
        show_error_about_roi()

    try:
        assert min_car_w > 0 and min_car_h > 0, "Aucune ROI sélectionnée"
    except AssertionError:
        show_error_about_min_car()

    cap = cv2.VideoCapture(video_path)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))  # Nombre total de frames
    
    video_name = os.path.basename(video_path)      # On enlève tout le chemin avant
    video_name = os.path.splitext(video_name)[0]   # On enlève l'extension

    # Supprime la fenêtre de la première frame affichée pour l'horodatage
    if frame_window:
            frame_window.destroy()

    # Obtenir les FPS
    fps = cap.get(cv2.CAP_PROP_FPS)
    print(f"FPS de la vidéo : {fps}")

    # Initialiser le soustracteur de fond (Background Subtractor)
    fgbg = cv2.createBackgroundSubtractorMOG2()
    
    frame_count = 0
    car_id = 0
    detected_cars = []
    active_cars = []

    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    min_car_area = min_car_w * min_car_h

    # Initialiser la barre de progression
    progress_bar["maximum"] = total_frames  # Définir le maximum de la barre de progression
    
    with tqdm(total=total_frames // frame_interval, desc="Processing Video", unit="frame") as pbar:
        start_time = time.time()  # Temps de début du traitement
        
        while True:

            if stop_processing:  # Vérifier si l'utilisateur a demandé l'arrêt
                print("Traitement interrompu par l'utilisateur.")
                break  # Sortir proprement de la boucle

            ret, frame = cap.read()
            if not ret:
                break  # Fin de la vidéo ou erreur de lecture de frame
            
            roi = frame[roi_y:roi_y+roi_h, roi_x:roi_x+roi_w]

            # Traiter uniquement les frames qui respectent l'intervalle
            if frame_count % frame_interval != 0:
                frame_count += 1
                continue     # on passe à l'itération suivante
        
            # Calculer le timestamp pour la frame courante
            current_time = start_datetime + timedelta(seconds=frame_count / fps)

            # Appliquer le soustracteur de fond
            fgmask = fgbg.apply(frame)

            # Filtrage morphologique pour éliminer le bruit
            kernel = np.ones((9, 9), np.uint8)
            fgmask = cv2.morphologyEx(fgmask, cv2.MORPH_OPEN, kernel)  # Retirer les petits bruits
            fgmask = cv2.morphologyEx(fgmask, cv2.MORPH_CLOSE, kernel)  # Fermer les trous dans les objets détectés

            #_, fgmask = cv2.threshold(fgmask, 200, 255, cv2.THRESH_BINARY)
            
            # Trouver les contours des objets en mouvement
            contours, _ = cv2.findContours(fgmask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            # Marquer toutes les voitures comme inactives par défaut
            for car in active_cars:
                car["inactive_frames"] += 1

            # Parcourir les contours détectés
            for contour in contours:
                if cv2.contourArea(contour) > min_car_area:  # Filtrer les petits contours (ajustez le seuil)
                    # Calculer la boîte englobante (bounding box) de l'objet
                    x, y, w, h = cv2.boundingRect(contour)
                    car_box = (x, y, w, h)
                    car_area = w * h
                    #car_img = frame[roi_y:roi_y+roi_h, roi_x:roi_x+roi_w]

                    # Vérifier si la boîte de l'objet est contenue dans la zone d'intérêt (ROI), est entièrement dans la frame et a un ratio cohérent avec une voiture
                    if is_in_roi(car_box, roi_x, roi_y, roi_w, roi_h) and is_entirely_in_frame(car_box, frame_width, frame_height):
                        matched = False
                        
                        # Ajouter le timestamp sur la capture
                        timestamp_str = current_time.strftime("%d-%m-%Y %H:%M:%S")
                        timestamp_x, timestamp_y = roi_x + 10, roi_y + 50
                        cv2.putText(frame, timestamp_str, (timestamp_x, timestamp_y), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

                        for car in active_cars:
                            if is_same_target(car["box"], car_box, iou_threshold):
                                matched = True

                                car["box"] = car_box
                                car["inactive_frames"] = 0
                                detected_cars[car["id"]]["box"] = car_box
                                detected_cars[car["id"]]["inactive_frames"] = 0

                                # Si l'image est meilleure
                                if car_area > car["area"]:
                                    car["area"] = car_area
                                    car["image"] = roi.copy()
                                    car["time"] = current_time
                                    detected_cars[car["id"]]["area"] = car_area
                                    detected_cars[car["id"]]["image"] = roi.copy()
                                    detected_cars[car["id"]]["time"] = current_time

                                break
                        
                        if not matched:
                            tmp = {
                                "box": car_box,
                                "area": car_area,
                                "image": roi.copy(),
                                "inactive_frames": 0,
                                "id": car_id,
                                "time": current_time
                            }
                            car_id += 1
                            detected_cars.append(tmp)
                            active_cars.append(tmp)
                        
                        
                        # Dessiner un rectangle autour de l'objet détecté
                        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                        
            active_cars = [car for car in active_cars if car["inactive_frames"] <= max_inactive_frames]

            # Dessiner la zone d'intérêt (ROI)
            cv2.rectangle(frame, (roi_x, roi_y), (roi_x + roi_w, roi_y + roi_h), (255, 0, 0), 2)
            
            # Afficher la vidéo avec les objets détectés et la zone d'intérêt (ROI) si c'est demandé
            if display_video:
                # Crée une fenêtre redimensionnable
                cv2.namedWindow("Frame", cv2.WINDOW_NORMAL)
                cv2.imshow("Frame", frame)

            # Quitter si l'utilisateur appuie sur "q"
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

            # Mettre à jour la barre de progression et le pourcentage
            progress_bar["value"] = frame_count
            percentage_label.config(text=f"{round(frame_count * 100 / total_frames)} %")

            # Calculer le temps écoulé
            elapsed_time = time.time() - start_time

            # Estimer la vitesse de traitement (frames par seconde)
            if frame_count > 0:
                processing_speed = frame_count / elapsed_time  # Nombre de frames traitées par seconde
                remaining_frames = total_frames - frame_count  # Frames restantes
                estimated_time_remaining = remaining_frames / processing_speed  # Temps restant en secondes
                estimated_time_remaining_str = time.strftime("%H:%M:%S", time.gmtime(estimated_time_remaining))
            else:
                estimated_time_remaining_str = "Calcul..."

            # Mettre à jour l'affichage du temps restant
            time_remaining_label.config(text=f"Temps restant estimé : {estimated_time_remaining_str}")

            root.update_idletasks()
            
            frame_count += 1

            # Mettre à jour la barre de progression
            pbar.set_postfix(cars_detected=len(detected_cars))
            pbar.update(1)


    # Sauvegarder les images des target
    if not os.path.exists(video_name):
        os.makedirs(video_name)

    for i, car in enumerate(detected_cars):
        file_name = f"{video_name}/car_{i}.jpg"
        cv2.imwrite(file_name, car["image"])

    # Libérer la vidéo et fermer les fenêtres
    cap.release()
    cv2.destroyAllWindows()


def start_processing(video_path, start_datetime, display_video, progress_bar, percentage_label, time_remaining_label):
    """Démarrer le traitement dans un thread séparé"""
    global processing_thread
    processing_thread = threading.Thread(target=process_video_queue, 
                                         args=(video_path, start_datetime, display_video, progress_bar, percentage_label, time_remaining_label))
    processing_thread.start()

def on_closing():
    """Gérer la fermeture de la fenêtre et arrêter proprement le traitement"""
    global stop_processing
    if messagebox.askokcancel("Quitter", "Voulez-vous vraiment arrêter le traitement et quitter ?"):
        stop_processing = True  # Définir le flag d'arrêt
        root.destroy()  # Fermer la fenêtre principale




def get_video_duration(video_path):
    """Retourne la durée d'une vidéo en secondes"""
    try:
        cap = cv2.VideoCapture(video_path)
        fps = cap.get(cv2.CAP_PROP_FPS)
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        cap.release()
        return total_frames / fps  # Durée en secondes
    except:
        return 0  # En cas d'erreur, on retourne 0


def update_timestamp(current_timestamp, video_path):
    """Met à jour l'horodatage pour la prochaine vidéo en fonction de sa durée"""
    duration = get_video_duration(video_path)  # Utilisation de la fonction optimisée
    new_time = datetime.strptime(current_timestamp, "%d-%m-%Y %H:%M:%S") + timedelta(seconds=duration+1)   # On ajoute le +1 car il y a un écart de 1 sec entre chaque vidéo
    return new_time.strftime("%d-%m-%Y %H:%M:%S")


def process_video_queue(start_time_entry, display_video, progress_bar, percentage_label, video_progress_label, time_remaining_label):
    """Traite toutes les vidéos en file d'attente"""
    global video_queue  # Liste des vidéos sélectionnées
    if not video_queue:
        show_error_about_video()
        return

    start_datetime = start_time_entry.get()  # Récupérer l'horodatage initial
    total_videos = len(video_queue)  # Nombre total de vidéos

    for i, video_path in enumerate(video_queue):
        # Mettre à jour le ratio des vidéos traitées
        video_progress_label.config(text=f"{i + 1}/{total_videos} vidéos")
        root.update_idletasks()

        # Obtenir la durée de la vidéo en minutes pour estimer le temps restant
        estimated_time = get_video_duration(video_path) / 60  # Convertir en minutes
        time_remaining_label.config(text=f"Temps restant estimé : ~ {round(estimated_time, 1)} min")

        detect_and_save_frames(video_path, start_datetime, display_video, progress_bar, percentage_label, time_remaining_label)
        start_datetime = update_timestamp(start_datetime, video_path)  # Mettre à jour l'heure de début

    # Fin du traitement, on remet le temps restant à zéro
    time_remaining_label.config(text="Traitement terminé.")

# Initialisation de l'interface
def main():
    global video_queue, root, display_video, warning_label, roi_selected_label, min_car_selected_label

    # Créer la fenêtre principale
    root = tk.Tk()
    root.title("Sélectionner une Vidéo")

    # Booléen pour afficher ou non la vidéo
    display_video = tk.BooleanVar(value=False)

    # Bouton pour charger la vidéo
    load_button = tk.Button(root, text="Charger Vidéos", command=lambda: load_video(path_label))
    load_button.pack(pady=10)

    # Label pour afficher le chemin de la vidéo
    path_label = tk.Label(root, text="")
    path_label.pack(pady=10)

    # Bouton pour visualiser l'horodatage initial
    view_timestamp_button = tk.Button(root, text="Visualiser l'horodatage initial", 
                                      command=lambda: display_first_frame(video_queue[0]))
    view_timestamp_button.pack(pady=10)

    # Label et champ pour l'heure de début
    start_time_label = tk.Label(root, text="Entrez la date et l'heure de début (JJ-MM-AAAA HH:MM:SS) :")
    start_time_label.pack(pady=5)

    start_time_entry = tk.Entry(root)
    start_time_entry.pack(pady=5)

    # Label pour afficher le chemin de la vidéo
    instructions_label = tk.Label(root,
                                  text="Instructions pour la sélection :\n"
                                  "- Utilisez les flèches gauche/droite ou les touches q/d pour parcourir la vidéo.\n"
                                  "- Cliquez et faites glisser pour sélectionner une zone d'intérêt.\n"
                                  "- Appuyez sur 'V' pour valider la sélection.\n"
                                  "- Appuyez sur 'R' pour réinitialiser la sélection.\n"
                                  "- Appuyez sur 'ECHAP' pour quitter sans valider.",
                                  font=("Helvetica", 11, "bold")
                                  )
    instructions_label.pack(pady=10)
    
    # Création d'une frame pour regrouper le bouton et le label
    roi_frame = tk.Frame(root)
    roi_frame.pack(pady=5)

    # Bouton pour sélectionner la ROI
    select_roi_button = tk.Button(roi_frame, text="Sélectionner la zone de traitement", 
                                  command=lambda: select_roi_from_video(video_queue[0]))
    select_roi_button.pack(side=tk.RIGHT, padx=5)

    # Label de confirmation de sélection de la roi
    roi_selected_label = tk.Label(roi_frame, text="", font=("Arial", 12, "bold"))  # Label vide au départ
    roi_selected_label.pack(side=tk.LEFT)

    # Création d'une frame pour regrouper les deux prochains boutons et le label
    min_car_frame = tk.Frame(root)
    min_car_frame.pack(pady=5)

    info_button = tk.Button(min_car_frame, text="Pourquoi ?", command=show_info_about_min_car_button)
    info_button.pack(side=tk.RIGHT)

    # Bouton pour sélectionner la taille de voiture minimale (+ bouton d'information)
    select_min_car_button = tk.Button(min_car_frame, text="Sélectionner la taille minimale des voitures à détecter", 
                                  command=lambda: select_min_car_from_video(video_queue[0]))
    select_min_car_button.pack(side=tk.RIGHT, padx=5)
    
    # Label de confirmation de sélection de la min car
    min_car_selected_label = tk.Label(min_car_frame, text="", font=("Arial", 12, "bold"))  # Label vide au départ
    min_car_selected_label.pack(side=tk.LEFT)


    # Bouton pour afficher ou non la vidéo
    display_checkbox = tk.Checkbutton(root, text="Afficher la vidéo pendant le traitement", 
                                  variable=display_video, command=toggle_warning)
    display_checkbox.pack(pady=10)

    # Label d'avertissement (caché au départ)
    warning_label = tk.Label(root, text="⚠ Avertissement : afficher la vidéo pendant le traitement\n"
                                        "peut légèrement rallonger la durée du traitement.",
                            fg="red", font=("Arial", 10, "italic"))
    

    # Créer une barre de progression et un pourcentage
    progress_bar = ttk.Progressbar(root, orient="horizontal", length=400, mode="determinate")
    percentage_label = tk.Label(root, text="0%", font=('Helvetica', 12))
    
    # Bouton pour lancer le traitement
    process_button = tk.Button(root, text="Lancer le traitement", 
                                command=lambda: start_processing(start_time_entry, display_video.get(), progress_bar, percentage_label, video_progress_label, time_remaining_label))
    process_button.pack(pady=20)

    progress_bar.pack()
    percentage_label.pack(pady=10)

    time_remaining_label = tk.Label(root, text="Temps restant estimé : --:--:--", font=('Helvetica', 12))
    time_remaining_label.pack(pady=5)

    video_progress_label = tk.Label(root, text="0/0 vidéos", font=('Helvetica', 12))
    video_progress_label.pack(pady=5)

    # Associer la gestion de la fermeture de la fenêtre
    root.protocol("WM_DELETE_WINDOW", on_closing)

    # On place la fenêtre sur le coin en haut à gauche
    root.geometry(f"+{0}+{0}")

    # Lancer l'interface
    root.mainloop()



if __name__ == "__main__":
    main()
