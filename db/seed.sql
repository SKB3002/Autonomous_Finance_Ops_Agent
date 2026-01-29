INSERT INTO vendors (name, gst_number, risk_level)
VALUES
('ABC Logistics', '27ABCDE1234F1Z5', 'low'),
('XYZ Consultants', '29XYZDE5678K9L', 'medium'),
('Suspicious Traders', NULL, 'high');

INSERT INTO invoices (vendor_id, amount, currency, invoice_date, status)
VALUES
(1, 120000, 'INR', '2025-01-10', 'paid'),
(2, 450000, 'INR', '2025-01-15', 'pending'),
(3, 980000, 'INR', '2025-01-20', 'flagged');
