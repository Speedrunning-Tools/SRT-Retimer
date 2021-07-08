import tkinter as tk
import json
import pip


from math import floor


def pinstall(package):
    pip.main(['install', package])


def str_time(seconds, milliseconds=0):
    """Do math stuff here"""
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    if hours != 0:
        if milliseconds:
            return "{0}:{1:0>2}:{2:0>2}.{3:0>3}".format(hours, minutes, seconds, milliseconds)
        else:
            return "{0}:{1:0>2}:{2:0>2}".format(hours, minutes, seconds)
    elif minutes != 0:
        if milliseconds:
            return "{0}:{1:0>2}.{2:0>3}".format(minutes, seconds, milliseconds)
        else:
            return "{0}:{1:0>2}".format(minutes, seconds)
    elif seconds != 0:
        if milliseconds:
            return "{0}.{1:0>3}".format(seconds, milliseconds)
        else:
            return "0:{0:0>2}".format(seconds)
    else:
        return "0.{0:0>3}".format(milliseconds)


class SRT_Retimer:
    def __init__(self, log_func=print):
        self.log_func = log_func

        self.window = tk.Tk()
        self.window.title("SRT Retimer (Modified version of VerifClient v2)")
        self.window.wm_attributes("-topmost", 1)

        # Rejection buttons
        # here you can add/modify the rejection buttons.
        tk.Label(self.window, text="Rejection Messages").grid(row=0, column=0, columnspan=7)
        tk.Button(self.window, text="Creation", command=self.world_creation).grid(row=2, column=2, sticky='news')
        tk.Button(self.window, text="Troll", command=self.troll_submission).grid(row=1, column=3, sticky='news')
        tk.Button(self.window, text="Dupe", command=self.copy_duplicate).grid(row=1, column=2, sticky='news')
        tk.Button(self.window, text="Twitch Run", command=self.twitch_run).grid(row=1, column=4, sticky='news')
        tk.Button(self.window, text="Video N/A", command=self.video_na).grid(row=2, column=4, sticky='news')
        tk.Button(self.window, text="FR", command=self.fr).grid(row=2, column=3, sticky='news')

        tk.Label(self.window, text=" ").grid(row=3, column=3)

        # Here are the other info
        tk.Label(self.window, text="Retiming").grid(row=4, column=0, columnspan=7)

        self.frV = tk.StringVar()

        tk.Label(self.window, text="Framerate").grid(row=5, column=2, columnspan=2)
        self.fps_field = tk.Entry(self.window, width=5, justify=tk.CENTER, textvariable=self.frV)
        self.fps_field.grid(row=5, column=4)

        self.startV = tk.StringVar()
        self.endV = tk.StringVar()

        tk.Label(self.window, text="Start").grid(row=6, column=1)
        self.start_field = tk.Entry(self.window, width=30, textvariable=self.startV)
        self.start_field.grid(row=6, column=2, columnspan=3)
        self.start_time = tk.Label(self.window, text="0.000")
        self.start_time.grid(row=6, column=5)

        tk.Label(self.window, text="End").grid(row=7, column=1)
        self.end_field = tk.Entry(self.window, width=30, textvariable=self.endV)
        self.end_field.grid(row=7, column=2, columnspan=3)
        self.end_time = tk.Label(self.window, text="0.000")
        self.end_time.grid(row=7, column=5)

        tk.Button(self.window, text="Calculate", command=self.calculate_time).grid(row=9, column=1, sticky='news')
        self.final_time = tk.Label(self.window, text="0.000")
        self.final_time.grid(row=8, column=2, columnspan=3)
        tk.Button(self.window, text="Clear", command=self.reset_time_fields).grid(row=9, column=5, sticky='news')
        tk.Button(self.window, text="Copy Mod Message to Clipboard", command=self.mod_message).grid(row=9, column=2, columnspan=3, sticky='news')

        self.window.mainloop()

    # Here you can find the def functions that go with both the rejection buttons and Mod Message Button
    def copy(self, text):
        self.window.clipboard_clear()
        self.window.clipboard_append(text)

    def world_creation(self):
        self.copy("You must show the world being created from the world selection screen.")

    def troll_submission(self):
        self.copy("This is a Troll submission")

    def copy_duplicate(self):
        self.copy("Duplicate submission. Your run is still in the queue.")

    def twitch_run(self):
        self.copy("Twitch Runs are banned from the leaderboards, reuplad you run to Youtube")

    def video_na(self):
        self.copy("This video/VOD is unavailable")

    def fr(self):
        self.copy("To low of a framerate to be able to verify. Sorry :(")

    def mod_message(self):
        self.copy(f'Mod Message: Time starts at {self.start_time.cget("text")} and ends at {self.end_time.cget("text")} at {self.fps_field.get()} fps to get a final time of {self.final_time.cget("text")}.')

    def calculate_time(self):
        """put the crap on the app"""
        try:
            fps = int(self.fps_field.get())

            startframe = floor(float(json.loads(self.start_field.get())['cmt']) * fps)
            endframe = floor(float(json.loads(self.end_field.get())['cmt']) * fps)

            self.start_time.configure(text=str(round(startframe / fps, 3)))
            self.end_time.configure(text=str(round(endframe / fps, 3)))

            duration = endframe - startframe
            seconds, frames = divmod(duration, fps)
            milliseconds = round(frames / fps * 1000)

            self.final_time.configure(text=str_time(seconds, milliseconds))
        except Exception as e:
            self.final_time.configure(text="Error, check console")
            self.log_func(f"Error: {e}")

    # Here you can add functions that can reset the text boxes and fields
    def reset_time_fields(self):
        self.endV.set("")
        self.startV.set("")
        self.frV.set("")


if __name__ == '__main__':
    client = SRT_Retimer()
