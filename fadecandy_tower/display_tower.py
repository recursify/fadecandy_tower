import asyncio
import os
import websockets
import itertools
import struct
import random
import time
import argparse
from fire_effect import FireEffect
from shimmer_effect import ShimmerEffect
from rotate_effect import RotateEffect

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

rainbow_fire_config = {
    'delay' : 0.08,
    'reduction' : 3,
    'gradient' : [
        (0, (0, 0, 0)),
        (20, (240, 0, 0)),
        (50, (240, 240, 0)),
        (100, (0, 0, 240))
    ]
}

def iter_forever(input_list):
    while True:
        for item in input_list:
            yield item



async def run_forever(websocket):
    base = os.path.join(
        os.path.split(os.path.abspath(__file__))[0],
        'images'
    )
    channel = 0
    effects = [
        RotateEffect({
            'img_path' : os.path.join(base, 'abstract.png'),
        }),
        RotateEffect({
            'img_path' : os.path.join(base, 'yellow_stripe.png'),
        }),
        FireEffect(rainbow_fire_config),
        FireEffect(fire_config),
        ShimmerEffect({})
    ]

    for effect in effects:
        effect.initialize()

    effect_iterator = iter_forever(effects)
    seconds_per_effect = 10
    while True:
        for effect in effect_iterator:
            effect.initialize()
            start = time.time()
            while (time.time() - start) < seconds_per_effect:
                canvas, delay = effect.run()
                cmd = list(itertools.chain(*canvas))
                c = get_command(channel, cmd)
                await websocket.send(c)
                await asyncio.sleep(delay)

async def run(uri):
    async with websockets.connect(uri) as websocket:
        await run_forever(websocket)

async def cleanup(uri):
    async with websockets.connect(uri) as websocket:
        turn_off_command = get_command(0, [(0, 0, 0) for i in range(512)])
        await websocket.send(turn_off_command)


def main(args):
    uri = f"ws://{args.host}:{args.port}"
    loop = asyncio.get_event_loop()

    try:
        tasks = asyncio.gather(run(uri))
        loop.run_until_complete(tasks)
    finally:
        print('Shutting down...')
        loop = asyncio.get_event_loop()
        loop.run_until_complete(cleanup(uri))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', dest='host', default='localhost')
    parser.add_argument('--port', dest='port', type=int, default=7890)
    args = parser.parse_args()
    main(args)
