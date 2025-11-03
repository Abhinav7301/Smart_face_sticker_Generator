import cv2
import numpy as np

def resize_image(image, max_width=800, max_height=800):
    h, w = image.shape[:2]
    scale = min(max_width / w, max_height / h)
    if scale < 1:
        new_w = int(w * scale)
        new_h = int(h * scale)
        return cv2.resize(image, (new_w, new_h), interpolation=cv2.INTER_AREA)
    return image

def preprocess_for_segmentation(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    bilateral = cv2.bilateralFilter(gray, 9, 75, 75)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    return clahe.apply(bilateral)

def detect_edges(preprocessed, low_threshold=100, high_threshold=200):
    return cv2.Canny(preprocessed, low_threshold, high_threshold)

def close_edge_gaps(edges, kernel_size=5, iterations=3):
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (kernel_size, kernel_size))
    closed = cv2.morphologyEx(edges, cv2.MORPH_CLOSE, kernel, iterations=iterations)
    return cv2.dilate(closed, kernel, iterations=2)

def find_largest_contour(edges):
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    return max(contours, key=cv2.contourArea) if contours else None

def create_mask_from_contour(image_shape, contour, padding=15):
    mask = np.zeros(image_shape[:2], dtype=np.uint8)
    cv2.drawContours(mask, [contour], -1, 255, -1)
    mask = cv2.GaussianBlur(mask, (7, 7), 0)
    _, mask = cv2.threshold(mask, 127, 255, cv2.THRESH_BINARY)
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (padding, padding))
    return cv2.dilate(mask, kernel, iterations=1)

def refine_mask_grabcut(image, initial_mask):
    gc_mask = np.where(initial_mask == 255, cv2.GC_PR_FGD, cv2.GC_PR_BGD).astype(np.uint8)
    bgd_model = np.zeros((1, 65), np.float64)
    fgd_model = np.zeros((1, 65), np.float64)
    try:
        cv2.grabCut(image, gc_mask, None, bgd_model, fgd_model, 5, cv2.GC_INIT_WITH_MASK)
        return np.where((gc_mask == cv2.GC_FGD) | (gc_mask == cv2.GC_PR_FGD), 255, 0).astype(np.uint8)
    except:
        return initial_mask

def extract_foreground(image, mask):
    return cv2.bitwise_and(image, image, mask=mask)

def create_sticker_border(mask, border_thickness=15):
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (border_thickness*2, border_thickness*2))
    dilated_mask = cv2.dilate(mask, kernel, iterations=1)
    return cv2.subtract(dilated_mask, mask)

def apply_sticker_effect(image, mask, border_thickness=15):
    foreground = extract_foreground(image, mask)
    border_mask = create_sticker_border(mask, border_thickness)
    h, w = image.shape[:2]
    border_img = np.zeros((h, w, 3), dtype=np.uint8)
    border_img[:] = (255, 255, 255)
    border_only = cv2.bitwise_and(border_img, border_img, mask=border_mask)
    combined_mask = cv2.bitwise_or(mask, border_mask)
    return cv2.add(foreground, border_only), combined_mask

def create_transparent_sticker(image, mask):
    b, g, r = cv2.split(image)
    return cv2.merge([b, g, r, mask])

def convert_to_black_and_white(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)