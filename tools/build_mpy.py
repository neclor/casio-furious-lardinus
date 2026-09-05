"""
Copy game/src into build/ and precompile every .py there (except main.py,
the entry point PythonExtra launches from its file browser) into .mpy
bytecode using mpy-cross. The original game/src is never touched -- this
only produces a ready-to-copy-to-calculator tree under build/.

Compiling ahead of time avoids compiling from source on-device, which is
by far the most memory-hungry step on the calculator's tiny heap.

Usage: python build_mpy.py [path/to/mpy-cross(.exe)] [path/to/game/src] [path/to/build]
Defaults to tools/mpy-cross/mpy-cross(.exe), ../game/src and tools/build.
"""

import os
import shutil
import subprocess
import sys

_ROOT = os.path.dirname(__file__)
_DEFAULT_SRC_DIR = os.path.join(_ROOT, "..", "game", "src")
_DEFAULT_OUT_DIR = os.path.join(_ROOT, "../build")
_DEFAULT_MPY_CROSS = os.path.join(
    _ROOT, "mpy-cross", "mpy-cross.exe" if os.name == "nt" else "mpy-cross"
)

_SKIP_NAMES = {"main.py", "__init__.py"}


def _compile_one(mpy_cross: str, py_path: str, rel_path: str) -> None:
    mpy_path = os.path.splitext(py_path)[0] + ".mpy"
    subprocess.run(
        [mpy_cross, "-s", rel_path, "-o", mpy_path, py_path],
        check=True,
    )
    os.remove(py_path)
    print(rel_path, "->", os.path.basename(mpy_path))


def main() -> None:
    mpy_cross = sys.argv[1] if len(sys.argv) > 1 else _DEFAULT_MPY_CROSS
    src_dir = sys.argv[2] if len(sys.argv) > 2 else _DEFAULT_SRC_DIR
    out_dir = sys.argv[3] if len(sys.argv) > 3 else _DEFAULT_OUT_DIR

    if not os.path.isfile(mpy_cross):
        print(f"error: {mpy_cross} not found; build mpy-cross first", file=sys.stderr)
        sys.exit(1)

    if os.path.exists(out_dir):
        shutil.rmtree(out_dir)
    shutil.copytree(
        src_dir, out_dir,
        ignore=shutil.ignore_patterns("__pycache__", "*.pyc"),
    )

    for root, _dirs, files in os.walk(out_dir):
        for filename in files:
            if not filename.endswith(".py") or filename in _SKIP_NAMES:
                continue
            py_path = os.path.join(root, filename)
            rel_path = os.path.relpath(py_path, out_dir).replace(os.sep, "/")
            _compile_one(mpy_cross, py_path, rel_path)

    print("---")
    print("build written to", out_dir)


if __name__ == "__main__":
    main()
