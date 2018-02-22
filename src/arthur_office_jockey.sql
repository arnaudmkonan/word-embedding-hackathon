SELECT id,
          CASE
              WHEN target IN('8810', '8742', '8820', '8723', '8721') THEN '1'
              ELSE '0'
          END AS target,
          DESC_of_operations
   FROM arthur_ncci_eval_50k
