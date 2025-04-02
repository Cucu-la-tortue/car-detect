# Variable globale pour stocker le chemin de la vidéo
video_path = None
frame_window = None  # Référence à la fenêtre contenant la première frame

min_car_x, min_car_y, min_car_w, min_car_h = -1, -1, 0, 0
roi_x, roi_y, roi_w, roi_h = -1, -1, 0, 0  # Coordonnées du ROI


iou_threshold = 0.4
frame_interval = 5
max_inactive_frames = 3  # Nombre maximal de frames où une voiture peut rester inactive


# Variables globales pour la gestion de la souris
drawing = False  # Détecte si l'utilisateur est en train de dessiner
frame = None  # Frame actuelle
start_point = (-1, -1)  # Point de départ du rectangle
original_frame = None  # Copie de la frame originale
current_frame_index = 0  # Index de la frame actuelle

# Flag pour indiquer si l'utilisateur souhaite arrêter le traitement
stop_processing = False