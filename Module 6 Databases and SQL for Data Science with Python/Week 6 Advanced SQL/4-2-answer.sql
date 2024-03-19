SELECT School_ID, NAME_OF_SCHOOL, Leaders_Icon, Leaders_Score FROM chicago_public_schools LIMIT 1;

CALL UPDATE_LEADERS_SCORE(610038, 50);

SELECT School_ID, NAME_OF_SCHOOL, Leaders_Icon, Leaders_Score FROM chicago_public_schools LIMIT 1;