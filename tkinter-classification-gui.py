from tkinter import *
from PIL import ImageTk, Image
import glob
import random
import os
from shutil import copyfile
import argparse


class CreateDisplay:
    def __init__(self, master, save_dir, images, current_image, classes="good", mode="save"):
        self.master = master
        self.count = 0
        self.save_dir = save_dir
        self.current_image = current_image
        self.images = images
        self.mode = mode
        self.classes = classes
        master.title("Classify Image")

        self.display_image()

        self.col = len(self.classes)

        buttons = [Button(self.master, text=self.classes[i], command=lambda: self.change_image(self.classes[i])).grid(row=1, column=i) for i in range(self.col)]

    def change_image(self, class_):

        self.count += 1

        path = self.current_image.split("/")[-1]

        if self.mode == "move":
            os.rename(self.current_image, self.save_dir + "/" + class_ + "/" + path)
        elif self.mode == "copy":
            copyfile(self.current_image, self.save_dir + "/" + class_ + "/" + path)

        else:
            raise ValueError('Mode must be set to "move" or "copy"')

        self.current_image = self.images[self.count]

        self.display_image()


    def display_image(self):
        img = Image.open(self.current_image)
        img = img.resize((512, 512))
        self.img = ImageTk.PhotoImage(img)
        self.image = Label(self.master, image=self.img)
        self.image.grid(row=0, columnspan=self.col)


def main(args):
    parser = argparse.ArgumentParser(description='Save cascading images from directory')
    parser.add_argument('--root_dir', default='in', type=str, help='where unclassified dataset is stored')
    parser.add_argument('--save_dir', default='out', type=str, help='where classified data is stored')
    parser.add_argument('--classes', nargs="+", default='uno', type=str, help='list of classses')
    parser.add_argument('--mode', default='move', type=str, help='"move" or "copy": "move" moves the files (deleting them from the root directory), where "copy" just makes a copy (keeps root)')

    args = parser.parse_args()

    save_dir = args.save_dir
    root_dir = args.root_dir
    
    print("Globbing")

    all_images = glob.glob(root_dir)

    print("Shuffling")
    random.shuffle(all_images)
    CURR_IMG = all_images[0]

    for class_ in args.classes:
        if not os.path.exists(args.save_dir + "/" + class_):
            os.mkdir(args.save_dir + "/" + class_)

    print("Creating GUI")

    root = Tk()
    CreateDisplay(root, save_dir, all_images, CURR_IMG, classes=args.classes, mode=args.mode)
    root.mainloop()


if __name__ == "__main__":
    from sys import argv

    try:
        main(argv)
    except KeyboardInterrupt:
        pass
    sys.exit()
