from suika.core.watcher.screen import WindowCapture
from matplotlib import pyplot as plt

if __name__ == '__main__':
    wc = WindowCapture()
    img = wc.take_screenshot()
    plt.imshow(img)
    plt.show()
