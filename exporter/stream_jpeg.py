import asyncio
import cv2
import websockets

SERVER_URL = "ws://192.168.1.39:8001/ws/camera"


async def stream_camera():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("❌ Не удалось открыть камеру")
        return

    async with websockets.connect(SERVER_URL) as websocket:
        print("✅ Подключен к серверу")

        while True:
            ret, frame = cap.read()
            if not ret:
                continue
            _, jpeg = cv2.imencode(".jpg", frame, [int(cv2.IMWRITE_JPEG_QUALITY), 80])
            await websocket.send(jpeg.tobytes())
            await asyncio.sleep(1 / 15)  # 15 fps


if __name__ == "__main__":
    asyncio.run(stream_camera())
