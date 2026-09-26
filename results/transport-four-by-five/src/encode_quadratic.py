"""Lossless complete raw-to-little-endian quadratic carrier conversion."""
from pathlib import Path
import struct, sys


def main():
    if sys.flags.optimize:
        raise RuntimeError('Optimized Python is refused for transport quadratic encoding')
    source, part, destination = sys.argv[1:]
    assert part in ('U', 'F')
    count = 591214 if part == 'U' else 41482
    with Path(source).open() as incoming, Path(destination).open('xb') as target:
        assert list(map(int, incoming.readline().split())) == [0, count, 45, 479001600]
        target.write(struct.pack('<4q', 0, count, 45, 479001600))
        for identity in range(count):
            row = list(map(int, incoming.readline().split()))
            assert len(row) == 46 and row[0] == identity
            target.write(struct.pack('<46q', *row))
        assert not incoming.read().strip()


if __name__ == '__main__':
    main()
