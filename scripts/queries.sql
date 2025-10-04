-- =========================================
-- University Rankings - SQLite Assignment
-- =========================================

-- BASIC EXPLORATION
SELECT * FROM rankings LIMIT 10;
SELECT COUNT(*) AS total_rows FROM rankings;
SELECT DISTINCT country FROM rankings;
SELECT year, AVG(score) AS avg_score
FROM rankings
GROUP BY year;
SELECT world_rank, institution, country, score
FROM rankings
WHERE year = 2015
ORDER BY world_rank
LIMIT 10;

-- =========================================
-- CRUD OPERATIONS
-- =========================================

-- (C) CREATE: Add new university (Duke Tech, 2014)
INSERT INTO rankings (institution, country, world_rank, score, year)
VALUES ('Duke Tech', 'USA', 350, 60.5, 2014);

-- (R) READ: Count Japanese universities in top 200 in 2013
SELECT COUNT(*) AS japan_top200_2013
FROM rankings
WHERE country = 'Japan'
  AND year = 2013
  AND world_rank <= 200;

-- (U) UPDATE: Increase University of Oxford 2014 score by 1.2
UPDATE rankings
SET score = score + 1.2
WHERE institution = 'University of Oxford'
  AND year = 2014;

-- (D) DELETE: Remove 2015 universities with score < 45
DELETE FROM rankings
WHERE year = 2015
  AND score < 45;

-- =========================================
-- OPTIONAL CHECKS AFTER EACH OPERATION
-- =========================================
SELECT * FROM rankings WHERE institution = 'Duke Tech' AND year = 2014;
SELECT institution, year, score FROM rankings WHERE institution = 'University of Oxford' AND year = 2014;
SELECT COUNT(*) FROM rankings WHERE year = 2015 AND score < 45;
