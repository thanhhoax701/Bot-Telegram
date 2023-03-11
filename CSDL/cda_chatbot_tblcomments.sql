-- MySQL dump 10.13  Distrib 8.0.32, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: cda_chatbot
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
-- Table structure for table `tblcomments`
--

DROP TABLE IF EXISTS `tblcomments`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `tblcomments` (
  `comment_id` int NOT NULL AUTO_INCREMENT,
  `comment_name` varchar(5000) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `comment_content` varchar(5000) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `comment_date` datetime DEFAULT NULL,
  PRIMARY KEY (`comment_id`),
  UNIQUE KEY `comment_UNIQUE` (`comment_id`)
) ENGINE=InnoDB AUTO_INCREMENT=55 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tblcomments`
--

LOCK TABLES `tblcomments` WRITE;
/*!40000 ALTER TABLE `tblcomments` DISABLE KEYS */;
INSERT INTO `tblcomments` VALUES (40,'Trần Thanh Hòa','đấy','2023-03-11 18:01:59'),(41,'Trần Thanh Luyến','Dịch vụ ổn','2023-03-11 18:02:19'),(42,'Mã Xíu An','Dịch vụ tốt','2023-03-11 18:03:05'),(43,'Trần Dần','được','2023-03-11 18:03:23'),(44,'Trần Việt Châu','dịch vụ hay','2023-03-11 18:04:48'),(45,'Lệ Quyên','dịch vụ hay','2023-03-11 18:05:47'),(46,'Mã Xíu An','lắm','2023-03-11 18:06:35'),(49,'Trần Văn Lựu','dịch vụ tốt','2023-03-11 19:37:18'),(50,'Trần Dầu Tiếng','dịch vụ ổn','2023-03-11 19:37:50'),(51,'Mã Xíu An','Dịch vụ hay','2023-03-11 19:38:17'),(52,'Cao Bá Quát','ổn','2023-03-11 19:38:55'),(53,'Trần Chí Nguyên','Bot của','2023-03-11 19:44:05'),(54,'Dương Quá','Bot của các bạn ngu không thể tả được','2023-03-11 19:45:03');
/*!40000 ALTER TABLE `tblcomments` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2023-03-11 20:29:59
