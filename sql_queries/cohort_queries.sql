-------------------------
-- INCLUSION CRITERIA: --
-------------------------

	-- AGE > 15
	-----------

query = """
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
"""

# person_age = pd.read_sql_query(query, conn)


-- ICU Units (tbc)
------------------
query = """
SELECT care_site_id, care_site_name, place_of_service_source_value
FROM care_site
WHERE LOWER(place_of_service_source_value) LIKE '%intensive%'     -- selecting ICUs
AND LOWER(place_of_service_source_value) NOT LIKE '%neonatal%'    -- removing Neonatal ICUs
LIMIT 100;
"""

# ICU = pd.read_sql_query(query, conn)