import customtkinter as ctk
from tkinter import messagebox

from models.category import Category


class CategoriesFrame(ctk.CTkFrame):

    def __init__(self, parent):
        super().__init__(
            parent,
            corner_radius=0,
            fg_color="transparent"
        )

        self.selected_category_id = None

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        self.create_header()
        self.create_form()
        self.create_table()

        self.load_categories()

    # ==================================================
    # HEADER
    # ==================================================

    def create_header(self):

        header = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )

        header.grid(
            row=0,
            column=0,
            sticky="ew",
            padx=25,
            pady=(20, 10)
        )

        ctk.CTkLabel(
            header,
            text="Categories",
            font=ctk.CTkFont(
                size=28,
                weight="bold"
            )
        ).pack(anchor="w")

        ctk.CTkLabel(
            header,
            text="Organize products into manageable categories",
            text_color="gray"
        ).pack(
            anchor="w",
            pady=(3, 0)
        )

    # ==================================================
    # FORM
    # ==================================================

    def create_form(self):

        frame = ctk.CTkFrame(
            self,
            corner_radius=12
        )

        frame.grid(
            row=1,
            column=0,
            sticky="ew",
            padx=25,
            pady=10
        )

        frame.grid_columnconfigure(
            0,
            weight=1
        )

        frame.grid_columnconfigure(
            1,
            weight=2
        )

        ctk.CTkLabel(
            frame,
            text="Category Name"
        ).grid(
            row=0,
            column=0,
            sticky="w",
            padx=15,
            pady=(15, 5)
        )

        self.name_entry = ctk.CTkEntry(
            frame,
            placeholder_text="Category name"
        )

        self.name_entry.grid(
            row=1,
            column=0,
            sticky="ew",
            padx=15,
            pady=(0, 15)
        )

        ctk.CTkLabel(
            frame,
            text="Description"
        ).grid(
            row=0,
            column=1,
            sticky="w",
            padx=15,
            pady=(15, 5)
        )

        self.description_entry = ctk.CTkEntry(
            frame,
            placeholder_text="Category description"
        )

        self.description_entry.grid(
            row=1,
            column=1,
            sticky="ew",
            padx=15,
            pady=(0, 15)
        )

        buttons = ctk.CTkFrame(
            frame,
            fg_color="transparent"
        )

        buttons.grid(
            row=2,
            column=0,
            columnspan=2,
            sticky="e",
            padx=15,
            pady=(0, 15)
        )

        self.save_button = ctk.CTkButton(
            buttons,
            text="Add Category",
            width=130,
            command=self.save_category
        )

        self.save_button.pack(
            side="left",
            padx=5
        )

        ctk.CTkButton(
            buttons,
            text="Clear",
            width=100,
            command=self.clear_form
        ).pack(
            side="left",
            padx=5
        )

    # ==================================================
    # TABLE
    # ==================================================

    def create_table(self):

        frame = ctk.CTkFrame(
            self,
            corner_radius=12
        )

        frame.grid(
            row=2,
            column=0,
            sticky="nsew",
            padx=25,
            pady=(10, 25)
        )

        frame.grid_columnconfigure(0, weight=1)
        frame.grid_rowconfigure(1, weight=1)

        search_frame = ctk.CTkFrame(
            frame,
            fg_color="transparent"
        )

        search_frame.grid(
            row=0,
            column=0,
            sticky="ew",
            padx=15,
            pady=15
        )

        self.search_entry = ctk.CTkEntry(
            search_frame,
            placeholder_text="Search categories..."
        )

        self.search_entry.pack(
            side="left",
            fill="x",
            expand=True,
            padx=(0, 10)
        )

        ctk.CTkButton(
            search_frame,
            text="Search",
            width=100,
            command=self.search_categories
        ).pack(side="left")

        ctk.CTkButton(
            search_frame,
            text="Refresh",
            width=100,
            command=self.load_categories
        ).pack(
            side="left",
            padx=(10, 0)
        )

        self.table = ctk.CTkScrollableFrame(frame)

        self.table.grid(
            row=1,
            column=0,
            sticky="nsew",
            padx=15,
            pady=(0, 15)
        )

    # ==================================================
    # LOAD
    # ==================================================

    def load_categories(self):

        try:

            categories = Category.get_all()

            self.display_categories(
                categories
            )

        except Exception as error:

            messagebox.showerror(
                "Error",
                str(error)
            )

    # ==================================================
    # DISPLAY
    # ==================================================

    def display_categories(self, categories):

        for widget in self.table.winfo_children():
            widget.destroy()

        headers = [
            "ID",
            "Category",
            "Description",
            "Actions"
        ]

        for column, header in enumerate(headers):

            ctk.CTkLabel(
                self.table,
                text=header,
                font=ctk.CTkFont(
                    size=13,
                    weight="bold"
                )
            ).grid(
                row=0,
                column=column,
                padx=10,
                pady=8,
                sticky="w"
            )

        for row, category in enumerate(
            categories,
            start=1
        ):

            category_id = category[0]

            values = [
                category[0],
                category[1],
                category[2] or "-"
            ]

            for column, value in enumerate(values):

                ctk.CTkLabel(
                    self.table,
                    text=str(value)
                ).grid(
                    row=row,
                    column=column,
                    padx=10,
                    pady=6,
                    sticky="w"
                )

            actions = ctk.CTkFrame(
                self.table,
                fg_color="transparent"
            )

            actions.grid(
                row=row,
                column=3
            )

            ctk.CTkButton(
                actions,
                text="Edit",
                width=55,
                height=28,
                command=lambda c=category:
                    self.edit_category(c)
            ).pack(
                side="left",
                padx=2
            )

            ctk.CTkButton(
                actions,
                text="Delete",
                width=60,
                height=28,
                command=lambda cid=category_id:
                    self.delete_category(cid)
            ).pack(
                side="left",
                padx=2
            )

    # ==================================================
    # SAVE
    # ==================================================

    def save_category(self):

        try:

            name = self.name_entry.get().strip()
            description = (
                self.description_entry
                .get()
                .strip()
            )

            if not name:
                raise ValueError(
                    "Category name is required."
                )

            if self.selected_category_id is None:

                Category.create(
                    name,
                    description or None
                )

                messagebox.showinfo(
                    "Success",
                    "Category added successfully."
                )

            else:

                Category.update(
                    self.selected_category_id,
                    name,
                    description or None
                )

                messagebox.showinfo(
                    "Success",
                    "Category updated successfully."
                )

            self.clear_form()
            self.load_categories()

        except ValueError as error:

            messagebox.showwarning(
                "Invalid Input",
                str(error)
            )

        except Exception as error:

            messagebox.showerror(
                "Database Error",
                str(error)
            )

    # ==================================================
    # SEARCH
    # ==================================================

    def search_categories(self):

        term = self.search_entry.get().strip().lower()

        if not term:
            self.load_categories()
            return

        try:

            categories = Category.get_all()

            filtered = []

            for category in categories:

                name = str(category[1]).lower()
                description = str(
                    category[2] or ""
                ).lower()

                if (
                    term in name
                    or term in description
                ):
                    filtered.append(category)

            self.display_categories(
                filtered
            )

        except Exception as error:

            messagebox.showerror(
                "Search Failed",
                str(error)
            )

    # ==================================================
    # EDIT
    # ==================================================

    def edit_category(self, category):

        self.selected_category_id = category[0]

        self.name_entry.delete(0, "end")
        self.name_entry.insert(
            0,
            category[1]
        )

        self.description_entry.delete(
            0,
            "end"
        )

        self.description_entry.insert(
            0,
            category[2] or ""
        )

        self.save_button.configure(
            text="Update Category"
        )

    # ==================================================
    # DELETE
    # ==================================================

    def delete_category(self, category_id):

        if not messagebox.askyesno(
            "Confirm Delete",
            "Are you sure you want to delete this category?"
        ):
            return

        try:

            Category.delete(category_id)

            messagebox.showinfo(
                "Success",
                "Category deleted successfully."
            )

            self.load_categories()

        except Exception as error:

            messagebox.showerror(
                "Delete Failed",
                str(error)
            )

    # ==================================================
    # CLEAR
    # ==================================================

    def clear_form(self):

        self.selected_category_id = None

        self.name_entry.delete(
            0,
            "end"
        )

        self.description_entry.delete(
            0,
            "end"
        )

        self.save_button.configure(
            text="Add Category"
        )