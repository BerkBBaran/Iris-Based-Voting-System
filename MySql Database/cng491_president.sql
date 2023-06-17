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
-- Table structure for table `president`
--

DROP TABLE IF EXISTS `president`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `president` (
  `id` varchar(45) NOT NULL,
  `vote_ballot_id` varchar(45) DEFAULT NULL,
  `fullname` varchar(45) DEFAULT NULL,
  `keyword` varchar(45) DEFAULT NULL,
  `photo_path` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `vote_ballot_id_idx` (`vote_ballot_id`),
  CONSTRAINT `vote_ballot_id` FOREIGN KEY (`vote_ballot_id`) REFERENCES `vote_ballot` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `president`
--

LOCK TABLES `president` WRITE;
/*!40000 ALTER TABLE `president` DISABLE KEYS */;
INSERT INTO `president` VALUES ('1212','12','12','12',NULL),('asd12','12','asd','asd',NULL),('berk bekir782','1','berk bekir','berk bekir',NULL),('candidate188','12','candidate1','candidate1',NULL),('candidate19','55','Kemal Kilic','candidate4',NULL),('candidate20','55','Idil Candan','candidate5',NULL),('candidate21','55','Enver Ever','candidate6',NULL),('candidate299','12','candidate2','candidate2',NULL),('candidate3120','12','candidate3','candidate3',NULL),('denem 68 1','69','denem 68 1','denem 68 1',NULL),('deneme 68 2','69','deneme 68 2','deneme 68 2',NULL),('deneme 68 3','69','deneme 68 3','deneme 68 3',NULL),('deneme ekledim390','1','deneme ekledim','deneme ekledim',NULL),('deneme99','55','deneme','deneme',NULL),('efe kır','76','efe kır','efe kır',NULL),('efe12','17','efe','efe',NULL),('efe1212','1','efe','efe',NULL),('Okan Topcu','55','Okan Topcu','Okan Topcu',NULL),('rte12','12','rte','rte',NULL);
/*!40000 ALTER TABLE `president` ENABLE KEYS */;
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
