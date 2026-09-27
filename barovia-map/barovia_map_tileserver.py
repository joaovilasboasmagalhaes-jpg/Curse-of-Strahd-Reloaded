#!/usr/bin/env python3
"""Serve the Barovia player map as XYZ tiles with matching landmark coordinates."""

from functools import lru_cache
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from io import BytesIO
import argparse
import json
import math
import os
from pathlib import Path
from urllib.parse import urlsplit

from PIL import Image


MAP_PATH = Path(__file__).with_name("008-cos201.webp")
BIND_HOST = os.environ.get("BAROVIA_MAP_BIND_HOST", "127.0.0.1")
PUBLIC_HOST = os.environ.get("BAROVIA_MAP_PUBLIC_HOST", "127.0.0.1")
PORT = int(os.environ.get("BAROVIA_MAP_PORT", "8765"))
TILE_SIZE = 256
CENTER_LON = 0.0
CENTER_LAT = 45.0
LON_SPAN = 20.0

# Pixel pins from the Barovia Travel Planner's official player-map dataset.
# https://github.com/keemal94/barovia-travel-planner/blob/main/data/barovia-terrain.json
PINS = [
    ("Village of Barovia", 3994, 1955, 201, 85, True),
    ("Gates of Barovia", 3038, 1384, 153, 60, False),
    ("Tser Pool Encampment", 3246, 1954, 163, 85, True),
    ("Tser Falls", 3034, 1733, 152, 76, True),
    ("Black Carriage", 3042, 1544, 153, 67, False),
    ("Gates of Ravenloft", 3427, 1638, 172, 72, False),
    ("Castle Ravenloft", 3616, 1660, 182, 73, False),
    ("River Ivlis Crossroads", 3402, 2340, 171, 102, False),
    ("Old Bonegrinder", 2436, 1304, 123, 57, False),
    ("Town of Vallaki", 2011, 1137, 101, 50, True),
    ("Lake Zarovich", 2090, 814, 105, 36, False),
    ("Luna River Crossroads", 1775, 1172, 89, 51, False),
    ("Raven River Crossroads", 1096, 1080, 56, 48, False),
    ("Argynvostholt", 1662, 1580, 84, 69, False),
    ("Van Richten's Tower", 1262, 866, 64, 38, False),
    ("Village of Krezk", 641, 989, 33, 43, True),
    ("Wizard of Wines", 576, 1510, 29, 66, False),
    ("Yester Hill", 350, 2009, 18, 88, False),
    ("Ruins of Berez", 1659, 1934, 84, 85, False),
    ("Tsolenka Pass", 1240, 2452, 63, 107, True),
    ("The Amber Temple", 1687, 2698, 85, 117, False),
    ("Werewolf Den", 895, 731, 45, 32, False),
    ("Mad Mage of Mount Baratok", 2295, 476, 115, 21, False),
]

MAP = Image.open(MAP_PATH).convert("RGBA")
if MAP.size != (5025, 3225):
    raise SystemExit(f"Expected the planner's 5025x3225 player map; got {MAP.size}")


def mercator_y_fraction(latitude: float) -> float:
    latitude = max(-85.05112878, min(85.05112878, latitude))
    radians = math.radians(latitude)
    return (1.0 - math.asinh(math.tan(radians)) / math.pi) / 2.0


def inverse_mercator_latitude(y_fraction: float) -> float:
    return math.degrees(math.atan(math.sinh(math.pi * (1.0 - 2.0 * y_fraction))))


def normalized_bounds() -> tuple[float, float, float, float]:
    left = (CENTER_LON - LON_SPAN / 2.0 + 180.0) / 360.0
    right = (CENTER_LON + LON_SPAN / 2.0 + 180.0) / 360.0
    top_center = mercator_y_fraction(CENTER_LAT)
    height = (right - left) * MAP.height / MAP.width
    return left, top_center - height / 2.0, right, top_center + height / 2.0


def pins_payload() -> bytes:
    left, top, right, bottom = normalized_bounds()
    pins = []
    for name, px, py, col, row, player in PINS:
        x_fraction = left + (px / MAP.width) * (right - left)
        y_fraction = top + (py / MAP.height) * (bottom - top)
        pins.append(
            {
                "name": name,
                "latitude": round(inverse_mercator_latitude(y_fraction), 7),
                "longitude": round(x_fraction * 360.0 - 180.0, 7),
                "pixel": [px, py],
                "fineHex": [col, row],
                "playerMapLabel": player,
            }
        )
    payload = {
        "coordinateFrame": {
            "description": "Synthetic local frame; not real Barovian or Earth coordinates.",
            "center": [CENTER_LAT, CENTER_LON],
            "longitudeSpan": LON_SPAN,
            "imageSize": [MAP.width, MAP.height],
            "image": MAP_PATH.name,
        },
        "pins": pins,
    }
    return json.dumps(payload, indent=2).encode("utf-8")


