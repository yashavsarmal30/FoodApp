from customtkinter import CTkFrame, CTkButton

class Page(CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.master = master
        self.add_back_button()

    def add_back_button(self):
        back_button = CTkButton(
            self,
            text="← Back",
            font=("Arial", 14),
            fg_color="transparent",
            text_color="#2d6a4f",
            hover_color="#E8F5E9",
            width=100,
            command=self.master.show_previous_page
        )
        back_button.pack(anchor="w", padx=20, pady=10)

    def show(self):
        self.pack(fill="both", expand=True)

    def hide(self):
        self.pack_forget() 