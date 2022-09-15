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
-- Table `mydb`.`user`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`user` (
  `username` VARCHAR(16) NOT NULL,
  `email` VARCHAR(255) NOT NULL,
  `password` VARCHAR(60) NOT NULL,
  PRIMARY KEY (`username`),
  UNIQUE INDEX `email_UNIQUE` (`email` ASC) VISIBLE);


-- -----------------------------------------------------
-- Table `mydb`.`private_passwords`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`private_passwords` (
  `username` VARCHAR(16) NOT NULL,
  `service` VARCHAR(255) NOT NULL,
  `password` VARCHAR(60) NOT NULL,
  PRIMARY KEY (`username`, `service`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`shared_passwords`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`shared_passwords` (
  `groupid` INT NOT NULL,
  `associated_service` VARCHAR(255) NOT NULL,
  `req_username` VARCHAR(16) NOT NULL,
  `password` VARCHAR(60) NULL,
  `timer` VARCHAR(45) NULL,
  PRIMARY KEY (`groupid`, `associated_service`, `req_username`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`requests`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`requests` (
  `username` VARCHAR(45) NOT NULL,
  `groupid` INT NOT NULL,
  `associated_service` VARCHAR(255) NOT NULL,
  `req_username` VARCHAR(16) NOT NULL,
  `accepted` INT NOT NULL,
  `date` DATETIME NULL,
  PRIMARY KEY (`username`, `groupid`, `associated_service`, `req_username`),
  INDEX `fk_requests_shared_passwords_idx` (`groupid` ASC, `associated_service` ASC, `req_username` ASC) VISIBLE,
  CONSTRAINT `fk_requests_shared_passwords`
    FOREIGN KEY (`groupid` , `associated_service` , `req_username`)
    REFERENCES `mydb`.`shared_passwords` (`groupid` , `associated_service` , `req_username`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