@lru_cache(maxsize=512)
def render_tile(zoom: int, tile_x: int, tile_y: int) -> bytes | None:
    world_size = TILE_SIZE * (1 << zoom)
    left_n, top_n, right_n, bottom_n = normalized_bounds()
    left, top = left_n * world_size, top_n * world_size
    right, bottom = right_n * world_size, bottom_n * world_size
    tile_left, tile_top = tile_x * TILE_SIZE, tile_y * TILE_SIZE
    tile_right, tile_bottom = tile_left + TILE_SIZE, tile_top + TILE_SIZE

    if tile_right <= left or tile_left >= right or tile_bottom <= top or tile_top >= bottom:
        return None

    scale_x = MAP.width / (right - left)
    scale_y = MAP.height / (bottom - top)
    offset_x = (tile_left - left) * scale_x
    offset_y = (tile_top - top) * scale_y
    tile = MAP.transform(
        (TILE_SIZE, TILE_SIZE),
        Image.Transform.AFFINE,
        (scale_x, 0, offset_x, 0, scale_y, offset_y),
        resample=Image.Resampling.BICUBIC,
        fillcolor=(0, 0, 0, 0),
    )
    output = BytesIO()
    tile.save(output, format="PNG", optimize=True)
    return output.getvalue()


def export_tiles(output_dir: Path, max_zoom: int) -> int:
    if not 0 <= max_zoom <= 12:
        raise ValueError("Maximum zoom must be between 0 and 12")

    output_dir.mkdir(parents=True, exist_ok=True)
    left, top, right, bottom = normalized_bounds()
    tiles_written = 0

    for zoom in range(max_zoom + 1):
        world_tiles = 1 << zoom
        min_x = max(0, math.floor(left * world_tiles))
        max_x = min(world_tiles - 1, math.ceil(right * world_tiles) - 1)
        min_y = max(0, math.floor(top * world_tiles))
        max_y = min(world_tiles - 1, math.ceil(bottom * world_tiles) - 1)

        for tile_y in range(min_y, max_y + 1):
            for tile_x in range(min_x, max_x + 1):
                image = render_tile(zoom, tile_x, tile_y)
                if image is None:
                    continue
                tile_path = output_dir / str(zoom) / str(tile_x) / f"{tile_y}.png"
                tile_path.parent.mkdir(parents=True, exist_ok=True)
                tile_path.write_bytes(image)
                tiles_written += 1

        print(f"Rendered zoom {zoom}: {tiles_written} tiles total")

    return tiles_written


class MapHandler(BaseHTTPRequestHandler):
    def do_GET(self) -> None:
        path = urlsplit(self.path).path
        if path == "/" or path == "/index.html":
            body = (
                "Barovia map tile server is running.\n"
                f"Timelines custom map tile URL: http://{PUBLIC_HOST}:{PORT}/tiles/{{z}}/{{x}}/{{y}}.png\n"
                f"Landmark coordinate list: http://{PUBLIC_HOST}:{PORT}/pins.json\n"
                "Keep this server running while using Map View.\n"
            ).encode("utf-8")
            self._send(200, "text/plain; charset=utf-8", body)
            return

        if path == "/pins.json":
            self._send(200, "application/json; charset=utf-8", pins_payload())
            return

        parts = path.strip("/").split("/")
        if len(parts) == 4 and parts[0] == "tiles" and parts[3].endswith(".png"):
            try:
                zoom = int(parts[1])
                tile_x = int(parts[2])
                tile_y = int(parts[3][:-4])
            except ValueError:
                self.send_error(400, "Tile coordinates must be integers")
                return
            if not 0 <= zoom <= 22 or not 0 <= tile_x < (1 << zoom) or not 0 <= tile_y < (1 << zoom):
                self.send_error(404)
                return
            image = render_tile(zoom, tile_x, tile_y)
            if image is None:
                self.send_error(404)
                return
            self._send(200, "image/png", image, cache_control="public, max-age=3600")
            return

        self.send_error(404)

    def _send(self, status: int, content_type: str, body: bytes, cache_control: str = "no-cache") -> None:
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", cache_control)
        self.end_headers()
        self.wfile.write(body)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--export-tiles",
        type=Path,
        metavar="DIR",
        help="write a static XYZ tile pyramid to DIR instead of starting the HTTP server",
    )
    parser.add_argument("--max-zoom", type=int, default=9)
    args = parser.parse_args()

    if args.export_tiles:
        total = export_tiles(args.export_tiles, args.max_zoom)
        print(f"Wrote {total} tiles to {args.export_tiles.resolve()}")
        raise SystemExit(0)

    server = ThreadingHTTPServer((BIND_HOST, PORT), MapHandler)
    print(f"Listening on {BIND_HOST}:{PORT}")
    print(f"Serving Barovia map tiles at http://{PUBLIC_HOST}:{PORT}/tiles/{{z}}/{{x}}/{{y}}.png")
    print(f"Landmark coordinates: http://{PUBLIC_HOST}:{PORT}/pins.json")
    print("Press Ctrl+C to stop.")
    server.serve_forever()