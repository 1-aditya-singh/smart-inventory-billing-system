import customtkinter as ctk
from tkinter import messagebox

from models.customer import Customer


class CustomersFrame(ctk.CTkFrame):

    def __init__(self, parent):
        super().__init__(
            parent,
            corner_radius=0,
            fg_color="transparent"
        )

        self.selected_customer_id = None

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        self.create_header()
        self.create_form()
        self.create_customer_table()

        self.load_customers()

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

        title = ctk.CTkLabel(
            header,
            text="Customers",
            font=ctk.CTkFont(
                size=28,
                weight="bold"
            )
        )

        title.pack(anchor="w")

        subtitle = ctk.CTkLabel(
            header,
            text="Manage customer information and contact details",
            text_color="gray"
        )

        subtitle.pack(
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

        # ------------------------------------------
        # Name
        # ------------------------------------------

        ctk.CTkLabel(
            self.form_frame,
            text="Customer Name"
        ).grid(
            row=0,
            column=0,
            sticky="w",
            padx=15,
            pady=(15, 5)
        )

        self.name_entry = ctk.CTkEntry(
            self.form_frame,
            placeholder_text="Customer name"
        )

        self.name_entry.grid(
            row=1,
            column=0,
            sticky="ew",
            padx=15,
            pady=(0, 15)
        )

        # ------------------------------------------
        # Contact
        # ------------------------------------------

        ctk.CTkLabel(
            self.form_frame,
            text="Contact"
        ).grid(
            row=0,
            column=1,
            sticky="w",
            padx=15,
            pady=(15, 5)
        )

        self.contact_entry = ctk.CTkEntry(
            self.form_frame,
            placeholder_text="9876543210"
        )

        self.contact_entry.grid(
            row=1,
            column=1,
            sticky="ew",
            padx=15,
            pady=(0, 15)
        )

        # ------------------------------------------
        # Email
        # ------------------------------------------

        ctk.CTkLabel(
            self.form_frame,
            text="Email"
        ).grid(
            row=0,
            column=2,
            sticky="w",
            padx=15,
            pady=(15, 5)
        )

        self.email_entry = ctk.CTkEntry(
            self.form_frame,
            placeholder_text="customer@example.com"
        )

        self.email_entry.grid(
            row=1,
            column=2,
            sticky="ew",
            padx=15,
            pady=(0, 15)
        )

        # ------------------------------------------
        # Address
        # ------------------------------------------

        ctk.CTkLabel(
            self.form_frame,
            text="Address"
        ).grid(
            row=0,
            column=3,
            sticky="w",
            padx=15,
            pady=(15, 5)
        )

        self.address_entry = ctk.CTkEntry(
            self.form_frame,
            placeholder_text="Customer address"
        )

        self.address_entry.grid(
            row=1,
            column=3,
            sticky="ew",
            padx=15,
            pady=(0, 15)
        )

        # ------------------------------------------
        # Buttons
        # ------------------------------------------

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
            text="Add Customer",
            width=130,
            command=self.save_customer
        )

        self.save_button.pack(
            side="left",
            padx=5
        )

        clear_button = ctk.CTkButton(
            button_frame,
            text="Clear",
            width=100,
            command=self.clear_form
        )

        clear_button.pack(
            side="left",
            padx=5
        )

    # ==================================================
    # CUSTOMER TABLE
    # ==================================================

    def create_customer_table(self):

        table_frame = ctk.CTkFrame(
            self,
            corner_radius=12
        )

        table_frame.grid(
            row=2,
            column=0,
            sticky="nsew",
            padx=25,
            pady=(10, 25)
        )

        table_frame.grid_columnconfigure(
            0,
            weight=1
        )

        table_frame.grid_rowconfigure(
            1,
            weight=1
        )

        # ------------------------------------------
        # Search
        # ------------------------------------------

        search_frame = ctk.CTkFrame(
            table_frame,
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
            placeholder_text="Search customers..."
        )

        self.search_entry.pack(
            side="left",
            fill="x",
            expand=True,
            padx=(0, 10)
        )

        search_button = ctk.CTkButton(
            search_frame,
            text="Search",
            width=100,
            command=self.search_customers
        )

        search_button.pack(
            side="left"
        )

        refresh_button = ctk.CTkButton(
            search_frame,
            text="Refresh",
            width=100,
            command=self.load_customers
        )

        refresh_button.pack(
            side="left",
            padx=(10, 0)
        )

        # ------------------------------------------
        # Table
        # ------------------------------------------

        self.table = ctk.CTkScrollableFrame(
            table_frame
        )

        self.table.grid(
            row=1,
            column=0,
            sticky="nsew",
            padx=15,
            pady=(0, 15)
        )

        for column in range(6):
            self.table.grid_columnconfigure(
                column,
                weight=1
            )

    # ==================================================
    # LOAD CUSTOMERS
    # ==================================================

    def load_customers(self):

        try:

            customers = Customer.get_all()

            self.display_customers(
                customers
            )

        except Exception as error:

            messagebox.showerror(
                "Error",
                f"Unable to load customers:\n{error}"
            )

    # ==================================================
    # DISPLAY CUSTOMERS
    # ==================================================

    def display_customers(self, customers):

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

            label = ctk.CTkLabel(
                self.table,
                text=header,
                font=ctk.CTkFont(
                    size=13,
                    weight="bold"
                )
            )

            label.grid(
                row=0,
                column=column,
                padx=8,
                pady=8,
                sticky="w"
            )

        for row_index, customer in enumerate(
            customers,
            start=1
        ):

            customer_id = customer[0]
            name = customer[1]
            contact = customer[2]
            email = customer[3] or "-"
            address = customer[4] or "-"

            values = [
                customer_id,
                name,
                contact,
                email,
                address
            ]

            for column, value in enumerate(values):

                label = ctk.CTkLabel(
                    self.table,
                    text=str(value)
                )

                label.grid(
                    row=row_index,
                    column=column,
                    padx=8,
                    pady=6,
                    sticky="w"
                )

            action_frame = ctk.CTkFrame(
                self.table,
                fg_color="transparent"
            )

            action_frame.grid(
                row=row_index,
                column=5,
                padx=5,
                pady=3
            )

            edit_button = ctk.CTkButton(
                action_frame,
                text="Edit",
                width=55,
                height=28,
                command=lambda c=customer:
                    self.edit_customer(c)
            )

            edit_button.pack(
                side="left",
                padx=2
            )

            delete_button = ctk.CTkButton(
                action_frame,
                text="Delete",
                width=60,
                height=28,
                command=lambda cid=customer_id:
                    self.delete_customer(cid)
            )

            delete_button.pack(
                side="left",
                padx=2
            )

    # ==================================================
    # SAVE CUSTOMER
    # ==================================================

    def save_customer(self):

        try:

            name = self.name_entry.get().strip()
            contact = self.contact_entry.get().strip()
            email = self.email_entry.get().strip()
            address = self.address_entry.get().strip()

            if not name:
                raise ValueError(
                    "Customer name is required."
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

            if self.selected_customer_id is None:

                Customer.create(
                    name,
                    contact,
                    email or None,
                    address or None
                )

                messagebox.showinfo(
                    "Success",
                    "Customer added successfully."
                )

            else:

                Customer.update(
                    self.selected_customer_id,
                    name,
                    contact,
                    email or None,
                    address or None
                )

                messagebox.showinfo(
                    "Success",
                    "Customer updated successfully."
                )

            self.clear_form()
            self.load_customers()

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

    def search_customers(self):

        search_term = self.search_entry.get().strip()

        if not search_term:

            self.load_customers()
            return

        try:

            customers = Customer.get_all()

            filtered_customers = []

            for customer in customers:

                name = str(customer[1]).lower()
                contact = str(customer[2]).lower()
                email = str(customer[3] or "").lower()

                if (
                    search_term.lower() in name
                    or search_term.lower() in contact
                    or search_term.lower() in email
                ):
                    filtered_customers.append(
                        customer
                    )

            self.display_customers(
                filtered_customers
            )

        except Exception as error:

            messagebox.showerror(
                "Search Failed",
                str(error)
            )

    # ==================================================
    # EDIT CUSTOMER
    # ==================================================

    def edit_customer(self, customer):

        self.selected_customer_id = customer[0]

        self.name_entry.delete(0, "end")
        self.name_entry.insert(
            0,
            customer[1]
        )

        self.contact_entry.delete(0, "end")
        self.contact_entry.insert(
            0,
            customer[2]
        )

        self.email_entry.delete(0, "end")
        self.email_entry.insert(
            0,
            customer[3] or ""
        )

        self.address_entry.delete(0, "end")
        self.address_entry.insert(
            0,
            customer[4] or ""
        )

        self.save_button.configure(
            text="Update Customer"
        )

    # ==================================================
    # DELETE CUSTOMER
    # ==================================================

    def delete_customer(self, customer_id):

        confirmation = messagebox.askyesno(
            "Confirm Delete",
            "Are you sure you want to delete this customer?"
        )

        if not confirmation:
            return

        try:

            deleted = Customer.delete(
                customer_id
            )

            if deleted:

                messagebox.showinfo(
                    "Success",
                    "Customer deleted successfully."
                )

            self.load_customers()

        except Exception as error:

            messagebox.showerror(
                "Delete Failed",
                str(error)
            )

    # ==================================================
    # CLEAR FORM
    # ==================================================

    def clear_form(self):

        self.selected_customer_id = None

        entries = [
            self.name_entry,
            self.contact_entry,
            self.email_entry,
            self.address_entry
        ]

        for entry in entries:
            entry.delete(0, "end")

        self.save_button.configure(
            text="Add Customer"
        )