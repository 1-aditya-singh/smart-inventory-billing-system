import customtkinter as ctk
from tkinter import messagebox

from models.sale import Sale
from services.billing_service import BillingService


class SalesFrame(ctk.CTkFrame):

    def __init__(self, parent):
        super().__init__(
            parent,
            corner_radius=0,
            fg_color="transparent"
        )

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self.create_header()
        self.create_table()

        self.load_sales()

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
            text="Sales History",
            font=ctk.CTkFont(
                size=28,
                weight="bold"
            )
        ).pack(anchor="w")

        ctk.CTkLabel(
            header,
            text="View completed invoices and transaction details",
            text_color="gray"
        ).pack(
            anchor="w",
            pady=(3, 0)
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
            row=1,
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
            placeholder_text="Search invoice number..."
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
            command=self.search_sales
        ).pack(side="left")

        ctk.CTkButton(
            search_frame,
            text="Refresh",
            width=100,
            command=self.load_sales
        ).pack(
            side="left",
            padx=(10, 0)
        )

        self.table = ctk.CTkScrollableFrame(
            frame
        )

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

    def load_sales(self):

        try:

            sales = Sale.get_all()

            self.display_sales(sales)

        except Exception as error:

            messagebox.showerror(
                "Error",
                str(error)
            )

    # ==================================================
    # DISPLAY
    # ==================================================

    def display_sales(self, sales):

        for widget in self.table.winfo_children():
            widget.destroy()

        headers = [
            "ID",
            "Invoice",
            "Date",
            "Customer",
            "Subtotal",
            "Tax",
            "Discount",
            "Total",
            "Payment",
            "Status",
            "Action"
        ]

        for column, header in enumerate(headers):

            ctk.CTkLabel(
                self.table,
                text=header,
                font=ctk.CTkFont(
                    size=12,
                    weight="bold"
                )
            ).grid(
                row=0,
                column=column,
                padx=7,
                pady=8
            )

        for row, sale in enumerate(
            sales,
            start=1
        ):

            sale_id = sale[0]

            values = [
                sale[0],
                sale[1],
                sale[2],
                sale[4] or "Walk-in",
                f"₹{float(sale[5]):,.2f}",
                f"₹{float(sale[6]):,.2f}",
                f"₹{float(sale[7]):,.2f}",
                f"₹{float(sale[8]):,.2f}",
                sale[9],
                sale[10]
            ]

            for column, value in enumerate(values):

                ctk.CTkLabel(
                    self.table,
                    text=str(value)
                ).grid(
                    row=row,
                    column=column,
                    padx=7,
                    pady=5
                )

            ctk.CTkButton(
                self.table,
                text="View",
                width=65,
                height=28,
                command=lambda sid=sale_id:
                    self.view_invoice(sid)
            ).grid(
                row=row,
                column=10,
                padx=5
            )

    # ==================================================
    # SEARCH
    # ==================================================

    def search_sales(self):

        term = self.search_entry.get().strip().lower()

        if not term:

            self.load_sales()
            return

        try:

            sales = Sale.get_all()

            filtered = []

            for sale in sales:

                if term in str(
                    sale[1]
                ).lower():

                    filtered.append(sale)

            self.display_sales(filtered)

        except Exception as error:

            messagebox.showerror(
                "Search Failed",
                str(error)
            )

    # ==================================================
    # VIEW INVOICE
    # ==================================================

    def view_invoice(self, sale_id):

        try:

            invoice = BillingService.get_invoice(
                sale_id
            )

            if invoice is None:

                messagebox.showwarning(
                    "Not Found",
                    "Invoice could not be found."
                )

                return

            sale = invoice["sale"]
            items = invoice["items"]

            window = ctk.CTkToplevel(self)

            window.title(
                f"Invoice - {sale[1]}"
            )

            window.geometry(
                "700x600"
            )

            window.grab_set()

            ctk.CTkLabel(
                window,
                text=f"Invoice {sale[1]}",
                font=ctk.CTkFont(
                    size=24,
                    weight="bold"
                )
            ).pack(
                pady=(25, 5)
            )

            customer = sale[4] or "Walk-in Customer"

            ctk.CTkLabel(
                window,
                text=f"Customer: {customer}"
            ).pack(
                pady=3
            )

            ctk.CTkLabel(
                window,
                text=f"Date: {sale[2]}"
            ).pack(
                pady=3
            )

            table = ctk.CTkScrollableFrame(
                window
            )

            table.pack(
                fill="both",
                expand=True,
                padx=20,
                pady=20
            )

            headers = [
                "Product",
                "Qty",
                "Price",
                "Subtotal"
            ]

            for column, header in enumerate(headers):

                ctk.CTkLabel(
                    table,
                    text=header,
                    font=ctk.CTkFont(
                        weight="bold"
                    )
                ).grid(
                    row=0,
                    column=column,
                    padx=10,
                    pady=8
                )

            for row, item in enumerate(
                items,
                start=1
            ):

                values = [
                    item[2],
                    item[4],
                    f"₹{float(item[5]):,.2f}",
                    f"₹{float(item[6]):,.2f}"
                ]

                for column, value in enumerate(values):

                    ctk.CTkLabel(
                        table,
                        text=str(value)
                    ).grid(
                        row=row,
                        column=column,
                        padx=10,
                        pady=5
                    )

            ctk.CTkLabel(
                window,
                text=(
                    f"Subtotal: ₹{float(sale[6]):,.2f}\n"
                    f"Tax: ₹{float(sale[7]):,.2f}\n"
                    f"Discount: ₹{float(sale[8]):,.2f}\n"
                    f"Total: ₹{float(sale[9]):,.2f}\n"
                    f"Payment: {sale[10]}"
                ),
                font=ctk.CTkFont(
                    size=15,
                    weight="bold"
                )
            ).pack(
                pady=(0, 25)
            )

        except Exception as error:

            messagebox.showerror(
                "Invoice Error",
                str(error)
            )