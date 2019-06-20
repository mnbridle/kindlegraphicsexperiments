import mmap
import os
import time
import random
import math
from freetype.raw import *

class FB_GFXInterface(object):
    def __init__(self, bg_shade=0):
        self.screen_height = 800
        self.screen_width = 600
        self.bg_shade = bg_shade

        self.sign = lambda x: math.copysign(1, x)

        self.init_screen()


    def to_c_str(self, text):
        ''' Convert python strings to null terminated c strings. '''
        cStr = create_string_buffer(text.encode(encoding='UTF-8'))
        return cast(pointer(cStr), POINTER(c_char))


    def init_screen(self):
        self.fb_contents = bytearray.fromhex(self.screen_height*self.screen_width*format(self.bg_shade, 'x'))

    def write_screen(self):
        start_time = time.time()
        with open("/dev/fb0", "w+b") as fb:
            mm = mmap.mmap(fb.fileno(), length=(self.screen_width*self.screen_height)/2)
            mm.write(bytes(self.fb_contents))
            mm.flush()
            mm.close()

        os.system("echo 1 > /proc/eink_fb/update_display")

        print("write_screen duration: {} s".format(time.time() - start_time))


    def plot(self, x, y, fg_shade=15):
        # Convert rectangular space to byte-space
        byte_pos = (y*(self.screen_width/2))+(x/2.0)
        if byte_pos - int(byte_pos) == 0.5:
            # Right hand subpixel
            self.fb_contents[int(byte_pos)] |= fg_shade
        else:
            self.fb_contents[int(byte_pos)] |= (fg_shade << 4)

    def vertical_line(self, x=0, fg_shade=15):
        start_time = time.time()
        for y in range(0, self.screen_height):
            self.plot(x, y, fg_shade=fg_shade)

        print("vertical_line duration: {} s".format(time.time() - start_time))


    def horizontal_line(self, y=0, fg_shade=15):
        start_time = time.time()
        for x in range(0, self.screen_width):
            self.plot(x, y, fg_shade=fg_shade)

        print("horizontal_line duration: {} s".format(time.time() - start_time))


    def line(self, x1=0, y1=0, x2=0, y2=0, fg_shade=15):
        start_time = time.time()
        x1=int(x1)
        x2=int(x2)
        y1=int(y1)
        y2=int(y2)

        # Implement Bresenham's Line Algorithm

        print("line: {},{} to {},{} - shade: {}".format(x1, y1, x2, y2, fg_shade))
        delta_x = x2 - x1
        delta_y = y2 - y1
        if float(delta_x) == 0:
            for y in range(y1, y2):
                self.plot(x1, y, fg_shade)

        else:
            delta_err = abs(float(delta_y) / float(delta_x))
            err = 0.0

            y = y1
            for x in range(x1, x2):
                self.plot(x, y, fg_shade)
                err = err + delta_err
                if err >= 0.5:
                    y += self.sign(delta_y) * 1
                    err -= 1.0

        print("Line duration: {} s".format(time.time() - start_time))


    def polygon(self, point_list=[], fg_shade=15):
        start_time = time.time()

        for idx, point in enumerate(point_list):
            if idx+1 < len(point_list):
                self.line(x1=point[0], y1=point[1], x2=point_list[idx+1][0], y2=point_list[idx+1][1], fg_shade=fg_shade)

        print("Polygon duration: {} s".format(time.time() - start_time))

    def circle(self, x0, y0, radius, fg_shade=15):
        start_time = time.time()

        circle_points = []
        x = radius - 1
        y = 0
        dx = 1
        dy = 1
        err = dx - (radius << 1)

        while (x >= y):
            circle_points.append((x0+x,y0+y))
            circle_points.append((x0+y,y0+x))
            circle_points.append((x0-y,y0+x))
            circle_points.append((x0-x,y0+y))
            circle_points.append((x0-x,y0-y))
            circle_points.append((x0-y,y0-x))
            circle_points.append((x0+y,y0-x))
            circle_points.append((x0+x,y0-y))

            if err <= 0:
                y += 1
                err += dy
                dy += 2

            if err > 0:
                x -= 1
                dx += 2
                err += dx - (radius << 1)

        for point in circle_points:
            self.plot(point[0], point[1], fg_shade=fg_shade)

        print("Circle duration: {} s".format(time.time() - start_time))


    def render_string(self, font_filename='COMIC.TTF', text="AaBbCcDdEeFfGgHhIiJjKkLlMm", angle=0, start_x=0, start_y=50, font_size=12, font_res=167):
        # Renders a string into a block of bytes - plots directly to start with
        start_time = time.time()

        self.library = FT_Library()
        self.matrix = FT_Matrix()
        self.face = FT_Face()
        self.pen = FT_Vector()

        FT_Init_FreeType(byref(self.library))

        filename = font_filename
        num_chars = len(text)

        rad_angle = (angle/360.0) * 3.14159 * 2

        FT_New_Face( self.library, self.to_c_str(filename), 0, byref(self.face))

        FT_Set_Char_Size(self.face, font_size * 64, 0, font_res, 0)
        slot = self.face.contents.glyph

        self.matrix.xx = (int)(math.cos(rad_angle)*0x10000)
        self.matrix.xy = (int)(-math.sin(rad_angle)*0x10000)
        self.matrix.yx = (int)(math.sin(rad_angle)*0x10000)
        self.matrix.yy = (int)(math.cos(rad_angle)*0x10000)

        self.pen.x = start_x * 64
        self.pen.y = (self.screen_height - start_y) * 64

        for n in range(num_chars):
            FT_Set_Transform(self.face, byref(self.matrix), byref(self.pen))
            charcode = ord(text[n])
            index = FT_Get_Char_Index(self.face, charcode)
            FT_Load_Glyph(self.face, index, FT_LOAD_RENDER)

            self.draw_bitmap(slot.contents.bitmap, slot.contents.bitmap_left, self.screen_height-slot.contents.bitmap_top)

            self.pen.x += slot.contents.advance.x
            self.pen.y += slot.contents.advance.y

        FT_Done_Face(self.face)
        FT_Done_FreeType(self.library)
        print("Time taken to render string '{}': {}".format(text, time.time()-start_time))

    def draw_bitmap(self, bitmap, x, y):
        start_time = time.time()
        x_max = x + bitmap.width
        y_max = y + bitmap.rows

        p = 0
        for p, i in enumerate(range(x, x_max)):
            for q, j in enumerate(range(y, y_max)):
                if i < 0 or j < 0 or i >= 600 or j >= 800:
                    continue

                self.plot(i, j, fg_shade=bitmap.buffer[q*bitmap.width + p] >> 4)

        #print("Time taken to draw_bitmap: {}".format(time.time() - start_time))


    def write_block(self, x=0, y=0, data=[[]], clearBlock=False, canRollover=False):
        start_time = time.time()

        # Check that dimensions in data are sane
        it = iter(data)
        x_len = len(next(it))
        y_len = len(data)

        if not all(len(l) == x_len for l in it):
            raise ValueError('Not all lists have the same length!')

        if x + x_len > self.screen_width or y + y_len > self.screen_height:
            raise ValueError('Cannot write block without going off screen')

        for idx, row in enumerate(data):
            startByteOffset = int(self.coordsToByteOffset(x, y+idx))
            endByteOffset = int(self.coordsToByteOffset(x+x_len, y+idx))

            self.fb_contents[startByteOffset:endByteOffset] = bytearray.fromhex(row)

        print("write_block duration: {} s".format(time.time() - start_time))

    def coordsToByteOffset(self, x, y):
        return (y*(self.screen_width/2))+(x/2.0)
