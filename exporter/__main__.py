import argparse
import sys
from exporter.terminal_exporter import start_terminal
from exporter.stream_exporter import start_camera_stream

def main():
    parser = argparse.ArgumentParser(
        description="Экспортёр терминала: режимы работы all / stream / term"
    )

    parser.add_argument(
        "--export",
        type=str,
        choices=["all", "stream", "term"],
        required=True,
        help="Режим экспорта: all, stream, или term"
    )

    parser.add_argument(
        "--server",
        type=str,
        required=False,
        help="Адрес сервера для подключения, например ws://localhost:8000"
    )

    args = parser.parse_args()

    if args.export == "all":
        start_terminal()
        start_camera_stream()

    elif args.export == "stream":
        start_camera_stream()

    elif args.export == "term":
        start_terminal()

    else:
        print(f"Неизвестный режим экспорта: {args.export}")
        sys.exit(1)


if __name__ == "__main__":
    main()