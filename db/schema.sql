-- Vendors master
CREATE TABLE IF NOT EXISTS vendors (
    vendor_id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    gst_number TEXT,
    risk_level TEXT CHECK (risk_level IN ('low','medium','high')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Historical invoices
CREATE TABLE IF NOT EXISTS invoices (
    invoice_id SERIAL PRIMARY KEY,
    vendor_id INT REFERENCES vendors(vendor_id),
    amount NUMERIC,
    currency TEXT,
    invoice_date DATE,
    status TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Persistent memory (approved facts)
CREATE TABLE IF NOT EXISTS persistent_memory (
    memory_id SERIAL PRIMARY KEY,
    key TEXT UNIQUE,
    value TEXT,
    source TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Audit logs (non-negotiable)
CREATE TABLE IF NOT EXISTS audit_logs (
    log_id SERIAL PRIMARY KEY,
    run_id TEXT,
    agent_name TEXT,
    action TEXT,
    input_data JSONB,
    output_data JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

