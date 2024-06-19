#!/usr/bin/env python3

import cv2
import numpy as np
from geometry_msgs.msg import Point


def detect_largest_red_object(image, low_th, up_th, low_th2, up_th2, blur=0, imshow=False, 
                              search_window=None, real_object_width=None, focal_length=None,
                              cx = 0, cy = 0, fx = 0, fy = 0):
    # Desenfocar la imagen para eliminar el ruido
    if blur > 0:
        image = cv2.blur(image, (blur, blur))
        # Mostrar el resultado del desenfoque
        if imshow:
            cv2.imshow("Blur", image)
            cv2.waitKey(0)
    
    # Definir la ventana de búsqueda
    if search_window is None:
        search_window = [0.0, 0.0, 1.0, 1.0]
    
    # Convertir a espacio de color HSV y crear máscaras para el rojo
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    mask1 = cv2.inRange(hsv, low_th, up_th)
    mask2 = cv2.inRange(hsv, low_th2, up_th2)
    mask = cv2.bitwise_or(mask1, mask2)
    mask = cv2.dilate(mask, None, iterations=6)
    mask = cv2.erode(mask, None, iterations=4)
    
    # Encontrar contornos
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    largest_contour = None
    max_area = 0

    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > max_area:
            max_area = area
            largest_contour = cnt
    
    reverse_mask = np.zeros_like(mask)
    
    if largest_contour is not None:
        
        f = (mask.shape[0] + mask.shape[1])/2

        m = f/focal_length

        # Calcular el rectángulo delimitador y el tamaño del contorno
        x, y, w, h = cv2.boundingRect(largest_contour)
        cv2.drawContours(image, [largest_contour], 0, (0, 255, 0), 5)

        # Calcular el centroide
        M = cv2.moments(largest_contour)
        cX = int(M["m10"] / M["m00"]) if M["m00"] != 0 else 0
        cY = int(M["m01"] / M["m00"]) if M["m00"] != 0 else 0
        cv2.circle(image, (cX, cY), 10, (255, 0, 0), -1)
        
        # Estimación basada en la anchura del objeto
        #print("w", w)
        Z = (focal_length * real_object_width) / w
        #Z = real_object_width * focal_length /m
        #print("CX", cX)
        #print("CY", cY)
        #print("fx", fx)
        #print("fy", fy)

        # Convertir las coordenadas de la imagen a coordenadas del mundo
        X = (cX - cx) * Z / fx
        Y = (cY - cy) * Z / fy
        #print("X, Y ,Z :", X, Y, Z) 
        
        reverse_mask = cv2.drawContours(reverse_mask, [largest_contour], 0, 255, thickness=cv2.FILLED)
        reverse_mask = cv2.bitwise_not(reverse_mask)
        
        return (X, Y, Z) , reverse_mask

    return (0,0,0), reverse_mask
