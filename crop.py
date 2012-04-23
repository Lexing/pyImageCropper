from PIL import Image
from PIL.ExifTags import TAGS
import sys, os
import Tkinter
import ImageTk


class ImageCropper:
    def __init__(self):
        self.root = root = Tkinter.Tk()
        self.root.bind("<Button-1>", self.__on_mouse_down)
        self.root.bind("<ButtonRelease-1>", self.__on_mouse_release)
        self.root.bind("<B1-Motion>", self.__on_mouse_move)
        self.root.bind("<Key>", self.__on_key_down)
        self.message = None
        self.rectangle = None

    def get_image_exif(self, image):
        if image is None:
            img_exif = None
        info = image._getexif()
        if info is not None:
            img_exif = {}
            for tag, value in info.items():
                decoded = TAGS.get(tag, tag)
                img_exif[decoded] = value
        return img_exif

    def set_image(self, filename):
        self.filename = filename
        self.outputname = filename[:filename.rfind('.')] + '_cropped'
        self.img = Image.open(filename)
        # exif = self.get_image_exif(image)
        ratio = float(self.img.size[1]) / self.img.size[0]
        if self.img.size[0] > 1200:
            self.scale = self.img.size[0] / 1200
            self.resized_img = self.img.resize( (self.img.size[0] / self.scale,
                                                   self.img.size[1] / self.scale),
                                                Image.ANTIALIAS )
        if self.img.size[1] > 800:
            self.scale = self.img.size[1] / 800
            self.resized_img = self.img.resize( (self.img.size[0] / self.scale,
                                                    self.img.size[1] / self.scale),
                                                Image.ANTIALIAS )
        if self.img.size[0] <= 1200 and self.img.size[1] <= 800:
            self.resized_img = self.img
            self.scale = 1
        self.photo = ImageTk.PhotoImage(self.resized_img)
        self.canvas = Tkinter.Canvas(self.root, 
                                     width = self.resized_img.size[0],
                                     height = self.resized_img.size[1],
                                     highlightthickness = 0,
                                     bd = 0)
        self.canvas.create_image(0, 0, anchor = Tkinter.NW, image = self.photo)
        self.canvas.pack()

    def __on_mouse_down(self, event):
        self.top_left_x, self.top_left_y = event.x, event.y
        print "top left coordinates: %s/%s" % (event.x, event.y)
        self.canvas.delete(self.message)

    def __on_mouse_release(self, event):
        self.bottom_right_x, self.bottom_right_y = event.x, event.y
        print "bottom_right coordinates: %s/%s" % (event.x, event.y)
        self.box = (self.top_left_x * self.scale,
                    self.top_left_y * self.scale,
                    self.bottom_right_x * self.scale, 
                    self.bottom_right_y * self.scale)
        print self.box
        try:
            cropped = self.img.crop(self.box)
            if cropped.size[0] == 0 and cropped.size[1] == 0:
                raise SystemError('no size')
            cropped.save(self.outputname + '.jpg', 'jpeg')
            self.message = self.canvas.create_text(10, 10, anchor = Tkinter.NW, text = 'Saved: ' + self.outputname + '.jpg', fill = 'red')
        except SystemError as e:
            self.message = self.canvas.create_text(10, 10, anchor = Tkinter.NW, text = 'Not saved', fill = 'red')

    def __on_mouse_move(self, event):
        self.canvas.delete(self.rectangle)
        self.rectangle = self.canvas.create_rectangle(self.top_left_x, self.top_left_y, event.x, event.y)

    def __on_key_down(self, event):
        if event.char == ' ':
            pass
        elif event.char == 'q':
            self.root.destroy()

    def run(self):
        self.root.mainloop()

cropper = ImageCropper()
cropper.set_image(sys.argv[1])
cropper.run()