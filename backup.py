'''
class BufferReadThread(QThread):
    micro_names = []
    global snaps
    def __init__(self, micro_names):
        super(BufferReadThread, self).__init__()
        self.micro_names = micro_names

    def run(self):
        for micro_name in self.micro_names:
            img = np.uint8(ctf.show_mrc(micro_name, 0.1))
            snaps[micro_name]=img

            # print(img.dtype)
         #   y, x = img.shape
         #   byte_img = img.tobytes()
         #   Qimg = QImage(byte_img, x, y, QImage.Format_Grayscale8)

          #  pix = QPixmap.fromImage(Qimg)
         #   item = QGraphicsPixmapItem(pix)
         #   snaps[micro_name]=item


class preReadT(QThread):

    micro_name = ""
    trigger=pyqtSignal()
    def __init__(self, micro_name):
        super(preReadT, self).__init__()
        self.micro_name = micro_name


    def run(self):
        img = np.uint8(ctf.show_mrc(self.micro_name, 0.1))

        y, x = img.shape
        byte_img = img.tobytes()
        Qimg = QImage(byte_img, x, y, QImage.Format_Grayscale8)
        global snaps
        snaps[self.micro_name]=Qimg
        pass

        self.trigger.emit()
'''