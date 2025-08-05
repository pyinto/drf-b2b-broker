-- This script benchmarks SELECT performance into the `finances_transaction` table.


-- 1. Set a random wallet_id.
\set random_wallet_id random_zipfian(1, 20 * :scale, 1.1)

-- 2. Generate the components for our random decimal amount.
\set random_whole random(-1000000000, 1000000000)
\set random_fraction random(0, 999999999999999999)

-- 3. Choose a random operator.
\set operator_choice random(1, 4)


-- 4. The actual query to be benchmarked.
SELECT
  id,
  txid,
  wallet_id,
  amount

FROM
  finances_transaction

WHERE
    "wallet_id" = :random_wallet_id
  AND
    CASE CAST(:operator_choice AS integer)
      WHEN 1 THEN amount >  (:random_whole + (:random_fraction / 1000000000000000000.0))::numeric
      WHEN 2 THEN amount <  (:random_whole + (:random_fraction / 1000000000000000000.0))::numeric
      WHEN 3 THEN amount <= (:random_whole + (:random_fraction / 1000000000000000000.0))::numeric
      ELSE        amount =  (:random_whole + (:random_fraction / 1000000000000000000.0))::numeric
    END

ORDER BY
  "id" DESC

LIMIT
    100
;
