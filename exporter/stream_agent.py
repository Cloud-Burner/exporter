import asyncio

from aiohttp import web
from aiortc import RTCPeerConnection, RTCSessionDescription
from aiortc.contrib.media import MediaPlayer, MediaRelay

pcs = set()
relay = MediaRelay()

player = MediaPlayer("/dev/video0", format="v4l2", options={"video_size": "640x480"})


async def offer(request):
    body = await request.json()
    pc = RTCPeerConnection()
    pcs.add(pc)
    await pc.setRemoteDescription(
        RTCSessionDescription(sdp=body["sdp"], type=body["type"])
    )
    if player.video:
        pc.addTrack(relay.subscribe(player.video))
    for transceiver in pc.getTransceivers():
        if transceiver.kind == "audio":
            pc.removeTrack(transceiver.sender)

    answer = await pc.createAnswer()
    await pc.setLocalDescription(answer)

    return web.json_response(
        {"sdp": pc.localDescription.sdp, "type": pc.localDescription.type}
    )


async def on_shutdown(app):
    coros = [pc.close() for pc in pcs]
    await asyncio.gather(*coros)
    pcs.clear()


app = web.Application()
app.router.add_post("/offer", offer)
app.on_shutdown.append(on_shutdown)


def start_stream():
    web.run_app(app, host="0.0.0.0", port=8080)


if __name__ == "__main__":
    web.run_app(app, host="0.0.0.0", port=8080)
