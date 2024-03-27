import azure.functions as func
from PIL import Image
from io import BytesIO
from urllib.request import urlopen
from SharedCode.image_utils import preprocess_image_for_classification

def preprocess_image(image_data):
    
    image = Image.open(io.BytesIO(image_data))
    image = image.resize(224, 224)).convert('L')
    return image

def main(req: func.HttpRequest) -> func.HttpResponse:
    image_url = req.params.get('img')
    
    if not image_url:
        return func.HttpResponse(
            "Please pass an image URL on the query string",
            status_code=400
        )
        
    try:
        response = urlopen(image_url)
        image_data = response.read()
        image = preprocess_image(image_data)
        img_byte_arr = io.BytesIO()
        image.save(img_byte_arr, format='PNG')
        img_byte_arr = img_byte_arr.getvalue()
        
        return func.HTTPResponse(
            img_byte_arr,
            status_code=200,
            headers={'Content-Type': 'image/png'}
        )
    except Exception as e:
        return func.HttpResponse(
            f"An error occurred: {e}",
            status_code=500
        )