-- Create table
CREATE TABLE IF NOT EXISTS products (
  platform        TEXT    NOT NULL,                 
  product_id      TEXT    NOT NULL,                 
  title           TEXT    NOT NULL,
  price           NUMERIC(12,2) NOT NULL,
  original_price  NUMERIC(12,2),
  currency        TEXT    NOT NULL,
  discount        TEXT,
  image_url       TEXT,
  last_updated    TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  PRIMARY KEY (platform, product_id)
);

-- Full-text index on title
CREATE INDEX IF NOT EXISTS idx_products_title ON products USING gin (to_tsvector('english', title));
