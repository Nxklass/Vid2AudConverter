
# Vid2AudConverter

Vid2AudConverter is a user-friendly Python-based application for converting video and audio files into various audio formats. It provides advanced features like batch processing, format customization, multi-language support, and a clean graphical user interface.

---

## Features

- **Convert Video to Audio**: Extract audio from video files such as MP4.
- **Multiple Audio Formats**: Supports MP3, WAV, FLAC, OGG, AAC, and M4A outputs.
- **Batch Processing**: Convert multiple files simultaneously with a detailed progress indicator.
- **Custom Settings**: Configure bitrate, sample rate, and channels (mono/stereo) for output files.
- **Drag-and-Drop Functionality**: Easily add files or directories to the application.
- **Localized Interface**: Multi-language support with gettext for an inclusive user experience.
- **Advanced Error Handling**: Ensures seamless usage with detailed error messages and logs.
- **Performance Optimizations**: Utilizes threading and a thread pool for fast and efficient conversions.
- **Clean and Responsive GUI**: Built with Tkinter for an intuitive and modern interface.

---

## Installation

### Prerequisites

- Python 3.8 or higher
- Required Python libraries:
  - `pydub`
  - `tkinter`
  - `wave`
  - `gettext`
  - `concurrent.futures`
  - `tkinterdnd2`

You can install the required dependencies using pip:

```bash
pip install pydub
pip install tkinter
pip install tkinterdnd2
```

### FFmpeg Installation

Vid2AudConverter uses FFmpeg for audio processing. Install FFmpeg by following the instructions for your operating system:

- **Windows**: Download FFmpeg binaries from [FFmpeg Official Website](https://ffmpeg.org/).
- **Linux**: Install via your package manager (e.g., `sudo apt install ffmpeg`).
- **macOS**: Install using Homebrew (`brew install ffmpeg`).

Ensure FFmpeg is added to your system's PATH.

---

## Usage

### Running the Application

1. Clone this repository:
   ```bash
   git clone https://github.com/Nxklass/Vid2AudConverter.git
   ```

2. Navigate to the project directory:
   ```bash
   cd Vid2AudConverter
   ```

3. Run the application:
   ```bash
   python vid2audconverter.py
   ```

### Features Walkthrough

1. **Add Files**: Use the "Browse" button to select video/audio files or drag and drop files directly into the application.
2. **Choose Output Directory**: Specify where the converted files will be saved.
3. **Set Output Format**: Choose from MP3, WAV, FLAC, OGG, AAC, or M4A.
4. **Customize Settings**:
   - Select the desired **bitrate** (e.g., 64k, 128k, 320k).
   - Set the **sample rate** (e.g., 44100 Hz, 48000 Hz).
   - Choose the number of **channels** (Mono or Stereo).
5. **Start Conversion**: Click the "Convert" button to begin the process.

---

## Roadmap

Planned features for future versions:

- **Dark Mode**: A theme toggle for better usability.
- **Metadata Editor**: Edit ID3 tags for MP3 outputs.
- **Automatic Updates**: Add a feature to check for and install updates.
- **Queue Management**: Pause, resume, or reorder conversion tasks.

---

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork this repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Make your changes and commit them (`git commit -m 'Add new feature'`).
4. Push your branch (`git push origin feature-branch`).
5. Create a Pull Request.

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## Acknowledgments

- Built with Python and Tkinter.
- Powered by Pydub and FFmpeg.
- Inspired by the need for a simple yet powerful audio converter.