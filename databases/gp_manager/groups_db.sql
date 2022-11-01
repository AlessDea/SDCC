-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `mydb` DEFAULT CHARACTER SET utf8 ;
USE `mydb` ;

-- -----------------------------------------------------
-- Table `mydb`.`groups`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`group` (
  `idgroup` INT NOT NULL AUTO_INCREMENT,
  `service` VARCHAR(45) NOT NULL,
  `num_part` INT NULL,
  PRIMARY KEY (`idgroup`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`table2`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`participant` (
  `groups_idgroup` INT NOT NULL,
  `username` VARCHAR(45) NOT NULL,
  `email_addr` VARCHAR(45) NOT NULL,
  INDEX `fk_table2_groups_idx` (`groups_idgroup` ASC) VISIBLE,
  PRIMARY KEY (`groups_idgroup`, `username`),
  CONSTRAINT `fk_table2_groups`
    FOREIGN KEY (`groups_idgroup`)
    REFERENCES `mydb`.`group` (`idgroup`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;


INSERT INTO `group`(`service`, `num_part`) VALUES('login-facebook', 3);
INSERT INTO `group`(`service`, `num_part`) VALUES('reserved-leonardo', 5);
INSERT INTO `group`(`service`, `num_part`) VALUES('reserved-aeronautica', 7);


INSERT INTO `participant`(`groups_idgroup`, `username`, `email_addr`) VALUES(1, 'aless', 'ale.flanker97@gmail.com');
INSERT INTO `participant`(`groups_idgroup`, `username`, `email_addr`) VALUES(1, 'enric', 'ale.flanker97@gmail.com');
INSERT INTO `participant`(`groups_idgroup`, `username`, `email_addr`) VALUES(1, 'pierp', 'ale.flanker97@gmail.com');
INSERT INTO `participant`(`groups_idgroup`, `username`, `email_addr`) VALUES(2, 'vale', 'ale.flanker97@gmail.com');
INSERT INTO `participant`(`groups_idgroup`, `username`, `email_addr`) VALUES(2, 'ludo', 'ale.flanker97@gmail.com');
INSERT INTO `participant`(`groups_idgroup`, `username`, `email_addr`) VALUES(2, 'giu', 'ale.flanker97@gmail.com');
INSERT INTO `participant`(`groups_idgroup`, `username`, `email_addr`) VALUES(2, 'vit', 'ale.flanker97@gmail.com');
INSERT INTO `participant`(`groups_idgroup`, `username`, `email_addr`) VALUES(2, 'ana', 'ale.flanker97@gmail.com');
INSERT INTO `participant`(`groups_idgroup`, `username`, `email_addr`) VALUES(3, 'mar', 'ale.flanker97@gmail.com');
INSERT INTO `participant`(`groups_idgroup`, `username`, `email_addr`) VALUES(3, 'ric', 'ale.flanker97@gmail.com');
INSERT INTO `participant`(`groups_idgroup`, `username`, `email_addr`) VALUES(3, 'gius', 'ale.flanker97@gmail.com');
INSERT INTO `participant`(`groups_idgroup`, `username`, `email_addr`) VALUES(3, 'ani', 'ale.flanker97@gmail.com');
INSERT INTO `participant`(`groups_idgroup`, `username`, `email_addr`) VALUES(3, 'fra', 'ale.flanker97@gmail.com');
INSERT INTO `participant`(`groups_idgroup`, `username`, `email_addr`) VALUES(3, 'jess', 'ale.flanker97@gmail.com');
INSERT INTO `participant`(`groups_idgroup`, `username`, `email_addr`) VALUES(3, 'ale', 'ale.flanker97@gmail.com');

