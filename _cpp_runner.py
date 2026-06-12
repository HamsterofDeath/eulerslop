#!/usr/bin/env python3
import hashlib
import subprocess
import tempfile
from pathlib import Path


def run_cpp(source_path, args=()):
    source_path = Path(source_path)
    source = source_path.read_text()
    digest = hashlib.sha256(source.encode()).hexdigest()[:16]
    build_root = Path(tempfile.gettempdir()) / "eulerslop_build"
    build_root.mkdir(exist_ok=True)

    stem = f"{source_path.stem}_{digest}"
    cached_source = build_root / f"{stem}.cpp"
    executable = build_root / stem
    if not executable.exists():
        cached_source.write_text(source)
        subprocess.run(
            [
                "g++",
                "-O3",
                "-march=native",
                "-std=c++17",
                "-pthread",
                str(cached_source),
                "-o",
                str(executable),
            ],
            check=True,
        )

    return subprocess.check_output(
        [str(executable), *(str(arg) for arg in args)],
        text=True,
    )
