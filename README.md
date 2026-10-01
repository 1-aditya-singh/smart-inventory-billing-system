# Smart Inventory And Billing System

A desktop-based Inventory and Billing Management System built using Python, CustomTkinter, and PostgreSQL.

The application helps businesses manage products, categories, suppliers, customers, inventory, sales, billing, and business reports from a single desktop application.

---

## 📌 Project Overview

The Smart Inventory And Billing System is designed as a real-world business management application.

It provides a complete workflow from product and inventory management to billing and sales reporting.

The system uses:

- Python for application logic
- CustomTkinter for the graphical user interface
- PostgreSQL for relational database management
- psycopg2 for database connectivity
- python-dotenv for environment variable management

The project follows a layered architecture separating the user interface, business logic, and database models.

---

## 🚀 Features

### Dashboard

- Total sales
- Total revenue
- Total customers
- Total products
- Total inventory units
- Inventory value
- Low-stock count
- Business summary

### Product Management

- Add products
- Update products
- Delete products
- Search products
- SKU management
- Selling price management
- Cost price management
- Stock quantity management
- Reorder level management
- Category association
- Supplier association

### Category Management

- Add categories
- Update categories
- Delete categories
- Search categories
- Category descriptions

### Supplier Management

- Add suppliers
- Update suppliers
- Delete suppliers
- Supplier contact information
- Supplier email and address

### Customer Management

- Add customers
- Update customers
- Delete customers
- Customer search
- Customer contact information
- Customer purchase history

### Inventory Management

- Stock-in operations
- Stock-out operations
- Stock adjustments
- Inventory transaction history
- Low-stock detection
- Reorder level tracking
- Inventory valuation

### Billing System

- Customer selection
- Product selection
- Shopping cart
- Quantity management
- Automatic subtotal calculation
- 5% tax calculation
- Discount support
- Automatic total calculation
- Multiple payment methods
- Invoice generation
- Automatic stock deduction

### Sales Management

- Sales history
- Invoice search
- Invoice details
- Customer-wise sales
- Date-based sales retrieval
- Payment method tracking
- Sale status tracking

### Reports

- Total revenue
- Total profit
- Total sales
- Sales by payment method
- Sales by category
- Top-selling products
- Customer sales analysis
- Sales by date
- Sales by month
- Low-stock report
- Inventory valuation

---

# 🏗️ System Architecture

The project follows a layered architecture:

```text
┌─────────────────────────────┐
│       CustomTkinter UI      │
│                             │
│ Dashboard                   │
│ Products                    │
│ Customers                   │
│ Suppliers                   │
│ Categories                  │
│ Billing                     │
│ Sales History               │
│ Reports                     │
│ Low Stock                   │
└──────────────┬──────────────┘
               │
               ▼
┌─────────────────────────────┐
│       Service Layer         │
│                             │
│ BillingService              │
│ InventoryService            │
│ ReportService               │
└──────────────┬──────────────┘
               │
               ▼
┌─────────────────────────────┐
│         Model Layer         │
│                             │
│ Customer                    │
│ Category                    │
│ Supplier                    │
│ Product                     │
│ Sale                        │
│ SaleItem                    │
│ InventoryTransaction        │
└──────────────┬──────────────┘
               │
               ▼
┌─────────────────────────────┐
│         PostgreSQL          │
│                             │
│ customers                   │
│ categories                  │
│ suppliers                   │
│ products                    │
│ sales                       │
│ sale_items                  │
│ inventory_transactions      │
└─────────────────────────────┘