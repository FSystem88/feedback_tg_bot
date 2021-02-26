DROP TABLE IF EXISTS `AdminsFeedback`;
CREATE TABLE `AdminsFeedback` (
  `id` int(11) NOT NULL,
  `tgid` varchar(64) CHARACTER SET utf8 NOT NULL,
  `name` varchar(64) CHARACTER SET utf8 NOT NULL,
  `username` varchar(64) CHARACTER SET utf8 NOT NULL,
  `status` varchar(64) CHARACTER SET utf8 NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

INSERT INTO `AdminsFeedback` (`id`, `tgid`, `name`, `username`, `status`) VALUES
(1, 'ТВОЙ АЙДИ В ТЕЛЕГЕ', 'ТВОЁ ИМЯ', 'ТВОЙ ЮЗЕРНЕЙМ', 'god');

-- ВАЖНО! --> ПОСЛЕ ЮЗЕРНЕЙМА НЕ МЕНЯТЬ "god" НА ДРУГОЕ, ЭТО ЗНАЧИТ СТАТУС БОГА, А-ЛЯ САМЫЙ ГЛАВНЫЙ АДМИН !!!

ALTER TABLE `AdminsFeedback`
  ADD PRIMARY KEY (`id`);

ALTER TABLE `AdminsFeedback`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=;
