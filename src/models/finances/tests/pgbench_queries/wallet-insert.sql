-- This script benchmarks INSERT performance into the `finances_wallet` table.


-- 1. Generate the components for our random decimal balance.
\set random_whole random(1, 100000000)
\set random_fraction random(0, 999999999999999999)

-- 2. The actual query to be benchmarked.
INSERT INTO finances_wallet (label, balance)
VALUES (
  md5(random()::text),
  (:random_whole + (:random_fraction / 1000000000000000000.0))::numeric
);
