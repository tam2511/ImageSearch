from typing import Tuple
from time import time
import logging

import torch

from src.search_utils.base_index import BaseIndex


class MatrixIndex(BaseIndex):
    matrix = torch.tensor([])

    def native_search(
            self,
            vector: torch.Tensor
    ) -> Tuple[torch.Tensor, torch.Tensor]:
        if self.matrix.numel() == 0:
            return torch.tensor([], dtype=torch.long), torch.tensor([], dtype=torch.float)
        start_time = time()
        dists = torch.matmul(vector, self.matrix.t())
        matmul_end_time = time()
        scores, idxs = torch.sort(dists, descending=True)
        sort_end_time = time()
        logging.info(
            'matrix query search statistics: matmul time {:.4f}, sorting time {:.4f}'.format(
                matmul_end_time - start_time,
                sort_end_time - matmul_end_time
            )
        )

        return idxs, scores

    def native_add(
            self,
            vectors: torch.Tensor
    ):
        start_time = time()
        self.matrix = torch.cat((self.matrix, vectors), dim=0) if self.matrix.numel() > 0 else vectors
        end_time = time()
        logging.info(
            '{} vectors were added to matrix index, new size is {} ({:.4f} MB), elapsed time {:.4f} seconds'.format(
                vectors.shape[0],
                self.matrix.shape[0],
                self.matrix.numel() / (256 * 1024),
                end_time - start_time
            )
        )
