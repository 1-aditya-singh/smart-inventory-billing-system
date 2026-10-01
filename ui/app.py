import customtkinter as ctk

from ui.dashboard import DashboardFrame
from ui.products import ProductsFrame
from ui.customers import CustomersFrame
from ui.suppliers import SuppliersFrame
from ui.categories import CategoriesFrame
from ui.billing import BillingFrame
from ui.sales import SalesFrame
from ui.reports import ReportsFrame
from ui.low_stock import LowStockFrame

class InventoryApp(ctk.CTk):

    def __init__(self):
        super().__init__()

        # ------------------------------------------
        # Window configuration
        # ------------------------------------------

        self.title("Smart Inventory & Billing System")
        self.geometry("1400x800")
        self.minsize(1100, 650)

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        # ------------------------------------------
        # Main grid
        # ------------------------------------------

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # ------------------------------------------
        # Create sidebar
        # ------------------------------------------

        self.create_sidebar()

        # ------------------------------------------
        # Main content
        # ------------------------------------------

        self.content_frame = ctk.CTkFrame(
            self,
            corner_radius=0,
            fg_color=("gray95", "gray10")
        )

        self.content_frame.grid(
            row=0,
            column=1,
            sticky="nsew"
        )

        self.content_frame.grid_columnconfigure(
            0,
            weight=1
        )

        self.content_frame.grid_rowconfigure(
            1,
            weight=1
        )

        self.show_dashboard()

    # ==================================================
    # SIDEBAR
    # ==================================================

    def create_sidebar(self):

        self.sidebar = ctk.CTkFrame(
            self,
            width=240,
            corner_radius=0
        )

        self.sidebar.grid(
            row=0,
            column=0,
            sticky="nsew"
        )

        self.sidebar.grid_propagate(False)

        # ------------------------------------------
        # Application title
        # ------------------------------------------

        title_label = ctk.CTkLabel(
            self.sidebar,
            text="SMART INVENTORY",
            font=ctk.CTkFont(
                size=20,
                weight="bold"
            )
        )

        title_label.pack(
            pady=(30, 5)
        )

        subtitle_label = ctk.CTkLabel(
            self.sidebar,
            text="Inventory & Billing",
            font=ctk.CTkFont(
                size=12
            ),
            text_color="gray"
        )

        subtitle_label.pack(
            pady=(0, 30)
        )

        # ------------------------------------------
        # Navigation buttons
        # ------------------------------------------

        self.create_nav_button(
            "📊  Dashboard",
            self.show_dashboard
        )

        self.create_nav_button(
            "📦  Products",
            self.show_products
        )

        self.create_nav_button(
            "👥  Customers",
            self.show_customers
        )

        self.create_nav_button(
            "🚚  Suppliers",
            self.show_suppliers
        )

        self.create_nav_button(
            "🏷️  Categories",
            self.show_categories
        )

        self.create_nav_button(
            "🧾  Billing",
            self.show_billing
        )

        self.create_nav_button(
            "📋  Sales History",
            self.show_sales
        )

        self.create_nav_button(
            "📈  Reports",
            self.show_reports
        )

        self.create_nav_button(
            "⚠️  Low Stock",
            self.show_low_stock
        )

        # ------------------------------------------
        # Bottom section
        # ------------------------------------------

        bottom_frame = ctk.CTkFrame(
            self.sidebar,
            fg_color="transparent"
        )

        bottom_frame.pack(
            side="bottom",
            fill="x",
            padx=15,
            pady=20
        )

        settings_button = ctk.CTkButton(
            bottom_frame,
            text="⚙  Settings",
            height=40,
            command=self.show_settings
        )

        settings_button.pack(
            fill="x"
        )

    # ==================================================
    # NAVIGATION BUTTON
    # ==================================================

    def create_nav_button(self, text, command):

        button = ctk.CTkButton(
            self.sidebar,
            text=text,
            height=42,
            corner_radius=8,
            anchor="w",
            command=command
        )

        button.pack(
            fill="x",
            padx=15,
            pady=4
        )

    # ==================================================
    # CONTENT HELPER
    # ==================================================

    def clear_content(self):

        for widget in self.content_frame.winfo_children():
            widget.destroy()

    # ==================================================
    # DASHBOARD
    # ==================================================

    def show_dashboard(self):

        self.clear_content()

        dashboard = DashboardFrame(
            self.content_frame
        )

        dashboard.pack(
            fill="both",
            expand=True
        )
    # ==================================================
    # PLACEHOLDER SCREENS
    # ==================================================

    def show_products(self):

        self.clear_content()

        products = ProductsFrame(
            self.content_frame
        )

        products.pack(
            fill="both",
            expand=True
        )

    def show_customers(self):

        self.clear_content()

        customers = CustomersFrame(
            self.content_frame
        )

        customers.pack(
            fill="both",
            expand=True
        )

    
    def show_suppliers(self):

        self.clear_content()

        frame = SuppliersFrame(
            self.content_frame
        )

        frame.pack(
            fill="both",
            expand=True
        )


    def show_categories(self):

        self.clear_content()

        frame = CategoriesFrame(
            self.content_frame
        )

        frame.pack(
            fill="both",
            expand=True
        )


    def show_billing(self):

        self.clear_content()

        frame = BillingFrame(
            self.content_frame
        )

        frame.pack(
            fill="both",
            expand=True
        )


    def show_sales(self):

        self.clear_content()

        frame = SalesFrame(
            self.content_frame
        )

        frame.pack(
            fill="both",
            expand=True
        )


    def show_reports(self):

        self.clear_content()

        frame = ReportsFrame(
            self.content_frame
        )

        frame.pack(
            fill="both",
            expand=True
        )


    def show_low_stock(self):

        self.clear_content()

        frame = LowStockFrame(
            self.content_frame
        )

        frame.pack(
            fill="both",
            expand=True
        )
    def show_settings(self):
        self.show_placeholder("Settings")

    # ==================================================
    # PLACEHOLDER
    # ==================================================

    def show_placeholder(self, screen_name):

        self.clear_content()

        title = ctk.CTkLabel(
            self.content_frame,
            text=screen_name,
            font=ctk.CTkFont(
                size=28,
                weight="bold"
            )
        )

        title.grid(
            row=0,
            column=0,
            padx=30,
            pady=(30, 10),
            sticky="w"
        )

        message = ctk.CTkLabel(
            self.content_frame,
            text=f"{screen_name} screen will be implemented next.",
            font=ctk.CTkFont(size=16)
        )

        message.grid(
            row=1,
            column=0,
            padx=30,
            pady=20,
            sticky="nw"
        )


if __name__ == "__main__":
    app = InventoryApp()
    app.mainloop()