-- phpMyAdmin SQL Dump
-- version 5.0.1
-- https://www.phpmyadmin.net/
--
-- Хост: std-mysql
-- Время создания: Фев 21 2020 г., 18:10
-- Версия сервера: 5.7.26-0ubuntu0.16.04.1
-- Версия PHP: 7.4.1

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- База данных: `std_851`
--

-- --------------------------------------------------------

--
-- Структура таблицы `lists`
--

CREATE TABLE `lists` (
  `id` int(11) NOT NULL,
  `data` date NOT NULL,
  `login_users` varchar(25) NOT NULL,
  `type_id` int(11) NOT NULL,
  `status_id` int(11) NOT NULL,
  `message` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Дамп данных таблицы `lists`
--

INSERT INTO `lists` (`id`, `data`, `login_users`, `type_id`, `status_id`, `message`) VALUES
(6, '2020-02-23', 'user', 2, 4, 'не отказано');

-- --------------------------------------------------------

--
-- Структура таблицы `people`
--

CREATE TABLE `people` (
  `id` int(10) NOT NULL,
  `last_name` varchar(25) NOT NULL,
  `first_name` varchar(25) NOT NULL,
  `middle_name` varchar(25) DEFAULT NULL,
  `birthday` date NOT NULL,
  `sex` tinyint(1) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Дамп данных таблицы `people`
--

INSERT INTO `people` (`id`, `last_name`, `first_name`, `middle_name`, `birthday`, `sex`) VALUES
(1, 'Петров', 'Петр', 'Петрович', '2019-11-19', 1);

-- --------------------------------------------------------

--
-- Структура таблицы `people_posts`
--

CREATE TABLE `people_posts` (
  `person_id` int(11) NOT NULL,
  `post_id` int(11) NOT NULL,
  `salary` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Структура таблицы `posts`
--

CREATE TABLE `posts` (
  `id` int(10) NOT NULL,
  `name` varchar(25) NOT NULL,
  `short_name` varchar(15) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Структура таблицы `roles`
--

CREATE TABLE `roles` (
  `id` int(10) UNSIGNED NOT NULL,
  `name` varchar(20) NOT NULL,
  `level` tinyint(3) UNSIGNED NOT NULL,
  `description` text
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Дамп данных таблицы `roles`
--

INSERT INTO `roles` (`id`, `name`, `level`, `description`) VALUES
(1, 'Администратор', 1, 'Это администратор. '),
(6, 'Администратор1', 1, 'Это робот, он тут рулит. '),
(7, 'Пользователь', 3, NULL);

-- --------------------------------------------------------

--
-- Структура таблицы `roles_exam`
--

CREATE TABLE `roles_exam` (
  `id` int(11) NOT NULL,
  `title` varchar(25) NOT NULL,
  `id_roles` int(11) NOT NULL,
  `description` varchar(25) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Дамп данных таблицы `roles_exam`
--

INSERT INTO `roles_exam` (`id`, `title`, `id_roles`, `description`) VALUES
(1, 'admin', 1, 'Суперпользователь'),
(2, 'user', 2, 'Обычный пользователь'),
(3, 'sysadmin', 3, 'специалист ');

-- --------------------------------------------------------

--
-- Структура таблицы `status`
--

CREATE TABLE `status` (
  `id` int(11) NOT NULL,
  `title` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Дамп данных таблицы `status`
--

INSERT INTO `status` (`id`, `title`) VALUES
(1, 'новое'),
(2, 'в работе'),
(3, 'ошибочно'),
(4, 'отказано'),
(5, 'решено');

-- --------------------------------------------------------

--
-- Структура таблицы `types`
--

CREATE TABLE `types` (
  `id` int(11) NOT NULL,
  `title` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Дамп данных таблицы `types`
--

INSERT INTO `types` (`id`, `title`) VALUES
(1, 'Проблемы с компьютером'),
(2, 'Доступ в интернет'),
(3, 'Доступ к общим ресурсам организации'),
(4, 'Предоставление доступа'),
(5, 'другое');

-- --------------------------------------------------------

--
-- Структура таблицы `users`
--

CREATE TABLE `users` (
  `id` int(11) NOT NULL,
  `login` varchar(28) NOT NULL,
  `password` varchar(40) NOT NULL,
  `first_name` varchar(20) NOT NULL,
  `last_name` varchar(20) NOT NULL,
  `middle_name` varchar(20) DEFAULT NULL,
  `role_id` int(10) UNSIGNED DEFAULT NULL,
  `crested_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Дамп данных таблицы `users`
--

INSERT INTO `users` (`id`, `login`, `password`, `first_name`, `last_name`, `middle_name`, `role_id`, `crested_at`) VALUES
(1, 'admin', 'qwerty', 'Геннадий', 'Иванов', 'Николаевич', 1, '2019-11-12 16:24:55'),
(2, 'user', 'skfaf10', 'Урсула', 'Меркель', 'Петровна', 1, '2019-11-12 16:24:55'),
(100, 'gters', 'qwerty', 'Иван', 'Иванов', NULL, 1, '2019-11-12 16:24:55'),
(101, 'user345', 'quertws', 'Ричард', 'Дик', NULL, 1, '2019-11-12 16:24:55');

-- --------------------------------------------------------

--
-- Структура таблицы `users_exam`
--

CREATE TABLE `users_exam` (
  `id` int(11) NOT NULL,
  `login` varchar(25) NOT NULL,
  `password_hash` varchar(59) NOT NULL,
  `roles_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Дамп данных таблицы `users_exam`
--

INSERT INTO `users_exam` (`id`, `login`, `password_hash`, `roles_id`) VALUES
(1, 'admin', '58acb7acccce58ffa8b953b12b5a7702bd42dae441c1ad85057fa70b', 1),
(2, 'user', '147ad31215fd55112ce613a7883902bb306aa35bba879cd2dbe500b9', 2),
(3, 'sysadmin', '02f382b76ca1ab7aa06ab03345c7712fd5b971fb0c0f2aef98bac9cd', 3);

--
-- Индексы сохранённых таблиц
--

--
-- Индексы таблицы `lists`
--
ALTER TABLE `lists`
  ADD PRIMARY KEY (`id`),
  ADD KEY `login_users` (`login_users`,`type_id`,`status_id`),
  ADD KEY `status_id` (`status_id`),
  ADD KEY `type_id` (`type_id`);

--
-- Индексы таблицы `people`
--
ALTER TABLE `people`
  ADD PRIMARY KEY (`id`);

--
-- Индексы таблицы `people_posts`
--
ALTER TABLE `people_posts`
  ADD KEY `person_id` (`person_id`),
  ADD KEY `post_id` (`post_id`);

--
-- Индексы таблицы `posts`
--
ALTER TABLE `posts`
  ADD PRIMARY KEY (`id`);

--
-- Индексы таблицы `roles`
--
ALTER TABLE `roles`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `name` (`name`);

--
-- Индексы таблицы `roles_exam`
--
ALTER TABLE `roles_exam`
  ADD PRIMARY KEY (`id`),
  ADD KEY `id_roles` (`id_roles`);

--
-- Индексы таблицы `status`
--
ALTER TABLE `status`
  ADD PRIMARY KEY (`id`);

--
-- Индексы таблицы `types`
--
ALTER TABLE `types`
  ADD PRIMARY KEY (`id`);

--
-- Индексы таблицы `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `unique _login` (`login`),
  ADD KEY `role_id` (`role_id`);

--
-- Индексы таблицы `users_exam`
--
ALTER TABLE `users_exam`
  ADD PRIMARY KEY (`id`),
  ADD KEY `roles_id` (`roles_id`),
  ADD KEY `login` (`login`);

--
-- AUTO_INCREMENT для сохранённых таблиц
--

--
-- AUTO_INCREMENT для таблицы `lists`
--
ALTER TABLE `lists`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=19;

--
-- AUTO_INCREMENT для таблицы `people`
--
ALTER TABLE `people`
  MODIFY `id` int(10) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT для таблицы `posts`
--
ALTER TABLE `posts`
  MODIFY `id` int(10) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT для таблицы `roles`
--
ALTER TABLE `roles`
  MODIFY `id` int(10) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- AUTO_INCREMENT для таблицы `roles_exam`
--
ALTER TABLE `roles_exam`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT для таблицы `status`
--
ALTER TABLE `status`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT для таблицы `types`
--
ALTER TABLE `types`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT для таблицы `users`
--
ALTER TABLE `users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=102;

--
-- AUTO_INCREMENT для таблицы `users_exam`
--
ALTER TABLE `users_exam`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- Ограничения внешнего ключа сохраненных таблиц
--

--
-- Ограничения внешнего ключа таблицы `lists`
--
ALTER TABLE `lists`
  ADD CONSTRAINT `lists_ibfk_1` FOREIGN KEY (`login_users`) REFERENCES `users_exam` (`login`),
  ADD CONSTRAINT `lists_ibfk_2` FOREIGN KEY (`status_id`) REFERENCES `status` (`id`),
  ADD CONSTRAINT `lists_ibfk_3` FOREIGN KEY (`type_id`) REFERENCES `types` (`id`);

--
-- Ограничения внешнего ключа таблицы `people_posts`
--
ALTER TABLE `people_posts`
  ADD CONSTRAINT `people_posts_ibfk_1` FOREIGN KEY (`person_id`) REFERENCES `people` (`id`),
  ADD CONSTRAINT `people_posts_ibfk_2` FOREIGN KEY (`post_id`) REFERENCES `posts` (`id`);

--
-- Ограничения внешнего ключа таблицы `roles_exam`
--
ALTER TABLE `roles_exam`
  ADD CONSTRAINT `roles_exam_ibfk_1` FOREIGN KEY (`id_roles`) REFERENCES `users_exam` (`roles_id`);

--
-- Ограничения внешнего ключа таблицы `users`
--
ALTER TABLE `users`
  ADD CONSTRAINT `users_ibfk_1` FOREIGN KEY (`role_id`) REFERENCES `roles` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
