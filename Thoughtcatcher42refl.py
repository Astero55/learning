import tkinter as tk
from threading import Thread
import time
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from PIL import Image, ImageTk
from datetime import datetime

class App:
    def __init__(self, root):
        self.root = root
        self.time_left = 0
        self.glitches = 0
        self.mind_wandering = 0
        self.timer_running = False
        self.timer_paused = False
        self.info_window = None
        self.reflection_text = tk.StringVar()

        # window title and size
        root.title("Thoughtcatcher")
        root.geometry("895x895")

        # color scheme
        button_color = "#4B8BBE"
        text_color = "#F7F7F7"
        root.configure(bg=text_color)

        reflection_frame = tk.Frame(root, bg=text_color)
        reflection_frame.pack(pady=(20, 10))

        reflection_label = tk.Label(reflection_frame, text="Reflection", font=("Arial", 14), bg=text_color)
        reflection_label.pack()

        self.reflection_entry = tk.Entry(reflection_frame, textvariable=self.reflection_text, width=80, font=("Arial", 10))
        self.reflection_entry.pack()

        title_frame = tk.Frame(root, bg=text_color)
        title_frame.pack(pady=(20, 10))

        timer_frame = tk.Frame(root, bg=text_color)
        timer_frame.pack(pady=(10, 20))

        button_frame = tk.Frame(root, bg=text_color)
        button_frame.pack(pady=(10, 20))

        summary_frame = tk.Frame(root, bg=text_color)
        summary_frame.pack(pady=(10, 20))

        info_frame = tk.Frame(root, bg=text_color)
        info_frame.pack(side="bottom", anchor="e", pady=(10, 20))

        #  frame for the graph
        self.graph_frame = tk.Frame(root, bg=text_color)
        self.graph_frame.pack(pady=(10, 20))

        # widgets to the frames
        self.title_label = tk.Label(title_frame, text="Thoughtcatcher", font=("Arial", 20), bg=text_color)
        self.title_label.pack()

        # Add a subtitle under the title
        self.subtitle_label = tk.Label(title_frame, text="Catch your rumination and mind-wandering to improve your concentration.", font=("Arial", 10), bg=text_color)
        self.subtitle_label.pack()

        self.timer_label = tk.Label(timer_frame, text="00:00", font=("Arial", 18), bg=text_color)
        self.timer_label.pack(pady=(10, 0))

        self.glitch_button = tk.Button(button_frame, text="Rumination", command=self.glitch, font=("Arial", 14), bg=button_color, fg=text_color, relief="flat")
        self.glitch_button.pack(side="left", padx=(0, 10))

        self.mind_wandering_button = tk.Button(button_frame, text="Mind Wandering", command=self.mind_wander, font=("Arial", 14), bg=button_color, fg=text_color, relief="flat")
        self.mind_wandering_button.pack(side="left")

        tk.Label(root, text="").pack() 

        self.timer_button = tk.Button(timer_frame, text="Start Timer", command=self.start_timer, font=("Arial", 14), bg=button_color, fg=text_color, relief="flat")
        self.timer_button.pack(pady=(10, 0))

        self.pause_button = tk.Button(timer_frame, text="Pause Timer", command=self.pause_timer, font=("Arial", 14), bg=button_color, fg=text_color, relief="flat")
        self.pause_button.pack(pady=(10, 20)) 

        tk.Label(root, text="").pack() 

        self.summary_button = tk.Button(summary_frame, text="Show Summary", command=self.show_summary, font=("Arial", 14), bg=button_color, fg=text_color, relief="flat")
        self.summary_button.pack(pady=(10, 10))

        self.timer25_button = tk.Button(timer_frame, text="25 min", command=lambda: self.set_timer(25), font=("Arial", 14), bg=button_color, fg=text_color, relief="flat")
        self.timer25_button.pack(side="left", padx=(0, 10))

        self.timer50_button = tk.Button(timer_frame, text="50 min", command=lambda: self.set_timer(50), font=("Arial", 14), bg=button_color, fg=text_color, relief="flat")
        self.timer50_button.pack(side="left", padx=(0, 10))

        self.timer120_button = tk.Button(timer_frame, text="120 min", command=lambda: self.set_timer(120), font=("Arial", 14), bg=button_color, fg=text_color, relief="flat")
        self.timer120_button.pack(side="left", padx=(0, 20))  

        self.summary_label = tk.Label(summary_frame, text="", font=("Arial", 14), bg=text_color)
        self.summary_label.pack()

        # Information button
        self.info_button = tk.Button(info_frame, text="Info", command=self.show_info, font=("Arial", 14), bg=button_color, fg=text_color, relief="flat")
        self.info_button.pack(side="right", padx=(0, 10))

    def set_timer(self, minutes):
        self.time_left = minutes * 60

    def glitch(self):
        if self.timer_running and not self.timer_paused:
            self.glitches += 1

    def mind_wander(self):
        if self.timer_running and not self.timer_paused:
            self.mind_wandering += 1

    def start_timer(self):
        self.glitches = 0
        self.mind_wandering = 0
        self.timer_running = True
        self.timer_paused = False
        self.timer_button.config(text="Stop Timer", command=self.stop_timer)
        self.reflection_text.set("")  # Clear the reflection text box
        Thread(target=self.countdown).start()

    def stop_timer(self):
        self.timer_running = False
        self.timer_button.config(text="Start Timer", command=self.start_timer)
        self.show_summary()

    def pause_timer(self):
        self.timer_paused = not self.timer_paused
        self.pause_button.config(text="Resume Timer" if self.timer_paused else "Pause Timer")

    def countdown(self):
        while self.time_left > 0 and self.timer_running:
            if not self.timer_paused:
                mins, secs = divmod(self.time_left, 60)
                self.timer_label.config(text=f"{mins:02d}:{secs:02d}")
                time.sleep(1)
                self.time_left -= 1

    def show_summary(self):
        summary = f"Time = {self.time_left//60} min, Rumination = {self.glitches}, Mind wondering = {self.mind_wandering}"
        self.summary_label.config(text=summary)
        with open("summary.txt", "a") as f:
            # Add a timestamp to each session summary
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            f.write(f"{timestamp}: {summary}\n")
            # Save the reflection text with a timestamp
            reflection = self.reflection_text.get()
            if reflection:
                f.write(f"{timestamp}: Reflection: {reflection}\n")

        # Clear graph frame
        for widget in self.graph_frame.winfo_children():
            widget.destroy()

        # Pie chart
        fig = plt.Figure(figsize=(5, 5), dpi=100)
        y = [self.glitches, self.mind_wandering]
        labels = ["Rumination", "Mind Wandering"]
        ax = fig.add_subplot(111)
        ax.pie(y, labels=labels, autopct='%1.1f%%', startangle=90, colors=['blue', 'darkgreen'])

        # Add the graph to the frame
        canvas = FigureCanvasTkAgg(fig, master=self.graph_frame)
        canvas.draw()
        canvas.get_tk_widget().pack()

    def show_info(self):
       
        if self.info_window is not None:
            return

        self.info_window = tk.Toplevel(self.root)
        self.info_window.title("Information")
        self.info_window.geometry("400x400")

        info_text = """This app is designed to help you track and reduce rumination and mind wandering during timed sessions.

Rumination is the process of continuously thinking about the same thoughts, which tend to be sad or dark. It's different from worry in that rumination focuses on bad feelings and experiences from the past, while worry is concerned with potential bad things in the future.

Mind wandering, on the other hand, is the experience of thoughts not remaining on a single topic for a long period of time, particularly when people are engaged in an attention-demanding task.

To use the app, select a time duration and start the timer. Whenever you catch yourself ruminating or your mind wandering, click the corresponding button. At the end of the session, you can view a summary of your session."""

        tk.Label(self.info_window, text=info_text, wraplength=350, font=("Arial", 11)).pack()


        self.info_window.protocol("WM_DELETE_WINDOW", self.on_info_window_close)

    def on_info_window_close(self):
        # Reset the info window and close it
        self.info_window.destroy()
        self.info_window = None

root = tk.Tk()
app = App(root)
root.mainloop()
