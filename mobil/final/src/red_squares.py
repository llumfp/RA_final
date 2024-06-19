#!/usr/bin/env python3

import cv2
import numpy as np
from geometry_msgs.msg import Point

def detect_largest_red_object(image, low_th, up_th, low_th2, up_th2, blur=0, imshow=False, search_window=None):
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
    
    # Recortar la imagen según la ventana de búsqueda
    height, width = image.shape[:2]
    x_start = int(search_window[0] * width)
    y_start = int(search_window[1] * height)
    x_end = int(search_window[2] * width)
    y_end = int(search_window[3] * height)
    #cropped_image = image[y_start:y_end, x_start:x_end]
    
    #print(image, cropped_image)
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    # Definir los rangos para rojo en HSV
    mask1 = cv2.inRange(hsv, low_th, up_th)
    mask2 = cv2.inRange(hsv, low_th2, up_th2)
    mask = cv2.bitwise_or(mask1, mask2)

    # Mejorar la máscara
    mask = cv2.dilate(mask, None, iterations=6)
    mask = cv2.erode(mask, None, iterations=4)
    if imshow:
        cv2.imshow('Mascara Roja', mask)
        cv2.waitKey(0)
    
    # Encontrar contornos
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    largest_contour = None
    max_area = 0

    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > max_area:
            max_area = area
            largest_contour = cnt  # Guarda el contorno más grande sin importar la forma

    keypoint = cv2.KeyPoint(0, 0, 0)
    reverse_mask = np.zeros_like(mask)

    # Dibujar el contorno más grande y detectar el centroide
    if largest_contour is not None and cv2.contourArea(largest_contour) > 2500:
        cv2.drawContours(image, [largest_contour], 0, (0, 255, 0), 5)

        # Calcular el centroide usando momentos
        M = cv2.moments(largest_contour)
        if M["m00"] != 0:
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
        else:
            cX, cY = 0, 0

        # Crear el keypoint con el centroide
        keypoint = cv2.KeyPoint(cX, cY, 1)

        # Dibujar el centroide en la imagen
        cv2.circle(image, (cX, cY), 10, (255, 0, 0), -1)

        # Crear la reverse mask
        reverse_mask = cv2.drawContours(reverse_mask, [largest_contour], 0, 255, thickness=cv2.FILLED)
        reverse_mask = cv2.bitwise_not(reverse_mask)
    
    #cv2.imshow('Reverse_mask', reverse_mask)
    return keypoint, reverse_mask

# Función para dibujar rectángulos (adaptada de draw_keypoints)
def draw_rectangles(image, kp, rect_color=(0,0,255), imshow=False):
    x, y = int(kp.pt[0]), int(kp.pt[1])
    size = int(kp.size)
    top_left = (x - size, y - size)
    bottom_right = (x + size, y + size)
    image = cv2.rectangle(image, top_left, bottom_right, rect_color, 2)
    if imshow:
        cv2.imshow("Rectangles", image)
    return image

# Función para dibujar la ventana de búsqueda (ya adaptada)
def draw_window(image, window_adim, color=(255,0,0), line=5, imshow=False):
    rows = image.shape[0]
    cols = image.shape[1]
    x_min_px = int(cols * window_adim[0])
    y_min_px = int(rows * window_adim[1])
    x_max_px = int(cols * window_adim[2])
    y_max_px = int(rows * window_adim[3])
    image = cv2.rectangle(image, (x_min_px, y_min_px), (x_max_px, y_max_px), color, line)
    if imshow:
        cv2.imshow("Window", image)
    return image

# Función para dibujar el marco X-Y (ya adaptada)
def draw_frame(image, dimension=0.3, line=2):
    rows = image.shape[0]
    cols = image.shape[1]
    size = min([rows, cols])
    center_x = int(cols / 2.0)
    center_y = int(rows / 2.0)
    line_length = int(size * dimension)
    image = cv2.line(image, (center_x, center_y), (center_x + line_length, center_y), (0, 0, 255), line)
    image = cv2.line(image, (center_x, center_y), (center_x, center_y + line_length), (0, 255, 0), line)
    return image

# Función para aplicar la ventana de búsqueda (ya adaptada)
def apply_search_window(image, window_adim=[0.0, 0.0, 1.0, 1.0]):
    rows = image.shape[0]
    cols = image.shape[1]
    x_min_px = int(cols * window_adim[0])
    y_min_px = int(rows * window_adim[1])
    x_max_px = int(cols * window_adim[2])
    y_max_px = int(rows * window_adim[3])
    mask = np.zeros(image.shape, np.uint8)
    mask[y_min_px:y_max_px, x_min_px:x_max_px] = image[y_min_px:y_max_px, x_min_px:x_max_px]
    return mask

# Función para desenfocar fuera de la ventana de búsqueda (ya adaptada)
def blur_outside(image, blur=5, window_adim=[0.0, 0.0, 1.0, 1.0]):
    rows = image.shape[0]
    cols = image.shape[1]
    x_min_px = int(cols * window_adim[0])
    y_min_px = int(rows * window_adim[1])
    x_max_px = int(cols * window_adim[2])
    y_max_px = int(rows * window_adim[3])
    mask = cv2.blur(image, (blur, blur))
    mask[y_min_px:y_max_px, x_min_px:x_max_px] = image[y_min_px:y_max_px, x_min_px:x_max_px]
    return mask

# Función para obtener la posición relativa del rectángulo
def get_rectangle_relative_position(image, keypoint):
    if keypoint.pt[0] != 0 or keypoint.pt[1] != 0:
        rows = float(image.shape[0])
        cols = float(image.shape[1])
        center_x = 0.5 * cols
        center_y = 0.5 * rows
        x = (keypoint.pt[0] - center_x) / center_x
        y = (keypoint.pt[1] - center_y) / center_y
        return x,y
    return 0,0

