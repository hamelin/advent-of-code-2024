from collections.abc import Iterator
from dataclasses import dataclass
from typing import Optional, Self


FREE = -1
Block = tuple[int, int]


@dataclass
class Disk:
    blocks: list[int]

    @classmethod
    def read_map(cls, map_: str) -> Self:
        map = [int(c) for c in map_]
        if len(map) & 1:
            map.append(0)
        assert not (len(map) & 1)

        blocks = []
        for i in range(0, len(map), 2):
            id_file = i // 2
            size = map[i]
            num_free = map[i + 1]
            blocks += [id_file] * size
            blocks += [FREE] * num_free
        return cls(blocks=blocks)

    def defragment(self) -> Self:
        num_free = sum((1 if block == FREE else 0 for block in self.blocks))
        i_left = 0
        i_right = len(self.blocks) - 1
        while i_right > len(self.blocks) - 1 - num_free:
            while i_left < i_right and self.blocks[i_left] != FREE:
                i_left += 1
            while i_right >= i_left and self.blocks[i_right] == FREE:
                i_right -= 1
            if i_left < i_right:
                self.blocks[i_left], self.blocks[i_right] = (
                    self.blocks[i_right],
                    self.blocks[i_left]
                )
        return self

    def defragment_free(self) -> Self:
        for s_file, e_file in self.iter_blocks_reverse():
            size = e_file - s_file
            if se_free := self.find_free_lower(s_file, size):
                s_free, e_free = se_free
                self.blocks[s_free:e_free] = self.blocks[s_file:e_file]
                self.blocks[s_file:e_file] = [FREE] * size
        return self

    def iter_blocks_reverse(self) -> Iterator[Block]:
        i_end = len(self.blocks)
        files_moved = {FREE}
        while i_end > 0:
            i_start = i_end - 1
            if self.blocks[i_start] not in files_moved:
                while self.blocks[i_start - 1] == self.blocks[i_end - 1]:
                    i_start -= 1
                files_moved.add(self.blocks[i_start])
                yield i_start, i_end
            i_end = i_start

    def find_free_lower(self, lower: int, size: int) -> Optional[Block]:
        i_start = 0
        while i_start < lower - size + 1:
            if self.blocks[i_start] == FREE:
                for i_end in range(i_start + 1, i_start + size):
                    if self.blocks[i_end] != FREE:
                        break
                else:
                    return i_start, i_start + size
                i_start = i_end
            else:
                i_start += 1

    def checksum(self) -> int:
        return sum(
            addr * id_file
            for addr, id_file in enumerate(self.blocks)
            if id_file != FREE
        )
