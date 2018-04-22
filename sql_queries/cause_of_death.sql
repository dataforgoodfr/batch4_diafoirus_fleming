-----------------------------------
-- DEFINING CAUSES/TYPE OF DEATH --
-----------------------------------

-- DEAD PATIENTS
----------------

SELECT DISTINCT(d.person_id), d.death_datetime
FROM visit_detail vd
JOIN death d ON vd.person_id = d.person_id
WHERE vd.discharge_to_source_value LIKE '%DEAD%'
;


-- CONDITIONS
-------------

SELECT co.person_id, co.condition_concept_name, co.visit_occurrence_id, vo.visit_start_datetime, vo.visit_end_datetime
FROM condition_occurrence co
JOIN visit_occurrence vo ON vo.visit_occurrence_id = co.visit_occurrence_id
ORDER BY co.person_id, vo.visit_start_datetime
;