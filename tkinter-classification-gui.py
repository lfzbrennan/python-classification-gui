from tkinter import *
from PIL import ImageTk, Image
import glob
import random
import os
from shutil import copyfile
import argparse


class CreateDisplay:
    def __init__(self, master, save_dir, images, current_image, class_one="good", class_two="bad", mode="move"):
        self.master = master
        self.count = 0
        self.save_dir = save_dir
        self.current_image = current_image
        self.images = images
        self.mode = mode
        self.class1 = class_one
        self.class2 = class_two
        master.title("Classify Image")

        self.display_image()

        self.button_1 = Button(self.master, text=class_one, command=self.change_image_good)
        self.button_1.grid(row=1, column=0)

        self.button_2 = Button(self.master, text=class_two, command=self.change_image_bad)
        self.button_2.grid(row=1, column=1)

    def change_image_good(self):
        self.count += 1

        path = self.current_image.split("/")[-1]

        if self.mode == "move":
            os.rename(self.current_image, self.save_dir + "/" + self.class1 + "/" + path)
        else:
            copyfile(self.current_image, self.save_dir + "/" + self.class1 + "/" + path)

        self.current_image = self.images[self.count]

        self.display_image()

    def change_image_bad(self):
        self.count += 1

        path = self.current_image.split("/")[-1]

        if self.mode == "move":
            os.rename(self.current_image, self.save_dir + "/" + self.class2 + "/" + path)
        else:
            copyfile(self.current_image, self.save_dir + "/" + self.class2 + "/" + path)

        self.current_image = self.images[self.count]

        self.display_image()

    def display_image(self):
        img = Image.open(self.current_image)
        img = img.resize((512, 512))
        self.img = ImageTk.PhotoImage(img)
        self.image = Label(self.master, image=self.img)
        self.image.grid(row=0, columnspan=2)


def main(args):
    parser = argparse.ArgumentParser(description='Save cascading images from directory')
    parser.add_argument('--root_dir', default='in', type=str, help='where unclassified dataset is stored')
    parser.add_argument('--save_dir', default='out', type=str, help='where classified data is stored')
    parser.add_argument('--class1', default='good', type=str, help='classification 1')
    parser.add_argument('--class2', default='bad', type=str, help='classification 2')
    parser.add_argument('--mode', default='move', type=str, help='"move" or "copy": "move" moves the files (deleting them from the root directory), where "copy" just makes a copy (keeps root)')

    args = parser.parse_args()

    save_dir = args.save_dir
    root_dir = args.root_dir

    print("Globbing")

    all_images = glob.glob(root_dir)

    print("Shuffling")
    random.shuffle(all_images)
    CURR_IMG = all_images[0]

    if not os.path.exists(args.save_dir + "/" + args.class1):
        os.mkdir(args.save_dir + "/" + args.class1)

    if not os.path.exists(args.save_dir + "/" + args.class2):
        os.mkdir(args.save_dir + "/" + args.class2)

    print("Creating GUI")

    root = Tk()
    CreateDisplay(root, save_dir, all_images, CURR_IMG, class_one=args.class1, class_two=args.class2, mode=args.mode)
    root.mainloop()


if __name__ == "__main__":
    from sys import argv

    try:
        main(argv)
    except KeyboardInterrupt:
        pass
    sys.exit()



