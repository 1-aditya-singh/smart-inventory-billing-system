import customtkinter as ctk

from services.report_service import ReportService


class LowStockFrame(ctk.CTkFrame):

    def __init__(self, parent):
        super().__init__(parent)

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        # -----------------------------
        # Header
        # -----------------------------

        title = ctk.CTkLabel(
            self,
            text="Low Stock Products",
            font=ctk.CTkFont(size=24, weight="bold")
        )

        title.grid(
            row=0,
            column=0,
            padx=20,
            pady=(20, 5),
            sticky="w"
        )

        self.count_label = ctk.CTkLabel(
            self,
            text="Low Stock Items: 0",
            font=ctk.CTkFont(size=14)
        )

        self.count_label.grid(
            row=1,
            column=0,
            padx=20,
            pady=(0, 15),
            sticky="w"
        )

        # -----------------------------
        # Table
        # -----------------------------

        self.table_frame = ctk.CTkScrollableFrame(
            self
        )

        self.table_frame.grid(
            row=2,
            column=0,
            padx=20,
            pady=10,
            sticky="nsew"
        )

        # -----------------------------
        # Refresh Button
        # -----------------------------

        refresh_button = ctk.CTkButton(
            self,
            text="Refresh",
            command=self.load_data
        )

        refresh_button.grid(
            row=3,
            column=0,
            padx=20,
            pady=20,
            sticky="w"
        )

        self.load_data()

    def load_data(self):

        for widget in self.table_frame.winfo_children():
            widget.destroy()

        products = ReportService.get_low_stock_report()

        self.count_label.configure(
            text=f"Low Stock Items: {len(products)}"
        )

        headers = [
            "ID",
            "Product",
            "SKU",
            "Category",
            "Stock",
            "Reorder Level",
            "Cost Price",
            "Selling Price"
        ]

        for column, header in enumerate(headers):

            label = ctk.CTkLabel(
                self.table_frame,
                text=header,
                font=ctk.CTkFont(weight="bold")
            )

            label.grid(
                row=0,
                column=column,
                padx=10,
                pady=10,
                sticky="w"
            )

        for row_index, product in enumerate(
            products,
            start=1
        ):

            (
                product_id,
                name,
                sku,
                category,
                quantity,
                reorder_level,
                cost_price,
                price
            ) = product

            values = [
                product_id,
                name,
                sku,
                category or "N/A",
                quantity,
                reorder_level,
                f"₹{cost_price}",
                f"₹{price}"
            ]

            for column, value in enumerate(values):

                label = ctk.CTkLabel(
                    self.table_frame,
                    text=str(value)
                )

                label.grid(
                    row=row_index,
                    column=column,
                    padx=10,
                    pady=8,
                    sticky="w"
                )