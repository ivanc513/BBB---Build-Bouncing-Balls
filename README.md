# Build Bouncing Balls

A real-time physics-based simulation built with **Python**, **Pygame** and **PyOpenGL** that renders multiple bouncing balls inside a window, complete with collision handling, gravity, and optional video recording via **FFmpeg**. This project focuses on user-friendly creation of bouncing ball simulation videos for Tiktok, Instagram, and Youtube without the need for programming knowledge.

---

## Features

* Real-time ball physics (gravity, velocity, collisions)
* Smooth rendering with Pygame
* Window-boundary collision handling
* Scalable to many objects
* Optional screen recording using FFmpeg

---

## Installation

1. **Clone the repository**

   ```cmd prompt
   git clone https://github.com/your-username/build-bouncing-balls.git
   cd build-bouncing-balls
   ```

2. **Create and activate a virtual environment (recommended)**

   ```cmd prompt
   python -m venv venv
   venv\scripts\Activate.ps1
   ```

3. **Install dependencies**

   ```cmd prompt
   pip install pygame PyOpenGL imageio-ffmpeg
   ```

4. **Ensure FFmpeg is available**

   * The project automatically locates FFmpeg via `imageio-ffmpeg`

---

## Running the Project

```bash
python main.py
```

A window will open displaying bouncing balls simulated in real time.

---

## Screen Recording (Optional)

The project supports recording the simulation to a video file using FFmpeg.

* Output videos are saved with **unique filenames** to avoid overwriting
* Resolution and FPS match the simulation window

Videos are set to match 9:16 resolution found in shorts, reels, and tiktok videos.
Automatically saved to saved_videos folder

---

## Project Structure

```
build-bouncing-balls/
│
├── main.py              # Entry point and game loop
├── ball.py              # Ball physics and behavior
├── recorder.py          # Screen recording logic (FFmpeg)
├── assets/              # Images or resources (if any)
├── recordings/          # Generated video files
└── README.md
```

---

## License

This project is open-source and free to use for learning and experimentation.

**Author:** Ivan Carmona

