import azure.functions as func
from PIL import Image
import io
from urllib.request import urlopen
import json

def main(req: funct.HttpRequest) -> func.HttpResponse:
    image_url = req.params.get('img')
    
    if not image_url:
        return func.HttpResponse(
            "please pass an image URL on the query string",
            status_code=400
        )
        
    try:
        #fetch the image from the URL
        response = urlopen(image_url)
        image_data = response.read()
        
        #open the image and extract metadata
        image = Image.open(io.BytesIO(image_data))
        metadata = {
            'format': image.format,
            'mode': image.mode,
            'size': image.size,
            'width': image.width,
            'height': image.height
        }
        
        if hasttr(image, '_getexif') and image._getexif() is not None:
            metadata['exif'] = image._getexif()
            
        return func.HttpResponse(json.dumps(metadata), mimetype='application/json')
    except Exception as e:
        return func.HttpResponse(f"An error occurred: {e}", status_code=500)))
    