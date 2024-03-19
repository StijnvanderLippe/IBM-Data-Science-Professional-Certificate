DELIMITER //

CREATE PROCEDURE UPDATE_LEADERS_SCORE(IN in_School_ID INTEGER, IN in_Leader_Score INTEGER)
BEGIN
	START TRANSACTION
	
	UPDATE chicago_public_schools
    SET Leaders_Score = in_Leader_Score
    WHERE in_School_ID = School_ID;
    
    IF in_Leader_Score > 0 AND in_Leader_Score < 20 THEN
    	UPDATE chicago_public_schools
        SET Leaders_Icon = 'Very weak'
        WHERE in_School_ID = School_ID;
    ELSEIF in_Leader_Score < 40 THEN
    	UPDATE chicago_public_schools
        SET Leaders_Icon = 'Weak'
        WHERE in_School_ID = School_ID;
	ELSEIF in_Leader_Score < 60 THEN
    	UPDATE chicago_public_schools
        SET Leaders_Icon = 'Average'
        WHERE in_School_ID = School_ID;
	ELSEIF in_Leader_Score < 80 THEN
    	UPDATE chicago_public_schools
        SET Leaders_Icon = 'Strong'
        WHERE in_School_ID = School_ID;
	ELSEIF in_Leader_Score < 100 THEN
    	UPDATE chicago_public_schools
        SET Leaders_Icon = 'Very strong'
        WHERE in_School_ID = School_ID;
	ELSE
		ROLLBACK;
    END IF;
	COMMIT;
END //

DELIMITER ;