import time
import kindle_graphics

def main():
    kindle_screen = kindle_graphics.FB_GFXInterface()
    kindle_screen.write_screen()
    # Clear artifacts by making the screen black, then making it white
    kindle_screen.bg_shade = 0x9
    kindle_screen.init_screen()
    kindle_screen.write_screen()
    kindle_screen.bg_shade = 0x0
    kindle_screen.init_screen()
    kindle_screen.write_screen()
    for idx, circle_radius in enumerate(range(50, 300, 50)):
        kindle_screen.circle(300,400,circle_radius,fg_shade=idx*2)

    kindle_screen.horizontal_line(y=200, fg_shade=15)
    kindle_screen.horizontal_line(y=300, fg_shade=15)
    kindle_screen.horizontal_line(y=500, fg_shade=15)
    kindle_screen.horizontal_line(y=600, fg_shade=15)
    kindle_screen.vertical_line(x=100, fg_shade=15)
    kindle_screen.vertical_line(x=200, fg_shade=15)
    kindle_screen.vertical_line(x=400, fg_shade=15)
    kindle_screen.vertical_line(x=500, fg_shade=15)

    kindle_screen.render_string(font_filename='/mnt/us/MySoftware/fonts/COMIC.TTF', text="The quick brown fox jumps over the lazy doge", angle=0, start_x=0, start_y=50, font_size=12)
    kindle_screen.render_string(font_filename='/mnt/us/MySoftware/fonts/COMIC.TTF', text="The quick brown fox jumps over the lazy doge omg he so smol doge", angle=0, start_x=0, start_y=90, font_size=6)
    kindle_screen.render_string(font_filename='/mnt/us/MySoftware/fonts/COMIC.TTF', text="Such sass", angle=0, start_x=100, start_y=400, font_size=24)
    kindle_screen.render_string(font_filename='/mnt/us/MySoftware/fonts/COMIC.TTF', text="Much kerning", angle=0, start_x=200, start_y=450, font_size=24)
    kindle_screen.render_string(font_filename='/mnt/us/MySoftware/fonts/LiberationSerif-Regular.ttf', text="Lorem ipsum dolor sit amet", angle=0, start_x=0, start_y=150, font_size=12)
    kindle_screen.render_string(font_filename='/mnt/us/MySoftware/fonts/LiberationSerif-Regular.ttf', text="Oh yes. Typography is a very serious business.", angle=0, start_x=0, start_y=200, font_size=12)

    kindle_screen.write_screen()

    time.sleep(30)

main()
