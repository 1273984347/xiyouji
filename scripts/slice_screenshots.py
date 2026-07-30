#!/usr/bin/env python3
"""Slice full-page screenshots into fixed-height chunks for pixel-level review."""

import argparse
import glob
import os
import sys
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_OUT = os.path.join(ROOT, 'scripts', 'output', 'screenshots')
DEFAULT_SLICE_HEIGHT = 800


def slice_image(src_path, dst_dir, slice_height=DEFAULT_SLICE_HEIGHT):
    """Slice a PNG into vertical chunks and return list of relative paths."""
    img = Image.open(src_path)
    w, h = img.size
    base = os.path.splitext(os.path.basename(src_path))[0]
    chunks = []
    idx = 0
    for y in range(0, h, slice_height):
        box = (0, y, w, min(y + slice_height, h))
        crop = img.crop(box)
        dst_name = f'{base}_{idx:03d}.png'
        dst_path = os.path.join(dst_dir, dst_name)
        crop.save(dst_path)
        chunks.append(os.path.relpath(dst_path, ROOT).replace(os.sep, '/'))
        idx += 1
    return chunks, (w, h), idx


def clean_dir(dst_dir):
    """Remove existing PNG slices to avoid stale residue from previous runs."""
    if os.path.isdir(dst_dir):
        for f in glob.glob(os.path.join(dst_dir, '*.png')):
            os.remove(f)


def main():
    parser = argparse.ArgumentParser(
        description='Slice full-page screenshots into fixed-height chunks for pixel-level review.'
    )
    parser.add_argument(
        '--output-dir',
        default=DEFAULT_OUT,
        help=f'Output root directory containing desktop/ and mobile/ screenshots (default: {DEFAULT_OUT})',
    )
    parser.add_argument(
        '--slice-height',
        type=int,
        default=DEFAULT_SLICE_HEIGHT,
        help=f'Height of each slice in pixels (default: {DEFAULT_SLICE_HEIGHT})',
    )
    args = parser.parse_args()

    output_dir = args.output_dir
    slice_height = args.slice_height

    slices_root = os.path.join(output_dir, 'slices')
    report = []
    report.append('# Screenshot Slice Index')
    report.append('')
    report.append(f'切片高度：{slice_height}px')
    report.append('')

    for viewport in ['desktop', 'mobile']:
        src_dir = os.path.join(output_dir, viewport)
        dst_dir = os.path.join(slices_root, viewport)
        os.makedirs(dst_dir, exist_ok=True)
        clean_dir(dst_dir)

        report.append(f'## {viewport}')
        report.append('')
        report.append('| 页面 | 原始尺寸 | 切片数 | 切片路径 |')
        report.append('|---|---|---|---|')

        files = sorted(glob.glob(os.path.join(src_dir, '*.png')))
        for src in files:
            chunks, (w, h), count = slice_image(src, dst_dir, slice_height)
            page_name = os.path.splitext(os.path.basename(src))[0]
            rel_chunks = ', '.join(chunks)
            report.append(f'| {page_name} | {w}x{h} | {count} | {rel_chunks} |')
        report.append('')

    index_path = os.path.join(output_dir, 'slice-index.md')
    with open(index_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(report))
    print(f'Slice index written to {index_path}')


if __name__ == '__main__':
    main()
