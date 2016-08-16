-- 分类和软件关系表

DROP TABLE IF EXISTS `categorys2softs`;
CREATE TABLE `categorys2softs` (
  `categoryno` varchar(11) COLLATE utf8_unicode_ci NOT NULL DEFAULT '' COMMENT '分类标识',
  `softunique` varchar(11) COLLATE utf8_unicode_ci NOT NULL DEFAULT '' COMMENT '软件唯一标识'
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--

-- 分类表

DROP TABLE IF EXISTS `categorys`;
CREATE TABLE `categorys` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `no` varchar(11) COLLATE utf8_unicode_ci NOT NULL DEFAULT '' COMMENT '分类编号',
  `name` varchar(11) COLLATE utf8_unicode_ci NOT NULL DEFAULT '' COMMENT '分类名称',
  `parentno` varchar(11) COLLATE utf8_unicode_ci NOT NULL DEFAULT '' COMMENT '父级编号',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;


--


-- 评论表

DROP TABLE IF EXISTS `comments`;
CREATE TABLE `comments` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) COLLATE utf8_unicode_ci NOT NULL DEFAULT '' COMMENT '评论人名称',
  `commentdate` date NOT NULL COMMENT '评论时间',
  `comment` varchar(500) COLLATE utf8_unicode_ci NOT NULL DEFAULT '' COMMENT '评论内容',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
--

-- 软件表
DROP TABLE IF EXISTS `softs`;
CREATE TABLE `softs` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `softunique` varchar(50) COLLATE utf8_unicode_ci NOT NULL DEFAULT '' COMMENT '软唯一标识',
  `name` varchar(50) COLLATE utf8_unicode_ci NOT NULL DEFAULT '' COMMENT '名称',
  `downloadtimes` int(11) NOT NULL DEFAULT '0' COMMENT '下载次数',
  `suporttimes` int(11) NOT NULL DEFAULT '0' COMMENT '喜欢人数',
  `commenttimes` int(11) NOT NULL DEFAULT '0' COMMENT '评论次数',
  `note` varchar(2000) COLLATE utf8_unicode_ci NOT NULL DEFAULT '' COMMENT '描述',
  `imgs` varchar(2000) COLLATE utf8_unicode_ci NOT NULL DEFAULT '' COMMENT '截图',
  `downloadlink` varchar(2000) COLLATE utf8_unicode_ci NOT NULL DEFAULT '' COMMENT '下载链接',
  `updatenote` varchar(2000) COLLATE utf8_unicode_ci NOT NULL DEFAULT '' COMMENT '更新内容',
  `version` varchar(2000) COLLATE utf8_unicode_ci NOT NULL DEFAULT '' COMMENT '版本',
  `size` varchar(200) COLLATE utf8_unicode_ci NOT NULL DEFAULT '' COMMENT '大小',
  `categorynos` varchar(400) COLLATE utf8_unicode_ci NOT NULL DEFAULT '' COMMENT '分类',
  `tag` varchar(500) COLLATE utf8_unicode_ci NOT NULL DEFAULT '' COMMENT '标签',
  `updatetimes` varchar(12) COLLATE utf8_unicode_ci NOT NULL DEFAULT '' COMMENT '更新时间',
  `request` varchar(2000) COLLATE utf8_unicode_ci NOT NULL DEFAULT '' COMMENT '权限要求',
  `createfrom` varchar(300) COLLATE utf8_unicode_ci NOT NULL DEFAULT '' COMMENT '生产厂家',
  `erweimatupian` varchar(200) COLLATE utf8_unicode_ci NOT NULL DEFAULT '' COMMENT '二维码图片',
  `recommends` varchar(2000) COLLATE utf8_unicode_ci NOT NULL DEFAULT '' COMMENT '相关推荐',
  `oldversion` varchar(400) COLLATE utf8_unicode_ci NOT NULL DEFAULT '' COMMENT '历史版本',
  `olddownload` varchar(3000) COLLATE utf8_unicode_ci NOT NULL DEFAULT '' COMMENT '历史下载路径',
  `created_at` varchar(20) COLLATE utf8_unicode_ci NOT NULL DEFAULT '',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;


--

-- 抓取链接的表
DROP TABLE IF EXISTS `urls`;
CREATE TABLE `urls` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `url` varchar(1000) COLLATE utf8_unicode_ci NOT NULL DEFAULT '',
  `status` int(11) NOT NULL DEFAULT '0' COMMENT '状态0-未抓取 1-已抓取',
  `create_time` datetime DEFAULT NULL COMMENT '创建时间',
  `update_time` datetime DEFAULT NULL COMMENT '修改时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=17283 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

