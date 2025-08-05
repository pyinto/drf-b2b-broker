-- This script benchmarks INSERT performance into the `finances_transaction` table.


-- 1. Set a random wallet_id.
\set random_wallet_id random_zipfian(1, 20 * :scale, 1.1)

-- 2. Generate the components for our random decimal amount.
\set random_whole random(-1000000000, 1000000000)
\set random_fraction random(0, 999999999999999999)

-- 3. The actual query to be benchmarked.
INSERT
    INTO finances_transaction (txid, wallet_id, amount)
VALUES (
  gen_random_uuid(),
  :random_wallet_id,
  (:random_whole + (:random_fraction / 1000000000000000000.0))::numeric
);

