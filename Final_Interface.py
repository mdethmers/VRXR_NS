import cv2
from customtkinter import *
from PIL import Image, ImageTk
import time

def initialize_app():
    set_appearance_mode("light")
    set_default_color_theme("dark-blue")
    app = CTk()
    app.geometry("1200x740")
    return app

def initialize_top_frame(app):
    # Create the top frame with specified width and height
    topframe = CTkFrame(master=app, border_color="#FFC917", fg_color="#FFC917", border_width=2, width=1200, height=70)
    topframe.place(x=0, y=500)
    return topframe

def calculate_spacing(num_elements, total_width):
    spacing = total_width // (num_elements + 1)
    x_values = [(i + 1) * spacing for i in range(num_elements)]
    return x_values

def create_decorative_boxes(parent_frame):
    num_boxes = 6
    box_width = 80
    box_height = 10
    total_width = 1200

    x_positions = calculate_spacing(num_boxes, total_width)
    decorative_boxes = []

    for x_center in x_positions:
        x_start = x_center - (box_width / 2)
        decorative_box = CTkFrame(master=parent_frame, width=box_width, height=box_height, border_width=1,
                                  fg_color="#003082")
        decorative_box.place(x=x_start, y=1)
        decorative_boxes.append(decorative_box)

    return decorative_boxes, x_positions

def create_circles_with_numbers_inside_top_frame(parent_frame, Score=0):
    num_circles = 6
    circle_diameter = 40
    x_positions = calculate_spacing(num_circles, 1200)
    circle_y_position = 20  # Y position inside the top frame

    circles = []
    for i, x_center in enumerate(x_positions):
        x_start = x_center - (circle_diameter // 2)

        circle_frame = CTkFrame(master=parent_frame, width=circle_diameter, height=circle_diameter, border_width=2,
                    fg_color="green")
        circle_frame.place(x=x_start, y=circle_y_position)

        if i == 0:
            if Score < 6:
                circle_frame.configure(fg_color="green")
            else:
                circle_frame.configure(fg_color="red")

        circles.append(circle_frame)

    return circles

def create_buttons_below_top_frame(app, num_buttons=6):
    button_width = 100
    button_height = 40
    x_positions = calculate_spacing(num_buttons, 1200)
    button_y_position = 600

    buttons = []
    for x_center in x_positions:
        x_start = x_center - (button_width // 2)

        close_button = CTkButton(
            master=app,
            width=button_width,
            height=button_height,
            fg_color="#003082",
            text="CLOSE",
            font=('Inter', 12, 'bold'),
            text_color="white"  # Set the text color to white
        )
        close_button.place(x=x_start, y=button_y_position)
        buttons.append(close_button)

        check_button = CTkButton(
            master=app,
            width=button_width,
            height=button_height,
            border_color="#003082",
            fg_color="white",
            border_width=3,
            text="CHECK",
            font=('Inter', 12, 'bold'),
            text_color="#003082"  # Set the text color to black
        )
        check_button.place(x=x_start, y=button_y_position + button_height + 10)
        buttons.append(check_button)

    return buttons

def create_countdown_timer(parent_frame):
    countdown_label = CTkLabel(master=parent_frame, text="01:00", font=('Arial', 75, 'bold'), text_color="#003082")
    countdown_label.place(relx=0.5, y=50, anchor=CENTER)  # Center the countdown timer in the top frame
    start_countdown(countdown_label)
    return countdown_label

def start_countdown(countdown_label):
    minutes = 1
    seconds = 0

    def update_countdown():
        nonlocal minutes, seconds

        if seconds == 0:
            if minutes == 0:
                minutes = 1
                seconds = 0
            else:
                minutes -= 1
                seconds = 59
        else:
            seconds -= 1

        countdown_text = f"{minutes:02d}:{seconds:02d}"
        countdown_label.configure(text=countdown_text)

        countdown_label.after(1000, update_countdown)  # Update every 1000 ms (1 second)

    update_countdown()

def update_clock(clock_label):
    current_time = time.strftime("%H:%M")
    clock_label.configure(text=current_time)
    clock_label.after(1000, update_clock, clock_label)  # Update every 1000 ms (1 second)

def main_interface(activity_score_func):
    app = initialize_app()
    top_frame = initialize_top_frame(app)
    decorative_boxes, x_positions = create_decorative_boxes(top_frame)
    app.update_idletasks()  # Ensure the top_frame has been placed before getting its dimensions
    circles = create_circles_with_numbers_inside_top_frame(top_frame)


    def update_activity_score():
        score = activity_score_func()  # Get the real-time activity score from the CV functio    n
        circles = create_circles_with_numbers_inside_top_frame(top_frame, score)
        app.after(250, update_activity_score)  # Schedule the next update in 1 second

    update_activity_score()  # Start the first update

    buttons = create_buttons_below_top_frame(app)
    countdown_label = create_countdown_timer(app)
    start_countdown(countdown_label)
    app.mainloop()

if __name__ == "__main__":
    main_interface(lambda: 0)
