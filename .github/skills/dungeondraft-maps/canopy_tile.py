"""Cut an overhead canopy tile (trees and shrubs only) from two Dungeondraft exports.

    python canopy_tile.py FULL_EXPORT GROUND_EXPORT OUT.webp [--scale 0.5] [--threshold 10 28]

FULL_EXPORT is the normal image; GROUND_EXPORT is the same map exported with identical settings
after `ddmap.py strip-canopy` (no trees or shrubs). Every pixel the vegetation changes (foliage,
trunks and their shadows) is kept from FULL_EXPORT; everything else becomes transparent.
Small speckles are removed, gaps inside crowns closed, enclosed holes up to --max-hole squares
filled (grass-coloured foliage diffs as ground) and edges feathered.
--scale shrinks the tile (Foundry stretches it to the scene); 0.5 keeps GPU memory reasonable.
"""
import argparse
import sys

import numpy as np
from PIL import Image, ImageFilter

Image.MAX_IMAGE_PIXELS = None


def canopy_alpha(full, ground, low, high, chunk=512):
    """0-255 alpha from the per-pixel colour difference, computed in row chunks to save memory."""
    a, b = np.asarray(full), np.asarray(ground)
    out = np.empty(a.shape[:2], dtype=np.uint8)
    for y in range(0, a.shape[0], chunk):
        diff = np.abs(a[y:y + chunk].astype(np.int16) - b[y:y + chunk].astype(np.int16)).max(axis=2)
        out[y:y + chunk] = (np.clip((diff - low) / (high - low), 0, 1) * 255).astype(np.uint8)
    return Image.fromarray(out)


def fill_holes(alpha, max_area):
    """Make enclosed transparent pockets smaller than max_area pixels opaque.

    Foliage whose colour is close to the grass diffs as 'ground' and leaves holes inside crowns;
    real clearings are larger or open to the map edge, so they stay transparent.
    """
    from scipy import ndimage

    a = np.asarray(alpha).copy()
    labels, count = ndimage.label(a < 64)
    if not count:
        return alpha, 0
    sizes = np.bincount(labels.ravel())
    edge = np.unique(np.concatenate([labels[0], labels[-1], labels[:, 0], labels[:, -1]]))
    small = sizes <= max_area
    small[0] = False
    small[edge] = False
    a[small[labels]] = 255
    return Image.fromarray(a), int(small.sum())


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("full")
    parser.add_argument("ground")
    parser.add_argument("out")
    parser.add_argument("--scale", type=float, default=0.5)
    parser.add_argument("--threshold", type=float, nargs=2, default=(10, 28), metavar=("LOW", "HIGH"),
                        help="colour difference treated as no vegetation / full vegetation")
    parser.add_argument("--quality", type=int, default=85)
    parser.add_argument("--ppi", type=int, default=70, help="export pixels per grid square (before --scale)")
    parser.add_argument("--max-hole", type=float, default=2.0,
                        help="enclosed gaps up to this many grid squares in area are filled as foliage")
    args = parser.parse_args(argv)

    full = Image.open(args.full).convert("RGB")
    ground = Image.open(args.ground).convert("RGB")
    if full.size != ground.size:
        sys.exit(f"Exports differ in size: {full.size} vs {ground.size}; export both at the same settings.")
    if args.scale != 1:
        size = (round(full.width * args.scale), round(full.height * args.scale))
        full, ground = full.resize(size, Image.LANCZOS), ground.resize(size, Image.LANCZOS)
    alpha = canopy_alpha(full, ground, *args.threshold)
    del ground
    k = max(3, round(6 * args.scale) | 1)  # odd kernel scaled with the image
    alpha = alpha.filter(ImageFilter.MedianFilter(3))  # compression speckle
    # Binary mask: partly-changed foliage must be fully opaque, only the outline is feathered.
    alpha = alpha.point(lambda v: 255 if v >= 48 else 0)
    alpha = alpha.filter(ImageFilter.MaxFilter(k)).filter(ImageFilter.MinFilter(k))  # close gaps in crowns
    alpha, filled = fill_holes(alpha, args.max_hole * (args.ppi * args.scale) ** 2)
    alpha = alpha.filter(ImageFilter.GaussianBlur(1.2))
    full.putalpha(alpha)
    full.save(args.out, "WEBP", quality=args.quality, method=4)
    coverage = (np.asarray(alpha) > 127).mean()
    print(f"Wrote {args.out}: {full.width}x{full.height}, canopy covers {coverage:.0%} of the map, "
          f"{filled} holes inside crowns filled")


if __name__ == "__main__":
    main()
