-------------------------
-- INCLUSION CRITERIA: --
-------------------------

-- AGE > 15
-----------

WITH person_age AS (
    SELECT p.person_id, (v.visit_start_date - p.birth_datetime)/365.25 age
    FROM person p
    LEFT OUTER JOIN visit_occurrence v
    ON p.person_id = v.person_id)
SELECT person_id, age
FROM person_age
WHERE age > 15            -- including persons older than 15
AND age < 150             -- removing any outliers
ORDER BY age
;

-- ICU Units (tbc)
------------------

WITH icu AS (
    SELECT care_site_id, care_site_name, place_of_service_source_value
    FROM care_site
    WHERE LOWER(place_of_service_source_value) LIKE '%intensive%'     -- selecting ICUs
    AND LOWER(place_of_service_source_value) NOT LIKE '%neonatal%'    -- removing Neonatal ICUs
    )
SELECT vd.person_id, icu.place_of_service_source_value
FROM visit_detail vd
JOIN icu ON icu.care_site_id = vd.care_site_id