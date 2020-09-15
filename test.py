import asyncio
import websockets
import struct
import random
import time

def get_command(channel, colors):
    cmd = bytearray()
    cmd.append(channel)
    cmd.extend([0,0,0])
    for c in colors:
        cmd.extend(c)
    return cmd

reduction = 3
fire_gradient = [
    # (value, (r, g, b)) tuples
    (0, (0, 0, 0)),
    (40, (200, 0, 0)),
    (70, (200, 102, 0)),
    (100, (255, 220, 90))
]

def make_fire_table(grad):
    table = []
    x = 0
    for i in range(len(grad) - 1):
        lo = grad[i]
        hi = grad[i+1]
        lo_color = lo[1]
        hi_color= hi[1]
        while x < hi[0]:
            pct = (x - lo[0])/(hi[0] - lo[0])
            color = (
                int(lo_color[0] + pct * (hi_color[0] - lo_color[0])),
                int(lo_color[1] + pct * (hi_color[1] - lo_color[1])),
                int(lo_color[2] + pct * (hi_color[2] - lo_color[2]))
            )
            table.append(color)
            x += 1
    return table

fire_table = make_fire_table(fire_gradient)
colors = [(128, 128, 128) for i in range(256)]

grid = [[0 for i in range(64)] for i in range(16)]

# Initialize bottom row
for i in range(len(grid)):
    grid[i][0] = 99 if random.random() > 0.5 else 0

# https://www.youtube.com/watch?v=_SzpMBOp1mE
async def do_fire_loop(websocket):
    channel = 0

    # randomly change a few of the base pixels
    for i in range(len(grid)):
        if random.random() > 0.9:
            # grid[i][0] = random.randint(0, 99)
            grid[i][0] = 0 if random.random() > 0.5 else 99


    # do the rest of the flames
    for i in range(1, len(grid) - 1):
        row = grid[i]
        for j in range(1, len(row)):
            a, b, c = (grid[i-1][j-1], grid[i][j-1], grid[i+1][j-1])
            v = int(max((a + b + c)/3.0 - reduction, 0))
            row[j] = v
            #print("i:%s j:%s    %s %s %s -> %s" % (i, j, a, b, c, row[j]))

    new_colors = [fire_table[x] for x in (grid[7] + grid[8] + grid[9])]
    c = get_command(channel, new_colors)
    await websocket.send(c)
    time.sleep(0.08)

async def do_random_loop(websocket):
    channel = 0

    for i in range(256):
        r = 96 + random.randint(-80, 48)
        colors[i] = (r, r, r)

    c = get_command(channel, colors)
    await websocket.send(c)
    time.sleep(0.7)


async def hello():
    uri = "ws://192.168.1.93:7890"
    async with websockets.connect(uri) as websocket:
        while True:
            await do_fire_loop(websocket)
print(grid)
asyncio.get_event_loop().run_until_complete(hello())
