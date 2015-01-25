CREATE DATABASE  IF NOT EXISTS `zen_blog` /*!40100 DEFAULT CHARACTER SET utf8 */;
USE `zen_blog`;
-- MySQL dump 10.13  Distrib 5.6.17, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: zen_blog
-- ------------------------------------------------------
-- Server version	5.6.21-log

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
-- Table structure for table `alembic_version`
--

DROP TABLE IF EXISTS `alembic_version`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `alembic_version` (
  `version_num` varchar(32) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `alembic_version`
--

LOCK TABLES `alembic_version` WRITE;
/*!40000 ALTER TABLE `alembic_version` DISABLE KEYS */;
INSERT INTO `alembic_version` VALUES ('470f17a7e60f');
/*!40000 ALTER TABLE `alembic_version` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `category`
--

DROP TABLE IF EXISTS `category`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `category` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `category_name` varchar(100) DEFAULT NULL,
  `category_post_count` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `category_name` (`category_name`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `category`
--

LOCK TABLES `category` WRITE;
/*!40000 ALTER TABLE `category` DISABLE KEYS */;
INSERT INTO `category` VALUES (1,'Linux',4),(2,'Python',2),(3,'Book',0);
/*!40000 ALTER TABLE `category` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `link`
--

DROP TABLE IF EXISTS `link`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `link` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `link_url` varchar(100) DEFAULT NULL,
  `link_name` varchar(100) DEFAULT NULL,
  `link_updated` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `link_url` (`link_url`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `link`
--

LOCK TABLES `link` WRITE;
/*!40000 ALTER TABLE `link` DISABLE KEYS */;
/*!40000 ALTER TABLE `link` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `post`
--

DROP TABLE IF EXISTS `post`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `post` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `category_id` int(11) DEFAULT NULL,
  `post_title` varchar(120) DEFAULT NULL,
  `post_date` datetime DEFAULT NULL,
  `post_excerpt` text,
  `post_content` text,
  `post_view_count` int(11) DEFAULT NULL,
  `post_comment_count` int(11) DEFAULT NULL,
  `post_love_count` int(11) DEFAULT NULL,
  `category_name` varchar(120) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `post_title` (`post_title`),
  KEY `category_id` (`category_id`),
  CONSTRAINT `post_ibfk_1` FOREIGN KEY (`category_id`) REFERENCES `category` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `post`
--

LOCK TABLES `post` WRITE;
/*!40000 ALTER TABLE `post` DISABLE KEYS */;
INSERT INTO `post` VALUES (3,NULL,'暴力破解保护方案','2015-01-21 15:48:42','<p>分析 <code>/var/log/auth.log</code> 登陆日志，可以发现很多SSH，FTP服务的登录尝试。其中FTP多为匿名用户的登录尝试。</p>\r\n<p>SSH服务多为root用户的登录尝试，时间集中于夜晚凌晨，不容易被管理员发现，并且破解方式采用建立连接后尝试一次密码断开再次请求连接。不受配置中MaxAuthTries的限制。</p>','<h2>原因分析</h2>\r\n<p>分析 <code>/var/log/auth.log</code> 登陆日志，可以发现很多SSH，FTP服务的登录尝试。其中FTP多为匿名用户的登录尝试。</p>\r\n<p>SSH服务多为root用户的登录尝试，时间集中于夜晚凌晨，不容易被管理员发现，并且破解方式采用建立连接后尝试一次密码断开再次请求连接。不受配置中MaxAuthTries的限制。</p>\r\n<h2>解决方案</h2>\r\n<h3>1 两个简单的设置可以很大程度防止密码被破解。</h3>\r\n<p>限制root登陆,更改默认端口</p>\r\n<p><code>Port 23946</code></p>\r\n<p><code>PermitRootLogin no</code> </p>\r\n<p>限制root登陆还是很有必要，登陆后直接su为root用户也只是多了两个步骤而已。一般情况下就能防止很多的无脑扫描。</p>\r\n<p>缺点是无法完全禁止爆破，依然会占用系统和带宽资源。</p>\r\n<h3>2 使用公钥登陆,禁止密码登陆。这是个一劳永逸的方法。</h3>\r\n<pre><code>RSAAuthentication yes\r\nPubkeyAuthentication yes\r\nAuthorizedKeysFile .ssh/authorized_keys\r\n</code></pre>\r\n\r\n<p>按照网上配置，成功后可以防止密码扫描。</p>\r\n<h3>3 Denyhosts</h3>\r\n<p>一款python写成的工具，可以根据日志内容找出可疑ip，通过Linux自带的TCP Wrappers来进行访问控制(<code>/etc/hosts.deny</code>)</p>\r\n<p>使用与配置</p>\r\n<p>1 正常使用<code>setup.py install</code>安装，默认安装路径为<code>/usr/local/Denyhosts</code></p>\r\n<p>2 配置与启动文件为</p>\r\n<pre><code>denyhosts.cfg\r\ndaemon-control\r\n</code></pre>\r\n\r\n<p>denyhosts.cfg关键配置为：</p>\r\n<pre><code>PURGE_DENY：当一个IP被阻止以后，过多长时间被自动解禁。可选如3m（三分钟）、5h（5小时）、2d（两天）、8w（8周）、1y（一年）；\r\nPURGE_THRESHOLD：定义了某一IP最多被解封多少次。即某一IP由于暴力破解SSH密码被阻止/解封达到了PURGE_THRESHOLD次，则会被永久禁止；\r\nBLOCK_SERVICE：需要阻止的服务名；\r\nDENY_THRESHOLD_INVALID：某一无效用户名（不存在的用户）尝试多少次登录后被阻止；\r\nDENY_THRESHOLD_VALID：某一有效用户名尝试多少次登陆后被阻止（比如账号正确但密码错误），root除外；\r\nDENY_THRESHOLD_ROOT：root用户尝试登录多少次后被阻止；\r\nHOSTNAME_LOOKUP：是否尝试解析源IP的域名；\r\nDAEMON_PURGE = 5m  ip禁止时间的真正控制，感觉前面的有问题，不起作用\r\n</code></pre>\r\n\r\n<p><code>daemon-control start</code> 启动</p>\r\n<p><code>/etc/hosts.deny</code>  禁止的ip保存文件，可手动清除。</p>',64,0,0,'Linux'),(15,2,'qewasdfadsf','2014-01-22 08:02:11','eqwfweq','ewqfewqf',17,0,0,'Python'),(16,1,'dsafsfadsfsdafdsfsdafsafsfsafsdsdfdsafdsafafsafafsa','2015-01-22 08:16:19','adsfasdf','adsfa',14,0,0,'Linux'),(17,1,'sdafsadf','2015-01-22 08:19:10','sdafasdf','dsafasdf',1,0,0,'Linux'),(19,1,'adsfsdaf','2015-01-22 08:19:50','asdfdsf','asdfasdf',11,0,0,'Linux'),(20,2,'sadfasdfa','2015-01-22 08:20:40','dsafdsaf','asdfdsaf',9,0,0,'Python');
/*!40000 ALTER TABLE `post` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tag`
--

DROP TABLE IF EXISTS `tag`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tag` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `post_id` int(11) DEFAULT NULL,
  `tag_name` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tag`
--

LOCK TABLES `tag` WRITE;
/*!40000 ALTER TABLE `tag` DISABLE KEYS */;
INSERT INTO `tag` VALUES (1,19,'tag2'),(2,20,'mysqldb'),(3,20,'tag2'),(4,20,'tag3'),(5,17,'tag5'),(6,15,'tag4');
/*!40000 ALTER TABLE `tag` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(64) DEFAULT NULL,
  `password` varchar(120) DEFAULT NULL,
  `role` smallint(6) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user`
--

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
INSERT INTO `user` VALUES (1,'admin','admin',1);
/*!40000 ALTER TABLE `user` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2015-01-25 10:39:50
