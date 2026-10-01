import customtkinter as ctk
from tkinter import messagebox

from models.product import Product
from models.category import Category
from models.supplier import Supplier


class ProductsFrame(ctk.CTkFrame):

    def __init__(self, parent):
        super().__init__(
            parent,
            corner_radius=0,
            fg_color="transparent"
        )

        self.selected_product_id = None

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        self.create_header()
        self.create_form()
        self.create_product_table()

        self.load_products()

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
            text="Products & Inventory",
            font=ctk.CTkFont(
                size=28,
                weight="bold"
            )
        )

        title.pack(anchor="w")

        subtitle = ctk.CTkLabel(
            header,
            text="Manage products, pricing and stock levels",
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

        # Name
        ctk.CTkLabel(
            self.form_frame,
            text="Product Name"
        ).grid(
            row=0,
            column=0,
            sticky="w",
            padx=15,
            pady=(15, 5)
        )

        self.name_entry = ctk.CTkEntry(
            self.form_frame,
            placeholder_text="Product name"
        )

        self.name_entry.grid(
            row=1,
            column=0,
            sticky="ew",
            padx=15,
            pady=(0, 10)
        )

        # SKU
        ctk.CTkLabel(
            self.form_frame,
            text="SKU"
        ).grid(
            row=0,
            column=1,
            sticky="w",
            padx=15,
            pady=(15, 5)
        )

        self.sku_entry = ctk.CTkEntry(
            self.form_frame,
            placeholder_text="SKU-001"
        )

        self.sku_entry.grid(
            row=1,
            column=1,
            sticky="ew",
            padx=15,
            pady=(0, 10)
        )

        # Category
        ctk.CTkLabel(
            self.form_frame,
            text="Category"
        ).grid(
            row=0,
            column=2,
            sticky="w",
            padx=15,
            pady=(15, 5)
        )

        self.category_combo = ctk.CTkComboBox(
            self.form_frame,
            values=["Select Category"]
        )

        self.category_combo.grid(
            row=1,
            column=2,
            sticky="ew",
            padx=15,
            pady=(0, 10)
        )

        # Supplier
        ctk.CTkLabel(
            self.form_frame,
            text="Supplier"
        ).grid(
            row=0,
            column=3,
            sticky="w",
            padx=15,
            pady=(15, 5)
        )

        self.supplier_combo = ctk.CTkComboBox(
            self.form_frame,
            values=["Select Supplier"]
        )

        self.supplier_combo.grid(
            row=1,
            column=3,
            sticky="ew",
            padx=15,
            pady=(0, 10)
        )

        # Price
        ctk.CTkLabel(
            self.form_frame,
            text="Selling Price"
        ).grid(
            row=2,
            column=0,
            sticky="w",
            padx=15,
            pady=(5, 5)
        )

        self.price_entry = ctk.CTkEntry(
            self.form_frame,
            placeholder_text="0.00"
        )

        self.price_entry.grid(
            row=3,
            column=0,
            sticky="ew",
            padx=15,
            pady=(0, 10)
        )

        # Cost Price
        ctk.CTkLabel(
            self.form_frame,
            text="Cost Price"
        ).grid(
            row=2,
            column=1,
            sticky="w",
            padx=15,
            pady=(5, 5)
        )

        self.cost_price_entry = ctk.CTkEntry(
            self.form_frame,
            placeholder_text="0.00"
        )

        self.cost_price_entry.grid(
            row=3,
            column=1,
            sticky="ew",
            padx=15,
            pady=(0, 10)
        )

        # Quantity
        ctk.CTkLabel(
            self.form_frame,
            text="Quantity"
        ).grid(
            row=2,
            column=2,
            sticky="w",
            padx=15,
            pady=(5, 5)
        )

        self.quantity_entry = ctk.CTkEntry(
            self.form_frame,
            placeholder_text="0"
        )

        self.quantity_entry.grid(
            row=3,
            column=2,
            sticky="ew",
            padx=15,
            pady=(0, 10)
        )

        # Reorder Level
        ctk.CTkLabel(
            self.form_frame,
            text="Reorder Level"
        ).grid(
            row=2,
            column=3,
            sticky="w",
            padx=15,
            pady=(5, 5)
        )

        self.reorder_entry = ctk.CTkEntry(
            self.form_frame,
            placeholder_text="5"
        )

        self.reorder_entry.grid(
            row=3,
            column=3,
            sticky="ew",
            padx=15,
            pady=(0, 10)
        )

        # Description
        ctk.CTkLabel(
            self.form_frame,
            text="Description"
        ).grid(
            row=4,
            column=0,
            sticky="w",
            padx=15,
            pady=(5, 5)
        )

        self.description_entry = ctk.CTkEntry(
            self.form_frame,
            placeholder_text="Product description"
        )

        self.description_entry.grid(
            row=5,
            column=0,
            columnspan=2,
            sticky="ew",
            padx=15,
            pady=(0, 15)
        )

        # Buttons
        button_frame = ctk.CTkFrame(
            self.form_frame,
            fg_color="transparent"
        )

        button_frame.grid(
            row=5,
            column=2,
            columnspan=2,
            sticky="e",
            padx=15,
            pady=(0, 15)
        )

        self.save_button = ctk.CTkButton(
            button_frame,
            text="Add Product",
            width=130,
            command=self.save_product
        )

        self.save_button.pack(
            side="left",
            padx=5
        )

        self.clear_button = ctk.CTkButton(
            button_frame,
            text="Clear",
            width=100,
            command=self.clear_form
        )

        self.clear_button.pack(
            side="left",
            padx=5
        )

        self.load_categories()
        self.load_suppliers()

    # ==================================================
    # TABLE
    # ==================================================

    def create_product_table(self):

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

        # Search
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
            placeholder_text="Search by product name or SKU..."
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
            command=self.search_products
        )

        search_button.pack(
            side="left"
        )

        refresh_button = ctk.CTkButton(
            search_frame,
            text="Refresh",
            width=100,
            command=self.load_products
        )

        refresh_button.pack(
            side="left",
            padx=(10, 0)
        )

        # Scrollable table
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

        for column in range(8):
            self.table.grid_columnconfigure(
                column,
                weight=1
            )

    # ==================================================
    # LOAD CATEGORIES
    # ==================================================

    def load_categories(self):

        try:
            categories = Category.get_all()

            self.category_map = {}

            values = []

            for category in categories:
                category_id = category[0]
                category_name = category[1]

                self.category_map[category_name] = category_id
                values.append(category_name)

            if not values:
                values = ["No Categories"]

            self.category_combo.configure(
                values=values
            )

            self.category_combo.set(
                values[0]
            )

        except Exception as error:

            messagebox.showerror(
                "Error",
                f"Unable to load categories:\n{error}"
            )

    # ==================================================
    # LOAD SUPPLIERS
    # ==================================================

    def load_suppliers(self):

        try:
            suppliers = Supplier.get_all()

            self.supplier_map = {}

            values = []

            for supplier in suppliers:
                supplier_id = supplier[0]
                supplier_name = supplier[1]

                self.supplier_map[supplier_name] = supplier_id
                values.append(supplier_name)

            if not values:
                values = ["No Suppliers"]

            self.supplier_combo.configure(
                values=values
            )

            self.supplier_combo.set(
                values[0]
            )

        except Exception as error:

            messagebox.showerror(
                "Error",
                f"Unable to load suppliers:\n{error}"
            )

    # ==================================================
    # SAVE PRODUCT
    # ==================================================

    def save_product(self):

        try:

            name = self.name_entry.get().strip()
            sku = self.sku_entry.get().strip()
            description = self.description_entry.get().strip()

            if not name:
                raise ValueError("Product name is required.")

            if not sku:
                raise ValueError("SKU is required.")

            price = float(self.price_entry.get())
            cost_price = float(self.cost_price_entry.get())
            quantity = int(self.quantity_entry.get())
            reorder_level = int(self.reorder_entry.get())

            category_name = self.category_combo.get()
            supplier_name = self.supplier_combo.get()

            category_id = self.category_map.get(
                category_name
            )

            supplier_id = self.supplier_map.get(
                supplier_name
            )

            if category_id is None:
                raise ValueError(
                    "Please select a valid category."
                )

            if supplier_id is None:
                raise ValueError(
                    "Please select a valid supplier."
                )

            if price < 0 or cost_price < 0:
                raise ValueError(
                    "Prices cannot be negative."
                )

            if quantity < 0:
                raise ValueError(
                    "Quantity cannot be negative."
                )

            if reorder_level < 0:
                raise ValueError(
                    "Reorder level cannot be negative."
                )

            if self.selected_product_id is None:

                Product.create(
                    name,
                    description,
                    category_id,
                    supplier_id,
                    sku,
                    price,
                    cost_price,
                    quantity,
                    reorder_level
                )

                messagebox.showinfo(
                    "Success",
                    "Product added successfully."
                )

            else:

                Product.update(
                    self.selected_product_id,
                    name,
                    description,
                    category_id,
                    supplier_id,
                    sku,
                    price,
                    cost_price,
                    quantity,
                    reorder_level
                )

                messagebox.showinfo(
                    "Success",
                    "Product updated successfully."
                )

            self.clear_form()
            self.load_products()

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
    # LOAD PRODUCTS
    # ==================================================

    def load_products(self):

        try:

            products = Product.get_all()

            self.display_products(products)

        except Exception as error:

            messagebox.showerror(
                "Error",
                f"Unable to load products:\n{error}"
            )

    # ==================================================
    # DISPLAY PRODUCTS
    # ==================================================

    def display_products(self, products):

        for widget in self.table.winfo_children():
            widget.destroy()

        headers = [
            "ID",
            "Product",
            "SKU",
            "Category",
            "Supplier",
            "Price",
            "Stock",
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

        for row_index, product in enumerate(
            products,
            start=1
        ):

            product_id = product[0]
            name = product[1]
            category_name = product[4] or "-"
            supplier_name = product[6] or "-"
            sku = product[7]
            price = product[8]
            quantity = product[10]
            reorder_level = product[11]

            values = [
                product_id,
                name,
                sku,
                category_name,
                supplier_name,
                f"₹{float(price):,.2f}",
                quantity
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
                column=7,
                padx=5,
                pady=3
            )

            edit_button = ctk.CTkButton(
                action_frame,
                text="Edit",
                width=55,
                height=28,
                command=lambda p=product:
                    self.edit_product(p)
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
                command=lambda pid=product_id:
                    self.delete_product(pid)
            )

            delete_button.pack(
                side="left",
                padx=2
            )

            # Low stock indicator
            if quantity <= reorder_level:

                warning = ctk.CTkLabel(
                    self.table,
                    text="LOW STOCK",
                    text_color="orange",
                    font=ctk.CTkFont(
                        size=11,
                        weight="bold"
                    )
                )

                warning.grid(
                    row=row_index,
                    column=6,
                    padx=(60, 0),
                    sticky="e"
                )

    # ==================================================
    # SEARCH
    # ==================================================

    def search_products(self):

        search_term = self.search_entry.get().strip()

        if not search_term:
            self.load_products()
            return

        try:

            products = Product.search(
                search_term
            )

            self.display_products(products)

        except Exception as error:

            messagebox.showerror(
                "Error",
                f"Search failed:\n{error}"
            )

    # ==================================================
    # EDIT
    # ==================================================

    def edit_product(self, product):

        self.selected_product_id = product[0]

        self.name_entry.delete(0, "end")
        self.name_entry.insert(0, product[1])

        self.description_entry.delete(0, "end")
        self.description_entry.insert(
            0,
            product[2] or ""
        )

        self.sku_entry.delete(0, "end")
        self.sku_entry.insert(0, product[7])

        self.price_entry.delete(0, "end")
        self.price_entry.insert(0, product[8])

        self.cost_price_entry.delete(0, "end")
        self.cost_price_entry.insert(0, product[9])

        self.quantity_entry.delete(0, "end")
        self.quantity_entry.insert(0, product[10])

        self.reorder_entry.delete(0, "end")
        self.reorder_entry.insert(0, product[11])

        category_name = product[4]

        if category_name:
            self.category_combo.set(
                category_name
            )

        supplier_name = product[6]

        if supplier_name:
            self.supplier_combo.set(
                supplier_name
            )

        self.save_button.configure(
            text="Update Product"
        )

    # ==================================================
    # DELETE
    # ==================================================

    def delete_product(self, product_id):

        confirmation = messagebox.askyesno(
            "Confirm Delete",
            "Are you sure you want to delete this product?"
        )

        if not confirmation:
            return

        try:

            deleted = Product.delete(
                product_id
            )

            if deleted:

                messagebox.showinfo(
                    "Success",
                    "Product deleted successfully."
                )

            self.load_products()

        except Exception as error:

            messagebox.showerror(
                "Delete Failed",
                str(error)
            )

    # ==================================================
    # CLEAR FORM
    # ==================================================

    def clear_form(self):

        self.selected_product_id = None

        entries = [
            self.name_entry,
            self.sku_entry,
            self.price_entry,
            self.cost_price_entry,
            self.quantity_entry,
            self.reorder_entry,
            self.description_entry
        ]

        for entry in entries:
            entry.delete(0, "end")

        self.category_combo.set(
            "Select Category"
        )

        self.supplier_combo.set(
            "Select Supplier"
        )

        self.save_button.configure(
            text="Add Product"
        )