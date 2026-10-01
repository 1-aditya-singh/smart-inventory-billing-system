import customtkinter as ctk
from tkinter import messagebox

from models.customer import Customer
from models.product import Product
from services.billing_service import BillingService


class BillingFrame(ctk.CTkFrame):

    def __init__(self, parent):
        super().__init__(
            parent,
            corner_radius=0,
            fg_color="transparent"
        )

        self.cart = []

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self.create_header()
        self.create_left_panel()
        self.create_cart_panel()

        self.load_customers()
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
            columnspan=2,
            sticky="ew",
            padx=25,
            pady=(20, 10)
        )

        ctk.CTkLabel(
            header,
            text="Billing / Point of Sale",
            font=ctk.CTkFont(
                size=28,
                weight="bold"
            )
        ).pack(anchor="w")

        ctk.CTkLabel(
            header,
            text="Create invoices and process customer purchases",
            text_color="gray"
        ).pack(
            anchor="w",
            pady=(3, 0)
        )

    # ==================================================
    # LEFT PANEL
    # ==================================================

    def create_left_panel(self):

        panel = ctk.CTkFrame(
            self,
            corner_radius=12
        )

        panel.grid(
            row=1,
            column=0,
            sticky="nsew",
            padx=(25, 10),
            pady=(10, 25)
        )

        panel.grid_columnconfigure(
            0,
            weight=1
        )

        ctk.CTkLabel(
            panel,
            text="Add Item",
            font=ctk.CTkFont(
                size=20,
                weight="bold"
            )
        ).grid(
            row=0,
            column=0,
            sticky="w",
            padx=20,
            pady=(20, 15)
        )

        # Customer
        ctk.CTkLabel(
            panel,
            text="Customer"
        ).grid(
            row=1,
            column=0,
            sticky="w",
            padx=20,
            pady=(5, 5)
        )

        self.customer_combo = ctk.CTkComboBox(
            panel,
            values=["Walk-in Customer"]
        )

        self.customer_combo.grid(
            row=2,
            column=0,
            sticky="ew",
            padx=20,
            pady=(0, 15)
        )

        # Product
        ctk.CTkLabel(
            panel,
            text="Product"
        ).grid(
            row=3,
            column=0,
            sticky="w",
            padx=20,
            pady=(5, 5)
        )

        self.product_combo = ctk.CTkComboBox(
            panel,
            values=["No Products"]
        )

        self.product_combo.grid(
            row=4,
            column=0,
            sticky="ew",
            padx=20,
            pady=(0, 15)
        )

        # Quantity
        ctk.CTkLabel(
            panel,
            text="Quantity"
        ).grid(
            row=5,
            column=0,
            sticky="w",
            padx=20,
            pady=(5, 5)
        )

        self.quantity_entry = ctk.CTkEntry(
            panel,
            placeholder_text="1"
        )

        self.quantity_entry.grid(
            row=6,
            column=0,
            sticky="ew",
            padx=20,
            pady=(0, 15)
        )

        ctk.CTkButton(
            panel,
            text="Add to Cart",
            height=40,
            command=self.add_to_cart
        ).grid(
            row=7,
            column=0,
            sticky="ew",
            padx=20,
            pady=(5, 25)
        )

    # ==================================================
    # CART
    # ==================================================

    def create_cart_panel(self):

        panel = ctk.CTkFrame(
            self,
            corner_radius=12
        )

        panel.grid(
            row=1,
            column=1,
            sticky="nsew",
            padx=(10, 25),
            pady=(10, 25)
        )

        panel.grid_columnconfigure(
            0,
            weight=1
        )

        panel.grid_rowconfigure(
            1,
            weight=1
        )

        ctk.CTkLabel(
            panel,
            text="Current Invoice",
            font=ctk.CTkFont(
                size=20,
                weight="bold"
            )
        ).grid(
            row=0,
            column=0,
            sticky="w",
            padx=20,
            pady=(20, 15)
        )

        self.cart_table = ctk.CTkScrollableFrame(
            panel
        )

        self.cart_table.grid(
            row=1,
            column=0,
            sticky="nsew",
            padx=15,
            pady=(0, 15)
        )

        self.summary_frame = ctk.CTkFrame(
            panel
        )

        self.summary_frame.grid(
            row=2,
            column=0,
            sticky="ew",
            padx=15,
            pady=15
        )

        self.create_summary()

    # ==================================================
    # SUMMARY
    # ==================================================

    def create_summary(self):

        self.subtotal_label = self.create_summary_row(
            "Subtotal",
            0
        )

        self.tax_label = self.create_summary_row(
            "Tax (5%)",
            1
        )

        ctk.CTkLabel(
            self.summary_frame,
            text="Discount"
        ).grid(
            row=2,
            column=0,
            padx=10,
            pady=5,
            sticky="w"
        )

        self.discount_entry = ctk.CTkEntry(
            self.summary_frame,
            width=120,
            placeholder_text="0"
        )

        self.discount_entry.grid(
            row=2,
            column=1,
            padx=10,
            pady=5
        )

        self.total_label = self.create_summary_row(
            "Total",
            3
        )

        ctk.CTkLabel(
            self.summary_frame,
            text="Payment Method"
        ).grid(
            row=4,
            column=0,
            padx=10,
            pady=5,
            sticky="w"
        )

        self.payment_combo = ctk.CTkComboBox(
            self.summary_frame,
            values=[
                "Cash",
                "UPI",
                "Card",
                "Bank Transfer"
            ],
            width=150
        )

        self.payment_combo.grid(
            row=4,
            column=1,
            padx=10,
            pady=5
        )

        self.payment_combo.set("Cash")

        ctk.CTkButton(
            self.summary_frame,
            text="Create Invoice",
            height=40,
            command=self.create_invoice
        ).grid(
            row=5,
            column=0,
            columnspan=2,
            sticky="ew",
            padx=10,
            pady=(15, 10)
        )

        ctk.CTkButton(
            self.summary_frame,
            text="Clear Cart",
            height=35,
            command=self.clear_cart
        ).grid(
            row=6,
            column=0,
            columnspan=2,
            sticky="ew",
            padx=10,
            pady=(0, 10)
        )

    def create_summary_row(self, title, row):

        ctk.CTkLabel(
            self.summary_frame,
            text=title
        ).grid(
            row=row,
            column=0,
            padx=10,
            pady=5,
            sticky="w"
        )

        label = ctk.CTkLabel(
            self.summary_frame,
            text="₹0.00",
            font=ctk.CTkFont(
                size=14,
                weight="bold"
            )
        )

        label.grid(
            row=row,
            column=1,
            padx=10,
            pady=5,
            sticky="e"
        )

        return label

    # ==================================================
    # LOAD CUSTOMERS
    # ==================================================

    def load_customers(self):

        try:

            customers = Customer.get_all()

            self.customer_map = {
                "Walk-in Customer": None
            }

            values = [
                "Walk-in Customer"
            ]

            for customer in customers:

                customer_id = customer[0]
                customer_name = customer[1]

                display = (
                    f"{customer_name} "
                    f"(ID: {customer_id})"
                )

                self.customer_map[
                    display
                ] = customer_id

                values.append(display)

            self.customer_combo.configure(
                values=values
            )

            self.customer_combo.set(
                "Walk-in Customer"
            )

        except Exception as error:

            messagebox.showerror(
                "Error",
                f"Unable to load customers:\n{error}"
            )

    # ==================================================
    # LOAD PRODUCTS
    # ==================================================

    def load_products(self):

        try:

            products = Product.get_all()

            self.product_map = {}

            values = []

            for product in products:

                product_id = product[0]
                name = product[1]
                sku = product[7]
                price = product[8]
                quantity = product[10]

                display = (
                    f"{name} | "
                    f"{sku} | "
                    f"₹{float(price):,.2f} | "
                    f"Stock: {quantity}"
                )

                self.product_map[
                    display
                ] = {
                    "id": product_id,
                    "name": name,
                    "sku": sku,
                    "price": float(price),
                    "stock": quantity
                }

                values.append(display)

            if not values:
                values = ["No Products"]

            self.product_combo.configure(
                values=values
            )

            self.product_combo.set(
                values[0]
            )

        except Exception as error:

            messagebox.showerror(
                "Error",
                f"Unable to load products:\n{error}"
            )

    # ==================================================
    # ADD TO CART
    # ==================================================

    def add_to_cart(self):

        try:

            selected_product = (
                self.product_combo.get()
            )

            if selected_product not in self.product_map:
                raise ValueError(
                    "Please select a valid product."
                )

            quantity = int(
                self.quantity_entry.get()
            )

            if quantity <= 0:
                raise ValueError(
                    "Quantity must be greater than 0."
                )

            product = self.product_map[
                selected_product
            ]

            if quantity > product["stock"]:
                raise ValueError(
                    f"Only {product['stock']} "
                    f"units are available."
                )

            # If product already exists in cart
            for item in self.cart:

                if item["product_id"] == product["id"]:

                    new_quantity = (
                        item["quantity"]
                        + quantity
                    )

                    if new_quantity > product["stock"]:
                        raise ValueError(
                            "Requested quantity exceeds stock."
                        )

                    item["quantity"] = new_quantity

                    self.refresh_cart()
                    return

            self.cart.append(
                {
                    "product_id": product["id"],
                    "product_name": product["name"],
                    "sku": product["sku"],
                    "quantity": quantity,
                    "unit_price": product["price"]
                }
            )

            self.quantity_entry.delete(
                0,
                "end"
            )

            self.quantity_entry.insert(
                0,
                "1"
            )

            self.refresh_cart()

        except ValueError as error:

            messagebox.showwarning(
                "Invalid Input",
                str(error)
            )

    # ==================================================
    # REFRESH CART
    # ==================================================

    def refresh_cart(self):

        for widget in self.cart_table.winfo_children():
            widget.destroy()

        headers = [
            "Product",
            "Qty",
            "Price",
            "Subtotal",
            "Remove"
        ]

        for column, header in enumerate(headers):

            ctk.CTkLabel(
                self.cart_table,
                text=header,
                font=ctk.CTkFont(
                    size=12,
                    weight="bold"
                )
            ).grid(
                row=0,
                column=column,
                padx=8,
                pady=8
            )

        subtotal = 0

        for row, item in enumerate(
            self.cart,
            start=1
        ):

            item_subtotal = (
                item["quantity"]
                * item["unit_price"]
            )

            subtotal += item_subtotal

            values = [
                item["product_name"],
                item["quantity"],
                f"₹{item['unit_price']:,.2f}",
                f"₹{item_subtotal:,.2f}"
            ]

            for column, value in enumerate(values):

                ctk.CTkLabel(
                    self.cart_table,
                    text=str(value)
                ).grid(
                    row=row,
                    column=column,
                    padx=8,
                    pady=5
                )

            ctk.CTkButton(
                self.cart_table,
                text="Remove",
                width=70,
                height=28,
                command=lambda index=row - 1:
                    self.remove_from_cart(index)
            ).grid(
                row=row,
                column=4,
                padx=5,
                pady=5
            )

        self.update_totals()

    # ==================================================
    # REMOVE
    # ==================================================

    def remove_from_cart(self, index):

        if 0 <= index < len(self.cart):

            self.cart.pop(index)

            self.refresh_cart()

    # ==================================================
    # TOTALS
    # ==================================================

    def update_totals(self):

        try:

            discount_text = (
                self.discount_entry
                .get()
                .strip()
            )

            discount = (
                float(discount_text)
                if discount_text
                else 0
            )

            totals = BillingService.calculate_totals(
                self.cart,
                discount
            )

            self.subtotal_label.configure(
                text=f"₹{totals['subtotal']:,.2f}"
            )

            self.tax_label.configure(
                text=f"₹{totals['tax']:,.2f}"
            )

            self.total_label.configure(
                text=f"₹{totals['total_amount']:,.2f}"
            )

        except Exception:

            self.subtotal_label.configure(
                text="₹0.00"
            )

            self.tax_label.configure(
                text="₹0.00"
            )

            self.total_label.configure(
                text="₹0.00"
            )

    # ==================================================
    # CREATE INVOICE
    # ==================================================

    def create_invoice(self):

        try:

            if not self.cart:
                raise ValueError(
                    "Cart is empty."
                )

            customer_name = (
                self.customer_combo.get()
            )

            customer_id = self.customer_map.get(
                customer_name
            )

            discount_text = (
                self.discount_entry
                .get()
                .strip()
            )

            discount = (
                float(discount_text)
                if discount_text
                else 0
            )

            payment_method = (
                self.payment_combo.get()
            )

            result = BillingService.create_invoice(
                customer_id,
                self.cart,
                discount,
                payment_method
            )

            messagebox.showinfo(
                "Invoice Created",
                (
                    f"Invoice created successfully!\n\n"
                    f"Invoice: {result['invoice_number']}\n"
                    f"Subtotal: ₹{result['subtotal']:,.2f}\n"
                    f"Tax: ₹{result['tax']:,.2f}\n"
                    f"Discount: ₹{result['discount']:,.2f}\n"
                    f"Total: ₹{result['total_amount']:,.2f}"
                )
            )

            self.clear_cart()
            self.load_products()

        except ValueError as error:

            messagebox.showwarning(
                "Unable to Create Invoice",
                str(error)
            )

        except Exception as error:

            messagebox.showerror(
                "Billing Error",
                str(error)
            )

    # ==================================================
    # CLEAR
    # ==================================================

    def clear_cart(self):

        self.cart = []

        self.discount_entry.delete(
            0,
            "end"
        )

        self.refresh_cart()