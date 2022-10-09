from typing import Tuple, List, Dict, Any

import torch


class BaseIndex(object):

    def search(
            self,
            vector: torch.Tensor
    ) -> Tuple[List, List]:
        idxs, scores = self.native_search(vector)
        return idxs.tolist(), scores.tolist()

    def add(
            self,
            vectors: torch.Tensor
    ):
        self.native_add(vectors)

    def native_search(
            self,
            vector: torch.Tensor
    ) -> Tuple[torch.Tensor, torch.Tensor]:
        raise NotImplementedError

    def native_add(
            self,
            vectors: torch.Tensor,
    ):
        raise NotImplementedError
