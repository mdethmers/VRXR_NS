from customtkinter import *
from PIL import Image
from DoorSegmentation import DoorSegmentation
import config

def initialize_app():
    set_appearance_mode("dark")
    set_default_color_theme("dark-blue")
    app = CTk()
    app.geometry("1200x600")
    return app

def initialize_top_frame(app):
    # Load image
    final_image = CTkImage(light_image=Image.open("data/cockpit_interface.jpg"),
                           dark_image=Image.open("data/cockpit_interface.jpg"),
                           size=(1150, 300))

    # Create the frame with specified width and height
    topframe = CTkFrame(master=app, border_color="White", border_width=2, width=1160, height=305)

    # Use place geometry manager to position the frame
    topframe.place(x=20, y=10)

    image_label = CTkLabel(app, text="", image=final_image)
    image_label.pack(pady=12)

def calculate_box_positions_with_margins(screen_width=1200, num_boxes=8, margin=22):
    total_width = screen_width - 2 * margin
    box_width = (total_width - (num_boxes - 1) * margin) // num_boxes
    start_margin = margin + (total_width - (num_boxes * box_width + (num_boxes - 1) * margin)) // 2
    positions = [start_margin + i * (box_width + margin) for i in range(num_boxes)]
    return positions, box_width

def update_scores(door_segments, app):
    for segment in door_segments:
        segment.update_score()
    app.after(1000, update_scores, door_segments, app)  # Update scores every second

def manually_update_first_door(door_segments, score):
    if door_segments:
        door_segments[0].update_activity_score(score)

def main_interface(activity_score_func):
    app = initialize_app()
    initialize_top_frame(app)

    positions, box_width = calculate_box_positions_with_margins()
    door_segments = [DoorSegmentation(x_pos, 320, f"Door {index + 1}", app) for index, x_pos in enumerate(positions)]

    for segment in door_segments:
        segment.segment()

    def update_activity_score():
        score = activity_score_func()  # Get the real-time activity score from the CV function
        manually_update_first_door(door_segments, score)
        app.after(1000, update_activity_score)  # Schedule the next update in 1 second

    update_activity_score()  # Start the first update

    update_scores(door_segments[1:], app)

    app.mainloop()

if __name__ == "__main__":
    main_interface(lambda: 0)  # Dummy call for testing
