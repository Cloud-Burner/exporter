import argparse
import sys
from exporter.terminal_agent import run as terminal_agent_run
from exporter.stream_jpeg import start_server

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
        required=True,
        help="Адрес сервера для подключения, например ws://localhost:8000"
    )

    args = parser.parse_args()

    if args.export == "all":
        terminal_agent_run()
        start_server()

    elif args.export == "stream":
        start_server()

    elif args.export == "term":
        terminal_agent_run()

    else:
        print(f"Неизвестный режим экспорта: {args.export}")
        sys.exit(1)


if __name__ == "__main__":
    main()