from __future__ import unicode_literals


CHUNK_SIZE = 20000  # We chunk data into rows of 20,000 entries for speed

DROP_AND_CREATE_STRING = """-- MySQL dump 10.13  Distrib 5.7.17
--
-- Host: (RDS)    Database: cfpb_django
-- ------------------------------------------------------
-- Server version   5.7.17

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `data_research_countymortgagedata`
--

DROP TABLE IF EXISTS `data_research_countymortgagedata`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `data_research_countymortgagedata` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `fips` varchar(6) NOT NULL,
  `date` date NOT NULL,
  `total` int(11) DEFAULT NULL,
  `current` int(11) DEFAULT NULL,
  `thirty` int(11) DEFAULT NULL,
  `sixty` int(11) DEFAULT NULL,
  `ninety` int(11) DEFAULT NULL,
  `other` int(11) DEFAULT NULL,
  `county_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `data_research_countymortgagedata_cbd9376b` (`fips`),
  KEY `data_research_countymortgagedata_5fc73231` (`date`),
  KEY `data_research_countymortgagedata_d19428be` (`county_id`)
) ENGINE=MyISAM AUTO_INCREMENT=347706 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;
"""  # noqa: E501

INSERTION_STRING = """
--
-- Dumping data for table `data_research_countymortgagedata`
--

LOCK TABLES `data_research_countymortgagedata` WRITE;
/*!40000 ALTER TABLE `data_research_countymortgagedata` DISABLE KEYS */;
"""

UNLOCK_STRING = """
/*!40000 ALTER TABLE `data_research_countymortgagedata` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on {}
"""


def chunk_entries(data, chunk):
    for i in xrange(0, len(data), chunk):
        yield [row for row in data[i:i + chunk]]


def assemble_insertions(data):
    intro = 'INSERT INTO `data_research_countymortgagedata` VALUES '
    insertions = ['{}{};'.format(intro, ','.join(list(batch)))
                  for batch in chunk_entries(data, CHUNK_SIZE)]
    return INSERTION_STRING + '\n'.join(line for line in insertions)
