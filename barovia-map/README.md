# Barovia Map Tiles

This folder contains the player-map raster, an XYZ tile generator/server, and its Python dependency. It works on Windows, macOS, and Linux with Python 3.10 or newer. Use generated local files for the packaged Timelines desktop app; its Content Security Policy blocks HTTP map images.

The included `008-cos201.webp` is 5025 x 3225 pixels and matches the pixel pin data embedded in `barovia_map_tileserver.py`. The map uses a synthetic coordinate frame centered at latitude 45, longitude 0. These coordinates are only for positioning the fictional map and are not real-world Barovia coordinates.

## Set up the environment

Run commands from the workspace root. Create a project virtual environment and install Pillow; choose the command block for your system.

### macOS or Linux

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r barovia-map/requirements-map.txt
```

### Windows PowerShell

```powershell
py -3 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r .\barovia-map\requirements-map.txt
```

## Use the map in Timelines Desktop

The packaged `v0.7.0-alpha.2` app's Content Security Policy allows `https:` and `file:` images but blocks `http:` images. This is why an HTTP tile works when opened directly in a browser but does not appear in the app. Coordinates and the tile data are not the problem.

Generate a local XYZ tile pyramid. From the workspace root on macOS/Linux/WSL:

```sh
.venv/bin/python barovia-map/barovia_map_tileserver.py --export-tiles barovia-map/tiles --max-zoom 9
```

Print the `file:` URL to paste into Timelines:

```sh
.venv/bin/python -c "from pathlib import Path; print(Path('barovia-map/tiles').resolve().as_uri() + '/{z}/{x}/{y}.png')"
```

On Windows PowerShell, export to a Windows-visible folder instead:

```powershell
.\.venv\Scripts\python.exe .\barovia-map\barovia_map_tileserver.py --export-tiles "$env:LOCALAPPDATA\BaroviaTiles" --max-zoom 9
```

Print the matching `file:` URL in PowerShell:

```powershell
$tilesPath = (Resolve-Path "$env:LOCALAPPDATA\BaroviaTiles").Path
([System.Uri]$tilesPath).AbsoluteUri.TrimEnd('/') + '/{z}/{x}/{y}.png'
```

In Timelines, open **Settings → Maps → Tile URL**, paste the printed URL, and use the map/timeline toggle to open Map View.

For a Windows desktop app with the workspace in WSL, tiles under `barovia-map/tiles` are available through the WSL file share. Build the URL from the WSL distro name and absolute folder path:

```sh
printf 'file://wsl.localhost/%s%s/{z}/{x}/{y}.png\n' "$WSL_DISTRO_NAME" "$(realpath barovia-map/tiles)"
```

Paste the printed URL into the Windows app's Tile URL setting. In this workspace, it resolves to `file://wsl.localhost/Ubuntu/home/joaomaga/Curse-of-Strahd-Reloaded/barovia-map/tiles/{z}/{x}/{y}.png`. Keep the generated folder in place; rerun the export command if it is deleted. The pyramid contains zoom levels 0 through 9.

## Run the HTTP server for browser testing

The on-demand HTTP server is useful for checking the image in a browser, but the packaged desktop app's CSP blocks its `http:` tile images. From the workspace root, run:

```sh
.venv/bin/python barovia-map/barovia_map_tileserver.py
```

It listens on `127.0.0.1:8765` by default. Open <http://127.0.0.1:8765/> to verify it is running; the landmark list is at <http://127.0.0.1:8765/pins.json>. To stop it, focus its terminal and press **Ctrl+C**. Stop an existing instance before starting another; otherwise the port reports `Address already in use`.

## Markers

Ensure **Map View** is enabled, then use the map/timeline toggle at the top-right of the canvas. Elements with `lat` and `lng` values appear as markers; elements without coordinates do not. The landmark list from the HTTP server includes latitude/longitude plus source pixels and fine-grid hexes. For example, Vallaki is latitude `46.3226007`, longitude `-1.9960199`.

The full landmark coordinate list is served at <http://127.0.0.1:8765/pins.json>. Each entry includes `latitude` and `longitude`, plus the source image pixel and fine-grid hex. Use those values in the element's Coordinates field in latitude, longitude order. For example, Vallaki is latitude `46.3226007`, longitude `-1.9960199`.

## Use a different image

The server transforms source-image pixels into Leaflet-compatible Web Mercator XYZ tiles as HTTP requests arrive. The export mode writes the same tile format to disk for use with the desktop app's allowed `file:` scheme.

The pin positions are calibrated specifically to the included image. A different crop, resize, or map version will misalign them. To substitute another raster, update `MAP_PATH`, the expected image-size check, the `PINS` pixel positions, and the synthetic coordinate-frame constants in `barovia_map_tileserver.py`. Remove or replace pins that do not belong on the new image. Keep image north at the top; the server does not rotate or georeference arbitrary source projections.

Tiles use `{z}/{x}/{y}.png`; only tiles intersecting the map image are generated.

## Git and map artwork

Commit `.gitignore` and the complete `barovia-map/` folder so a fresh checkout includes the image, generator/server, dependency list, and these instructions. Do not commit `.venv/` or `barovia-map/tiles/`; recreate both on each system with the commands above.

The tile URL is stored in the timeline JSON and must be an absolute URL. A `file:` URL points to the generated tiles on one machine, so it cannot be shared unchanged in Git. After cloning/importing on each environment, generate the tiles and set that machine's URL in **Settings → Maps → Tile URL**. The WSL `file:` URL generated by the command above is specific to this distro and folder; native Windows, macOS, Linux, or another WSL distro needs its own path. Do not commit a machine-specific `mapTileUrl` as though it were portable.

The included Barovia map artwork is copyrighted; only commit or redistribute it if your use and repository visibility permit. Otherwise, provide the raster locally before generating tiles.