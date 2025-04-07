-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 06-04-2025 a las 19:43:16
-- Versión del servidor: 10.4.32-MariaDB
-- Versión de PHP: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `cowtrack`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `dueño`
--

CREATE TABLE `dueño` (
  `ID_Dueno` int(11) NOT NULL,
  `Nombre` varchar(100) NOT NULL,
  `correo` varchar(100) NOT NULL,
  `password` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `dueño`
--

INSERT INTO `dueño` (`ID_Dueno`, `Nombre`, `correo`, `password`) VALUES
(1, 'Alex', 'al062587@uacam.mx', 'scrypt:32768:8:1$x77FPYdGrZiA01nS$932ee18aaba33ae3bad197fcfcbcb6b1f19dbcdf125d39f5cd2b95d7be139a8a231bfb3edaf0ced597b5419f32b31c1a7a1517c301f68ed2fd79701350e2821c');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `empleado`
--

CREATE TABLE `empleado` (
  `ID_Empleado` int(11) NOT NULL,
  `Nombre` varchar(100) NOT NULL,
  `ID_Rol` int(11) NOT NULL,
  `Correo` varchar(100) NOT NULL,
  `password` varchar(255) NOT NULL,
  `ID_Dueno` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `granja`
--

CREATE TABLE `granja` (
  `ID_Granja` int(11) NOT NULL,
  `Dirección` text NOT NULL,
  `Cant_Ganado` int(11) NOT NULL,
  `Status` tinyint(1) NOT NULL,
  `Tatuaje` varchar(20) NOT NULL,
  `ID_Dueño` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `granja`
--

INSERT INTO `granja` (`ID_Granja`, `Dirección`, `Cant_Ganado`, `Status`, `Tatuaje`, `ID_Dueño`) VALUES
(1, 'Avenida', 2, 1, 'herrado1', 1);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `lote`
--

CREATE TABLE `lote` (
  `ID_Lote` int(11) NOT NULL,
  `Fecha_Registro` date NOT NULL,
  `Herraje` varchar(100) NOT NULL,
  `Cant_Vacuno` int(11) NOT NULL,
  `Status` tinyint(1) NOT NULL,
  `ID_Granja` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `lote`
--

INSERT INTO `lote` (`ID_Lote`, `Fecha_Registro`, `Herraje`, `Cant_Vacuno`, `Status`, `ID_Granja`) VALUES
(9, '2025-03-08', 'herrado1', 2, 1, 1),
(10, '2025-03-10', 'herrado2', 3, 1, 1),
(11, '2025-03-14', 'herrado3', 3, 1, 1),
(12, '2025-03-16', 'herrado2', 2, 0, 1),
(13, '2025-03-17', 'herrado1', 2, 1, 1);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `rol`
--

CREATE TABLE `rol` (
  `ID_Rol` int(11) NOT NULL,
  `Nombre_Rol` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `vacuno`
--

CREATE TABLE `vacuno` (
  `ID_Vaca` int(11) NOT NULL,
  `ID_Lote` int(11) NOT NULL,
  `ID_Arete` varchar(50) NOT NULL,
  `Genero` enum('Macho','Hembra') NOT NULL,
  `Fecha_Nacimiento` date NOT NULL,
  `Raza` varchar(50) NOT NULL,
  `Estado_Salud` enum('Sano','Enfermo') NOT NULL,
  `Observaciones` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `vacuno`
--

INSERT INTO `vacuno` (`ID_Vaca`, `ID_Lote`, `ID_Arete`, `Genero`, `Fecha_Nacimiento`, `Raza`, `Estado_Salud`, `Observaciones`) VALUES
(1, 9, '7sjdf8', 'Macho', '2024-03-12', 'Toro', 'Sano', 'De bajo peso, se requiere mayor alimentación'),
(2, 12, 'sjak91', 'Hembra', '2024-11-09', 'Vaca', 'Sano', 'Preñada, pronto a dar a luz'),
(3, 9, '894jYo9P', 'Macho', '2025-03-15', 'Toro', 'Enfermo', 'Desarrolló una infección intestinal'),
(4, 11, '72JgMNh91', 'Macho', '2025-01-15', 'Toro', 'Enfermo', 'Presenta protuberancias en la zona de la oreja izquierda');

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `dueño`
--
ALTER TABLE `dueño`
  ADD PRIMARY KEY (`ID_Dueno`),
  ADD UNIQUE KEY `ID_Dueño` (`ID_Dueno`);

--
-- Indices de la tabla `empleado`
--
ALTER TABLE `empleado`
  ADD PRIMARY KEY (`ID_Empleado`),
  ADD UNIQUE KEY `ID_Rol` (`ID_Rol`),
  ADD UNIQUE KEY `ID_Dueno` (`ID_Dueno`) USING BTREE;

--
-- Indices de la tabla `granja`
--
ALTER TABLE `granja`
  ADD PRIMARY KEY (`ID_Granja`),
  ADD UNIQUE KEY `ID_Granja` (`ID_Granja`),
  ADD UNIQUE KEY `ID_Dueño` (`ID_Dueño`);

--
-- Indices de la tabla `lote`
--
ALTER TABLE `lote`
  ADD PRIMARY KEY (`ID_Lote`),
  ADD UNIQUE KEY `ID_Lote` (`ID_Lote`),
  ADD KEY `ID_Granja` (`ID_Granja`) USING BTREE;

--
-- Indices de la tabla `rol`
--
ALTER TABLE `rol`
  ADD PRIMARY KEY (`ID_Rol`),
  ADD UNIQUE KEY `ID_Rol` (`ID_Rol`);

--
-- Indices de la tabla `vacuno`
--
ALTER TABLE `vacuno`
  ADD PRIMARY KEY (`ID_Vaca`),
  ADD KEY `ID_Lote` (`ID_Lote`) USING BTREE;

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `dueño`
--
ALTER TABLE `dueño`
  MODIFY `ID_Dueno` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT de la tabla `empleado`
--
ALTER TABLE `empleado`
  MODIFY `ID_Empleado` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `granja`
--
ALTER TABLE `granja`
  MODIFY `ID_Granja` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT de la tabla `lote`
--
ALTER TABLE `lote`
  MODIFY `ID_Lote` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=14;

--
-- AUTO_INCREMENT de la tabla `rol`
--
ALTER TABLE `rol`
  MODIFY `ID_Rol` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `vacuno`
--
ALTER TABLE `vacuno`
  MODIFY `ID_Vaca` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `empleado`
--
ALTER TABLE `empleado`
  ADD CONSTRAINT `empleado_ibfk_1` FOREIGN KEY (`ID_Dueno`) REFERENCES `dueño` (`ID_Dueno`) ON UPDATE CASCADE,
  ADD CONSTRAINT `empleado_ibfk_2` FOREIGN KEY (`ID_Rol`) REFERENCES `rol` (`ID_Rol`) ON UPDATE CASCADE;

--
-- Filtros para la tabla `granja`
--
ALTER TABLE `granja`
  ADD CONSTRAINT `granja_ibfk_1` FOREIGN KEY (`ID_Dueño`) REFERENCES `dueño` (`ID_Dueno`) ON UPDATE CASCADE;

--
-- Filtros para la tabla `lote`
--
ALTER TABLE `lote`
  ADD CONSTRAINT `lote_ibfk_1` FOREIGN KEY (`ID_Granja`) REFERENCES `granja` (`ID_Granja`) ON UPDATE CASCADE;

--
-- Filtros para la tabla `vacuno`
--
ALTER TABLE `vacuno`
  ADD CONSTRAINT `vacuno_ibfk_1` FOREIGN KEY (`ID_Lote`) REFERENCES `lote` (`ID_Lote`) ON UPDATE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
