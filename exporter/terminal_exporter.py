import asyncio
import os
import pty
import websockets
import signal
import sys
from loguru import logger

BACKEND_URL = "ws://localhost:8001/terminal/exporter?token=terminal"
# BACKEND_URL = "ws://192.168.1.39:8001/terminal/exporter?token=terminal"
HEARTBEAT_INTERVAL = 10

fd = None
pid = None


async def handle_terminal(websocket):
    async def read_from_terminal():
        while True:
            try:
                data = await  asyncio.get_running_loop().run_in_executor(None, os.read, fd, 1024)
                if not data:
                    break
                await websocket.send(data.decode(errors="ignore"))
            except Exception as e:
                logger.error(f"Error reading from terminal: {e}")
                raise ConnectionError

    async def write_to_terminal():
        try:
            async for message in websocket:
                os.write(fd, message.encode())
        except Exception as e:
            logger.error(f"Error writing to terminal: {e}")
            raise ConnectionError

    await asyncio.gather(read_from_terminal(), write_to_terminal())


async def terminal_exporter():
    global fd, pid

    pid, fd = pty.fork()
    if pid == 0:
        os.execvp("/bin/bash", ["/bin/bash"])

    while True:
        try:
            logger.info("Connecting to backend")
            async with websockets.connect(BACKEND_URL, ping_interval=None) as websocket:
                logger.info("Connect success")
                await handle_terminal(websocket)

        except (websockets.ConnectionClosed, OSError):
            logger.info("Connection lost")
            await asyncio.sleep(3)
            logger.info("Reconnecting")
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            await asyncio.sleep(3)


def shutdown(signal_received, frame):
    try:
        if pid:
            os.kill(pid, signal.SIGKILL)
            logger.info("Terminal killed")
    except Exception as e:
        logger.error(f"Error killing child process: {e}")
    sys.exit(0)


def start_terminal():
    signal.signal(signal.SIGINT, shutdown)
    signal.signal(signal.SIGTERM, shutdown)
    asyncio.run(terminal_exporter())

if __name__ == "__main__":
    start_terminal()