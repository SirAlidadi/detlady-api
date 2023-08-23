from uuid import uuid1
from PIL import Image

def upload_image(image, dir: str, resize = (160,300)):
    buffer = Image.open(image.file)
    filename = f"{uuid1().hex}.{image.filename.split('.')[-1]}"
    buffer.resize(resize).save(f"{dir}{filename}")
    
    return filename
