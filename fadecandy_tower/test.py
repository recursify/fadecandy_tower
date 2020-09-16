import asyncio
import websockets
import itertools
import struct
import random
import time
from fire_effect import FireEffect
from shimmer_effect import ShimmerEffect

def get_command(channel, colors):
    cmd = bytearray()
    cmd.append(channel)
    cmd.extend([0,0,0])
    for c in colors:
        cmd.extend(c)
    return cmd

fire_config = {
    'delay' : 0.08,
    'reduction' : 3,
    'gradient' : [
        (0, (0, 0, 0)),
        (40, (200, 0, 0)),
        (70, (200, 102, 0)),
        (100, (255, 220, 90))
    ]
}

def iter_forever(input_list):
    while True:
        for item in input_list:
            yield item

async def hello():
    uri = "ws://192.168.1.93:7890"
    async with websockets.connect(uri) as websocket:
        channel = 0
        effects = [
            FireEffect(fire_config),
            ShimmerEffect({})
        ]

        for effect in effects:
            effect.initialize()

        effect_iterator = iter_forever(effects)
        seconds_per_effect = 10
        while True:
            for effect in effect_iterator:
                start = time.time()
                while (time.time() - start) < seconds_per_effect:
                    canvas, delay = effect.run()
                    cmd = list(itertools.chain(*canvas))
                    c = get_command(channel, cmd)
                    await websocket.send(c)
                    time.sleep(delay)


asyncio.get_event_loop().run_until_complete(hello())