SET NAMES utf8mb4;
USE kindergartens;

CREATE TABLE IF NOT EXISTS attendance_log (
  log_id INT NOT NULL AUTO_INCREMENT,
  child_id INT NOT NULL,
  visit_date DATE NOT NULL,
  status VARCHAR(20) NOT NULL,
  PRIMARY KEY (log_id),
  CONSTRAINT fk_attendance_child
    FOREIGN KEY (child_id) REFERENCES children (child_id)
    ON DELETE CASCADE
) ENGINE = InnoDB;

CREATE TABLE IF NOT EXISTS employee_audit_log (
  log_id INT NOT NULL AUTO_INCREMENT,
  employee_id INT NOT NULL,
  first_name VARCHAR(60) NOT NULL,
  last_name VARCHAR(60) NOT NULL,
  action VARCHAR(50) NOT NULL,
  log_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (log_id)
) ENGINE = InnoDB;

DELIMITER $$

CREATE PROCEDURE insert_new_child(
  IN p_first_name VARCHAR(60), IN p_last_name VARCHAR(60), IN p_birth_date DATE)
BEGIN
  INSERT INTO children (first_name, last_name, birth_date)
  VALUES (p_first_name, p_last_name, p_birth_date);
END$$

CREATE PROCEDURE assign_position_to_employee(
  IN p_first_name VARCHAR(60), IN p_last_name VARCHAR(60), IN p_title VARCHAR(100))
BEGIN
  DECLARE v_emp_id INT;
  DECLARE v_pos_id INT;

  SET v_emp_id = (SELECT employee_id FROM employees
                  WHERE first_name = p_first_name AND last_name = p_last_name LIMIT 1);
  SET v_pos_id = (SELECT position_id FROM positions WHERE title = p_title LIMIT 1);

  IF v_emp_id IS NULL THEN
    SELECT 'Співробітника не знайдено' AS result;
  ELSEIF v_pos_id IS NULL THEN
    SELECT 'Посаду не знайдено' AS result;
  ELSE
    INSERT INTO employee_positions (employee_id, position_id, start_date)
    VALUES (v_emp_id, v_pos_id, CURDATE())
    ON DUPLICATE KEY UPDATE start_date = start_date;
    SELECT 'Посаду успішно призначено' AS result;
  END IF;
END$$

CREATE PROCEDURE insert_dummy_children()
BEGIN
  DECLARE i INT DEFAULT 1;
  WHILE i <= 10 DO
    INSERT INTO children (first_name, last_name, birth_date)
    VALUES (CONCAT('Тест', i), CONCAT('Дитина', i), DATE_ADD('2021-01-01', INTERVAL i MONTH));
    SET i = i + 1;
  END WHILE;
END$$

CREATE PROCEDURE show_salary_stats()
BEGIN
  SELECT AVG(amount) AS average_salary FROM salaries WHERE end_date IS NULL;
END$$

CREATE PROCEDURE dynamic_table_cursor()
BEGIN
  DECLARE done INT DEFAULT 0;
  DECLARE v_id INT;
  DECLARE v_count INT DEFAULT 0;
  DECLARE cur CURSOR FOR SELECT kindergarten_id FROM kindergartens;
  DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = 1;

  OPEN cur;
  read_loop: LOOP
    FETCH cur INTO v_id;
    IF done = 1 THEN
      LEAVE read_loop;
    END IF;

    SET @drop_sql = CONCAT('DROP TABLE IF EXISTS kg_report_', v_id);
    PREPARE stmt FROM @drop_sql;
    EXECUTE stmt;
    DEALLOCATE PREPARE stmt;

    SET @create_sql = CONCAT('CREATE TABLE kg_report_', v_id,
      ' AS SELECT employee_id, first_name, last_name FROM employees WHERE kindergarten_id = ', v_id);
    PREPARE stmt FROM @create_sql;
    EXECUTE stmt;
    DEALLOCATE PREPARE stmt;

    SET v_count = v_count + 1;
  END LOOP;
  CLOSE cur;

  SELECT CONCAT('Створено таблиць: ', v_count) AS result;
END$$

CREATE TRIGGER trg_attendance_before_insert
BEFORE INSERT ON attendance_log
FOR EACH ROW
BEGIN
  IF NEW.visit_date > CURDATE() THEN
    SIGNAL SQLSTATE '45000'
      SET MESSAGE_TEXT = 'Не можна додати відвідування з майбутньою датою';
  END IF;
END$$

CREATE TRIGGER trg_parents_before_insert
BEFORE INSERT ON parents
FOR EACH ROW
BEGIN
  IF NEW.phone_number NOT REGEXP '^0[0-9]{9}$' THEN
    SIGNAL SQLSTATE '45000'
      SET MESSAGE_TEXT = 'Некоректний телефон: потрібно 10 цифр, що починаються з 0';
  END IF;
END$$

CREATE TRIGGER trg_kindergartens_before_delete
BEFORE DELETE ON kindergartens
FOR EACH ROW
BEGIN
  SIGNAL SQLSTATE '45000'
    SET MESSAGE_TEXT = 'Видалення садочків заборонено';
END$$

CREATE TRIGGER trg_employees_after_delete
AFTER DELETE ON employees
FOR EACH ROW
BEGIN
  INSERT INTO employee_audit_log (employee_id, first_name, last_name, action)
  VALUES (OLD.employee_id, OLD.first_name, OLD.last_name, 'DELETE');
END$$

DELIMITER ;