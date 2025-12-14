

class QuizTimer:
    def __init__(self, root, on_timeout, total_seconds=720):
        self.root = root
        self.on_timeout = on_timeout
        self.total_seconds = total_seconds
        self.time_left = total_seconds
        self.timer_id = None

    def reset(self):
        self.stop()
        self.time_left = self.total_seconds

    def start(self):
        self.stop()
        self._tick()

    def _tick(self):
        if self.time_left <= 0:
            self.on_timeout()
            return
        self.time_left -= 1
        self.timer_id = self.root.after(1000, self._tick)

    def stop(self):
        if self.timer_id is not None:
            try:
                self.root.after_cancel(self.timer_id)
            except Exception:
                pass
            self.timer_id = None