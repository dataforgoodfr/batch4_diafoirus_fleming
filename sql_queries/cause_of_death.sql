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

SELECT co.person_id person_id, co.condition_concept_name condition_name, c.concept_name condition_type, co.visit_occurrence_id, vo.visit_start_datetime, vo.visit_end_datetime
FROM condition_occurrence co
JOIN visit_occurrence vo ON vo.visit_occurrence_id = co.visit_occurrence_id
JOIN concept c ON c.concept_id = co.condition_type_concept_id
ORDER BY co.person_id, vo.visit_start_datetime, c.concept_name
;