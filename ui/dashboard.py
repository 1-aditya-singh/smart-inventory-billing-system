import customtkinter as ctk

from services.report_service import ReportService


class DashboardFrame(ctk.CTkFrame):

    def __init__(self, parent):
        super().__init__(
            parent,
            corner_radius=0,
            fg_color="transparent"
        )

        self.grid_columnconfigure(
            (0, 1, 2),
            weight=1
        )

        self.grid_rowconfigure(
            1,
            weight=1
        )

        self.create_dashboard()

    # ==================================================
    # DASHBOARD
    # ==================================================

    def create_dashboard(self):

        # ------------------------------------------
        # Header
        # ------------------------------------------

        header_frame = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )

        header_frame.grid(
            row=0,
            column=0,
            columnspan=3,
            sticky="ew",
            padx=30,
            pady=(25, 15)
        )

        title = ctk.CTkLabel(
            header_frame,
            text="Dashboard",
            font=ctk.CTkFont(
                size=30,
                weight="bold"
            )
        )

        title.pack(
            anchor="w"
        )

        subtitle = ctk.CTkLabel(
            header_frame,
            text="Overview of your inventory and sales",
            font=ctk.CTkFont(size=14),
            text_color="gray"
        )

        subtitle.pack(
            anchor="w",
            pady=(3, 0)
        )

        # ------------------------------------------
        # Load statistics
        # ------------------------------------------

        try:
            summary = ReportService.get_dashboard_summary()
            profit = ReportService.get_total_profit()

            self.create_stat_card(
                row=1,
                column=0,
                title="Total Revenue",
                value=f"₹{float(summary['total_revenue']):,.2f}"
            )

            self.create_stat_card(
                row=1,
                column=1,
                title="Total Sales",
                value=str(summary["total_sales"])
            )

            self.create_stat_card(
                row=1,
                column=2,
                title="Total Products",
                value=str(summary["total_products"])
            )

            self.create_stat_card(
                row=2,
                column=0,
                title="Total Customers",
                value=str(summary["total_customers"])
            )

            self.create_stat_card(
                row=2,
                column=1,
                title="Low Stock Items",
                value=str(summary["low_stock_count"])
            )

            self.create_stat_card(
                row=2,
                column=2,
                title="Total Profit",
                value=f"₹{float(profit):,.2f}"
            )

            # --------------------------------------
            # Inventory information
            # --------------------------------------

            inventory_frame = ctk.CTkFrame(
                self,
                corner_radius=12
            )

            inventory_frame.grid(
                row=3,
                column=0,
                columnspan=3,
                sticky="ew",
                padx=30,
                pady=20
            )

            inventory_frame.grid_columnconfigure(
                (0, 1, 2),
                weight=1
            )

            inventory_title = ctk.CTkLabel(
                inventory_frame,
                text="Inventory Overview",
                font=ctk.CTkFont(
                    size=18,
                    weight="bold"
                )
            )

            inventory_title.grid(
                row=0,
                column=0,
                columnspan=3,
                sticky="w",
                padx=20,
                pady=(20, 15)
            )

            self.create_inventory_value(
                inventory_frame,
                1,
                0,
                "Total Units",
                summary["total_units"]
            )

            self.create_inventory_value(
                inventory_frame,
                1,
                1,
                "Cost Value",
                f"₹{float(summary['inventory_cost_value']):,.2f}"
            )

            self.create_inventory_value(
                inventory_frame,
                1,
                2,
                "Retail Value",
                f"₹{float(summary['inventory_retail_value']):,.2f}"
            )

        except Exception as error:

            error_label = ctk.CTkLabel(
                self,
                text=f"Unable to load dashboard data.\n\n{error}",
                font=ctk.CTkFont(size=16),
                text_color="red"
            )

            error_label.grid(
                row=1,
                column=0,
                columnspan=3,
                padx=30,
                pady=30
            )

    # ==================================================
    # STAT CARD
    # ==================================================

    def create_stat_card(
        self,
        row,
        column,
        title,
        value
    ):

        card = ctk.CTkFrame(
            self,
            corner_radius=12
        )

        card.grid(
            row=row,
            column=column,
            sticky="nsew",
            padx=10,
            pady=10
        )

        title_label = ctk.CTkLabel(
            card,
            text=title,
            font=ctk.CTkFont(
                size=14
            ),
            text_color="gray"
        )

        title_label.pack(
            anchor="w",
            padx=20,
            pady=(20, 5)
        )

        value_label = ctk.CTkLabel(
            card,
            text=value,
            font=ctk.CTkFont(
                size=25,
                weight="bold"
            )
        )

        value_label.pack(
            anchor="w",
            padx=20,
            pady=(0, 20)
        )

    # ==================================================
    # INVENTORY VALUE
    # ==================================================

    def create_inventory_value(
        self,
        parent,
        row,
        column,
        title,
        value
    ):

        frame = ctk.CTkFrame(
            parent,
            fg_color="transparent"
        )

        frame.grid(
            row=row,
            column=column,
            sticky="ew",
            padx=20,
            pady=(0, 20)
        )

        title_label = ctk.CTkLabel(
            frame,
            text=title,
            font=ctk.CTkFont(size=13),
            text_color="gray"
        )

        title_label.pack()

        value_label = ctk.CTkLabel(
            frame,
            text=str(value),
            font=ctk.CTkFont(
                size=18,
                weight="bold"
            )
        )

        value_label.pack(
            pady=(5, 0)
        )