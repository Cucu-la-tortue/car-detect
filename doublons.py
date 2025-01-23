import cv2

for i in range(29):
    # Charger l'image de référence et l'image actuelle
    img1 = cv2.imread(f"Images/car_{i}.jpg", cv2.IMREAD_GRAYSCALE)
    img2 = cv2.imread(f"Images/car_{i+1}.jpg", cv2.IMREAD_GRAYSCALE)

    # Initialiser l'extracteur ORB
    orb = cv2.ORB_create()

    # Trouver les points clés et les descripteurs
    kp1, des1 = orb.detectAndCompute(img1, None)
    kp2, des2 = orb.detectAndCompute(img2, None)

    # Utiliser un matcher BFMatcher pour trouver les correspondances entre les descripteurs
    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
    matches = bf.match(des1, des2)

    # Trier les correspondances par distance
    matches = sorted(matches, key = lambda x:x.distance)

    # Calculer le ratio des correspondances bonnes
    good_matches_ratio = len(matches) / len(kp1)

    # Si le ratio de bonnes correspondances est suffisamment élevé, c'est probablement un doublon
    if good_matches_ratio > 0.85:
        print(f"Doublon détecté. Images {i} et {i+1}")
