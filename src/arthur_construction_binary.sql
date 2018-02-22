SELECT *
FROM (
        (SELECT ane.id,
                '1' target,
                    ane.desc_of_operations
         FROM arthur_ncci_eval_50k ane,
              ncci_class_ind_lookup ncl
         WHERE ncl.ncci_class_id = ane.target
           AND ncl.ncci_filing_industry_group = 'CONTRACTING' LIMIT 16000)
      UNION
        (SELECT ane.id,
                '0' target,
                    ane.desc_of_operations
         FROM arthur_ncci_eval_50k ane,
              ncci_class_ind_lookup ncl
         WHERE ncl.ncci_class_id = ane.target
           AND ncl.ncci_filing_industry_group <> 'CONTRACTING' LIMIT 16000)) sub
ORDER BY id