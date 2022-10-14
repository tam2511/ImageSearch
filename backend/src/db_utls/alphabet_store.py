import math
from typing import List, Tuple, Dict
import os

import numpy as np

from src.db_utls.base import BaseStore

alphabets = [
    '0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
    'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j',
    'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
    'u', 'v', 'w', 'x', 'y', 'z'
]


class AlphabetStore(BaseStore):
    def __init__(
            self,
            images_path: str,
            max_size: int = 1e+6
    ):
        self.images_path = images_path
        self.max_size = max(max_size, len(alphabets) + 1)

        self.num_levels = math.ceil(math.log(max_size, len(alphabets)))

        self.ids = np.array([], dtype='int')
        self.images_paths = np.array([], dtype=f'<U{self.num_levels}')
        self.it = 0

    def __next_image_path(self) -> str:
        num_levels = self.num_levels
        result = []
        it = self.it
        for level in range(num_levels):
            residual = it % len(alphabets)
            it = (it - residual) // len(alphabets)

            result.append(
                alphabets[residual]
            )
        self.it += 1
        return ''.join(result[::-1])

    def add(
            self,
            images: List[bytes],
            ids: List[int]
    ) -> int:
        current_size = self.it
        residue = self.max_size - current_size
        self.ids = np.concatenate((self.ids, ids))
        images_paths = []
        for image in images:
            image_path = self.__next_image_path()
            images_paths.append(image_path)
            dirs = list(image_path[:-1])
            name = f'{image_path[-1]}.png'
            dest_image_path = os.path.join(self.images_path, *dirs, name)
            os.makedirs(os.path.dirname(dest_image_path), exist_ok=True)
            with open(dest_image_path, 'wb') as file:
                file.write(image)

        self.images_paths = np.concatenate((self.images_paths, images_paths))
        return residue if residue < len(images) else len(images)

    def select(
            self,
            idxs: List[int]
    ) -> List[Dict]:
        images_paths = self.images_paths[idxs]
        ids = self.ids[idxs]
        return [
            {
                'image_path': os.path.join(
                    *list(images_paths[i][:-1]),
                    f'{images_paths[i][-1]}.png'
                ),
                'id': str(ids[i])
            }
            for i in range(len(idxs))
        ]
