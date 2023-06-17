-- MySQL dump 10.13  Distrib 8.0.32, for Win64 (x86_64)
--
-- Host: localhost    Database: cng491
-- ------------------------------------------------------
-- Server version	8.0.32

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `vote`
--

DROP TABLE IF EXISTS `vote`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `vote` (
  `ssn` varchar(45) NOT NULL,
  `vote_ballot_id` varchar(45) NOT NULL,
  `selection` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`ssn`,`vote_ballot_id`),
  KEY `vote_ballot_id_idx` (`vote_ballot_id`),
  CONSTRAINT `citizen_id` FOREIGN KEY (`ssn`) REFERENCES `citizen` (`ssn`),
  CONSTRAINT `vote_ballot_id_vote` FOREIGN KEY (`vote_ballot_id`) REFERENCES `vote_ballot` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `vote`
--

LOCK TABLES `vote` WRITE;
/*!40000 ALTER TABLE `vote` DISABLE KEYS */;
INSERT INTO `vote` VALUES ('2','69','deneme 68 2'),('2','76','efe kır'),('20','12','candidate3'),('20','17','efe'),('20','55','candidate4'),('22222222222','12','candidate1'),('22222222222','55','candidate4'),('22222222223','12','candidate2'),('22222222223','55','candidate5'),('22485963722','1','yes'),('22485963722','12','candidate1'),('22485963722','55','candidate4'),('36272172022','1','yes'),('36272172022','12','candidate2'),('36272172022','55','candidate2'),('61148592211','1','yes'),('61148592211','12','candidate3'),('61148592211','55','candidate2'),('95512264572','12','candidate1'),('95512264576','1','no'),('95512264576','55','candidate2'),('98208532546','1','yes'),('98208532546','55','candidate1');
/*!40000 ALTER TABLE `vote` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2023-06-17 21:27:10
