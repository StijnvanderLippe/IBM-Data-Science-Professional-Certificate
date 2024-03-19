CREATE VIEW SCHOOLS (School_Name, Safety_rating, Family_Rating, Environment_Rating, Instruction_Rating, Leaders_Rating, Teachers_Rating)
AS SELECT NAME_OF_SCHOOL, Safety_Icon, Family_Involment_Icon, Environment_Icon, Instruction_Icon, Leaders_Icon, Teachers_Icon
FROM chicago_public_schools

SELECT School_Name, Leaders_Rating FROM SCHOOLS
