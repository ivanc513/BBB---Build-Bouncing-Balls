import ffmpeg
import imageio_ffmpeg

class ScreenRecorder:
    def __init__(self, output_path, width, height, fps=60):
        self.output_path = output_path
        self.width = width
        self.height = height
        self.fps = fps
        self.ffmpeg_bin = imageio_ffmpeg.get_ffmpeg_exe()
        self.process = None

    def start(self):
        if self.process is not None:
            raise RuntimeError("Recording already started")

        self.process = (
            ffmpeg
            .input(
                "pipe:",
                format="rawvideo",
                pix_fmt="rgb24",
                s=f"{self.width}x{self.height}",
                framerate=self.fps
            )
            .output(
                self.output_path,
                vcodec="libx264",
                pix_fmt="yuv420p",
                preset="ultrafast",
                vf="vflip",
                r=self.fps
            )
            .overwrite_output()
            .run_async(
                cmd=self.ffmpeg_bin,
                pipe_stdin=True
            )
        )

    def write_frame(self, frame_bytes):
        if self.process:
            self.process.stdin.write(frame_bytes)

    def stop(self):
        if self.process:
            self.process.stdin.close()
            self.process.wait()
            self.process = None
