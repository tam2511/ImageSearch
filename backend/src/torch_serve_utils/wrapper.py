from typing import List

import requests
import torch


class TorchServeWrapper(object):
    def __init__(
            self,
            api_url: str
    ):
        self.api_url = api_url

    def __call__(
            self,
            images_blobs: List[bytes]
    ) -> torch.Tensor:
        result = []
        for image_blob in images_blobs:
            res = requests.post(
                self.api_url,
                files=[('data', image_blob)]
            )
            result.append(torch.tensor(res.json()))
        return torch.nn.functional.normalize(
            torch.stack(result),
            dim=1
        )
