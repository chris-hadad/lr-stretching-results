"""Small portable file bindings for the mathematical replay."""
from pathlib import Path
import hashlib, json, os


def sha(path):
    h = hashlib.sha256()
    with Path(path).open('rb') as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()


def check(path, expected, size=None):
    path = Path(path)
    if size is not None and path.stat().st_size != size:
        raise ValueError('Wrong input size: ' + str(path))
    if sha(path) != expected:
        raise ValueError('Wrong input SHA-256: ' + str(path))


def save(path, value):
    with Path(path).open('x') as stream:
        json.dump(value, stream, indent=2)
        stream.write('\n')
        stream.flush()
        os.fsync(stream.fileno())


def output_directory(path):
    path = Path(path).resolve(strict=True)
    if not path.is_dir():
        raise ValueError('Output is not an existing directory')
    return path
