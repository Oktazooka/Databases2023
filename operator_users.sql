SELECT br.Book_title, ba.Book_author_name
FROM Book_record AS br
INNER JOIN Book_author AS ba ON br.Book_ID = ba.Book_ID
INNER JOIN Book_category AS bc ON br.Book_ID = bc.Book_ID
WHERE bc.Book_category = %s
  AND (br.Book_title = %s OR %s = '')
  AND (ba.Book_author_name = %s OR %s = '')
  AND (br.Book_copies = %s OR %s = '')

--3.2.2.
SELECT ua.User_ID
FROM User_account AS ua
INNER JOIN Issue AS iss ON ua.User_ID = iss.User_ID
INNER JOIN Delayed_issue AS dis ON dis.Issue_ID = iss.Issue_ID
WHERE (ua.User_firstname = %s  OR %s = '')
  AND (ua.User_lastname = %s OR %s = '')
  AND (dis.Days_delayed = %s OR %s = '')
GROUP BY ua.User_ID
HAVING COUNT(*) >= 1;

--3.2.3
SELECT ua.User_ID, AVG(r.Rating), bc.Book_category
FROM User_account AS ua
INNER JOIN Review AS r ON ua.User_ID = r.User_ID
INNER JOIN Book_category AS bc ON r.Book_ID = bc.Book_ID
WHERE (ua.User_ID = %s OR %s = '')
  AND (bc.Book_category = %s OR %s ='')
GROUP BY ua.User_ID, bc.Book_category;

--3.3.1
SELECT br.Book_title, bc.Book_category, ba.Book_author_name
FROM Book_records as br INNER JOIN Book_category as bc
ON br.Book_ID = bc.Book_ID
INNER JOIN Book_author AS ba
ON br.Book_ID = ba.Book_ID

-- 3.3.2
SELECT br.Book_title
FROM User_account AS ua
INNER JOIN Issue AS iss ON ua.User_ID = iss.User_ID
INNER JOIN Book_records AS br ON iss.Book_ID = br.Book_ID
