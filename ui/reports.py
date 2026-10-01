import customtkinter as ctk
from tkinter import messagebox

from services.report_service import ReportService


class ReportsFrame(ctk.CTkFrame):

    def __init__(self, parent):
        super().__init__(
            parent,
            corner_radius=0,
            fg_color="transparent"
        )

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self.create_header()
        self.create_reports()

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
            text="Reports & Analytics",
            font=ctk.CTkFont(
                size=28,
                weight="bold"
            )
        ).pack(anchor="w")

        ctk.CTkLabel(
            header,
            text="Business performance and inventory insights",
            text_color="gray"
        ).pack(
            anchor="w",
            pady=(3, 0)
        )

    # ==================================================
    # REPORTS
    # ==================================================

    def create_reports(self):

        container = ctk.CTkScrollableFrame(
            self
        )

        container.grid(
            row=1,
            column=0,
            sticky="nsew",
            padx=25,
            pady=(10, 25)
        )

        try:

            summary = ReportService.get_dashboard_summary()
            profit = ReportService.get_total_profit()

            self.create_summary_section(
                container,
                summary,
                profit
            )

            self.create_payment_section(
                container
            )

            self.create_category_section(
                container
            )

            self.create_top_products_section(
                container
            )

        except Exception as error:

            ctk.CTkLabel(
                container,
                text=f"Unable to load reports:\n{error}",
                text_color="red"
            ).pack(
                padx=20,
                pady=20
            )

    # ==================================================
    # SUMMARY
    # ==================================================

    def create_summary_section(
        self,
        parent,
        summary,
        profit
    ):

        frame = ctk.CTkFrame(
            parent,
            corner_radius=12
        )

        frame.pack(
            fill="x",
            pady=(0, 15)
        )

        ctk.CTkLabel(
            frame,
            text="Business Summary",
            font=ctk.CTkFont(
                size=19,
                weight="bold"
            )
        ).pack(
            anchor="w",
            padx=20,
            pady=(20, 15)
        )

        values = [
            (
                "Revenue",
                f"₹{float(summary['total_revenue']):,.2f}"
            ),
            (
                "Profit",
                f"₹{float(profit):,.2f}"
            ),
            (
                "Sales",
                summary["total_sales"]
            ),
            (
                "Customers",
                summary["total_customers"]
            ),
            (
                "Products",
                summary["total_products"]
            ),
            (
                "Low Stock",
                summary["low_stock_count"]
            )
        ]

        row_frame = ctk.CTkFrame(
            frame,
            fg_color="transparent"
        )

        row_frame.pack(
            fill="x",
            padx=20,
            pady=(0, 20)
        )

        for column in range(6):
            row_frame.grid_columnconfigure(
                column,
                weight=1
            )

        for column, (title, value) in enumerate(values):

            box = ctk.CTkFrame(
                row_frame,
                corner_radius=8
            )

            box.grid(
                row=0,
                column=column,
                sticky="ew",
                padx=5
            )

            ctk.CTkLabel(
                box,
                text=title,
                text_color="gray"
            ).pack(
                pady=(12, 3)
            )

            ctk.CTkLabel(
                box,
                text=str(value),
                font=ctk.CTkFont(
                    size=17,
                    weight="bold"
                )
            ).pack(
                pady=(0, 12)
            )

    # ==================================================
    # PAYMENT METHOD
    # ==================================================

    def create_payment_section(self, parent):

        frame = ctk.CTkFrame(
            parent,
            corner_radius=12
        )

        frame.pack(
            fill="x",
            pady=15
        )

        ctk.CTkLabel(
            frame,
            text="Sales by Payment Method",
            font=ctk.CTkFont(
                size=19,
                weight="bold"
            )
        ).pack(
            anchor="w",
            padx=20,
            pady=(20, 10)
        )

        rows = ReportService.get_sales_by_payment_method()

        for row in rows:

            text = (
                f"{row[0]}    |    "
                f"Orders: {row[1]}    |    "
                f"Revenue: ₹{float(row[2]):,.2f}"
            )

            ctk.CTkLabel(
                frame,
                text=text
            ).pack(
                anchor="w",
                padx=25,
                pady=5
            )

        ctk.CTkLabel(
            frame,
            text=""
        ).pack(pady=5)

    # ==================================================
    # CATEGORY
    # ==================================================

    def create_category_section(self, parent):

        frame = ctk.CTkFrame(
            parent,
            corner_radius=12
        )

        frame.pack(
            fill="x",
            pady=15
        )

        ctk.CTkLabel(
            frame,
            text="Sales by Category",
            font=ctk.CTkFont(
                size=19,
                weight="bold"
            )
        ).pack(
            anchor="w",
            padx=20,
            pady=(20, 10)
        )

        rows = ReportService.get_sales_by_category()

        for row in rows:

            category = row[0] or "Uncategorized"

            text = (
                f"{category}    |    "
                f"Units: {row[1]}    |    "
                f"Revenue: ₹{float(row[2]):,.2f}"
            )

            ctk.CTkLabel(
                frame,
                text=text
            ).pack(
                anchor="w",
                padx=25,
                pady=5
            )

        ctk.CTkLabel(
            frame,
            text=""
        ).pack(pady=5)

    # ==================================================
    # TOP PRODUCTS
    # ==================================================

    def create_top_products_section(self, parent):

        frame = ctk.CTkFrame(
            parent,
            corner_radius=12
        )

        frame.pack(
            fill="x",
            pady=15
        )

        ctk.CTkLabel(
            frame,
            text="Top Selling Products",
            font=ctk.CTkFont(
                size=19,
                weight="bold"
            )
        ).pack(
            anchor="w",
            padx=20,
            pady=(20, 10)
        )

        rows = ReportService.get_top_selling_products(10)

        for row in rows:

            text = (
                f"{row[1]} ({row[2]})    |    "
                f"Units Sold: {row[3]}    |    "
                f"Revenue: ₹{float(row[4]):,.2f}"
            )

            ctk.CTkLabel(
                frame,
                text=text
            ).pack(
                anchor="w",
                padx=25,
                pady=5
            )

        ctk.CTkLabel(
            frame,
            text=""
        ).pack(pady=5)