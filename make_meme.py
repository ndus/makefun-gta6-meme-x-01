"""Draw an original, asset-free loading-screen meme with Pillow."""
from pathlib import Path
import math
from PIL import Image, ImageDraw, ImageFont, ImageFilter

SCALE = 2
SIZE = 1200
FONT = '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
PLUM = '#1D0B16'
MAGENTA = '#D63384'


def box(coords):
    return tuple(round(v * SCALE) for v in coords)


def font(size):
    return ImageFont.truetype(FONT, round(size * SCALE))


def gradient(image):
    stops = [(0, (39, 17, 70)), (0.32, (113, 32, 106)),
             (0.53, (218, 79, 131)), (0.68, (255, 168, 110)),
             (0.69, (102, 47, 73)), (1, (40, 22, 40))]
    draw = ImageDraw.Draw(image)
    for y in range(image.height):
        t = y / (image.height - 1)
        for (a, ca), (b, cb) in zip(stops, stops[1:]):
            if a <= t <= b:
                f = (t - a) / (b - a)
                color = tuple(round(x + (z - x) * f) for x, z in zip(ca, cb))
                draw.line((0, y, image.width, y), fill=color)
                break


def outlined_text(draw, text, y, size, max_width=1110, stroke=5):
    while draw.textbbox((0, 0), text, font=font(size), stroke_width=stroke*SCALE)[2] > max_width*SCALE:
        size -= 1
    draw.text((600*SCALE, y*SCALE), text, font=font(size), fill='white',
              stroke_width=stroke*SCALE, stroke_fill=PLUM, anchor='mt')


def skyline(draw):
    buildings = [(0, 65, 42), (55, 47, 75), (92, 70, 52), (151, 54, 101),
                 (199, 77, 57), (270, 56, 122), (320, 74, 74),
                 (387, 50, 46), (435, 85, 63), (517, 68, 41),
                 (583, 55, 88), (631, 75, 52), (700, 70, 65),
                 (766, 54, 94), (815, 92, 49), (901, 65, 75),
                 (962, 53, 110), (1007, 85, 62), (1087, 64, 91), (1142, 65, 45)]
    for x, w, h in buildings:
        draw.rectangle(box((x, 816-h, x+w, 827)), fill=PLUM)
    draw.line(box((295, 694, 295, 670)), fill=PLUM, width=4*SCALE)


def palm(draw, base_x, crown_x, crown_y, height):
    # Tapered, curving trunks and individually arched, pointed leaves.
    points = []
    for i in range(41):
        t = i/40
        x = base_x + (crown_x-base_x)*t*t
        y = crown_y + height*(1-t)
        points.append((x, y, 15*(1-t)+5))
    polygon = [(x-w, y) for x,y,w in points] + [(x+w,y) for x,y,w in reversed(points)]
    draw.polygon([box(p) for p in polygon], fill=PLUM)
    for dx, dy in [(-210, 65), (-190, -38), (-120, -112), (-30, -143),
                   (100, -115), (185, -45), (215, 65), (135, 125)]:
        leaf=[]
        for i in range(25):
            t=i/24
            x=crown_x+dx*t
            y=crown_y+dy*t-55*math.sin(math.pi*t)
            width=13*math.sin(math.pi*t)
            leaf.append((x,y,width))
        shape=[(x,y-w) for x,y,w in leaf]+[(x,y+w) for x,y,w in reversed(leaf)]
        draw.polygon([box(p) for p in shape], fill=PLUM)


def star(draw, x, y, r, fill, inner=0.27, points=4):
    vertices=[]
    for i in range(points*2):
        angle=-math.pi/2+i*math.pi/points
        radius=r if i%2==0 else r*inner
        vertices.append(box((x+math.cos(angle)*radius, y+math.sin(angle)*radius)))
    draw.polygon(vertices, fill=fill)


