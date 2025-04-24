import typer

from exporter.terminal_agent import start_exporter
from exporter.stream_jpeg import stream_camera

app = typer.Typer()


@app.command()
def run(
    export: str = typer.Option(
        ...,  # означает, что флаг обязателен
        "--export",
        help="Что экспортировать: all, video, terminal",
        show_default=False,
        case_sensitive=False,
    ),
):
    allowed = {"all", "video", "terminal"}
    export = export.lower()

    if export not in allowed:
        typer.secho(
            f"Ошибка: недопустимое значение --export: {export}", fg=typer.colors.RED
        )
        raise typer.Exit(code=1)
    match export:
        case "all":
            stream_camera()
            start_exporter()
        case "video":
            stream_camera()
        case "terminal":
            print("rem")
            start_exporter()


if __name__ == "__main__":
    app()
