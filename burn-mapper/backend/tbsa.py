"""
tbsa.py — region intersection using Pillow
"""

from io import BytesIO
import base64
from PIL import Image, ImageDraw
try:
    from .region_mapping import REGIONS, poly_to_pixels
except ImportError:
    from region_mapping import REGIONS, poly_to_pixels

def decode_base64_image(data_url):
    header, b64 = data_url.split(',', 1) if ',' in data_url else (None, data_url)
    b = base64.b64decode(b64)
    return Image.open(BytesIO(b)).convert('RGBA')

def image_has_marked_pixel(pixel):
    r,g,b,a = pixel
    return a > 20 and (r!=0 or g!=0 or b!=0)

def calculate_tbsa_from_mask(data_url):
    img = decode_base64_image(data_url)
    width, height = img.size
    pixels = img.load()
    total_tbsa = 0.0
    breakdown = {1:0.0,2:0.0,3:0.0}
    regions_out = []
    # For mapping, we assume mask is full-canvas aligned like front-end: polygons map inside image rect.
    # Here we treat the image rect as full canvas (since frontend sends full-canvas mask).
    for region in REGIONS:
        # build region mask image
        region_img = Image.new('L', (width, height), 0)
        draw = ImageDraw.Draw(region_img)
        px_poly = [(int(x*width), int(y*height)) for (x,y) in region['poly']]
        draw.polygon(px_poly, fill=255)
        region_mask = region_img.load()
        region_pixels = 0
        marked_pixels = 0
        deg_counts = {1:0,2:0,3:0}
        for y in range(height):
            for x in range(width):
                if region_mask[x,y] > 0:
                    region_pixels += 1
                    if image_has_marked_pixel(pixels[x,y]):
                        marked_pixels += 1
                        r,g,b,a = pixels[x,y]
                        if r>230 and g>200:
                            deg_counts[1]+=1
                        elif r>240 and g>100 and b>80:
                            deg_counts[2]+=1
                        elif r>140 and g<50 and b<50:
                            deg_counts[3]+=1
                        else:
                            deg_counts[2]+=1
        if region_pixels==0:
            continue
        frac = marked_pixels / region_pixels
        contrib = frac * region['percentage']
        if contrib>0:
            regions_out.append({"id":region['id'], "name":region['name'], "percent": round(contrib,2)})
        total_tbsa += contrib
        marked_total = deg_counts[1]+deg_counts[2]+deg_counts[3]
        if marked_total>0:
            breakdown[1] += (deg_counts[1]/marked_total) * contrib
            breakdown[2] += (deg_counts[2]/marked_total) * contrib
            breakdown[3] += (deg_counts[3]/marked_total) * contrib

    total_tbsa = min(100.0, total_tbsa)
    for k in breakdown: breakdown[k] = round(breakdown[k],2)
    return {"total_tbsa": round(total_tbsa,2), "breakdown": breakdown, "regions": regions_out}
