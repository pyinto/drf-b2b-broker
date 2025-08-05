-- This script benchmarks SELECT performance on the `finances_wallet` table.


-- 1. Generate the components for our random decimal balance.
\set random_whole random(0, 1000000)
\set random_fraction random(0, 999999999999999999)

-- 2. The actual query to be benchmarked.
SELECT
  id,
  label,
  balance

FROM
  finances_wallet

WHERE
  balance > (:random_whole + (:random_fraction / 1000000000000000000.0))::numeric

ORDER BY
  balance DESC, id DESC

LIMIT
    100
;
