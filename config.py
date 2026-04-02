"""Configuration for Jaundice Diagnosis System"""

# Bilirubin level thresholds (mg/dL)
BILIRUBIN_THRESHOLDS = {
    'normal': 1.2,
    'mild': 3.0,
    'moderate': 10.0,
    'severe': float('inf')
}

# Color detection ranges for HSV
COLOR_DETECTION = {
    'yellow': {
        'lower': [15, 100, 100],
        'upper': [35, 255, 255]
    }
}