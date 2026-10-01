import customtkinter as ctk
from tkinter import messagebox

from models.supplier import Supplier


class SuppliersFrame(ctk.CTkFrame):

    def __init__(self, parent):
        super().__init__(
            parent,
            corner_radius=0,
            fg_color="transparent"
        )

        self.selected_supplier_id = None

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        self.create_header()
        self.create_form()
        self.create_table()

        self.load_suppliers()

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
            text="Suppliers",
            font=ctk.CTkFont(
                size=28,
                weight="bold"
            )
        ).pack(anchor="w")

        ctk.CTkLabel(
            header,
            text="Manage supplier information and contact details",
            text_color="gray"
        ).pack(
            anchor="w",
            pady=(3, 0)
        )

    # ==================================================
    # FORM
    # ==================================================

    def create_form(self):

        self.form_frame = ctk.CTkFrame(
            self,
            corner_radius=12
        )

        self.form_frame.grid(
            row=1,
            column=0,
            sticky="ew",
            padx=25,
            pady=10
        )

        for column in range(4):
            self.form_frame.grid_columnconfigure(
                column,
                weight=1
            )

        fields = [
            ("Supplier Name", "name_entry", "Supplier name"),
            ("Contact", "contact_entry", "9876543210"),
            ("Email", "email_entry", "supplier@example.com"),
            ("Address", "address_entry", "Supplier address")
        ]

        for column, (label_text, attribute, placeholder) in enumerate(fields):

            ctk.CTkLabel(
                self.form_frame,
                text=label_text
            ).grid(
                row=0,
                column=column,
                sticky="w",
                padx=15,
                pady=(15, 5)
            )

            entry = ctk.CTkEntry(
                self.form_frame,
                placeholder_text=placeholder
            )

            entry.grid(
                row=1,
                column=column,
                sticky="ew",
                padx=15,
                pady=(0, 15)
            )

            setattr(
                self,
                attribute,
                entry
            )

        button_frame = ctk.CTkFrame(
            self.form_frame,
            fg_color="transparent"
        )

        button_frame.grid(
            row=2,
            column=0,
            columnspan=4,
            sticky="e",
            padx=15,
            pady=(0, 15)
        )

        self.save_button = ctk.CTkButton(
            button_frame,
            text="Add Supplier",
            width=130,
            command=self.save_supplier
        )

        self.save_button.pack(
            side="left",
            padx=5
        )

        ctk.CTkButton(
            button_frame,
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
            placeholder_text="Search suppliers..."
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
            command=self.search_suppliers
        ).pack(side="left")

        ctk.CTkButton(
            search_frame,
            text="Refresh",
            width=100,
            command=self.load_suppliers
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

    def load_suppliers(self):

        try:
            suppliers = Supplier.get_all()
            self.display_suppliers(suppliers)

        except Exception as error:
            messagebox.showerror(
                "Error",
                f"Unable to load suppliers:\n{error}"
            )

    # ==================================================
    # DISPLAY
    # ==================================================

    def display_suppliers(self, suppliers):

        for widget in self.table.winfo_children():
            widget.destroy()

        headers = [
            "ID",
            "Name",
            "Contact",
            "Email",
            "Address",
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

        for row, supplier in enumerate(
            suppliers,
            start=1
        ):

            supplier_id = supplier[0]

            values = [
                supplier[0],
                supplier[1],
                supplier[2],
                supplier[3] or "-",
                supplier[4] or "-"
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
                column=5
            )

            ctk.CTkButton(
                actions,
                text="Edit",
                width=55,
                height=28,
                command=lambda s=supplier:
                    self.edit_supplier(s)
            ).pack(
                side="left",
                padx=2
            )

            ctk.CTkButton(
                actions,
                text="Delete",
                width=60,
                height=28,
                command=lambda sid=supplier_id:
                    self.delete_supplier(sid)
            ).pack(
                side="left",
                padx=2
            )

    # ==================================================
    # SAVE
    # ==================================================

    def save_supplier(self):

        try:

            name = self.name_entry.get().strip()
            contact = self.contact_entry.get().strip()
            email = self.email_entry.get().strip()
            address = self.address_entry.get().strip()

            if not name:
                raise ValueError(
                    "Supplier name is required."
                )

            if not contact:
                raise ValueError(
                    "Contact number is required."
                )

            if not contact.isdigit():
                raise ValueError(
                    "Contact must contain only numbers."
                )

            if len(contact) < 10 or len(contact) > 15:
                raise ValueError(
                    "Contact must contain 10 to 15 digits."
                )

            if self.selected_supplier_id is None:

                Supplier.create(
                    name,
                    contact,
                    email or None,
                    address or None
                )

                messagebox.showinfo(
                    "Success",
                    "Supplier added successfully."
                )

            else:

                Supplier.update(
                    self.selected_supplier_id,
                    name,
                    contact,
                    email or None,
                    address or None
                )

                messagebox.showinfo(
                    "Success",
                    "Supplier updated successfully."
                )

            self.clear_form()
            self.load_suppliers()

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

    def search_suppliers(self):

        term = self.search_entry.get().strip().lower()

        if not term:
            self.load_suppliers()
            return

        try:

            suppliers = Supplier.get_all()

            filtered = []

            for supplier in suppliers:

                searchable = " ".join(
                    [
                        str(supplier[1]),
                        str(supplier[2]),
                        str(supplier[3] or "")
                    ]
                ).lower()

                if term in searchable:
                    filtered.append(supplier)

            self.display_suppliers(filtered)

        except Exception as error:

            messagebox.showerror(
                "Search Failed",
                str(error)
            )

    # ==================================================
    # EDIT
    # ==================================================

    def edit_supplier(self, supplier):

        self.selected_supplier_id = supplier[0]

        self.name_entry.delete(0, "end")
        self.name_entry.insert(0, supplier[1])

        self.contact_entry.delete(0, "end")
        self.contact_entry.insert(0, supplier[2])

        self.email_entry.delete(0, "end")
        self.email_entry.insert(
            0,
            supplier[3] or ""
        )

        self.address_entry.delete(0, "end")
        self.address_entry.insert(
            0,
            supplier[4] or ""
        )

        self.save_button.configure(
            text="Update Supplier"
        )

    # ==================================================
    # DELETE
    # ==================================================

    def delete_supplier(self, supplier_id):

        if not messagebox.askyesno(
            "Confirm Delete",
            "Are you sure you want to delete this supplier?"
        ):
            return

        try:

            Supplier.delete(supplier_id)

            messagebox.showinfo(
                "Success",
                "Supplier deleted successfully."
            )

            self.load_suppliers()

        except Exception as error:

            messagebox.showerror(
                "Delete Failed",
                str(error)
            )

    # ==================================================
    # CLEAR
    # ==================================================

    def clear_form(self):

        self.selected_supplier_id = None

        for entry in [
            self.name_entry,
            self.contact_entry,
            self.email_entry,
            self.address_entry
        ]:
            entry.delete(0, "end")

        self.save_button.configure(
            text="Add Supplier"
        )