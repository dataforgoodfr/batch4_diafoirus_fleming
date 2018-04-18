select 
	q1.admission_location as admission_location, q1.diagnosis as diagnosis, 
	avg(q1.length) as stay_duration, sum(q1.birth) as births, sum(q1.death) as deaths, count(distinct q1.subject_id) as total
from
	(select 
		a.subject_id as subject_id, a.admittime as admittime, a.admission_location as admission_location, a.diagnosis as diagnosis,
		DATE_PART('day', dischtime - admittime)+DATE_PART('hours', dischtime - admittime)/24+DATE_PART('minutes', dischtime - admittime)/(24*60) as length,
		case when p.dob between a.admittime and a.dischtime then 1 else 0 end as birth,
		case when p.dod between a.admittime and a.dischtime then 1 else 0 end as death
	from
		admissions a
		left outer join patients p
		on a.subject_id = p.subject_id) q1
group by
	q1.admission_location, q1.diagnosis;



-------------
-- Split by unit
------------

select 
	q1.admission_location as admission_location, avg(q1.length) as stay_duration, sum(q1.birth) as births, sum(q1.death) as deaths, count(distinct q1.subject_id) as total
from
	(select 
		a.subject_id as subject_id, a.admittime as admittime, a.admission_location as admission_location, a.diagnosis as diagnosis,
		DATE_PART('day', dischtime - admittime)+DATE_PART('hours', dischtime - admittime)/24+DATE_PART('minutes', dischtime - admittime)/(24*60) as length,
		case when p.dob between a.admittime and a.dischtime then 1 else 0 end as birth,
		case when p.dod between a.admittime and a.dischtime then 1 else 0 end as death
	from
		admissions a
		left outer join patients p
		on a.subject_id = p.subject_id) q1
group by
	q1.admission_location;



-------------
-- Stats by diagnostic
------------

select 
	q1.year as year, q1.diagnosis as diagnosis, sum(q1.birth) as births, sum(q1.death) as deaths, count(distinct q1.subject_id) as total
from
	(select 
		a.subject_id as subject_id, a.admittime as admittime, a.admission_location as admission_location, a.diagnosis as diagnosis,
		DATE_PART('year', admittime) as year,
		DATE_PART('day', dischtime - admittime)+DATE_PART('hours', dischtime - admittime)/24+DATE_PART('minutes', dischtime - admittime)/(24*60) as length,
		case when p.dob between a.admittime and a.dischtime then 1 else 0 end as birth,
		case when p.dod between a.admittime and a.dischtime then 1 else 0 end as death
	from
		admissions a
		left outer join patients p
		on a.subject_id = p.subject_id) q1
group by
	q1.year, q1.diagnosis
order by
	sum(q1.death)/count(distinct q1.subject_id) desc;



