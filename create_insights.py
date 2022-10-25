from common.base import session

# Create the view with the appropriate metrics
query = """
create or replace view insights AS
SELECT county,
       count(*) AS sales_count,
       sum(CAST(price AS int)) AS sales_total,
       max(CAST(price AS int)) AS sales_max,
       min(CAST(price AS int)) AS sales_min,
       avg(CAST(price AS int))::numeric(10,2) AS sales_avg
FROM ppr_clean_all
GROUP BY county
"""

# Execute and commit
session.execute(query)
session.commit()