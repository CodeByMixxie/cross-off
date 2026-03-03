import customtkinter as ctk
import database
import config


class ToDoApp:
    def __init__(self):
        ctk.set_appearance_mode("Light")

        self.app = ctk.CTk()
        self.app.title("𐔌   .  ⋮ Cross Off  .ᐟ  ֹ   ₊ ꒱")
        self.app.geometry(config.WINDOW_SIZE)
        self.app.resizable(False, False)

        database.create_table()

        self.create_widgets()
        self.load_tasks()
        self.apply_theme("Light")

    # ---------------- UI SETUP ---------------- #

    def create_widgets(self):
        # Title
        self.title_label = ctk.CTkLabel(
            self.app,
            text="My Tasks ──.☘︎ ݁˖",
            font=config.TITLE_FONT,
            corner_radius=10
        )
        self.title_label.pack(pady=20, padx=40, fill="x")

        # Theme Button
        self.theme_button = ctk.CTkButton(
            self.app,
            text="🌙",
            width=40,
            corner_radius=20,
            command=self.toggle_theme
        )
        self.theme_button.place(x=370, y=20)

        # Task Frame
        self.task_frame = ctk.CTkFrame(
            self.app,
            corner_radius=20
        )
        self.task_frame.pack(padx=20, pady=10, fill="both", expand=True)

        # Entry
        self.task_entry = ctk.CTkEntry(
            self.app,
            placeholder_text="Type a task here… ✏️",
            width=320,
            corner_radius=15
        )
        self.task_entry.pack(pady=10)
        self.task_entry.focus()
        self.task_entry.bind("<Return>", lambda event: self.add_task())

        # Add Button
        self.add_button = ctk.CTkButton(
            self.app,
            text="──Add Task.✦",
            corner_radius=20,
            command=self.add_task
        )
        self.add_button.pack(pady=20)

    # ---------------- THEME SYSTEM ---------------- #

    def apply_theme(self, mode):
        if mode == "Light":
            self.app.configure(fg_color=config.LIGHT_BACKGROUND)
            self.title_label.configure(
                fg_color=config.LIGHT_HEADER,
                text_color=config.LIGHT_TEXT
            )
            self.add_button.configure(
                fg_color=config.LIGHT_BUTTON,
                text_color=config.LIGHT_TEXT
            )
            self.task_frame.configure(
                fg_color=config.LIGHT_FRAME
            )
        else:
            self.app.configure(fg_color=config.DARK_BACKGROUND)
            self.title_label.configure(
                fg_color=config.DARK_HEADER,
                text_color=config.DARK_TEXT
            )
            self.add_button.configure(
                fg_color=config.DARK_BUTTON,
                text_color=config.DARK_TEXT
            )
            self.task_frame.configure(
                fg_color=config.DARK_FRAME
            )

    def toggle_theme(self):
        current = ctk.get_appearance_mode()

        if current == "Light":
            ctk.set_appearance_mode("Dark")
            self.apply_theme("Dark")
            self.theme_button.configure(text="☀️")
        else:
            ctk.set_appearance_mode("Light")
            self.apply_theme("Light")
            self.theme_button.configure(text="🌙")

    # ---------------- ANIMATION ---------------- #

    def pop_animation(self, widget):
        widget.configure(font=(config.TASK_FONT[0], config.TASK_FONT[1] + 2))
        widget.after(100, lambda: widget.configure(font=config.TASK_FONT))

    def scribble_text(self, text):
        return "".join(char + "̶" for char in text)

    # ---------------- TASK LOGIC ---------------- #

    def toggle_and_save(self, checkbox, checked, task_id):
        self.pop_animation(checkbox)

        if checked.get():
            checkbox.configure(
                text=self.scribble_text(checkbox.cget("text").replace("̶", "")),
                text_color=config.COMPLETED_COLOR
            )
            database.update_task_status(task_id, 1)
        else:
            clean_text = checkbox.cget("text").replace("̶", "")
            checkbox.configure(
                text=clean_text,
                text_color=config.LIGHT_TEXT if ctk.get_appearance_mode() == "Light"
                else config.DARK_TEXT
            )
            database.update_task_status(task_id, 0)

    def delete_task_ui(self, checkbox, task_id):
        try:
            checkbox.configure(command=None)
            checkbox._variable = None
            checkbox.destroy()
        except:
            pass

        database.delete_task(task_id)

    def add_task(self):
        task_text = self.task_entry.get().strip()

        if not task_text:
            return

        database.add_task_db(task_text)
        tasks = database.get_tasks()
        task_id = tasks[-1][0]

        checked = ctk.BooleanVar()

        checkbox = ctk.CTkCheckBox(
            self.task_frame,
            text=task_text,
            variable=checked,
            font=config.TASK_FONT
        )

        checkbox.pack(anchor="w", padx=20, pady=5)

        checkbox.bind(
            "<Button-3>",
            lambda event, cb=checkbox, tid=task_id: self.delete_task_ui(cb, tid)
        )

        checkbox.configure(
            command=lambda: self.toggle_and_save(checkbox, checked, task_id)
        )

        self.task_entry.delete(0, "end")

    def load_tasks(self):
        tasks = database.get_tasks()

        for task_id, text, completed in tasks:
            checked = ctk.BooleanVar(value=bool(completed))

            checkbox = ctk.CTkCheckBox(
                self.task_frame,
                text=text,
                variable=checked,
                font=config.TASK_FONT
            )

            checkbox.pack(anchor="w", padx=20, pady=5)

            checkbox.bind(
                "<Button-3>",
                lambda event, cb=checkbox, tid=task_id: self.delete_task_ui(cb, tid)
            )

            if completed:
                checkbox.configure(
                    text=self.scribble_text(text),
                    text_color=config.COMPLETED_COLOR
                )

            checkbox.configure(
                command=lambda cb=checkbox, var=checked, tid=task_id:
                self.toggle_and_save(cb, var, tid)
            )

    # ---------------- RUN ---------------- #

    def run(self):
        self.app.mainloop()


if __name__ == "__main__":
    app = ToDoApp()
    app.run()
