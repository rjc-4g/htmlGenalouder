CREATE DATABASE IF NOT EXISTS `devdb`;
USE `devdb`;

CREATE TABLE IF NOT EXISTS `users`
(
  `user_id` INT NOT NULL AUTO_INCREMENT COMMENT 'ユーザID',
  `user_name` VARCHAR(50) NOT NULL COMMENT 'ユーザ名',
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '作成日時',
  `updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新日時',
  PRIMARY KEY (`user_id`)
) COMMENT 'ユーザ';

INSERT INTO `users` VALUES (NULL, 'guest', default, default);
INSERT INTO `users` VALUES (NULL, 'test', default, default);

-- 生成履歴 (generation_history)
CREATE TABLE IF NOT EXISTS `generation_history`
(
  `request_id` CHAR(11) DEFAULT '00000000000' COMMENT 'リクエストID',
  `prompt_af` VARCHAR(255) COMMENT '指示（音声）',
  `prompt_ja` TEXT COMMENT '指示（日本語）',
  `prompt_en` TEXT COMMENT '指示（英語）',
  `html` TEXT COMMENT 'HTML',
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '作成日時',
  `updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新日時',
  PRIMARY KEY (`request_id`)
) COMMENT '生成履歴';

-- 順序（sequence）
CREATE TABLE IF NOT EXISTS `sequence`
(
  `id` INT PRIMARY KEY COMMENT 'ID',
  `updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新日時'
) COMMENT '順序';
INSERT INTO `sequence` VALUES (0, DEFAULT);

-- リクエストID作成トリガー（create_request_id）
delimiter // -- トリガー定義内で使用するため一時的に区切り文字を変更
CREATE TRIGGER IF NOT EXISTS `create_request_id` BEFORE INSERT ON `generation_history`
  FOR EACH ROW
    BEGIN
      IF (SELECT DATE(`updated_at`) FROM `sequence`) = CURRENT_DATE THEN
        -- 更新日が当日の場合はシーケンスを+1増加
        UPDATE `sequence` SET `id` = LAST_INSERT_ID(`id` + 1);
      ELSE
        -- 更新日が過去の場合はシーケンスをリセット
        UPDATE `sequence` SET `id` = LAST_INSERT_ID(1);
      END IF;
      -- リクエストID = 現在日付（YYMMDD）+ シーケンス（5桁0埋め）
      SET NEW.`request_id` = CONCAT(DATE_FORMAT(CURRENT_DATE, '%y%m%d'), LPAD(LAST_INSERT_ID(), 5, '0'));
    END;//
delimiter ; -- 区切り文字を元に戻す
