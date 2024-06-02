select * from
(
    select 
        bj.title "Name", 
        bj.site_id, 
        ss.name,
        bj.priority "Original Priority", 
        bj.subtitle "Object type", 
        avg(completed_at - started_at) "Avg runtime", 
        sc.name "Schedule",
        case 
            when avg(completed_at - started_at) <= '1 minutes'::interval then 10
            when avg(completed_at - started_at) < '15 minutes'::interval then 25
            when avg(completed_at - started_at) < '30 minutes'::interval then 30
            when avg(completed_at - started_at) < '60 minutes'::interval then 35
            when avg(completed_at - started_at) < '90 minutes'::interval then 40
            when avg(completed_at - started_at) < '180 minutes'::interval then 60
            when avg(completed_at - started_at) > '3 hours'::interval then 100
            else 50 
        end "New Priority"
    from
        background_jobs bj,
        workbooks wb,
        schedules sc,
        sites ss,
        tasks ts
    where 
        bj.job_type like '%_extracts%' and
        ss.id=wb.site_id and
        bj.subtitle = 'Workbook' and
        ts.obj_type = 'Workbook' and
        ts.type = 'RefreshExtractTask' and
        wb.name = bj.title and
        ts.schedule_id = sc.id and
        ts.obj_id = wb.id and
        bj.completed_at is not null
    group by 
        bj.title, 
        bj.subtitle, 
        sc.name, 
        bj.site_id, 
        ss.name, 
        bj.priority,
        --wb.id

    union

    select 
        bj.title "Name", 
        bj.site_id, 
        ss.name, 
        bj.priority "Original Priority", 
        bj.subtitle "Object type", 
        avg(completed_at - started_at) "Avg runtime", 
        sc.name "Schedule",
        case 
            when avg(completed_at - started_at) <= '1 minutes'::interval then 10
            when avg(completed_at - started_at) < '15 minutes'::interval then 25
            when avg(completed_at - started_at) < '30 minutes'::interval then 30
            when avg(completed_at - started_at) < '60 minutes'::interval then 35
            when avg(completed_at - started_at) < '90 minutes'::interval then 40
            when avg(completed_at - started_at) < '180 minutes'::interval then 60
            when avg(completed_at - started_at) > '3 hours'::interval then 100
            else 50 
        end "New Priority"
    from
        background_jobs bj,
        sites ss,
        datasources ds,
        schedules sc,
        tasks ts
    where 
        bj.job_type like '%_extracts%' and
        ss.id = ds.site_id and
        bj.subtitle = 'Datasource' and
        ts.obj_type = 'Datasource' and
        ts.type = 'RefreshExtractTask' and
        ds.name = bj.title and
        ts.schedule_id = sc.id and
        ts.obj_id = ds.id and
        bj.completed_at is not null
    group by 
        bj.title, 
        bj.subtitle, 
        sc.name, 
        bj.site_id, 
        ss.name, 
        bj.priority,
        --ds.id
) mn
order by 4,3,1