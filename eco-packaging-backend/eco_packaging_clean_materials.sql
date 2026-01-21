CREATE DATABASE  IF NOT EXISTS `eco_packaging_clean` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `eco_packaging_clean`;
-- MySQL dump 10.13  Distrib 8.0.44, for Win64 (x86_64)
--
-- Host: localhost    Database: eco_packaging_clean
-- ------------------------------------------------------
-- Server version	8.0.40

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
-- Table structure for table `materials`
--

DROP TABLE IF EXISTS `materials`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `materials` (
  `id` int NOT NULL AUTO_INCREMENT,
  `material_type` varchar(100) DEFAULT NULL,
  `biodegradability_score` int DEFAULT NULL,
  `co2_emission_score` int DEFAULT NULL,
  `recyclability_percent` int DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=98 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `materials`
--

LOCK TABLES `materials` WRITE;
/*!40000 ALTER TABLE `materials` DISABLE KEYS */;
INSERT INTO `materials` VALUES (1,'Kraft Paper',90,30,80),(2,'Corrugated Cardboard',91,29,81),(3,'Double Wall Cardboard',92,28,82),(4,'Molded Fiber Tray',93,27,83),(5,'Bagasse Packaging',94,26,84),(6,'Sugarcane Fiber Board',95,25,85),(7,'Bamboo Fiber Sheet',96,24,86),(8,'Bamboo Composite Panel',97,23,87),(9,'Palm Leaf Container',98,22,88),(10,'Mycelium Packaging',99,21,89),(11,'Seaweed Based Wrap',100,20,90),(12,'Hemp Fiber Board',89,31,79),(13,'Jute Fiber Packaging',88,32,78),(14,'Coconut Husk Fiber',87,33,77),(15,'Wheat Straw Board',86,34,76),(16,'Rice Husk Composite',85,35,75),(17,'Corn Husk Packaging',84,36,74),(18,'Banana Fiber Box',83,37,73),(19,'Areca Leaf Plate',82,38,72),(20,'Flax Fiber Composite',81,39,71),(21,'Paper Honeycomb Board',80,40,70),(22,'Cellulose Cushioning',79,41,69),(23,'Wood Pulp Molded Tray',78,42,68),(24,'Compressed Wood Fiber',77,43,67),(25,'Engineered Wood Panel',76,44,66),(26,'Natural Cork Sheet',75,45,65),(27,'Expanded Cork Board',74,46,64),(28,'Miscanthus Fiber Panel',73,47,63),(29,'Switchgrass Board',72,48,62),(30,'Sunflower Husk Fiber',71,49,61),(31,'Soy Fiber Packaging',70,50,60),(32,'Plant Based Foam',69,51,59),(33,'Bio Composite Foam',68,52,58),(34,'Recycled Paperboard',67,53,57),(35,'Thermoformed Fiber',66,54,56),(36,'Agro Waste Panel',65,55,55),(37,'Green Pulp Sheet',64,56,54),(38,'Forest Residue Board',63,57,53),(39,'Natural Latex Sheet',62,58,52),(40,'Organic Felt Mat',61,59,51),(41,'Kenaf Fiber Board',60,60,50),(42,'Linen Fiber Panel',59,61,49),(43,'Bio Resin Board',58,62,48),(44,'Wood Wool Cement',57,63,47),(45,'Recycled Carton',56,64,46),(46,'Biodegradable Laminate',55,65,45),(47,'Fiber Mold Cushion',54,66,44),(48,'Eco Cushion Wrap',53,67,43),(49,'Natural Packing Pad',52,68,42),(50,'Green Molded Insert',51,69,41),(51,'Organic Pulp Core',50,70,40),(52,'Paper Fiber Mesh',49,71,39),(53,'Eco Structural Board',48,72,38),(54,'Renewable Fiber Slab',47,73,37),(55,'Sustainable Sheet',46,74,36),(56,'Plant Fiber Block',45,75,35),(57,'Natural Cushion Board',44,76,34),(58,'Fiber Composite Pad',43,77,33),(59,'Eco Formed Tray',42,78,32),(60,'Bio Mold Panel',41,79,31),(61,'Agro Fiber Cushion',40,80,30),(62,'Green Wrap Sheet',39,81,29),(63,'Organic Support Insert',38,82,28),(64,'Renewable Pulp Tray',37,83,27),(65,'Eco Safe Fiber',36,84,26),(66,'Plant Based Insert',35,85,25),(67,'Bio Fiber Pad',34,86,24),(68,'Eco Cushion Mold',33,87,23),(69,'Green Packaging Board',32,88,22),(70,'Sustainable Fiber Pack',31,89,21),(71,'Plastic (PET)',80,88,10),(72,'Plastic (PET)',90,39,58),(73,'Jute',91,42,26),(74,'Cellulose Film',96,20,24),(75,'Jute',100,68,33),(76,'Paper',86,47,69),(77,'Paper',82,31,74),(78,'Bamboo',95,18,83),(79,'Bamboo',92,22,79),(80,'Glass',40,55,92),(81,'Glass',38,60,94),(82,'Aluminum',45,50,90),(83,'Aluminum',42,48,88),(84,'Steel',35,65,85),(85,'Steel',32,70,82),(86,'Cotton',88,28,76),(87,'Cotton',90,26,78),(88,'Cardboard',84,36,81),(89,'Cardboard',86,34,83),(90,'Wood',78,40,70),(91,'Wood',80,38,72),(92,'PLA Bioplastic',89,44,60),(93,'PLA Bioplastic',91,41,62),(94,'Bagasse',97,15,88),(95,'Bagasse',99,12,90),(96,'Hemp',94,21,85),(97,'Hemp',96,19,87);
/*!40000 ALTER TABLE `materials` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-01-21 12:15:49
