WITH 
CombinedResources as (
    SELECT name, id FROM _workbooks
    group by name, id 
    union ALL
    SELECT name, id FROM _datasources
    group by name, id 
),
TaskDurations AS (
    SELECT
        task_id,
        AVG(completed_at - started_at) AS avg_duration
    FROM
        background_jobs
    GROUP BY
        task_id
),
PriorityAdjustments AS (
    SELECT
        task_id,
        CASE
            WHEN avg_duration <= interval '1 minute' THEN 10
            WHEN avg_duration < interval '15 minutes' THEN 25
            WHEN avg_duration < interval '30 minutes' THEN 30
            WHEN avg_duration < interval '60 minutes' THEN 35
            WHEN avg_duration < interval '90 minutes' THEN 40
            WHEN avg_duration < interval '180 minutes' THEN 60
            WHEN avg_duration >= interval '180 minutes' THEN 100
            ELSE 50
        END AS new_priority
    FROM
        TaskDurations
),
CombinedPriorities AS (
    SELECT
        ss.url_namespace AS site_urlname,
        ss.name AS site_name,
        sc.name AS schedule_name,
        ts.priority AS old_priority,
        pa.new_priority,
        ts.obj_id
    FROM
        tasks ts
    INNER JOIN _schedules sc ON ts.schedule_id = sc.id
    INNER JOIN _sites ss ON ts.site_id = ss.id
    INNER JOIN PriorityAdjustments pa ON ts.id = pa.task_id
    WHERE
        (ts.type = 'IncrementExtractTask' OR ts.type = 'RefreshExtractTask')
    GROUP BY
        ss.url_namespace, 
        ss.name,
        sc.name, 
        ts.priority, 
        pa.new_priority, 
        ts.obj_id
), 
FinalQuery as (
	select 
		cp.site_urlname, 
        cp.site_name,
		cr.name as "extract_name",
		cp.schedule_name, 
		cp.old_priority,
        cp.new_priority
	from
		CombinedPriorities cp
	inner join 
		CombinedResources cr on cp.obj_id = cr.id
)
SELECT * FROM FinalQuery
ORDER BY site_name, extract_name, schedule_name;