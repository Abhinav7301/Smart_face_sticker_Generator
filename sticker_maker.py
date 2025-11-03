import cv2
import numpy as np
from image_utils import (
    resize_image,
    preprocess_for_segmentation,
    detect_edges,
    close_edge_gaps,
    find_largest_contour,
    create_mask_from_contour,
    refine_mask_grabcut,
    apply_sticker_effect,
    create_transparent_sticker,
    convert_to_black_and_white
)

class StickerMaker:
    def __init__(self, style='normal'):
        self.style = style
    
    def process(self, image, border_thickness=15, use_grabcut=True,
                low_threshold=100, high_threshold=200):
        original = image.copy()
        
        resized = resize_image(image)
        preprocessed = preprocess_for_segmentation(resized)
        edges = detect_edges(preprocessed, low_threshold, high_threshold)
        closed_edges = close_edge_gaps(edges)
        largest_contour = find_largest_contour(closed_edges)
        
        if largest_contour is None:
            h, w = resized.shape[:2]
            mask = np.ones((h, w), dtype=np.uint8) * 255
        else:
            mask = create_mask_from_contour(resized.shape, largest_contour)
            if use_grabcut:
                mask = refine_mask_grabcut(resized, mask)
        
        if self.style == 'black and white':
            styled = convert_to_black_and_white(resized)
            styled = cv2.cvtColor(styled, cv2.COLOR_GRAY2BGR)
        else:
            styled = resized.copy()
        
        sticker, combined_mask = apply_sticker_effect(styled, mask, border_thickness)
        transparent = create_transparent_sticker(sticker, combined_mask)
        coverage = (cv2.countNonZero(mask) / (mask.shape[0] * mask.shape[1])) * 100
        
        return {
            'original': original,
            'resized': resized,
            'edges': edges,
            'closed_edges': closed_edges,
            'mask': mask,
            'sticker': sticker,
            'transparent': transparent,
            'coverage': round(coverage, 2),
            'contour': largest_contour
        }

def create_sticker(image_path, style='normal', **kwargs):
    image = cv2.imread(image_path)
    if image is None:
        raise ValueError(f"Could not read image from {image_path}")
    maker = StickerMaker(style=style)
    return maker.process(image, **kwargs)