--3.1.1
SELECT iss.School_ID, COUNT(*) AS TotalIssues
FROM Issue AS iss
WHERE YEAR(iss.Start_date) = input_year OR MONTH(iss.Start_date) = input_month
GROUP BY iss.School_ID;

--3.1.2
SELECT ba.Book_author_name
FROM Book_records as br
INNER JOIN Book_category as bc ON bc.Book_ID = br.Book_ID
INNER JOIN Book_author as ba ON ba.Book_ID = br.Book_ID
WHERE bc.Book_category = 'Computers';

SELECT ua.User_firstname, ua.User_lastname
FROM User_account as ua
WHERE ua.User_role = 1
  AND ua.User_ID IN (
    SELECT iss.User_ID
    FROM Issue as iss
    INNER JOIN Book_category as bc ON bc.Book_ID = iss.Book_ID
    WHERE bc.Book_category= 'Computers' AND YEAR(iss.Start_date) = 2023
    GROUP BY ua.User_ID
)

--3.1.3
SELECT COUNT(*) as num_issues
FROM Issue as iss
INNER JOIN User_account as ua ON iss.User_ID = ua.User_ID
WHERE ua.User_role = 1 AND ua.User_age < 40
GROUP BY ua.User_ID
ORDER BY num_issues DESC
LIMIT 5;

--3.1.4
SELECT ba.Book_author_name
FROM Book_author as ba
WHERE ba.Book_ID NOT IN (
  SELECT iss.Book_ID
  FROM Issue as iss
)
GROUP BY ba.Book_author_name

--3.1.5
SELECT ua.User_firstname, ua.User_lastname
FROM User_account as ua
WHERE ua.User_ID = (
    SELECT op.User_ID
    FROM Operator as op
    INNER JOIN Issue as iss ON op.School_ID = iss.School_ID
    GROUP BY op.User_ID, YEAR(iss.Start_date)
    HAVING COUNT(iss.Issue_ID) > 20
)

--3.1.6
SELECT DISTINCT
    LEAST(bc1.Book_category, bc2.Book_category) AS category1,
    GREATEST(bc1.Book_category, bc2.Book_category) AS category2,
    COUNT(*) AS num_borrowings
FROM Book_records AS br
JOIN Book_category AS bc1 ON br.Book_ID = bc1.Book_ID
JOIN Book_category AS bc2 ON br.Book_ID = bc2.Book_ID AND bc1.Book_category <> bc2.Book_category
GROUP BY category1, category2
ORDER BY num_borrowings DESC
LIMIT 3;


--3.1.7
SELECT ba2.Book_author_name AS authors
FROM Book_author AS ba2
GROUP BY ba2.Book_author_name
HAVING COUNT(*) + 5 <
  (SELECT MAX(book_counts)
  FROM (
    SELECT COUNT(*) AS book_counts
    FROM Book_author as ba
    GROUP BY ba.Book_author_name
  ) AS subquery
);
