-- =========================================
-- BASIC EXPLORATION
-- =========================================

-- Total number of records
SELECT COUNT(*) AS total_rows FROM university_rankings;

--  View first 10 records
SELECT * FROM university_rankings LIMIT 10;

-- List all distinct years in the dataset
SELECT DISTINCT year
FROM university_rankings
ORDER BY year;

--  How many universities appear in multiple years
SELECT institution, COUNT(DISTINCT year) AS years_present
FROM university_rankings
GROUP BY institution
HAVING COUNT(DISTINCT year) > 1
ORDER BY years_present DESC, institution
LIMIT 10;

--  Average rank per country in 2015
SELECT country,
       ROUND(AVG(world_rank), 2) AS avg_rank_2015
FROM university_rankings
WHERE year = 2015
GROUP BY country
ORDER BY avg_rank_2015 ASC
LIMIT 10;

--  Year-over-year change in average score
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


-- =========================================
-- CRUD OPERATIONS
-- =========================================

-- (C) CREATE: Add new university (Duke Tech, 2014)
INSERT INTO university_rankings (institution, country, world_rank, score, year)
VALUES ('Duke Tech', 'USA', 350, 60.5, 2014);

-- (R) READ: Verify Duke Tech insertion
SELECT * FROM university_rankings WHERE institution = 'Duke Tech' AND year = 2014;

-- (R) READ: Count Japanese universities in top 200 in 2013
SELECT COUNT(*) AS japan_top200_2013
FROM university_rankings
WHERE country = 'Japan'
  AND year = 2013
  AND world_rank <= 200;

-- (U) UPDATE: Increase University of Oxford 2014 score by 1.2
UPDATE university_rankings
SET score = score + 1.2
WHERE institution = 'University of Oxford'
  AND year = 2014;

-- (R) READ: Verify University of Oxford score update
SELECT institution, year, score FROM rankings WHERE institution = 'University of Oxford' AND year = 2014;

-- (D) DELETE: Remove 2015 universities with score < 45
DELETE FROM university_rankings
WHERE year = 2015
  AND score < 45;

-- (R) READ: Verify deletion of low-score 2015 universities
SELECT COUNT(*) FROM university_rankings WHERE year = 2015 AND score < 45;



