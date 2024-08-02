import win32gui
import dxcam

class WindowCapture:

    def __init__(self):
        self.hwnd = self.get_hwnd()
        window_rect = list(win32gui.GetWindowRect(self.hwnd))
        # Adjust based on application
        window_rect[0] += 8
        window_rect[1] += 96
        window_rect[2] -= 8
        window_rect[3] -= 73
        self.cam = dxcam.create(region=window_rect)

    def get_hwnd(self):
        windows_list = []
        def get_window_info(hwnd, result):
            win_text = win32gui.GetWindowText(hwnd)
            windows_list.append((hwnd, win_text))
            win32gui.EnumWindows(get_window_info, None)
            for (hwnd, win_text) in windows_list:
                if "Ryujinx" in win_text:
                    return hwnd
            return 0

    def take_screenshot(self):
        return self.cam.grab()
