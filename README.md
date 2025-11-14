# AnalyticsPipeline
Real-time e-commerce analytics pipeline
This is a build of a production-style pipeline. 

### Project architecture and scope
#### High-level components
<li> Sources: Simulated e-commerce events (clicks, carts, purchases) and external APIs (currency rates).
<li> Streaming ingestion: Kafka topics for each event type.
<li> Data lake: S3 buckets for raw and curated layers.
<li> Batch processing: Spark jobs for daily ETL and dimension builds.
<li> Streaming processing: Kafka Streams or Flink for rolling aggregations.
<li> Warehouse: Redshift or PostgreSQL with star schema.
<li> Orchestration: Airflow DAGs across batch jobs and checks.
<li> Analytics: A dashboard for real-time sales and funnel metrics.
<li> Ops: Docker, optional Kubernetes, CI/CD, data quality, monitoring.

Milestones
M1: Local dev environment + data generator + Kafka topics.
M2: S3 raw layer + Spark batch job + schema.
M3: Streaming aggregations + stateful windowing.
M4: Warehouse load + BI dashboard.
M5: Airflow orchestration + alerts + docs.

#### Environment setup
##### Core tooling
<li> Containers: Docker for reproducibility.
<li> Local cloud emulators (optional): LocalStack for S3, or use real AWS.
<li> Languages: Python (Airflow, utilities), Scala or Python for Spark; Java/Scala for Kafka Streams or Flink.
<li> Infra as code: Terraform (optional) for AWS resources.

##### Repository structure
<li><b>repo/</b>
<li><b>infra/</b> Dockerfiles, Terraform
<li><b>ingestion/</b> data generator, Kafka producers
<li><b>streaming/</b> Kafka Streams or Flink jobs
<li><b>batch/</b> Spark ETL jobs
<li><b>orchestration/</b> Airflow DAGs and operators
<li><b>warehouse/</b> DDL, dbt models (optional)
<li><b>analytics/</b> dashboard assets
<li><b>tests/</b> unit/integration tests
<li><b>docs/</b> architecture, runbooks

##### Data design and schemas
###### Event schemas (JSON)
**Clicks**:
Required: event_id, user_id, session_id, product_id, ts, page, referrer

**Cart**:
Required: event_id, user_id, session_id, product_id, quantity, ts

**Purchase**:
Required: event_id, user_id, session_id, items[], total_amount, currency, ts

##### Dimensions and facts (star schema)
<li> **Dimensions**: dim_user, dim_product, dim_time, dim_currency
<li> **Facts**: fact_clicks, fact_cart, fact_orders
<li> **Surrogate keys**: Use warehouse-generated IDs for dims; facts reference them.
