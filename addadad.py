import tkinter as tk
from tkinter import messagebox, font

class Job:
    def __init__(self, job_id, deadline, profit):
        self.job_id = job_id
        self.deadline = deadline
        self.profit = profit

class TaskSchedulerApp:
    def __init__(self, root):
        self.root = root
        root.title("Task Scheduler with Auto Assignment")
        root.geometry("900x500")
        root.minsize(850, 450)

        self.jobs = {}
        self.max_slots = 5
        self.slots = [None] * (self.max_slots + 1)

        self.job_colors = [
            "#FFB3BA", "#BAE1FF", "#BAFFC9", "#FFFFBA", "#FFDFBA",
            "#D7BAFF", "#BAFFD9", "#FFC2E2", "#B9E0FF", "#BAFFC9"
        ]
        self.job_to_color = {}

        self.header_font = font.Font(family="Helvetica", size=20, weight="bold")
        self.slot_label_font = ("Helvetica", 11, "bold")
        self.job_font_title = ("Helvetica", 13, "bold")
        self.job_font_profit = ("Helvetica", 10)
        self.job_font_deadline = ("Helvetica", 9, "italic")
        self.empty_font = ("Helvetica", 12, "italic")
        self.total_profit_font = ("Helvetica", 18, "bold")

        self.setup_widgets()
        self.draw_visualization()

    def setup_widgets(self):
        top_frame = tk.Frame(self.root)
        top_frame.pack(pady=10, fill=tk.X)

        tk.Label(top_frame, text="Job ID:").pack(side=tk.LEFT, padx=5)
        self.entry_job_id = tk.Entry(top_frame, width=5)
        self.entry_job_id.pack(side=tk.LEFT, padx=5)

        tk.Label(top_frame, text="Deadline:").pack(side=tk.LEFT, padx=5)
        self.entry_deadline = tk.Entry(top_frame, width=5)
        self.entry_deadline.pack(side=tk.LEFT, padx=5)

        tk.Label(top_frame, text="Profit:").pack(side=tk.LEFT, padx=5)
        self.entry_profit = tk.Entry(top_frame, width=7)
        self.entry_profit.pack(side=tk.LEFT, padx=5)

        tk.Button(top_frame, text="Add Job", command=self.add_job).pack(side=tk.LEFT, padx=10)

        self.canvas = tk.Canvas(self.root, width=850, height=260, bg="#F4F6F7")
        self.canvas.pack(pady=10, fill=tk.BOTH, expand=True)

        self.profit_label = tk.Label(self.root, text="Total Profit: ₹0", font=self.total_profit_font, fg="#27AE60")
        self.profit_label.pack(pady=5)

        self.canvas.bind("<Button-1>", self.on_canvas_click)

    def add_job(self):
        job_id = self.entry_job_id.get().strip()
        deadline = self.entry_deadline.get().strip()
        profit = self.entry_profit.get().strip()

        if not job_id or not deadline.isdigit() or not profit.isdigit():
            messagebox.showerror("Invalid Input", "Enter valid Job ID, numeric Deadline and Profit.")
            return

        # Check if all slots are full
        if all(slot is not None for slot in self.slots[1:]):
            messagebox.showinfo("Slots Full", "All slots are already filled!")
            return

        deadline = int(deadline)
        profit = int(profit)

        if deadline > self.max_slots:
            messagebox.showerror("Deadline Exceeded", f"Deadline cannot exceed {self.max_slots}.")
            return

        if profit <= 0 or deadline <= 0:
            messagebox.showerror("Invalid Input", "Deadline and Profit must be positive.")
            return

        if job_id in self.jobs:
            messagebox.showerror("Duplicate Job", f"Job ID '{job_id}' already exists.")
            return

        self.jobs[job_id] = Job(job_id, deadline, profit)
        self.entry_job_id.delete(0, tk.END)
        self.entry_deadline.delete(0, tk.END)
        self.entry_profit.delete(0, tk.END)

        self.auto_schedule()

    def auto_schedule(self):
        jobs_sorted = sorted(self.jobs.values(), key=lambda x: x.profit, reverse=True)

        for job in jobs_sorted:
            if any(job == slot for slot in self.slots):
                continue  # Already assigned

            for slot in range(job.deadline, 0, -1):
                if self.slots[slot] is None:
                    self.slots[slot] = job
                    break

        self.draw_visualization()

    def on_canvas_click(self, event):
        x, y = event.x, event.y
        box_width = 120
        box_height = 70
        x_start = 30
        y_start = 60

        for i in range(1, len(self.slots)):
            x1 = x_start + (i - 1) * box_width
            y1 = y_start
            x2 = x1 + box_width
            y2 = y1 + box_height

            if x1 <= x <= x2 and y1 <= y <= y2:
                if self.slots[i] is not None:
                    job = self.slots[i]
                    if messagebox.askyesno("Delete Task", f"Delete Job '{job.job_id}' from Slot {i}?"):
                        self.slots[i] = None
                        self.draw_visualization()
                break

    def create_rounded_rect(self, canvas, x1, y1, x2, y2, radius=15, **kwargs):
        points = [
            x1 + radius, y1,
            x2 - radius, y1,
            x2, y1,
            x2, y1 + radius,
            x2, y2 - radius,
            x2, y2,
            x2 - radius, y2,
            x1 + radius, y2,
            x1, y2,
            x1, y2 - radius,
            x1, y1 + radius,
            x1, y1,
        ]
        return canvas.create_polygon(points, smooth=True, **kwargs)

    def draw_visualization(self):
        self.canvas.delete("all")
        box_width = 120
        box_height = 70
        x_start = 30
        y_start = 60

        for i in range(1, len(self.slots)):
            x1 = x_start + (i - 1) * box_width
            y1 = y_start
            x2 = x1 + box_width
            y2 = y1 + box_height

            self.create_rounded_rect(self.canvas, x1, y1, x2, y2, radius=15,
                                     fill="#D6EAF8", outline="#95A5A6", width=3)

            label_bar_height = 25
            self.create_rounded_rect(self.canvas, x1 + 5, y1 + 5, x2 - 5, y1 + label_bar_height,
                                     radius=10, fill="#5DADE2", outline="")

            self.canvas.create_text((x1 + x2) // 2, y1 + label_bar_height // 2 + 2,
                                    text=f"Slot {i}", font=self.slot_label_font, fill="white")

            job = self.slots[i]
            if job is not None:
                if job.job_id not in self.job_to_color:
                    self.job_to_color[job.job_id] = self.job_colors[len(self.job_to_color) % len(self.job_colors)]
                color = self.job_to_color[job.job_id]

                self.create_rounded_rect(self.canvas, x1 + 10, y1 + label_bar_height + 5,
                                         x2 - 10, y2 - 10, radius=12,
                                         fill=color, outline="#555555", width=2)

                self.canvas.create_text((x1 + x2) // 2, y1 + label_bar_height + 25,
                                        text=f"Job {job.job_id}", font=self.job_font_title)
                self.canvas.create_text((x1 + x2) // 2, y1 + label_bar_height + 45,
                                        text=f"₹{job.profit}", font=self.job_font_profit)
                self.canvas.create_text((x1 + x2) // 2, y1 + label_bar_height + 60,
                                        text=f"Deadline: {job.deadline}", font=self.job_font_deadline)
            else:
                self.canvas.create_text((x1 + x2) // 2, (y1 + y2) // 2,
                                        text="Empty", font=self.empty_font, fill="#7F8C8D")

        total_profit = sum(job.profit for job in self.slots if job is not None)
        self.profit_label.config(text=f"Total Profit: ₹{total_profit}")

def main():
    root = tk.Tk()
    app = TaskSchedulerApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
