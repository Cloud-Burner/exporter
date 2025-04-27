import asyncio
import cv2
import websockets

# SERVER_URL = "ws://192.168.1.39:8001/camera/exporter?token=rpi&&type=raspberry_pi"
SERVER_URL="ws://localhost:8001/camera/exporter?token=rpi&&type=raspberry_pi"
async def stream_camera():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Не удалось открыть камеру")
        return

    try:
        while True:
            try:
                print("Пытаемся подключиться к серверу...")
                async with websockets.connect(SERVER_URL) as websocket:
                    print("Подключен к серверу")

                    while True:
                        ret, frame = cap.read()
                        if not ret:
                            continue
                        _, jpeg = cv2.imencode(".jpg", frame, [int(cv2.IMWRITE_JPEG_QUALITY), 80])
                        await websocket.send(jpeg.tobytes())
                        await asyncio.sleep(1/10)  # 15 fps

            except (websockets.ConnectionClosedError, websockets.ConnectionClosedOK) as e:
                print(f"⚡ Потеря соединения: {e}. Переподключаемся через 3 секунды...")
                await asyncio.sleep(3)
            except Exception as e:
                print(f"Ошибка: {e}. Переподключаемся через 3 секунды...")
                await asyncio.sleep(3)

    finally:
        cap.release()
        print("Камера освобождена")

def start_camera_stream():
    asyncio.run(stream_camera())

if __name__ == "__main__":
    start_camera_stream()