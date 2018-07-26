from grpc.beta import implementations
import numpy as np
from PIL import Image

import tensorflow as tf
from tensorflow_serving.apis import predict_pb2
from tensorflow_serving.apis import prediction_service_pb2

server = 'localhost:8500'
model_name = 'deeplab'
signature_name = 'predict_image'

host, port = server.split(':')
_channel = implementations.insecure_channel(host, int(port))
_TFstub = prediction_service_pb2.beta_create_PredictionService_stub(_channel)

_TFrequest = predict_pb2.PredictRequest()
_TFrequest.model_spec.name = model_name
_TFrequest.model_spec.signature_name = signature_name


def tf_predict(image_path, mask_path, request=_TFrequest, stub=_TFstub):
    """Predict image segmentation using TF Server
    Args:
        image_name: str
    Return:
        res: dict {'status': int, 'mask_path': str, 'height': int, 'width': int}.
            status: 0 is SUCCESS, 1 is FileNotFound, 2 is TFServerError, 3 is MaskSaveError, 4 is OtherErroe
    """
    res = {'status': 104, 'mask_path': 'null', 'height': 0, 'width': 0}

    try:
        im = np.array(Image.open(image_path))
    except IOError:
        res['status'] = 101
        return res

    height, width, _ = im.shape
    res['height'] = height
    res['width'] = width

    try:
        request.inputs["image"].CopyFrom(
            tf.contrib.util.make_tensor_proto(im.astype(dtype=np.float32), shape=[1, height, width, 3]))
        response = stub.Predict(request, 10.0)
        output = np.array(response.outputs['seg'].int64_val)
    except:
        res['status'] = 102
        return res

    try:
        output = np.reshape(output, (height, width)).astype(np.uint8)
        mask = Image.fromarray(output)
        mask.save(mask_path)
    except:
        res['status'] = 103
        return res
    else:
        res['status'] = 0
        res['mask_path'] = mask_path.split('/')[-1]
        return res

