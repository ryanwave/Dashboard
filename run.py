"""Start DocHub.

    python run.py                         # uses C:\\Dashboard on Windows
    python run.py --root D:\\Docs --port 8080
    set DOCHUB_ROOT=\\\\server\\share\\Dashboard && python run.py
"""
import argparse
import socket

from server.app import create_app, default_root


def main():
    ap = argparse.ArgumentParser(description="DocHub - engineering document workspace")
    ap.add_argument("--root", default=default_root(), help="Folder containing Model/Milestone/Variant folders")
    ap.add_argument("--host", default="0.0.0.0")
    ap.add_argument("--port", type=int, default=8080)
    ap.add_argument("--dev", action="store_true", help="Use the Flask development server")
    args = ap.parse_args()

    app = create_app(args.root)
    print(f"\n  DocHub is serving documents from: {app.store.root}")
    print(f"  Open  http://localhost:{args.port}  (or http://{socket.gethostname()}:{args.port} from other PCs)\n")
    if args.dev:
        app.run(host=args.host, port=args.port, debug=True)
        return
    try:
        from waitress import serve
    except ImportError:
        app.run(host=args.host, port=args.port, threaded=True)
    else:
        serve(app, host=args.host, port=args.port, threads=8)


if __name__ == "__main__":
    main()
