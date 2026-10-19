"""Canvas-independent geometry for Windows dashed outlines."""
import math


def dash_runs(coords, pattern, offset=0):
    """Yield visible polylines, retaining dash phase across path vertices."""
    pattern = tuple(pattern)
    if not pattern or any(value <= 0 for value in pattern):
        raise ValueError('Dash lengths must be positive')
    if len(pattern) % 2:
        pattern *= 2
    offset %= sum(pattern)
    index = 0
    while offset >= pattern[index]:
        offset -= pattern[index]
        index = (index+1) % len(pattern)
    remaining = pattern[index]-offset
    run = []
    for pos in range(2,len(coords),2):
        x,y = coords[pos-2:pos]
        endx,endy = coords[pos:pos+2]
        length = math.hypot(endx-x,endy-y)
        if not length:
            continue
        ux,uy = (endx-x)/length,(endy-y)/length
        distance = 0
        while distance < length:
            step = min(remaining,length-distance)
            nx,ny = x+ux*step,y+uy*step
            if index % 2 == 0:
                if not run:
                    run = [x,y]
                run.extend((nx,ny))
            distance += step
            x,y = nx,ny
            remaining -= step
            if remaining <= 1e-10:
                if run:
                    yield run
                    run = []
                index = (index+1) % len(pattern)
                remaining = pattern[index]
    if run:
        yield run


def shape_path(kind, coords, options):
    """Flatten an outline; ellipse samples are anchored to its starting angle.

    Chords deviate by at most about 0.1 canvas units from the ellipse.
    Keeping the angular step fixed makes animated prefixes stable.
    """
    coords = list(coords)
    if kind == 'line':
        return coords
    if kind == 'polygon':
        return coords+coords[:2] if coords[-2:] != coords[:2] else coords
    x1,y1,x2,y2 = coords
    if kind == 'rectangle':
        return [x1,y1,x2,y1,x2,y2,x1,y2,x1,y1]
    cx,cy = (x1+x2)/2,(y1+y2)/2
    rx,ry = abs(x2-x1)/2,abs(y2-y1)/2
    radius = max(rx,ry)
    step = min(math.pi/36,math.sqrt(0.8/radius)) if radius else math.pi/36
    start = math.radians(options.get('start',0)) if kind == 'arc' else 0
    extent = math.radians(options.get('extent',90)) if kind == 'arc' else 2*math.pi
    extent = max(-2*math.pi,min(2*math.pi,extent))
    count = int(abs(extent)/step)
    direction = 1 if extent >= 0 else -1
    angles = [start+direction*i*step for i in range(count+1)]
    if not angles or abs(angles[-1]-(start+extent)) > 1e-12:
        angles.append(start+extent)
    path = []
    for angle in angles:
        path.extend((cx+rx*math.cos(angle),cy-ry*math.sin(angle)))
    style = options.get('style','pieslice')
    if kind == 'oval':
        path[-2:] = path[:2]
    elif style == 'chord':
        path.extend(path[:2])
    elif style == 'pieslice':
        path.extend((cx,cy))
        path.extend(path[:2])
    return path
