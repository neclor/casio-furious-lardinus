import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "Fx-SDK-2.11.0", "fxconv"))

import fxconv

_ASSETS_DIR = os.path.join(os.path.dirname(__file__), "..", "game", "src", "assets")
_PROFILE_NAME = "gray_alpha"


def _pack_layers(img: "fxconv.Image.Image", profile: "fxconv.FxProfile") -> bytes:
    layers = [fxconv._image_project(img, layer) for layer in profile.layers]
    count = len(layers)
    size = len(layers[0])

    data = bytearray(count * size)
    n = 0
    for longword in range(size // 4):
        for layer in layers:
            for i in range(4):
                data[n] = layer[4 * longword + i]
                n += 1
    return bytes(data)


def _convert(png_path: str, py_path: str) -> None:
    img = fxconv.Image.open(png_path)
    img = fxconv.quantize(img, dither=False)
    profile = fxconv.FxProfile.find(_PROFILE_NAME)

    data = _pack_layers(img, profile)
    width, height = img.size

    with open(py_path, "w") as file:
        file.write("import gint\n\n")
        file.write(f"image = gint.image({profile.id}, {width}, {height}, {data!r})\n")


def _ensure_init_py(directory: str) -> None:
    init_path = os.path.join(directory, "__init__.py")
    if not os.path.exists(init_path):
        open(init_path, "w").close()


def main() -> None:
    init_dirs = set()
    for root, _dirs, files in os.walk(_ASSETS_DIR):
        pngs = [f for f in files if f.lower().endswith(".png")]
        if not pngs:
            continue

        directory = root
        while True:
            init_dirs.add(directory)
            if os.path.normpath(directory) == os.path.normpath(_ASSETS_DIR):
                break
            directory = os.path.dirname(directory)

        for filename in pngs:
            png_path = os.path.join(root, filename)
            py_path = os.path.splitext(png_path)[0] + ".py"
            _convert(png_path, py_path)
            print(py_path)

    for directory in init_dirs:
        _ensure_init_py(directory)


if __name__ == "__main__":
    main()
