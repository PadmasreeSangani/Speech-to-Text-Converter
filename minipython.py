import speech_recognition as sr
import tkinter as tk
from tkinter import messagebox

class SpeechToTextConverter:
    def __init__(self, root):
        self.root = root
        self.root.title("Speech to Text Converter")

        self.recognizer = sr.Recognizer()
        self.is_recording = False

        self.header_label = tk.Label(root, text="Speech to Text Converter", font=("Helvetica", 16))
        self.header_label.pack(pady=10)

        self.start_button = tk.Button(root, text="Start Recording", command=self.start_recording)
        self.start_button.pack(pady=5)

        self.stop_button = tk.Button(root, text="Stop Recording", command=self.stop_recording, state=tk.DISABLED)
        self.stop_button.pack(pady=5)

        self.text_output = tk.Text(root, height=10, width=40)
        self.text_output.pack(padx=10, pady=10)

        self.exit_button = tk.Button(root, text="Exit", command=self.exit_program)
        self.exit_button.pack(pady=5)

    def start_recording(self):
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        self.is_recording = True

        try:
            with sr.Microphone() as source:
                self.recognizer.adjust_for_ambient_noise(source)
                self.audio = self.recognizer.listen(source)
                self.text_output.delete(1.0, tk.END)
                self.text_output.insert(tk.END, "Recording...\n")
        except sr.RequestError as e:
            messagebox.showerror("Error", f"Could not request audio: {e}")

    def stop_recording(self):
        if self.is_recording:
            self.is_recording = False
            self.start_button.config(state=tk.NORMAL)
            self.stop_button.config(state=tk.DISABLED)

            try:
                text = self.recognizer.recognize_google(self.audio)
                self.text_output.insert(tk.END, text + "\n")
            except sr.UnknownValueError:
                messagebox.showerror("Error", "Could not understand audio.")
            except sr.RequestError as e:
                messagebox.showerror("Error", f"Could not request results from Google Web Speech API: {e}")

    def exit_program(self):
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = SpeechToTextConverter(root)
    root.mainloop()

