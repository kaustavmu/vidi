import pyaudio
import argparse
import asyncio
import aiohttp
import json
import os
import sys
import wave
import websockets
from websockets import client

from datetime import datetime

startTime = datetime.now()

all_mic_data = []
all_transcripts = []

FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
CHUNK = 8000

audio_queue = asyncio.Queue()

async def run(key, method, format, **kwargs):
    deepgram_url = f'{kwargs["host"]}/v1/listen?punctuate=true'
    data = kwargs["data"]
    deepgram_url += f'&channels={kwargs["channels"]}&sample_rate={kwargs["sample_rate"]}&encoding=linear16'

    # Connect to the real-time streaming endpoint, attaching our credentials.
    async with websockets.connect(
        deepgram_url, extra_headers={"Authorization": "Token {}".format(key)}
    ) as ws:

        async def sender(ws):
            nonlocal data
            try:
                await ws.send(data)
                await ws.send(json.dumps({"type": "CloseStream"}))
            except Exception as e:
                print(f"🔴 ERROR: Something happened while sending, {e}")
                raise e

            return

        async def receiver(ws):
            """Print out the messages received from the server."""
            transcript = ""

            async for msg in ws:
                res = json.loads(msg)
                try:
                    # handle local server messages
                    if res.get("msg"):
                        print(res["msg"])
                    if res.get("is_final"):
                        transcript = (
                            res.get("channel", {})
                            .get("alternatives", [{}])[0]
                            .get("transcript", "")
                        )
                        if transcript != "":
                            #print(transcript)
                            all_transcripts.append(transcript)

                except KeyError:
                    print(f"🔴 ERROR: Received unexpected API response! {msg}")

        functions = [
            asyncio.ensure_future(sender(ws)),
            asyncio.ensure_future(receiver(ws)),
        ]

        await asyncio.gather(*functions)


def speechtotext():
    """Entrypoint for the example."""
    input = "test1.wav"
    host = "wss://api.deepgram.com"

    try:
        with wave.open(input, "rb") as fh:
            (channels, sample_width, sample_rate, num_samples, _, _) = fh.getparams()
            assert sample_width == 2, "WAV data must be 16-bit."
            data = fh.readframes(num_samples)
            asyncio.run(
                run(
                    "65cc1afb3f203208cd5786f14ee206fde4ed0490",
                    "wav",
                    "text",
                    data=data,
                    channels=channels,
                    sample_width=sample_width,
                    sample_rate=sample_rate,
                    filepath=input,
                    host=host,
                )
            )
        return all_transcripts
    
      
    except websockets.exceptions.InvalidStatusCode as e:
        print(f'🔴 ERROR: Could not connect to Deepgram! {e.headers.get("dg-error")}')
        print(
            f'🔴 Please contact Deepgram Support (developers@deepgram.com) with request ID {e.headers.get("dg-request-id")}'
        )
        return
    except websockets.exceptions.ConnectionClosedError as e:
        error_description = f"Unknown websocket error."
        print(
            f"🔴 ERROR: Deepgram connection unexpectedly closed with code {e.code} and payload {e.reason}"
        )

        if e.reason == "DATA-0000":
            error_description = "The payload cannot be decoded as audio. It is either not audio data or is a codec unsupported by Deepgram."
        elif e.reason == "NET-0000":
            error_description = "The service has not transmitted a Text frame to the client within the timeout window. This may indicate an issue internally in Deepgram's systems or could be due to Deepgram not receiving enough audio data to transcribe a frame."
        elif e.reason == "NET-0001":
            error_description = "The service has not received a Binary frame from the client within the timeout window. This may indicate an internal issue in Deepgram's systems, the client's systems, or the network connecting them."

        print(f"🔴 {error_description}")
        # TODO: update with link to streaming troubleshooting page once available
        # print(f'🔴 Refer to our troubleshooting suggestions: ')
        print(
            f"🔴 Please contact Deepgram Support (developers@deepgram.com) with the request ID listed above."
        )
        return

    except websockets.exceptions.ConnectionClosedOK:
        return

    except Exception as e:
        print(f"🔴 ERROR: Something went wrong! {e}")
        return

