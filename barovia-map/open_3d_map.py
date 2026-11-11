import argparse
import ctypes
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import socket
import sys
import tempfile
import traceback
from urllib.error import URLError
from urllib.request import urlopen
import webbrowser


ROOT = Path(__file__).resolve().parent
VIEWERS = {
    "zootlocker": (
        ROOT / "zootlocker-3d",
        "/nofog.html",
        18765,
        ["nofog.html", "1barovia.js", "Qgis2threejsnofog.js",
         "threejs/three.min.js", "threejs/OrbitControls.js",
         "dat-gui/dat.gui.min.js", "dat-gui_panel.js"],
    ),
    "stl": (
        ROOT / "stl-viewer-3d",
        "/3dnd_maps/index.html?map=barovia1v2",
        18766,
        ["3dnd_maps/index.html", "3dnd_maps/assets/index.dev-Bs_4guqf.js",
         "3dnd_maps/assets/barovia1/Barovia-5e_trim.png",
         "3dnd_maps/assets/barovia1/barovia_map_v2.stl"],
    ),
}
IDENTITY_PATH = "/__barovia_3d_viewer__"


class MapServer(ThreadingHTTPServer):
    allow_reuse_address = False

    def server_bind(self):
        if hasattr(socket, "SO_EXCLUSIVEADDRUSE"):
            self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_EXCLUSIVEADDRUSE, 1)
        super().server_bind()


class MapHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, directory, identity, **kwargs):
        self.identity = identity
        super().__init__(*args, directory=directory, **kwargs)

    def do_GET(self):
        if self.path == IDENTITY_PATH:
            body = self.identity.encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "text/plain; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
        else:
            super().do_GET()


def existing_server_matches(port, identity):
    try:
        with urlopen(f"http://127.0.0.1:{port}{IDENTITY_PATH}", timeout=2) as response:
            return response.read() == identity.encode("utf-8")
    except (URLError, TimeoutError, OSError):
        return False


def open_browser(url):
    if not webbrowser.open(url):
        raise RuntimeError("Could not open a browser automatically.")


def main():
    parser = argparse.ArgumentParser(description="Open an offline 3D Barovia map.")
    parser.add_argument("viewer", choices=VIEWERS)
    parser.add_argument("--background", action="store_true")
    args = parser.parse_args()
    directory, path, port, required = VIEWERS[args.viewer]

    missing = [str(directory / name) for name in required if not (directory / name).is_file()]
    if missing:
        raise FileNotFoundError("Missing map files:\n" + "\n".join(missing))

    identity = f"{args.viewer}:{directory.resolve()}"
    url = f"http://127.0.0.1:{port}{path}"
    handler = partial(MapHandler, directory=str(directory), identity=identity)
    try:
        server = MapServer(("127.0.0.1", port), handler)
    except OSError as error:
        if existing_server_matches(port, identity):
            open_browser(url)
            return
        raise RuntimeError(f"Cannot start the map server on port {port}: {error}") from error

    with server:
        print(f"Opening {url}", flush=True)
        open_browser(url)
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            print("\nMap server stopped.")


if __name__ == "__main__":
    if "--background" in sys.argv:
        log_path = Path(tempfile.gettempdir()) / "barovia-3d-viewers.log"
        with log_path.open("a", encoding="utf-8", buffering=1) as log:
            sys.stdout = sys.stderr = log
            try:
                main()
            except Exception as error:
                traceback.print_exc()
                ctypes.windll.user32.MessageBoxW(
                    0, f"{error}\n\nDetails: {log_path}", "Barovia 3D map", 0x10
                )
                raise SystemExit(1)
    else:
        main()
