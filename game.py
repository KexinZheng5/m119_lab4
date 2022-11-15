# game gui

# reference: https://www.quickprogrammingtips.com/python/how-to-create-canvas-animation-using-tkinter.html

import tkinter

 
class Game():
    # window size
    window_width = 1500
    window_height = 800

    # wall thickness
    thickness = 20

    # bar size and postion
    bar1 = None
    bar_width = 50
    bar_height = 150
    bar1_x = 1400
    bar1_y = 0
    bar1_offset = 0

    # ball radius
    ball = None
    ball_x = window_width / 2
    ball_y = window_height / 2
    radius = 30
    shift_x = 20
    shift_y = 0
    
    # player 1
    p1_score = 0
    p1_display = None
    
    exit = False

    # main window of the animation
    def create_animation_window(self):
        window = tkinter.Tk()
        window.title("Pong (single player)")
        window.geometry(f'{self.window_width}x{self.window_height}')
        window.protocol("WM_DELETE_WINDOW", self.on_close)
        return window
    
    # create a canvas for animation and add it to main window
    def create_animation_canvas(self, window):
        canvas = tkinter.Canvas(window)
        canvas.configure(bg="black")
        canvas.pack(fill="both", expand=True)
        return canvas

    # get position
    def get_position(self):
        self.bar1.pos = 1

    # initialize window
    def initialize(self, mode):
        self.window = self.create_animation_window()
        self.canvas = self.create_animation_canvas(self.window)
        self.mode = mode
        self.canvas.create_rectangle(0, 0, self.window_width, self.thickness, fill="#737373", outline="")
        self.canvas.create_rectangle(0, self.window_height - self.thickness, self.window_width, self.window_height, fill="#737373", outline="")
        # single player mode
        if (mode):
            self.canvas.create_rectangle(0, 0, self.thickness, self.window_height, fill="#737373", outline="")
            self.ball = self.canvas.create_oval(self.ball_x - self.radius, 
                                    self.ball_y - self.radius,
                                    self.ball_x + self.radius, 
                                    self.ball_y + self.radius, 
                                    fill="#ff9a1f", outline=""),
        
    # update bar position
    def update_frame(self, value):
        if self.bar1 is not None: 
            self.canvas.delete(self.bar1)
        new_y = self.new_position(value)
        self.bar1_offset = new_y - self.bar1_y
        self.bar1_y = new_y
        self.bar1 = self.draw_bar(self.bar1_x, self.bar1_y)
        self.update_display()
        self.update_ball()
        self.window.update()

    # calculate new position
    def new_position(self, value):
        new_pos =  int(value * self.window_height /2 + self.window_height /2 )
        if new_pos < self.bar_height/2:
            return self.bar_height/2
        elif new_pos > self.window_height - self.bar_height/2:
            return self.window_height - self.bar_height/2
        else:
            return new_pos

    # draw bar
    def draw_bar(self, x, y):
        return self.canvas.create_rectangle(x-(self.bar_width)/2, 
            y-(self.bar_height)/2, 
            x+(self.bar_width)/2, 
            y+(self.bar_height)/2, 
            fill="#fff", outline="")

    # draw ball
    def update_ball(self):
        # hit left edge
        if self.ball_x - self.radius / 2 < self.thickness:
            self.shift_x = -self.shift_x
        # hit top edge
        elif self.ball_y - self.radius / 2 < self.thickness:
            self.shift_y = -self.shift_y
        # hit bottom edge 
        elif self.ball_y + self.radius / 2 > self.window_height - self.thickness:
            self.shift_y = -self.shift_y 
        # hit player
        elif self.ball_x > self.bar1_x - (self.radius + self.bar_width) / 2 \
            and self.ball_y - self.radius / 2 < self.bar1_y + self.bar_height / 2 \
            and self.ball_y + self.radius / 2 > self.bar1_y - self.bar_height / 2:
                self.p1_score += 1
                self.shift_x = -self.shift_x
                self.shift_y = self.shift_y + self.bar1_offset // 10
        # out of bound
        elif self.ball_x - self.radius/2 > self.window_width:
            self.p1_score -= 1
            self.reset_ball()
        self.ball_x = self.ball_x + self.shift_x
        self.ball_y = self.ball_y + self.shift_y
        self.canvas.move(self.ball, self.shift_x, self.shift_y)
        self.canvas.tag_raise(self.ball)

    # reset ball position
    def reset_ball(self):
        self.ball_x = self.window_width / 2
        self.ball_y = self.window_height / 2
        self.shift_x = 20
        self.shift_y = 0
        self.canvas.delete(self.ball)
        self.ball = self.canvas.create_oval(self.ball_x - self.radius, 
                                    self.ball_y - self.radius,
                                    self.ball_x + self.radius, 
                                    self.ball_y + self.radius, 
                                    fill="#ff9a1f", outline=""),

    # update player score display
    def update_display(self):
        if self.p1_display is not None:
            self.canvas.delete(self.p1_display)
        self.p1_display = self.canvas.create_text(1100, self.window_height / 2, text=str(self.p1_score), fill="#38271d", font=('Calibri 300'))
    

    def on_close(self):
        print("exiting...")
        self.exit = True
        self.window.destroy()
