from typing import Tuple, List, Dict, Any

import torch


class BaseIndex(object):
    id_map = []

    def search(
            self,
            vector: torch.Tensor
    ) -> List[Dict]:
        idxs, scores = self.native_search(vector)
        # TODO: fix slow place
        return [
            {
                'id': self.id_map[idx.item()],
                'score': scores[i].item(),
                'idx': idx.item()
            }
            for i, idx in enumerate(idxs)
        ]

    def add(
            self,
            vectors: torch.Tensor,
            ids: List[Any]
    ):
        self.native_add(vectors)
        self.id_map += ids

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
