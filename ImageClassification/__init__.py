import azure.functions as func
from SharedCode.model import load_model, get_class_labels
from SharedCode.image_utils import preprocess_image
from PIL import Image
from io import BytesIO
from urllib.request import urlopen

def main(req: func.HttpRequest) -> func.HttpResponse:
    image_url = req.params.get('img')

    if not image_url:
        return func.HttpResponse(
             "Please pass an image URL on the query string",
             status_code=400
        )

    model = load_model()
    class_labels = get_class_labels()

    try:
        with urlopen(image_url) as test_image:
            image = Image.open(test_image).convert('RGB')
            processed_image = preprocess_image(image)

            # Predict the class of the image
            prediction, confidence = model.predict(processed_image)
            predicted_class_name = class_labels[prediction]

            response = {
                'created': datetime.utcnow().isoformat(),
                'predictedTagName': predicted_class_name,
                'prediction': confidence
            }

            return func.HttpResponse(json.dumps(response), mimetype="application/json")
    except Exception as e:
        return func.HttpResponse(str(e), status_code=500)
