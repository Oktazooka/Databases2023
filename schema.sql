-- test_db.Authentication_system definition

CREATE TABLE `Authentication_system` (
  `Username` varchar(30) NOT NULL,
  `Password` varchar(30) NOT NULL,
  PRIMARY KEY (`Username`,`Password`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;


-- test_db.School_unit definition

CREATE TABLE `School_unit` (
  `School_ID` int(1) NOT NULL AUTO_INCREMENT,
  `School_name` varchar(30) NOT NULL,
  `School_operator` varchar(30) NOT NULL,
  `School_headmaster` varchar(30) NOT NULL,
  `School_email` varchar(30) DEFAULT NULL,
  `School_city` varchar(30) DEFAULT NULL,
  `School_street` varchar(30) DEFAULT NULL,
  `School_street_number` int(3) DEFAULT NULL,
  `School_postal_code` int(5) DEFAULT NULL,
  PRIMARY KEY (`School_ID`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;


-- test_db.Admin definition

CREATE TABLE `Admin` (
  `Username` varchar(30) NOT NULL,
  `Password` varchar(30) NOT NULL,
  KEY `Admin_FK` (`Username`,`Password`),
  CONSTRAINT `Admin_FK` FOREIGN KEY (`Username`, `Password`) REFERENCES `Authentication_system` (`Username`, `Password`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;


-- test_db.Backup definition

CREATE TABLE `Backup` (
  `Backup_ID` int(2) NOT NULL AUTO_INCREMENT,
  `School_ID` int(1) NOT NULL,
  `Filename` varchar(50) NOT NULL,
  PRIMARY KEY (`Backup_ID`),
  KEY `Backup_FK` (`School_ID`),
  CONSTRAINT `Backup_FK` FOREIGN KEY (`School_ID`) REFERENCES `School_unit` (`School_ID`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;


-- test_db.Book_records definition

CREATE TABLE `Book_records` (
  `Book_ID` int(6) NOT NULL AUTO_INCREMENT,
  `Book_title` varchar(500) NOT NULL,
  `Book_ISBN` varchar(13) NOT NULL,
  `Book_keywords` varchar(1000) DEFAULT NULL,
  `Book_publisher` varchar(200) DEFAULT NULL,
  `Book_pages` int(4) DEFAULT NULL,
  `Book_language` varchar(30) DEFAULT NULL,
  `Book_abstract` varchar(10000) DEFAULT NULL,
  `Book_image` varchar(1000) DEFAULT NULL,
  `Book_copies` int(2) NOT NULL,
  `School_ID` int(1) NOT NULL,
  PRIMARY KEY (`Book_ID`),
  KEY `Book_records_FK` (`School_ID`),
  CONSTRAINT `Book_records_FK` FOREIGN KEY (`School_ID`) REFERENCES `School_unit` (`School_ID`)
) ENGINE=InnoDB AUTO_INCREMENT=405 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;


-- test_db.Review definition

CREATE TABLE `Review` (
  `Review_ID` int(4) NOT NULL AUTO_INCREMENT,
  `Book_ID` int(6) NOT NULL,
  `Rating` int(1) NOT NULL,
  `Review_text` varchar(1000) NOT NULL,
  `School_ID` int(1) NOT NULL,
  `User_ID` int(4) NOT NULL,
  PRIMARY KEY (`Review_ID`),
  KEY `Review_FK` (`Book_ID`),
  KEY `Review_FK_1` (`School_ID`),
  CONSTRAINT `Review_FK` FOREIGN KEY (`Book_ID`) REFERENCES `Book_records` (`Book_ID`),
  CONSTRAINT `Review_FK_1` FOREIGN KEY (`School_ID`) REFERENCES `School_unit` (`School_ID`),
  CONSTRAINT `Review_CHECK` CHECK (`Rating` >= 1 and `Rating` <= 5)
) ENGINE=InnoDB AUTO_INCREMENT=33 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;


-- test_db.School_phone definition

CREATE TABLE `School_phone` (
  `School_ID` int(1) NOT NULL,
  `Phone_number` int(10) DEFAULT NULL,
  PRIMARY KEY (`School_ID`),
  CONSTRAINT `School_phone_FK` FOREIGN KEY (`School_ID`) REFERENCES `School_unit` (`School_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;


-- test_db.User_account definition

CREATE TABLE `User_account` (
  `User_ID` int(4) NOT NULL AUTO_INCREMENT,
  `Username` varchar(30) NOT NULL,
  `Password` varchar(30) NOT NULL,
  `Status` tinyint(1) NOT NULL,
  `School_ID` int(1) NOT NULL,
  `User_role` tinyint(1) NOT NULL,
  `User_date_of_birth` date DEFAULT NULL,
  `User_age` int(2) DEFAULT NULL,
  `User_firstname` varchar(100) DEFAULT NULL,
  `User_lastname` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`User_ID`),
  KEY `User_account_FK_1` (`School_ID`),
  KEY `User_account_FK` (`Username`,`Password`),
  CONSTRAINT `User_account_FK` FOREIGN KEY (`Username`, `Password`) REFERENCES `Authentication_system` (`Username`, `Password`) ON UPDATE CASCADE,
  CONSTRAINT `User_account_FK_1` FOREIGN KEY (`School_ID`) REFERENCES `School_unit` (`School_ID`)
) ENGINE=InnoDB AUTO_INCREMENT=169 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;


-- test_db.Book_author definition

CREATE TABLE `Book_author` (
  `Book_ID` int(6) NOT NULL,
  `Book_author_name` varchar(70) NOT NULL,
  KEY `Book_author_FK` (`Book_ID`),
  CONSTRAINT `Book_author_FK` FOREIGN KEY (`Book_ID`) REFERENCES `Book_records` (`Book_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;


-- test_db.Book_category definition

CREATE TABLE `Book_category` (
  `Book_ID` int(6) NOT NULL,
  `Book_category` varchar(1000) DEFAULT NULL,
  KEY `Book_category_FK` (`Book_ID`),
  CONSTRAINT `Book_category_FK` FOREIGN KEY (`Book_ID`) REFERENCES `Book_records` (`Book_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;


-- test_db.Issue definition

CREATE TABLE `Issue` (
  `Issue_ID` int(5) NOT NULL AUTO_INCREMENT,
  `Start_date` date NOT NULL,
  `Due_date` date NOT NULL,
  `User_ID` int(4) NOT NULL,
  `Book_ID` int(6) NOT NULL,
  `School_ID` int(1) NOT NULL,
  `Pending` tinyint(1) NOT NULL,
  `Completed` tinyint(1) NOT NULL,
  PRIMARY KEY (`Issue_ID`),
  KEY `Issue_FK` (`Book_ID`),
  KEY `Issue_FK_1` (`User_ID`),
  KEY `Issue_FK_2` (`School_ID`),
  CONSTRAINT `Issue_FK` FOREIGN KEY (`Book_ID`) REFERENCES `Book_records` (`Book_ID`),
  CONSTRAINT `Issue_FK_1` FOREIGN KEY (`User_ID`) REFERENCES `User_account` (`User_ID`),
  CONSTRAINT `Issue_FK_2` FOREIGN KEY (`School_ID`) REFERENCES `School_unit` (`School_ID`)
) ENGINE=InnoDB AUTO_INCREMENT=170 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;


-- test_db.Operator definition

CREATE TABLE `Operator` (
  `User_ID` int(4) NOT NULL,
  `Username` varchar(30) NOT NULL,
  `Password` varchar(30) NOT NULL,
  `School_ID` int(1) NOT NULL,
  KEY `Operator_FK_1` (`Username`,`Password`),
  KEY `Operator_FK_2` (`School_ID`),
  KEY `Operator_FK_3` (`User_ID`),
  CONSTRAINT `Operator_FK` FOREIGN KEY (`User_ID`) REFERENCES `User_account` (`User_ID`),
  CONSTRAINT `Operator_FK_1` FOREIGN KEY (`Username`, `Password`) REFERENCES `Authentication_system` (`Username`, `Password`),
  CONSTRAINT `Operator_FK_2` FOREIGN KEY (`School_ID`) REFERENCES `School_unit` (`School_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;


-- test_db.Reservation definition

CREATE TABLE `Reservation` (
  `Reservation_ID` int(5) NOT NULL AUTO_INCREMENT,
  `Start_date` date NOT NULL,
  `Due_date` date NOT NULL,
  `Book_ID` int(6) NOT NULL,
  `User_ID` int(4) NOT NULL,
  `On_hold` tinyint(1) DEFAULT NULL,
  `School_ID` int(1) NOT NULL,
  `Pending` tinyint(1) NOT NULL,
  PRIMARY KEY (`Reservation_ID`),
  KEY `Reservation_FK` (`Book_ID`),
  KEY `Reservation_FK_1` (`User_ID`),
  KEY `Reservation_FK_2` (`School_ID`),
  CONSTRAINT `Reservation_FK` FOREIGN KEY (`Book_ID`) REFERENCES `Book_records` (`Book_ID`),
  CONSTRAINT `Reservation_FK_1` FOREIGN KEY (`User_ID`) REFERENCES `User_account` (`User_ID`),
  CONSTRAINT `Reservation_FK_2` FOREIGN KEY (`School_ID`) REFERENCES `School_unit` (`School_ID`)
) ENGINE=InnoDB AUTO_INCREMENT=206 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;


-- test_db.Delayed_issue definition

CREATE TABLE `Delayed_issue` (
  `Issue_ID` int(5) NOT NULL,
  `Days_delayed` int(3) NOT NULL,
  KEY `Delayed_issue_FK` (`Issue_ID`),
  CONSTRAINT `Delayed_issue_FK` FOREIGN KEY (`Issue_ID`) REFERENCES `Issue` (`Issue_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

CREATE DEFINER=`root`@`localhost` TRIGGER book_ISBN_length
BEFORE INSERT
ON Book_records FOR EACH ROW
BEGIN
  IF LENGTH(NEW.Book_ISBN) <> 13 THEN
    SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'ISBN length must be 13 characters';
  END IF;
END;

CREATE DEFINER=`root`@`localhost` TRIGGER book_ISBN_numeric
BEFORE INSERT
ON Book_records FOR EACH ROW
BEGIN
  IF NOT (NEW.Book_ISBN REGEXP '^[0-9]+$' AND LENGTH(NEW.Book_ISBN) = 13) THEN
 	SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'ISBN must be numeric of length 13';
  END IF;
END;

CREATE DEFINER=`root`@`localhost` TRIGGER book_ISBN_numeric2
BEFORE UPDATE
ON Book_records FOR EACH ROW
BEGIN
  IF NOT (NEW.Book_ISBN REGEXP '^[0-9]+$' AND LENGTH(NEW.Book_.ISBN) = 13) THEN
 	SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'ISBN must be numeric of length 13';
  END IF;
END;

CREATE DEFINER=`root`@`localhost` TRIGGER book_update_copies
AFTER UPDATE
ON Book_records FOR EACH ROW
BEGIN
IF ((OLD.Book_copies = 0) AND (NEW.Book_copies > 0)) THEN
 	UPDATE Reservation as r
 	SET r.Hold_on = FALSE
 	WHERE r.Book_ID = NEW.Book_ID;
END IF;
END;

CREATE DEFINER=`root`@`localhost` TRIGGER num_reservations_allowed
BEFORE INSERT ON Reservation
FOR EACH ROW
BEGIN
 DECLARE num_res INT;
 DECLARE user_role BOOL;

 SELECT COUNT(r.User_ID) INTO num_res
 FROM Reservation as r
 WHERE r.User_ID = NEW.User_ID AND (DATE_ADD(r.Start_date, INTERVAL 1 WEEK) >= CURRENT_DATE());

 SELECT ua.User_role INTO user_role
 FROM User_account as ua
 WHERE ua.User_ID = NEW.User_ID;

 IF ((user_role = 1 AND num_res >= 1) OR (user_role = 0 AND num_res >= 2)) THEN
    SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Has reached the maximum number of issues';
 END IF;

END;

CREATE DEFINER=`root`@`localhost` TRIGGER delayed_issue_reservation
BEFORE INSERT
ON Reservation FOR EACH ROW
BEGIN
  IF EXISTS (
    SELECT 1
    FROM Issue AS i
    WHERE i.Issue_ID IN (
        SELECT di.Issue_ID
        FROM Delayed_issue AS di
    )
    AND i.User_ID = NEW.User_ID
  ) THEN
    SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'No reservations allowed if delayed issue';
  END IF;
END;

CREATE DEFINER=`root`@`localhost` TRIGGER already_issued
BEFORE INSERT
ON Reservation FOR EACH ROW
BEGIN
  IF NEW.User_ID IN (
    SELECT i.User_ID
    FROM Issue AS i
    WHERE i.Book_ID IN (
      SELECT br2.Book_ID
      FROM Book_records AS br
      INNER JOIN Book_records AS br2 ON br.Book_title = br2.Book_title and br.Book_ID = NEW.Book_ID
    )
  ) THEN
    SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'No reservations allowed if already issued';
  END IF;
END;

CREATE DEFINER=`root`@`localhost` TRIGGER put_on_hold
AFTER INSERT
ON Reservation FOR EACH ROW
BEGIN
  DECLARE num_copies INT;

  SELECT br.Book_copies INTO num_copies
  FROM Book_records AS br
  WHERE br.Book_ID = NEW.Book_ID;

  IF (num_copies = 0) THEN
    UPDATE Reservation AS r
    SET r.Hold_on = TRUE
    WHERE r.Book_ID = NEW.Book_ID;
  END IF;
END;

CREATE DEFINER=`root`@`localhost` TRIGGER num_issues_allowed
BEFORE INSERT ON Issue
FOR EACH ROW
BEGIN
 DECLARE num_issues INT;
 DECLARE user_role BOOL;

 SELECT COUNT(User_ID) INTO num_issues
 FROM Issue as iss
 WHERE iss.User_ID = NEW.User_ID AND (DATE_ADD(iss.Start_date, INTERVAL 1 WEEK) >= CURRENT_DATE());

 SELECT ua.User_role INTO user_role
 FROM User_account as ua
 WHERE ua.User_ID = NEW.User_ID;

 IF ((user_role = 1 AND num_issues >= 1) OR (user_role = 0 AND num_issues >= 2)) THEN
    SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Has reached the maximum number of issues';
 END IF;

END;

CREATE DEFINER=`root`@`localhost` TRIGGER delayed_issue_issue
BEFORE INSERT
ON Issue FOR EACH ROW
BEGIN
  IF EXISTS (
    SELECT i.User_ID
    FROM Issue AS i
    WHERE i.Issue_ID IN (
      SELECT di.Issue_ID
      FROM Delayed_issue AS di
    )
    AND i.User_ID = NEW.User_ID
  ) THEN
    SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'No reservations allowed if delayed issue';
  END IF;
END;

CREATE DEFINER=`root`@`localhost` TRIGGER check_if_reserved
BEFORE INSERT
ON Issue FOR EACH ROW

BEGIN
  DECLARE available_copies INT;

  SELECT br.Book_copies INTO available_copies
  FROM Book_records as br
  WHERE br.Book_ID = NEW.Book_ID;

  IF available_copies <= 0 THEN
    SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'No available copies for the book';
  END IF;
END;

CREATE DEFINER=`root`@`localhost` TRIGGER school_phone_numeric BEFORE INSERT ON School_phone
FOR EACH ROW
BEGIN
  IF NOT (NEW.Phone_number REGEXP '^[0-9]+$' OR LENGTH(NEW.Phone_number) = 10) THEN
    SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Phone must be numeric of length 10';
  END IF;
END;

CREATE DEFINER=`root`@`localhost` TRIGGER school_phone_numeric2 BEFORE UPDATE ON School_phone
FOR EACH ROW
BEGIN
  IF NOT (NEW.Phone_number REGEXP '^[0-9]+$' OR LENGTH(NEW.Phone_number) = 10) THEN
    SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Phone must be numeric of length 10';
  END IF;
END;

CREATE EVENT delete_reservation
ON SCHEDULE AT '2023-06-08 22:03:19.000'
ON COMPLETION PRESERVE
ENABLE
DO DELETE FROM Reservation WHERE Reservation.Start_date  >= (Reservation.Due_date + INTERVAL 1 WEEK);
