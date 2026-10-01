-- ============================================================
-- SMART INVENTORY AND BILLING SYSTEM
-- DATABASE SCHEMA
-- ============================================================

-- ============================================================
-- CUSTOMERS
-- ============================================================

CREATE TABLE IF NOT EXISTS customers (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    contact VARCHAR(15) NOT NULL,
    email VARCHAR(100),
    address TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


-- ============================================================
-- CATEGORIES
-- ============================================================

CREATE TABLE IF NOT EXISTS categories (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


-- ============================================================
-- SUPPLIERS
-- ============================================================

CREATE TABLE IF NOT EXISTS suppliers (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    contact VARCHAR(15) NOT NULL,
    email VARCHAR(100),
    address TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


-- ============================================================
-- PRODUCTS
-- ============================================================

CREATE TABLE IF NOT EXISTS products (
    id SERIAL PRIMARY KEY,

    name VARCHAR(100) NOT NULL,

    description TEXT,

    category_id INT,

    supplier_id INT,

    sku VARCHAR(50) UNIQUE,

    price DECIMAL(10,2) NOT NULL CHECK (price >= 0),

    cost_price DECIMAL(10,2) NOT NULL CHECK (cost_price >= 0),

    quantity INT NOT NULL DEFAULT 0 CHECK (quantity >= 0),

    reorder_level INT NOT NULL DEFAULT 5 CHECK (reorder_level >= 0),

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (category_id)
        REFERENCES categories(id)
        ON DELETE SET NULL,

    FOREIGN KEY (supplier_id)
        REFERENCES suppliers(id)
        ON DELETE SET NULL
);


-- ============================================================
-- SALES
-- ============================================================

CREATE TABLE IF NOT EXISTS sales (
    id SERIAL PRIMARY KEY,

    customer_id INT,

    invoice_number VARCHAR(50) UNIQUE NOT NULL,

    sale_date DATE NOT NULL DEFAULT CURRENT_DATE,

    subtotal DECIMAL(10,2) NOT NULL DEFAULT 0
        CHECK (subtotal >= 0),

    tax DECIMAL(10,2) NOT NULL DEFAULT 0
        CHECK (tax >= 0),

    discount DECIMAL(10,2) NOT NULL DEFAULT 0
        CHECK (discount >= 0),

    total_amount DECIMAL(10,2) NOT NULL DEFAULT 0
        CHECK (total_amount >= 0),

    payment_method VARCHAR(20)
        DEFAULT 'Cash',

    status VARCHAR(20)
        DEFAULT 'Completed',

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (customer_id)
        REFERENCES customers(id)
        ON DELETE SET NULL
);


-- ============================================================
-- SALE ITEMS
-- ============================================================

CREATE TABLE IF NOT EXISTS sale_items (
    id SERIAL PRIMARY KEY,

    sale_id INT NOT NULL,

    product_id INT NOT NULL,

    quantity INT NOT NULL CHECK (quantity > 0),

    unit_price DECIMAL(10,2) NOT NULL
        CHECK (unit_price >= 0),

    subtotal DECIMAL(10,2) NOT NULL
        CHECK (subtotal >= 0),

    FOREIGN KEY (sale_id)
        REFERENCES sales(id)
        ON DELETE CASCADE,

    FOREIGN KEY (product_id)
        REFERENCES products(id)
        ON DELETE RESTRICT
);


-- ============================================================
-- INVENTORY TRANSACTIONS
-- ============================================================

CREATE TABLE IF NOT EXISTS inventory_transactions (
    id SERIAL PRIMARY KEY,

    product_id INT NOT NULL,

    transaction_type VARCHAR(20) NOT NULL,

    quantity INT NOT NULL,

    reference_id INT,

    notes TEXT,

    transaction_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (product_id)
        REFERENCES products(id)
        ON DELETE CASCADE
);


-- ============================================================
-- INDEXES
-- ============================================================

CREATE INDEX IF NOT EXISTS idx_products_category
    ON products(category_id);

CREATE INDEX IF NOT EXISTS idx_products_supplier
    ON products(supplier_id);

CREATE INDEX IF NOT EXISTS idx_products_sku
    ON products(sku);

CREATE INDEX IF NOT EXISTS idx_sales_customer
    ON sales(customer_id);

CREATE INDEX IF NOT EXISTS idx_sales_date
    ON sales(sale_date);

CREATE INDEX IF NOT EXISTS idx_sale_items_sale
    ON sale_items(sale_id);

CREATE INDEX IF NOT EXISTS idx_sale_items_product
    ON sale_items(product_id);

CREATE INDEX IF NOT EXISTS idx_inventory_product
    ON inventory_transactions(product_id);