import torch

from ts.torch_handler.vision_handler import VisionHandler

from torchvision.transforms import *


class EmbedderHandler(VisionHandler):
    image_processing = Compose([
        transforms.Resize(224),
        ToTensor(),
        Normalize((0.485, 0.456, 0.406), (0.229, 0.224, 0.225)),
    ])

    def postprocess(self, data):
        return torch.nn.functional.normalize(data, dim=1).tolist()
