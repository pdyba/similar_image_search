import timm
import torch
from numpy import ndarray
from PIL import Image
from sklearn.preprocessing import normalize
from timm.data import resolve_data_config
from timm.data.transforms_factory import create_transform

from config import MODEL_NAME


class FeatureExtractor:
    def __init__(self):
        self.model = timm.create_model(
            MODEL_NAME.value, pretrained=True, num_classes=0, global_pool="avg"
        )
        self.model.eval()
        self.input_size = self.model.default_cfg["input_size"]
        config = resolve_data_config({}, model=MODEL_NAME.value)
        self.preprocess = create_transform(**config)

    def __call__(self, image: Image):
        input_image = image.convert("RGB")
        input_image = self.preprocess(input_image)
        input_tensor = input_image.unsqueeze(0)

        with torch.no_grad():
            output: torch.Tensor = self.model(input_tensor)

        feature_vector = output.squeeze().numpy()
        return normalize(feature_vector.reshape(1, -1), norm="l2").flatten()


def get_image_embedding(image: Image) -> ndarray:
    image_encoder = FeatureExtractor()
    return image_encoder(image)
