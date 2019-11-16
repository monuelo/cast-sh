import os
import time


class Logging:
    """
    This class implements a logging function for the streamed data
    There are some bugs as of yet in this code. Will be slowly addressed
    and updated as they are encountered.
    """

    def __init__(self, session_id):
        self.folder = r"cast/log_data"
        self.file_location = r"cast/log_data/log_" + str(session_id) + r".log"

    def write_log(self, data_value):
        # Streams the data into a file for the Logging
        data_value_checker = data_value.encode("UTF-8")
        with open(self.file_location, "a+") as f:
            if data_value_checker != b"\x7f" and data_value_checker != b"\r":
                f.write(data_value)
            elif data_value_checker == b"\x7f":
                f.seek(0, os.SEEK_END)
                f.seek(f.tell() - 1, os.SEEK_SET)
                f.truncate()
            elif data_value_checker == b"\r":
                seconds = time.time()
                local_time = time.ctime(seconds)
                f.write("  [{}]\n".format(local_time))
                # f.write(f"   [{local_time}]\n") # For upgrade to Python >3.5

    def make_log_folder(self):
        if not os.path.exists(self.folder):
            os.mkdir(self.folder)
            return "Made Folder"
        else:
            return "Folder already exists"
