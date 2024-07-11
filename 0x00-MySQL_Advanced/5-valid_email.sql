-- sql script that triggers the atrribut
-- valid_email only when the email has been changed
DROP TRIGGER IF EXISTS validate_email;
DELIMITER $$
CREATE TRIGGER validate_email
BEFORE UPDATE ON users
FOR EACH ROW
BEGIN
    IF OLD.email != NEW.email THEN
        SET NEW.vaild_email = 0;
    ELSE
        SET NEW.valid_email = NEW.valid_email;
    END IF;
END $$
DELIMITER;
