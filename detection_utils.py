def is_in_roi(box, roi_x, roi_y, roi_w, roi_h, intersection_threshold=0.8):
    """Vérifie si une voiture est suffisamment dans la zone d'intérêt (80% dans la fenêtre par défaut)."""
    x, y, w, h = box
    # Calculer l'intersection entre la boîte de la voiture et la zone d'intérêt
    inter_x1 = max(x, roi_x)
    inter_y1 = max(y, roi_y)
    inter_x2 = min(x + w, roi_x + roi_w)
    inter_y2 = min(y + h, roi_y + roi_h)

    # Si il n'y a pas d'intersection
    if inter_x1 >= inter_x2 or inter_y1 >= inter_y2:
        return False

    # Aire d'intersection
    inter_area = (inter_x2 - inter_x1) * (inter_y2 - inter_y1)
    # Aire de la boîte de la voiture
    car_area = w * h

    # Calculer le pourcentage de la voiture dans la fenêtre
    intersection_ratio = inter_area / car_area
    return intersection_ratio >= intersection_threshold



##### Fonction pour vérifier que la target est entièrement dans l'écran
def is_entirely_in_frame(box, frame_width, frame_height):
    x, y, w, h = box
    return x > 0 and x + w < frame_width and y > 0 and y + h < frame_height



##### Fonction pour vérifier l'intersection des bounding boxes =======================================================================================================
def is_same_target(box1, box2, iou_threshold=0.5):
    """Cette fonction calculele rapport IoU (Intersection over Union) de deux bounding boxes et le compare à un seuil (iou_threshold) pour estimer si les deux box correspondent à la même voiture"""
    x1, y1, w1, h1 = box1
    x2, y2, w2, h2 = box2
    
    # Intersection
    inter_x1 = max(x1, x2)
    inter_y1 = max(y1, y2)
    inter_x2 = min(x1 + w1, x2 + w2)
    inter_y2 = min(y1 + h1, y2 + h2)
    inter_area = max(0, inter_x2 - inter_x1) * max(0, inter_y2 - inter_y1)
    
    # Union
    box1_area = w1 * h1
    box2_area = w2 * h2
    union_area = box1_area + box2_area - inter_area
    
    # IoU
    iou = inter_area / union_area if union_area > 0 else 0
    
    return iou > iou_threshold