**Milestone 1**

**Module 1: Data Collection \& Management**
Objective: To architect a scalable data storage solution and automate the ingestion of eco-friendly material attributes.

1.1 Database Architecture
A relational database schema was designed using PostgreSQL to maintain data integrity and support complex analytical queries. The schema consists of two primary entities:

* materials Table: Categorizes raw attributes including material type, mechanical strength, biodegradability index, CO\_2 emission scores, and unit costs.
* products Table: Defines product dimensions across various industries such as Electronics, Food \& Beverage, and Healthcare.

1.2 Data Ingestion Strategy (db\_ingestion.py)
To ensure high-performance data loading, bypassed standard iterative insertion methods in favor of a Bulk Stream Ingestion approach:

* Buffer Management: Utilized io.StringIO to create an in-memory text stream of the material dataset.
* psycopg2 copy\_from: Leveraged the PostgreSQL COPY command to pipe data directly into the database. This reduced ingestion time significantly compared to standard INSERT statements.
* Tech Stack: PostgreSQL 15, psycopg2-binary, Pandas.

**Module 2: Data Cleaning and Feature Engineering**  
Objective: To transform raw data into a normalized, high-signal dataset suitable for machine learning model training.

2.1 Data Cleaning \& Validation

* Numerical Handling: Applied pd.to\_numeric with coercion to identify data type inconsistencies.
* Imputation: Missing values were handled via Median Imputation to preserve the central tendency of the material properties and prevent bias in the CO\_2 and Cost predictions.
* Feature Scaling: Implemented the MinMaxScaler to transform all numerical features into a uniform range of \[0, 1]. This normalization is critical for algorithms like Random Forest and XGBoost to prevent features with larger magnitudes from dominating the objective function.

2.2 Advanced Feature Engineering (data\_pipeline.py) developed three proprietary indices to serve as the "Sustainability Intelligence" of the system:

* CO\_2 Impact Index: A weighted composite score reflecting environmental damage.
* Cost Efficiency Index: A metric used to evaluate the economic viability relative to material durability.
* Material Suitability Score: The primary target variable that ranks materials based on a balance of biodegradability, environmental impact, and fiscal cost.
