from tqdm.auto import tqdm
from . import count_stones_after_blinks


INPUT = "0 89741 316108 7641 756 9 7832357 91"


if __name__ == "__main__":
    stones = [int(n) for n in INPUT.split()]
    for num_blinks in [25, 75]:
        num_stones_after = sum(
            count_stones_after_blinks(stone, num_blinks)
            for stone in tqdm(stones)
        )
        print(f"Number of stones after {num_blinks} blinks:", num_stones_after)
