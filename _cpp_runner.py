#!/usr/bin/env python3
import hashlib
import os
import shutil
import subprocess
import tempfile
from pathlib import Path


def _find_compiler():
    compiler = shutil.which("g++")
    if compiler:
        return compiler, None

    local_mingw = Path.home() / "Documents" / "mingw" / "mingw64" / "bin" / "g++.exe"
    if local_mingw.exists():
        return str(local_mingw), str(local_mingw.parent)

    return "g++", None


def _environment(extra_path):
    if not extra_path:
        return None
    env = os.environ.copy()
    env["PATH"] = extra_path + os.pathsep + env.get("PATH", "")
    return env


def run_cpp(source_path, args=()):
    source_path = Path(source_path)
    source = source_path.read_text()
    digest = hashlib.sha256(source.encode()).hexdigest()[:16]
    build_root = Path(tempfile.gettempdir()) / "eulerslop_build"
    build_root.mkdir(exist_ok=True)

    stem = f"{source_path.stem}_{digest}"
    cached_source = build_root / f"{stem}.cpp"
    executable = build_root / f"{stem}{'.exe' if os.name == 'nt' else ''}"
    compiler, compiler_bin = _find_compiler()
    env = _environment(compiler_bin)
    if not executable.exists():
        cached_source.write_text(source)
        subprocess.run(
            [
                compiler,
                "-O3",
                "-march=native",
                "-std=c++17",
                "-pthread",
                str(cached_source),
                "-o",
                str(executable),
            ],
            check=True,
            env=env,
        )

    return subprocess.check_output(
        [str(executable), *(str(arg) for arg in args)],
        text=True,
        env=env,
    )
