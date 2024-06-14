from customtkinter import CTkFrame, CTkLabel


import random


class DoorSegmentation():
    def __init__(self, xvalue, yvalue, title, app):
        self.xvalue = xvalue
        self.yvalue = yvalue
        self.title = title
        self.app = app
        self.score = random.uniform(0, 10)  # Initial random score

    def segment(self):
        border_color, bg_color = self.get_colors()
        self.frame = CTkFrame(master=self.app, border_color=border_color, border_width=2, fg_color=bg_color, width=125,
                              height=200)
        self.frame.place(x=self.xvalue, y=self.yvalue)

        # Create and place the title label
        title_label = CTkLabel(master=self.frame, text=self.title, text_color="white", font=("Arial", 22, "bold"))
        title_label.place(relx=0.5, rely=0.1, anchor="center")  # Center the title inside the frame

        # Create and place the score label
        self.score_label = CTkLabel(master=self.frame, text="{:.2f}".format(self.score), text_color="white",
                                    font=("Arial", 48, "bold"))
        self.score_label.place(relx=0.5, rely=0.5, anchor="center")  # Center the score inside the frame

    def update_score(self):
        self.score = random.uniform(0, 10)  # Update the score with a new random value
        border_color, bg_color = self.get_colors()
        self.frame.configure(border_color=border_color, fg_color=bg_color)  # Update the colors of the frame
        self.score_label.configure(text="{:.1f}".format(self.score))  # Update the score label text

    def update_activity_score(self, score):
        self.score = score  # Manually update the score
        border_color, bg_color = self.get_colors()
        self.frame.configure(border_color=border_color, fg_color=bg_color)  # Update the colors of the frame
        self.score_label.configure(text="{:.1f}".format(self.score))  # Update the score label text

    def get_colors(self):
        if self.score >= 7:
            return "red", "dark red"
        elif self.score >= 2:
            return "orange", "dark orange"
        else:
            return "green", "dark green"