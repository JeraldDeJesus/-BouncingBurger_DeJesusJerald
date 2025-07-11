import tkinter as tk
from PIL import Image, ImageTk
import random

class Burger:
    def __init__(self, canvas, image, x, y, dx=5, dy=4, label=None):
        self.canvas = canvas
        self.image = image
        self.id = canvas.create_image(x, y, image=image, anchor=tk.NW)
        self.dx = dx
        self.dy = dy
        self.label = label  # optional label ID (only for original)

    def move(self, canvas_width, canvas_height):
        x0, y0, x1, y1 = self.canvas.bbox(self.id)
        hit_wall = False

        if x0 <= 0 or x1 >= canvas_width:
            self.dx = -self.dx
            hit_wall = True
        if y0 <= 0 or y1 >= canvas_height:
            self.dy = -self.dy
            hit_wall = True

        self.canvas.move(self.id, self.dx, self.dy)

        # Move label if it exists
        if self.label:
            self.canvas.move(self.label, self.dx, self.dy)

        return hit_wall

    def destroy(self):
        self.canvas.delete(self.id)
        if self.label:
            self.canvas.delete(self.label)

class BouncingBurgerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Bouncing Burger")

        self.canvas_width = 800
        self.canvas_height = 600
        self.canvas = tk.Canvas(root, width=self.canvas_width, height=self.canvas_height, bg="black")
        self.canvas.pack()

        # Add name on the background
        self.canvas.create_text(
            self.canvas_width // 2,
            self.canvas_height // 2,
            text="Jerald De Jesus",
            font=("Helvetica", 30, "bold"),
            fill="lightgray",
            anchor="center"
        )

        # Load images
        original_img = Image.open("burger.png").resize((100, 100), Image.Resampling.LANCZOS)
        clone_img = original_img.resize((50, 50), Image.Resampling.LANCZOS)
        self.original_photo = ImageTk.PhotoImage(original_img)
        self.clone_photo = ImageTk.PhotoImage(clone_img)

        # Create original burger with label "JDJ"
        label = self.canvas.create_text(100 + 50, 100 - 10, text="JDJ", font=("Helvetica", 14, "bold"), fill="white")
        self.original = Burger(self.canvas, self.original_photo, 100, 100, dx=5, dy=4, label=label)
        self.burgers = [self.original]

        # State
        self.paused = False
        self.growing = True
        self.MAX_BURGERS = 5  # 1 original + 4 clones

        self.root.bind("<space>", self.toggle_pause)
        self.animate()

    def toggle_pause(self, event=None):
        self.paused = not self.paused

    def animate(self):
        if not self.paused:
            self.move_burgers()
        self.root.after(16, self.animate)

    def move_burgers(self):
        for burger in self.burgers:
            hit = burger.move(self.canvas_width, self.canvas_height)
            if burger == self.original and hit:
                self.canvas.config(bg=self.random_color())
                self.handle_cloning()

    def handle_cloning(self):
        count = len(self.burgers)

        if self.growing:
            if count < self.MAX_BURGERS:
                rand_x = random.randint(0, self.canvas_width - 50)
                rand_y = random.randint(0, self.canvas_height - 50)
                rand_dx = random.choice([-8, -7, 7, 8])  # faster than original
                rand_dy = random.choice([-8, -7, 7, 8])
                clone = Burger(self.canvas, self.clone_photo, rand_x, rand_y, rand_dx, rand_dy)
                self.burgers.append(clone)
            if len(self.burgers) == self.MAX_BURGERS:
                self.growing = False
        else:
            if count > 1:
                clone = self.burgers.pop()
                clone.destroy()
            if len(self.burgers) == 1:
                self.growing = True

    def random_color(self):
        r = random.randint(0, 100)
        g = random.randint(0, 100)
        b = random.randint(0, 100)
        return f"#{r:02x}{g:02x}{b:02x}"

# Run the app
if __name__ == "__main__":
    root = tk.Tk()
    app = BouncingBurgerApp(root)
    root.mainloop()