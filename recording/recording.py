# src/screen_recorder.py

import ffmpeg
import imageio_ffmpeg
import platform

class ScreenRecorder:
    def __init__(self, output_path, width, height, fps=60):
        self.output_path = output_path
        self.width = width
        self.height = height
        self.fps = fps

        self.ffmpeg_bin = imageio_ffmpeg.get_ffmpeg_exe()
        self.process = None
        self.system = platform.system()

    def start(self):
        if self.process is not None:
            raise RuntimeError("Recording already started")

        if self.system == "Windows":
            input_kwargs = dict(
                format="gdigrab",
                framerate=self.fps,
                video_size=f"{self.width}x{self.height}",
                draw_mouse=1
            )
            source = "desktop"
        else:
            raise RuntimeError("Unsupported OS")

        self.process = (
            ffmpeg
            .input(source, **input_kwargs)
            .output(
                self.output_path,
                vcodec="libx264",
                preset="ultrafast",
                tune="zerolatency",
                pix_fmt="yuv420p",
                r=self.fps
            )
            .run_async(
                cmd=self.ffmpeg_bin,
                pipe_stdin=True,
                pipe_stdout=True,
                pipe_stderr=True
            )
        )

    def stop(self):
        if self.process is None:
            return

        self.process.stdin.close()
        self.process.wait()
        self.process = None