def ghost(image):
    shadow=Image.new('RGBA', image.size)
    sd=ImageDraw.Draw(shadow)
    sd.ellipse(box((706, 867, 1045, 915)), fill=(10, 3, 16, 160))
    image.alpha_composite(shadow.filter(ImageFilter.GaussianBlur(12*SCALE)))
    draw=ImageDraw.Draw(image)
    # A rounded hand and bent wrist form the raised wave.
    wave=[(731, 681), (735, 708), (748, 726), (780, 740)]
    for width, color in ((52, PLUM), (34, 'white')):
        radius=width/2
        draw.line([box(point) for point in wave], fill=color,
                  width=width*SCALE, joint='curve')
        x,y=wave[0]
        draw.ellipse(box((x-radius,y-radius,x+radius,y+radius)), fill=color)
    draw.rounded_rectangle(box((755, 540, 1005, 895)), radius=124*SCALE,
                           fill='white', outline=PLUM, width=9*SCALE)
    draw.rectangle(box((755, 686, 1005, 889)), fill='white')
    draw.line(box((759, 684, 759, 889, 1001, 889, 1001, 684)), fill=PLUM, width=9*SCALE, joint='curve')
    # Two little square cutouts in the otherwise flat hem form three feet.
    for x in (822, 917):
        draw.line(box((x, 894, x, 873)), fill=PLUM, width=10*SCALE)
    star(draw, 827, 670, 28, PLUM)
    star(draw, 930, 670, 28, PLUM)
    draw.ellipse(box((975, 550, 1051, 626)), fill=MAGENTA, outline=PLUM, width=6*SCALE)
    star(draw, 1013, 588, 23, 'white', inner=0.44, points=5)
    # Forearms slope from the sides of the body into the controller grips.
    for arm in ([(774, 708), (784, 742), (808, 766)],
                [(983, 708), (978, 742), (960, 766)]):
        for width, color in ((25, PLUM), (15, 'white')):
            radius=width/2
            draw.line([box(point) for point in arm], fill=color,
                      width=width*SCALE, joint='curve')
            x,y=arm[0]
            draw.ellipse(box((x-radius,y-radius,x+radius,y+radius)), fill=color)
    draw.rounded_rectangle(box((801, 720, 958, 786)), radius=23*SCALE, fill='#30283D', outline=PLUM, width=5*SCALE)
    draw.line(box((821, 749, 845, 749)), fill='#EBDCEE', width=6*SCALE)
    draw.line(box((833, 737, 833, 761)), fill='#EBDCEE', width=6*SCALE)
    for x,y,c in [(930,742,MAGENTA),(943,755,'#F9AF88')]:
        draw.ellipse(box((x-5,y-5,x+5,y+5)), fill=c)
    for x in (864,895):
        draw.ellipse(box((x-8,756,x+8,772)), fill='#110C1A')
    for x in (796, 948):
        draw.ellipse(box((x, 753, x+24, 781)), fill='white', outline=PLUM, width=4*SCALE)


def main():
    image=Image.new('RGBA', (SIZE*SCALE, SIZE*SCALE))
    gradient(image)
    draw=ImageDraw.Draw(image)
    draw.ellipse(box((365, 494, 835, 964)), fill=MAGENTA, outline=PLUM, width=20*SCALE)
    skyline(draw)
    draw.rectangle(box((0, 816, 1200, 1200)), fill='#442538')
    reflection=Image.new('RGBA', image.size)
    rd=ImageDraw.Draw(reflection)
    rd.polygon([box(p) for p in [(509,820),(691,820),(797,1035),(393,1035)]], fill=(224,112,138,40))
    image.alpha_composite(reflection.filter(ImageFilter.GaussianBlur(19*SCALE)))
    draw=ImageDraw.Draw(image)
    for i in range(13):
        y=827+i*9
        half=79+i*5
        draw.line(box((600-half,y,600+half,y)), fill=(131-i*3,65-i,88-i), width=2*SCALE)
    palm(draw, -30, 167, 450, 478)
    palm(draw, 1250, 1060, 410, 525)
    ghost(image)
    draw=ImageDraw.Draw(image)
    outlined_text(draw, '13 YEARS OF LOADING...', 57, 92, stroke=6)
    # Leave clear air between the character's feet and the loading UI.
    draw.rounded_rectangle(box((91, 948, 1109, 1008)), radius=16*SCALE, fill=PLUM, outline='white', width=5*SCALE)
    draw.rounded_rectangle(box((102, 959, 1098, 997)), radius=8*SCALE, fill='white')
    draw.text(box((600,978)), '100%', font=font(32), fill=PLUM, anchor='mm')
    outlined_text(draw, 'GTA 6 - DAY ONE', 1027, 44, stroke=4)
    band=Image.new('RGBA', image.size)
    ImageDraw.Draw(band).rectangle(box((0,1097,1200,1200)), fill=(0,0,0,172))
    image.alpha_composite(band)
    draw=ImageDraw.Draw(image)
    outlined_text(draw, 'TIP: MY AGENT SPENT THE WAIT', 1110, 38, stroke=2)
    outlined_text(draw, 'EARNING REAL MONEY ON MAKE.FUN', 1155, 38, stroke=2)
    output=Path(__file__).resolve().parent/'meme.png'
    image.convert('RGB').resize((SIZE,SIZE),Image.Resampling.LANCZOS).save(output)
    print(f'{output.name}: {SIZE}x{SIZE}, {output.stat().st_size:,} bytes')


if __name__ == '__main__':
    main()
