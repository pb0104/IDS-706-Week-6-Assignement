
# University Rankings SQLite Assignment

## Project Overview

This assignment is part of the **Data Storage and Management** series. The purpose of this project is to:

1. Explore a relational database using **SQL and Python**.
2. Perform **CRUD operations** on the database.
3. Analyze data using basic statistics and summary operations.

The database used is a **SQLite database** (`university_database.db`) containing university rankings from 2012 to 2015.


## Project Structure

```
university_rankings_project/
│
├─ data/
│   └─ university_database.db       # Provided SQLite database
│
├─ scripts/
│   ├─ query.py                     # Python script for exploration and CRUD
│   └─ queries.sql                  # SQL statements for exploration + CRUD
│
├─ README.md                        # This documentation
└─ requirements.txt                 # Optional Python dependencies
```



## Database Schema

The database contains a single table:

**`university_rankings`**

| Column Name | Data Type |
| ----------- | --------- |
| institution | TEXT      |
| country     | TEXT      |
| world_rank  | INTEGER   |
| score       | REAL      |
| year        | INTEGER   |


## Initial Data Exploration

The following SQL queries were executed to summarize and understand the dataset:

1. **Total number of records**

```sql
SELECT COUNT(*) AS total_rows FROM university_rankings;
```

2. **View first 10 records**

```sql
SELECT * FROM university_rankings LIMIT 10;
```

3. **List all distinct years in the dataset**

```sql
SELECT DISTINCT year FROM university_rankings ORDER BY year;
```

4. **Universities appearing in multiple years**

```sql
SELECT institution, COUNT(DISTINCT year) AS years_present
FROM university_rankings
GROUP BY institution
HAVING COUNT(DISTINCT year) > 1
ORDER BY years_present DESC, institution
LIMIT 10;
```

5. **Average world rank per country in 2015**

```sql
SELECT country,
       ROUND(AVG(world_rank), 2) AS avg_rank_2015
FROM university_rankings
WHERE year = 2015
GROUP BY country
ORDER BY avg_rank_2015 ASC
LIMIT 10;
```

6. **Year-over-year change in average score**

```sql
WITH yearly_avg AS (
    SELECT year, AVG(score) AS avg_score
    FROM university_rankings
    GROUP BY year
)
SELECT a.year,
       ROUND(a.avg_score, 2) AS avg_score,
       ROUND(a.avg_score - b.avg_score, 2) AS change_from_last_year
FROM yearly_avg a
LEFT JOIN yearly_avg b
     ON a.year = b.year + 1
ORDER BY a.year;
```


> These queries are executed in `query.py` using Python and Pandas for clearer output.


## CRUD Operations

### 1. **Create**

* **Insert Duke Tech** for year 2014:

  ```sql
  INSERT INTO university_rankings (institution, country, world_rank, score, year)
  VALUES ('Duke Tech', 'USA', 350, 60.5, 2014);
  ```
* Verification confirms the row was added.

### 2. **Read**

* Count universities from **Japan in the top 200** in 2013:

  ```sql
  SELECT COUNT(*) FROM university_rankings
  WHERE country = 'Japan' AND year = 2013 AND world_rank <= 200;
  ```
* Result returned the correct count.

### 3. **Update**

* **University of Oxford 2014 score** increased by +1.2 points:

  ```sql
  UPDATE university_rankings
  SET score = score + 1.2
  WHERE institution = 'University of Oxford' AND year = 2014;
  ```
* Verified by selecting the updated row.

### 4. **Delete**

* Remove universities in **2015 with score < 45**:

  ```sql
  DELETE FROM university_rankings
  WHERE year = 2015 AND score < 45;
  ```
* Verified by checking remaining 2015 rows.

---

## How to Run

1. **Install dependencies** (optional, if using Pandas):

```bash
pip install pandas
```

2. **Run Python script**:

```bash
python scripts/query.py
```

3. **Run SQL file in SQLite CLI**:

```bash
sqlite3 data/university_database.db < scripts/queries.sql
```

> Both methods execute initial exploration and CRUD operations.


## Results & Observations

* Dataset covers **2012–2015** with hundreds of universities.
* Top countries by representation: **USA, UK, Germany**.
* Average score gradually increases from 2012 to 2015.
* Universities appearing in multiple years are mostly top-ranked institutions.
* Insert, update, and delete operations were successfully applied.


## Notes

* All SQL queries are included in `queries.sql`.
* Python script `query.py` automates execution and prints results.
* The database used is `university_database.db`.




## 📜 Author

- Author: PRANSHUL BHATNAGAR  
- Date: 05 October 2025  