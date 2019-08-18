-- phpMyAdmin SQL Dump
-- version 4.8.5
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1:3306
-- Generation Time: Aug 18, 2019 at 01:12 PM
-- Server version: 5.7.26
-- PHP Version: 7.2.18

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `resolved2`
--

-- --------------------------------------------------------

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
CREATE TABLE IF NOT EXISTS `user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `drugName` text NOT NULL,
  `v1` float DEFAULT NULL,
  `v2` float DEFAULT NULL,
  `v3` float DEFAULT NULL,
  `v4` float DEFAULT NULL,
  `v5` float DEFAULT NULL,
  `v6` float DEFAULT NULL,
  `v7` float DEFAULT NULL,
  `v8` float DEFAULT NULL,
  `v9` float DEFAULT NULL,
  `v10` float DEFAULT NULL,
  `v11` float DEFAULT NULL,
  `v12` float DEFAULT NULL,
  `v13` float DEFAULT NULL,
  `v14` float DEFAULT NULL,
  `v15` float DEFAULT NULL,
  `v16` float DEFAULT NULL,
  `v17` float DEFAULT NULL,
  `v18` float DEFAULT NULL,
  `v19` float DEFAULT NULL,
  `v20` float DEFAULT NULL,
  `v21` float DEFAULT NULL,
  `v22` float DEFAULT NULL,
  `v23` float DEFAULT NULL,
  `v24` float DEFAULT NULL,
  `v25` float DEFAULT NULL,
  `v26` float DEFAULT NULL,
  `v27` float DEFAULT NULL,
  `v28` float DEFAULT NULL,
  `hasResults` int(11) DEFAULT NULL,
  `oldResults` float DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=56 DEFAULT CHARSET=latin1;

--
-- Dumping data for table `user`
--


COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
