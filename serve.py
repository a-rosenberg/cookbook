import argparse
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

from build import build_recipes


def main():
    parser = argparse.ArgumentParser(description="Build and serve Nora's Kitchen locally.")
    parser.add_argument("--host", default="127.0.0.1", help="interface to bind (default: 127.0.0.1)")
    parser.add_argument("--port", default=8000, type=int, help="port to serve on (default: 8000)")
    args = parser.parse_args()

    project_root = Path(__file__).resolve().parent
    output_dir = project_root / "docs"
    build_recipes(output_dir=output_dir)

    handler = partial(SimpleHTTPRequestHandler, directory=str(output_dir))
    server = ThreadingHTTPServer((args.host, args.port), handler)
    print(f"Serving Nora's Kitchen at http://{args.host}:{args.port}")
    print("Press Ctrl-C to stop.")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopped.")
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
