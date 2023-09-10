import tkinter as tk
from PIL import Image, ImageTk


class ScrollableList:
    def __init__(self):
        self.item_container = None
        self.canvas = None
        self.scroll_bar = None
        self.container = None
        self.items = []

    def start(self, root):
        self.container = tk.Frame(root)
        self.container.pack(fill=tk.BOTH, expand=True)

        self.scroll_bar = tk.Scrollbar(self.container, orient=tk.VERTICAL)
        self.scroll_bar.pack(side=tk.RIGHT, fill=tk.Y)

        self.canvas = tk.Canvas(self.container, yscrollcommand=self.scroll_bar.set)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        self.scroll_bar.config(command=self.canvas.yview)

        self.item_container = tk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.item_container, anchor=tk.NW)
        self.canvas.bind_all("<MouseWheel>", self.on_mousewheel)

    def update_canvas_scrollregion(self):
        self.item_container.update_idletasks()
        self.canvas.config(scrollregion=self.canvas.bbox("all"))

    def on_mousewheel(self, event):
        self.canvas.yview_scroll(event.delta, "units")

    def add_item(self, item, kwargs):
        self.items.append(item(**kwargs))
        self.items[-1].start(self.item_container, lambda: self.delete_item(len(self.items) - 1))
        self.update_canvas_scrollregion()

    def delete_item(self, index):
        self.items[index] = None
        self.update_canvas_scrollregion()


class ImageEditUI:
    def __init__(self, root, image_path):
        self.remove_from_parent = None
        self.root = root
        self.input = None
        self.frame = None

        self.PIL_image = Image.open(image_path)
        self.PIL_image.thumbnail((800, 800))
        self.image = ImageTk.PhotoImage(self.PIL_image)

    def start(self, container, remove_from_parent):
        self.remove_from_parent = remove_from_parent
        self.frame = tk.Frame(container)
        self.frame.pack()

        image_label = tk.Label(self.frame, image=self.image)
        image_label.image = self.image
        image_label.pack(padx=5, pady=5)

        label = tk.Label(self.frame, text="entre words in image: ")
        label.pack()

        self.input = tk.Entry(self.frame, width=50)
        self.input.pack()

        delete_button = tk.Button(self.frame, text="Delete", command=self.delete)
        delete_button.pack()

    def delete(self):
        for child in self.frame.winfo_children():
            child.destroy()
        self.frame.destroy()

        root.after(100, self.remove_from_parent)


scrollable_list = ScrollableList()

root = tk.Tk()
scrollable_list.start(root)
scrollable_list.update_canvas_scrollregion()
scrollable_list.add_item(ImageEditUI, {"image_path": "test.png", "root": root})
root.mainloop()
