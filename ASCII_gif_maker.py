import pygame as pg
from PIL import Image, ImageFont


im = Image.open("oshi.gif") #used gif
width =im.size [0]
height = im.size[1]

clock = pg.time.Clock()
num_iterations = 100
intensity_multiplier = 1
font_size = 15
font_color = ("pink")
bg_color = ("black")

def extract_gif_frames(gif, fillEmpty=False):
    frames = []
    try:
        while True:
            gif.seek(gif.tell() + 1)
            new_frame = Image.new('RGBA', gif.size)
            new_frame.paste(im, (0, 0), im.convert('RGBA'))

            # check if we are painting over a canvas
            if fillEmpty:
                canvas = Image.new('RGBA', new_frame.size, (255, 255, 255, 255))
                canvas.paste(new_frame, mask=new_frame)
                new_frame = canvas

            frames.append(new_frame)
    except EOFError:
        pass
    return frames

def image_to_ascii(image):
    font = ImageFont.load_default()
    (chrx, chry) = font.getsize(chr(32))

    weights = []
    for i in range(32, 127):
        chrImage = font.getmask(chr(i))
        ctr = 0
        for y in range(chry):
            for x in range(chrx):
                if chrImage.getpixel((x, y)) > 0:
                    ctr += 1
        weights.append(float(ctr) / (chrx * chry))
    output = ""
    (imgx, imgy) = image.size
    imgx = int(imgx / chrx)
    imgy = int(imgy / chry)


    image = image.resize((imgx, imgy), Image.BICUBIC)
    image = image.convert("L")


    pixels = image.load()
    for y in range(imgy):
        for x in range(imgx):
            w = float(pixels[x, y]) / 255 / intensity_multiplier
            wf = -1.0;
            k = -1
            for i in range(len(weights)):
                if abs(weights[i] - w) <= abs(wf - w):
                    wf = weights[i];
                    k = i
            output += chr(k + 32)
        output += "\n"
    return output

def frames_to_ascii(frames):
    ascii_frames = []
    for frame in frames:
        new_frame = image_to_ascii(frame)
        ascii_frames.append(new_frame)
    return ascii_frames

def draw_ascii_image(surface, ascii_frame, font, font_size, font_color):
    surface.fill(bg_color)
    x, y = 0, 0
    for line in ascii_frame.split('\n'):
        text = font.render(line, True, font_color)
        surface.blit(text, (x, y))
        y += font_size
    pg.display.flip()


def main():
    pg.init()
    res = width, height
    surface = pg.display.set_mode(res)
    pg.display.set_caption("ASCII gif-maker")
    font = pg.font.Font(None, font_size)


    frames = extract_gif_frames(im, fillEmpty=True)
    ascii_frames = frames_to_ascii(frames)

    frame_index = 0
    while frame_index < num_iterations:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                exit()

        draw_ascii_image(surface, ascii_frames[frame_index], font, font_size, font_color)
        frame_index = (frame_index + 1) % len(ascii_frames)

        pg.time.delay(50)  # Adjust the delay to control animation speed
        clock.tick(45)  # Adjust the FPS as needed


if __name__ == "__main__":
    main()

