-- 创建数据库
create database `iqiwx` default character set utf8 collate utf8_general_ci;

use iqiwx;

-- 建表
SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for ready_spider
-- ----------------------------
CREATE TABLE `ready_spider` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '主键，自增',
  `book_id` int(11) DEFAULT NULL COMMENT '书的id',
  `create_date` datetime DEFAULT NULL COMMENT '新建时间',
  `update_date` datetime DEFAULT NULL COMMENT '更新爬取时间',
  `status` int(11) DEFAULT NULL COMMENT '是否要爬取：1：爬取，0：不爬取，默认：1',
  PRIMARY KEY (`id`),
  KEY `id` (`id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


CREATE TABLE `book_chapter` (
  `id` int(21) NOT NULL AUTO_INCREMENT,
  `book_id` int(21) NOT NULL,
  `chapter_name` varchar(1024) NOT NULL,
  `chapter_content` text NOT NULL,
  `num` int(12) NOT NULL,
  `create_date` datetime DEFAULT NULL ON UPDATE current_timestamp(),
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`) USING BTREE,
  KEY `book` (`book_id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=120869 DEFAULT CHARSET=utf8mb4;


CREATE TABLE `book_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '主键，自增',
  `type_name` varchar(255) DEFAULT NULL COMMENT '类名',
  `create_date` datetime DEFAULT NULL COMMENT '创建时间',
  `update_date` datetime DEFAULT NULL COMMENT '更新时间',
  `status` int(11) DEFAULT 1 COMMENT '状态，默认：1，其他待定',
  PRIMARY KEY (`id`),
  KEY `id` (`id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4;


CREATE TABLE `author` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '主键，自增',
  `author_name` varchar(255) NOT NULL COMMENT '作者',
  `author_intro` text DEFAULT NULL COMMENT '作者简介',
  `author_img` varchar(255) DEFAULT NULL COMMENT '作者图片',
  `author_info` text CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '作者信息的扩展字段',
  `create_date` datetime DEFAULT NULL COMMENT '创建时间',
  `update_date` datetime DEFAULT NULL COMMENT '更新时间',
  `status` int(11) NOT NULL DEFAULT 1 COMMENT '状态，默认：1，其他待定',
  PRIMARY KEY (`id`),
  KEY `id` (`id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=373 DEFAULT CHARSET=utf8mb4;


CREATE TABLE `book` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '主键，自增',
  `book_name` varchar(255) NOT NULL COMMENT '书名',
  `author_id` int(11) NOT NULL COMMENT '作者id',
  `img` varchar(255) DEFAULT NULL COMMENT '书的封面图片',
  `type_id` int(11) DEFAULT NULL COMMENT '书的分类id',
  `book_intro` text DEFAULT NULL COMMENT '书的简介',
  `create_date` datetime DEFAULT NULL COMMENT '插入时间',
  `update_date` datetime DEFAULT NULL ON UPDATE current_timestamp() COMMENT '更新时间',
  `status` int(11) DEFAULT 0 COMMENT '书的状态：1：完结，0：连载，默认：0',
  PRIMARY KEY (`id`),
  KEY `id` (`id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=374 DEFAULT CHARSET=utf8mb4;


CREATE TABLE `insert_error` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '主键',
  `msg` text DEFAULT NULL COMMENT '错误信息',
  `create_date` datetime DEFAULT NULL COMMENT '创建时间',
  `status` int(11) DEFAULT NULL COMMENT '是否处理，1：已处理，0：未处理',
  PRIMARY KEY (`id`),
  KEY `id` (`id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4;


CREATE TABLE `book_all` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `book_name` varchar(255) DEFAULT NULL,
  `book_login_url` varchar(255) DEFAULT NULL,
  `type_name` varchar(255) DEFAULT NULL,
  `type_url` varchar(255) DEFAULT NULL,
  `book_author` varchar(255) DEFAULT NULL,
  `book_img` varchar(255) DEFAULT NULL,
  `book_intro` text DEFAULT NULL,
  `chapter_login_url` varchar(255) DEFAULT NULL,
  `chapter_name` varchar(255) DEFAULT NULL,
  `chapter_url` varchar(255) DEFAULT NULL,
  `chapter_content` text DEFAULT NULL,
  `num` int(12) NOT NULL DEFAULT 0,
  `status` int(4) NOT NULL DEFAULT 0,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`) USING BTREE,
  KEY `book_name` (`book_name`) USING BTREE,
  KEY `chapter_name` (`chapter_name`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=111803 DEFAULT CHARSET=utf8mb4;
