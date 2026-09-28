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
    ap.add_argument("--check", action="store_true", help="Test that every document can be opened, then exit")
    args = ap.parse_args()

    if args.check:
        raise SystemExit(check(args.root))

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


def check(root: str) -> int:
    """Try to open every document and print a report (useful for support)."""
    import time
    import warnings
    from server import excel_reader
    from server.storage import DocError, Store, check_readable

    warnings.filterwarnings("ignore")
    store = Store(root)
    docs = store.all_docs(supported_only=False)
    print(f"\nChecking {len(docs)} document(s) under {store.root}\n")
    bad = 0
    for f in docs:
        rel = store.rel(f)
        t = time.time()
        try:
            check_readable(f)
            model = excel_reader.read_workbook(str(f))
            cells = sum(s["maxRow"] * s["maxCol"] for s in model["sheets"])
            print(f"  OK    {time.time() - t:5.1f}s  {len(model['sheets'])} sheet(s), {cells:,} cells  {rel}")
        except DocError as e:
            bad += 1
            print(f"  FAIL  {rel}\n        {e.message}\n        {e.hint}")
        except Exception as e:  # noqa: BLE001 - report everything
            bad += 1
            print(f"  FAIL  {rel}\n        {type(e).__name__}: {e}")
    print(f"\n{len(docs) - bad} OK, {bad} failed\n")
    return 1 if bad else 0


if __name__ == "__main__":
    main()
