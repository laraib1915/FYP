
"""
region_mapping.py

Normalized polygons for body regions (detailed) matching the uploaded images.
Coordinates normalized to [0,1]; must match frontend script.js polygons.
"""

REGIONS = [
    {"id":"head_front","name":"Head (front)","percentage":4.5,"poly":[(0.395,0.02),(0.605,0.02),(0.675,0.095),(0.605,0.155),(0.395,0.155),(0.325,0.095)]},
    {"id":"head_back","name":"Head (back)","percentage":4.5,"poly":[(0.395,0.02),(0.605,0.02),(0.675,0.095),(0.605,0.155),(0.395,0.155),(0.325,0.095)]},

    {"id":"left_arm_front","name":"Left Arm (front)","percentage":4.5,"poly":[(0.08,0.17),(0.17,0.17),(0.24,0.30),(0.21,0.43),(0.14,0.48),(0.09,0.35)]},
    {"id":"left_arm_back","name":"Left Arm (back)","percentage":4.5,"poly":[(0.08,0.17),(0.17,0.17),(0.24,0.30),(0.21,0.43),(0.14,0.48),(0.09,0.35)]},
    {"id":"right_arm_front","name":"Right Arm (front)","percentage":4.5,"poly":[(0.92,0.17),(0.83,0.17),(0.76,0.30),(0.79,0.43),(0.86,0.48),(0.91,0.35)]},
    {"id":"right_arm_back","name":"Right Arm (back)","percentage":4.5,"poly":[(0.92,0.17),(0.83,0.17),(0.76,0.30),(0.79,0.43),(0.86,0.48),(0.91,0.35)]},

    {"id":"anterior_trunk","name":"Anterior Trunk","percentage":18,"poly":[(0.395,0.155),(0.605,0.155),(0.71,0.355),(0.62,0.63),(0.38,0.63),(0.29,0.355)]},
    {"id":"posterior_trunk","name":"Posterior Trunk","percentage":18,"poly":[(0.395,0.155),(0.605,0.155),(0.71,0.355),(0.62,0.63),(0.38,0.63),(0.29,0.355)]},

    {"id":"left_leg_front","name":"Left Leg (front)","percentage":9,"poly":[(0.395,0.63),(0.47,0.63),(0.49,0.92),(0.47,0.99),(0.395,0.99),(0.36,0.92)]},
    {"id":"left_leg_back","name":"Left Leg (back)","percentage":9,"poly":[(0.395,0.63),(0.47,0.63),(0.49,0.92),(0.47,0.99),(0.395,0.99),(0.36,0.92)]},
    {"id":"right_leg_front","name":"Right Leg (front)","percentage":9,"poly":[(0.605,0.63),(0.53,0.63),(0.51,0.92),(0.53,0.99),(0.605,0.99),(0.64,0.92)]},
    {"id":"right_leg_back","name":"Right Leg (back)","percentage":9,"poly":[(0.605,0.63),(0.53,0.63),(0.51,0.92),(0.53,0.99),(0.605,0.99),(0.64,0.92)]},

    {"id":"perineum","name":"Perineum","percentage":1,"poly":[(0.485,0.835),(0.515,0.835),(0.515,0.895),(0.485,0.895)]}
]

def poly_to_pixels(poly, width, height, image_rect=None):
    """
    Convert normalized polygon to pixel coords.
    If image_rect provided as (ox,oy,w,h), coordinates will be mapped inside that rect.
    """
    if image_rect:
        ox, oy, iw, ih = image_rect
        return [(int(ox + x*iw), int(oy + y*ih)) for (x,y) in poly]
    return [(int(x*width), int(y*height)) for (x,y) in poly]
