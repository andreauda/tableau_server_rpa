WITH 
-- union between _workbooks and _datasources
CombinedResources as (
	SELECT 
		ws.name, 
		ws.id as content_id,
		ws.id as id_url, --i need a second one for the union all
		'workbooks' as content_type
	FROM _workbooks ws
	group by ws.name, content_id, id_url, content_type
	union all
	SELECT 
		ds.name, 
		ds.id as content_id,
        /* Some values of _datasources.id are associated to multiple values of data_connections.id,
        because a data source can contain multiple data connections.
        However, each data_connections.id land to the same page of the datasource,
        for this reason we use the max of data_connections.id
        (also the min would work) */
		max(dcs.id) as id_url, 
		'datasources' as content_type
	FROM _datasources ds
    /* the id of the url is not _datasources.id, 
    but data_connections.id */
	inner join data_connections dcs on ds.id = dcs.datasource_id 
	group by ds.name, content_id, content_type
),
-- create the average durations grouped by task id and assign them a new value
PriorityAdjustments AS (
    select
    	task_id,
        CASE
            WHEN AVG(completed_at - started_at) <= interval '1 minute' THEN 10
            WHEN AVG(completed_at - started_at) < interval '2 minutes' THEN 25
            WHEN AVG(completed_at - started_at) < interval '3 minutes' THEN 30
            WHEN AVG(completed_at - started_at) < interval '6 minutes' THEN 35
            WHEN AVG(completed_at - started_at) < interval '9 minutes' THEN 40
            WHEN AVG(completed_at - started_at) < interval '18 minutes' THEN 60
            WHEN AVG(completed_at - started_at) >= interval '18 minutes' THEN 100
            ELSE 50
        END AS new_priority
    FROM
        background_jobs
    GROUP BY
        task_id
),
-- let's join the tables: tasks, _schedules and _sites
-- then, we can join this result with the above PriorityAdjustments
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
-- where we join CombinedPriorities and CombinedResources (union between _workbooks and _datasources)
FinalQuery as (
	select 
		cp.site_urlname, 
        cp.site_name,
        cr.content_type,
        cr.id_url,
		cr.name as "extract_name",
		cp.schedule_name, 
		cp.old_priority,
        cp.new_priority
	from
		CombinedPriorities cp
	inner join 
		CombinedResources cr on cp.obj_id = cr.content_id 
)
SELECT * FROM FinalQuery
where 
    -- let's keep only changes in priority
    old_priority <> new_priority
ORDER BY 
    site_name, extract_name, schedule_name