import os
import logging
from pydub import AudioSegment
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import threading
from concurrent.futures import ThreadPoolExecutor
import wave
import contextlib
import gettext

# Configure logging
logging.basicConfig(
    filename="conversion.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# Setup gettext for translations
locales_dir = os.path.join(os.path.dirname(__file__), "locales")
gettext.bindtextdomain("app", locales_dir)
gettext.textdomain("app")
_ = gettext.gettext

def analyze_audio(file_path):
    """
    Analyze the audio file for its duration and quality.

    Args:
        file_path (str): Path to the audio file.

    Returns:
        dict: A dictionary containing audio quality information such as duration, channels, and frame rate.
    """
    try:
        with contextlib.closing(wave.open(file_path, 'r')) as audio_file:
            params = audio_file.getparams()
            duration = params.nframes / params.framerate
            quality_info = {
                _("Channels"): params.nchannels,
                _("Sample Width"): params.sampwidth * 8,  # in bits
                _("Frame Rate (Hz)"): params.framerate,
                _("Duration (s)"): round(duration, 2),
            }
            logging.info(f"Audio analysis for {file_path}: {quality_info}")
            return quality_info
    except FileNotFoundError:
        logging.error(f"File not found: {file_path}")
        raise FileNotFoundError(_("The specified file does not exist."))
    except wave.Error:
        logging.error(f"Invalid audio format: {file_path}")
        raise ValueError(_("The file is not a valid audio format."))
    except Exception as e:
        logging.error(f"Failed to analyze audio file {file_path}: {e}")
        raise RuntimeError(_("Failed to analyze the audio file: {e}"))

def convert_audio(input_file: str, output_file: str, output_format: str, bitrate: str):
    """
    Convert an audio file to the specified format.

    Args:
        input_file (str): Path to the input audio file.
        output_file (str): Path to the output audio file.
        output_format (str): Desired output format (e.g., "mp3", "wav", "flac").
        bitrate (str): Bitrate for the output file (e.g., "192k").
    """
    try:
        # Ensure the input file exists
        if not os.path.exists(input_file):
            logging.error(f"Input file does not exist: {input_file}")
            raise FileNotFoundError(_("The input file does not exist."))

        # Validate output format
        valid_formats = ["mp3", "wav", "flac"]
        if output_format not in valid_formats:
            logging.error(f"Invalid output format: {output_format}")
            raise ValueError(_(f"The output format must be one of: {', '.join(valid_formats)}."))

        # Load the input audio file
        try:
            logging.info(f"Loading file: {input_file}")
            audio = AudioSegment.from_file(input_file)
        except Exception as e:
            logging.error(f"Error loading audio file {input_file}: {e}")
            raise RuntimeError(_("Failed to load the input file. Please ensure it is a valid audio file."))

        # Export the audio in the desired format
        try:
            export_params = {"format": output_format}
            if output_format == "mp3":
                export_params["bitrate"] = bitrate
            audio.export(output_file, **export_params)
            logging.info(f"Successfully exported file: {output_file}")
        except Exception as e:
            logging.error(f"Error exporting audio file {output_file}: {e}")
            raise RuntimeError(_("Failed to export the audio file. Please check the output path and format."))

    except FileNotFoundError as e:
        logging.error(str(e))
        raise
    except ValueError as e:
        logging.error(str(e))
        raise
    except RuntimeError as e:
        logging.error(str(e))
        raise
    except Exception as e:
        logging.error(f"Unexpected error during conversion: {e}")
        raise RuntimeError(_("An unexpected error occurred during the conversion process."))

def start_batch_conversion(input_files, output_dir, output_format, bitrate):
    total_files = len(input_files)
    progress = [0]

    def update_progress():
        progress_bar["value"] = (progress[0] / total_files) * 100
        progress_label["text"] = _(f"Processed {progress[0]} of {total_files} files.")
        progress_bar.update()

    def process_file(file_path):
        try:
            output_file = os.path.join(output_dir, os.path.basename(file_path).rsplit(".", 1)[0] + f".{output_format}")
            convert_audio(file_path, output_file, output_format, bitrate)
        except Exception as e:
            messagebox.showerror(_("Error"), f"{_("Failed to process file")}: {file_path}\n{e}")
        finally:
            progress[0] += 1
            update_progress()

    try:
        if not os.path.exists(output_dir):
            logging.error(f"Output directory does not exist: {output_dir}")
            raise FileNotFoundError(_("The specified output directory does not exist."))

        with ThreadPoolExecutor() as executor:
            futures = [executor.submit(process_file, file_path) for file_path in input_files]
            for future in futures:
                future.result()  # Wait for all tasks to complete

        messagebox.showinfo(_("Success"), _("Batch conversion completed successfully."))
    except FileNotFoundError as e:
        messagebox.showerror(_("Error"), str(e))
    except Exception as e:
        messagebox.showerror(_("Error"), _("An unexpected error occurred during the batch conversion."))
        logging.error(f"Unexpected error during batch conversion: {e}")

def open_files():
    try:
        files = filedialog.askopenfilenames(filetypes=[(_("Audio files"), "*.mp4 *.wav *.flac *.mp3")])
        if files:
            input_files_var.set(";".join(files))
    except Exception as e:
        logging.error(f"Error selecting files: {e}")
        messagebox.showerror(_("Error"), _("Failed to select files. Please try again."))

def save_directory():
    try:
        directory = filedialog.askdirectory()
        if directory:
            output_dir_var.set(directory)
    except Exception as e:
        logging.error(f"Error selecting directory: {e}")
        messagebox.showerror(_("Error"), _("Failed to select output directory. Please try again."))

def start_conversion_thread():
    try:
        input_files = input_files_var.get().split(";")
        output_dir = output_dir_var.get()
        output_format = output_format_var.get()
        bitrate = bitrate_var.get()

        if not input_files or not output_dir:
            raise ValueError(_("Please specify both input files and an output directory."))

        # Run the batch conversion in a separate thread
        thread = threading.Thread(target=start_batch_conversion, args=(input_files, output_dir, output_format, bitrate))
        thread.start()
    except ValueError as e:
        logging.error(str(e))
        messagebox.showerror(_("Error"), str(e))
    except Exception as e:
        logging.error(f"Unexpected error starting conversion: {e}")
        messagebox.showerror(_("Error"), _("An unexpected error occurred while starting the conversion."))

# GUI Setup
app = tk.Tk()
app.title(_("Vid2AudConverter"))
app.geometry("600x400")
app.resizable(False, False)

# Define styles
style = ttk.Style()
style.configure("TButton", font=("Helvetica", 10), padding=5)
style.configure("TLabel", font=("Helvetica", 10))
style.configure("TEntry", font=("Helvetica", 10))
style.configure("TProgressbar", thickness=10)

# Header
header_frame = tk.Frame(app, bg="#4CAF50", height=50)
header_frame.pack(fill="x")
header_label = tk.Label(header_frame, text=_("Vid2AudConverter"), bg="#4CAF50", fg="white", font=("Helvetica", 16))
header_label.pack(pady=10)

# Input Files
input_frame = tk.Frame(app, pady=10)
input_frame.pack(fill="x", padx=20)
input_label = tk.Label(input_frame, text=_("Input Audio Files:"), font=("Helvetica", 10))
input_label.grid(row=0, column=0, sticky="w")
input_files_var = tk.StringVar()
input_entry = ttk.Entry(input_frame, textvariable=input_files_var, width=50)
input_entry.grid(row=0, column=1, padx=10)
input_button = ttk.Button(input_frame, text=_("Browse"), command=open_files)
input_button.grid(row=0, column=2, padx=10)

# Output Directory
output_frame = tk.Frame(app, pady=10)
output_frame.pack(fill="x", padx=20)
output_label = tk.Label(output_frame, text=_("Output Directory:"), font=("Helvetica", 10))
output_label.grid(row=0, column=0, sticky="w")
output_dir_var = tk.StringVar()
output_entry = ttk.Entry(output_frame, textvariable=output_dir_var, width=50)
output_entry.grid(row=0, column=1, padx=10)
output_button = ttk.Button(output_frame, text=_("Browse"), command=save_directory)
output_button.grid(row=0, column=2, padx=10)

# Output Format Options
format_frame = tk.Frame(app, pady=10)
format_frame.pack(fill="x", padx=20)
format_label = tk.Label(format_frame, text=_("Select Output Format:"), font=("Helvetica", 10))
format_label.grid(row=0, column=0, sticky="w")
output_format_var = tk.StringVar(value="mp3")
format_menu = ttk.Combobox(format_frame, textvariable=output_format_var, values=["mp3", "wav", "flac"], state="readonly", width=10)
format_menu.grid(row=0, column=1, padx=10, sticky="w")

# Bitrate Options
bitrate_frame = tk.Frame(app, pady=10)
bitrate_frame.pack(fill="x", padx=20)
bitrate_label = tk.Label(bitrate_frame, text=_("Select Bitrate:"), font=("Helvetica", 10))
bitrate_label.grid(row=0, column=0, sticky="w")
bitrate_var = tk.StringVar(value="192k")
bitrate_menu = ttk.Combobox(bitrate_frame, textvariable=bitrate_var, values=["64k", "128k", "192k", "256k", "320k"], state="readonly", width=10)
bitrate_menu.grid(row=0, column=1, padx=10, sticky="w")

# Progress Bar and Label
progress_frame = tk.Frame(app, pady=10)
progress_frame.pack(fill="x", padx=20)
progress_bar = ttk.Progressbar(progress_frame, orient="horizontal", mode="determinate", length=400)
progress_bar.pack(pady=5)
progress_label = tk.Label(progress_frame, text="", font=("Helvetica", 10))
progress_label.pack()

# Convert Button
convert_button = ttk.Button(app, text=_("Convert"), command=start_conversion_thread)
convert_button.pack(pady=20)

# Run the app
app.mainloop()