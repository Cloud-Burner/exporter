import asyncio
import os
import pty
import signal
import sys

import websockets


async def terminal_handler(websocket):
    pid, fd = pty.fork()
    if pid == 0:
        os.execvp("bash", ["bash"])
    else:

        async def read_from_pty():
            loop = asyncio.get_event_loop()
            while True:
                try:
                    data = await loop.run_in_executor(None, os.read, fd, 1024)
                    await websocket.send(data.decode(errors="ignore"))
                except Exception:
                    break

        async def write_to_pty():
            async for message in websocket:
                try:
                    os.write(fd, message.encode())
                except Exception:
                    break

        await asyncio.gather(read_from_pty(), write_to_pty())
        try:
            os.kill(pid, signal.SIGKILL)
        except Exception:
            pass


async def export_terminal():
    async with websockets.serve(terminal_handler, "0.0.0.0", 8765):
        await asyncio.Future()


def start_exporter():
    try:
        asyncio.run(export_terminal())
    except KeyboardInterrupt:
        sys.exit(0)


if __name__ == "__main__":
    start_exporter()
