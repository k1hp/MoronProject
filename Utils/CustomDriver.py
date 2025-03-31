import os
import shutil
from undetected_chromedriver import Chrome

class OurDriver(Chrome):
    def quit(self):
        try:
            self.service.process.kill()

        except (AttributeError, RuntimeError, OSError):
            pass
        try:
            self.reactor.event.set()

        except AttributeError:
            pass
        try:
            os.kill(self.browser_pid, 15)

        except Exception as e:  # noqa
            pass
        if (
            hasattr(self, "keep_user_data_dir")
            and hasattr(self, "user_data_dir")
            and not self.keep_user_data_dir
        ):
            for _ in range(5):
                try:
                    shutil.rmtree(self.user_data_dir, ignore_errors=False)
                except FileNotFoundError:
                    pass
                except (RuntimeError, OSError, PermissionError) as e:
                    pass
                else:
                    break
