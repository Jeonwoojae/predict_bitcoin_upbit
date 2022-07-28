CREATE TABLE IF NOT EXISTS `data` (
  `dateCoin` datetime DEFAULT NULL,
  `idCoin` text COLLATE utf8mb3_unicode_ci DEFAULT NULL,
  `open` double DEFAULT NULL,
  `high` double DEFAULT NULL,
  `low` double DEFAULT NULL,
  `close` double DEFAULT NULL,
  `volume` double DEFAULT NULL,
  `value` double DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_unicode_ci;