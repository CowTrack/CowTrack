-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 08-05-2025 a las 07:16:51
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
(1, 'Alex', 'al062587@uacam.mx', 'scrypt:32768:8:1$x77FPYdGrZiA01nS$932ee18aaba33ae3bad197fcfcbcb6b1f19dbcdf125d39f5cd2b95d7be139a8a231bfb3edaf0ced597b5419f32b31c1a7a1517c301f68ed2fd79701350e2821c'),
(2, 'Kevin', 'saraviakex@gmail.com', 'scrypt:32768:8:1$x77FPYdGrZiA01nS$932ee18aaba33ae3bad197fcfcbcb6b1f19dbcdf125d39f5cd2b95d7be139a8a231bfb3edaf0ced597b5419f32b31c1a7a1517c301f68ed2fd79701350e2821c');

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
(1, 'Avenida', 2, 1, 'herrado3', 1);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `lote`
--

CREATE TABLE `lote` (
  `ID_Lote` int(11) NOT NULL,
  `Fecha_Registro` date NOT NULL,
  `Cant_Vacuno` int(11) NOT NULL,
  `Status` tinyint(1) NOT NULL,
  `ID_Granja` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `lote`
--

INSERT INTO `lote` (`ID_Lote`, `Fecha_Registro`, `Cant_Vacuno`, `Status`, `ID_Granja`) VALUES
(9, '2025-03-08', 2, 1, 1),
(10, '2025-03-10', 8, 1, 1),
(11, '2025-03-14', 3, 1, 1),
(12, '2025-03-16', 2, 0, 1),
(13, '2025-03-17', 2, 1, 1),
(14, '2025-05-07', 1, 1, 1);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `reporte`
--

CREATE TABLE `reporte` (
  `ID_Reporte` int(11) NOT NULL,
  `ID_Vaca` int(11) NOT NULL,
  `Fecha_Reporte` date NOT NULL,
  `Tipo_Reporte` varchar(50) NOT NULL,
  `Observacion` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `reporte`
--

INSERT INTO `reporte` (`ID_Reporte`, `ID_Vaca`, `Fecha_Reporte`, `Tipo_Reporte`, `Observacion`) VALUES
(1, 3, '2025-05-07', 'Diagnóstico', 'El vacuno presenta manchas en la zona de la pata delantera derecha');

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
  `ID_Fierro` varchar(50) NOT NULL,
  `Genero` enum('Macho','Hembra') NOT NULL,
  `Fecha_Nacimiento` date NOT NULL,
  `Fecha_Registro` date NOT NULL,
  `Raza` varchar(50) NOT NULL,
  `Estado_Salud` enum('Sano','Enfermo') NOT NULL,
  `Proposito` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `vacuno`
--

INSERT INTO `vacuno` (`ID_Vaca`, `ID_Lote`, `ID_Arete`, `ID_Fierro`, `Genero`, `Fecha_Nacimiento`, `Fecha_Registro`, `Raza`, `Estado_Salud`, `Proposito`) VALUES
(1, 9, '7sjdf8', 'CD-738', 'Macho', '2024-03-12', '2025-04-01', 'Gyr', 'Sano', 'Carne'),
(2, 12, 'sjak91', 'KJ-234', 'Hembra', '2024-11-09', '2025-04-10', 'Guzerat', 'Sano', 'Lechera'),
(3, 9, '894jYo9P', 'LM-111', 'Macho', '2025-01-04', '2025-04-09', 'Guzerat', 'Enfermo', 'Carne'),
(8, 11, '9jsu2', 'CD-543', 'Hembra', '2024-03-14', '2025-04-09', 'Brahman', 'Sano', 'Lechera'),
(9, 14, '3jak91', 'LZ-230', 'Macho', '2022-06-07', '2025-05-07', 'Suizo americano', 'Sano', 'Fin zootecnico'),
(11, 10, '22222', 'MA-234', 'Macho', '2025-01-01', '2025-05-07', 'Brahman', 'Sano', 'Carne'),
(12, 10, '5kjlp1', 'GF-000', 'Hembra', '2025-03-17', '2025-05-07', 'Guzerat', 'Sano', 'Reproductora'),
(13, 10, 'lp23rt', 'KL397', 'Hembra', '2025-05-02', '2025-05-07', 'Simbrah', 'Sano', 'Reproductora'),
(14, 10, '12345', 'XS-123', 'Macho', '2024-11-21', '2025-05-07', 'Gyr', 'Sano', 'Carne');

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
  ADD KEY `ID_Dueño` (`ID_Dueño`) USING BTREE;

--
-- Indices de la tabla `lote`
--
ALTER TABLE `lote`
  ADD PRIMARY KEY (`ID_Lote`),
  ADD UNIQUE KEY `ID_Lote` (`ID_Lote`),
  ADD KEY `ID_Granja` (`ID_Granja`) USING BTREE;

--
-- Indices de la tabla `reporte`
--
ALTER TABLE `reporte`
  ADD PRIMARY KEY (`ID_Reporte`),
  ADD KEY `ID_Vaca` (`ID_Vaca`);

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
  ADD UNIQUE KEY `ID_Arete` (`ID_Arete`),
  ADD KEY `ID_Lote` (`ID_Lote`) USING BTREE;

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `dueño`
--
ALTER TABLE `dueño`
  MODIFY `ID_Dueno` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT de la tabla `empleado`
--
ALTER TABLE `empleado`
  MODIFY `ID_Empleado` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `granja`
--
ALTER TABLE `granja`
  MODIFY `ID_Granja` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT de la tabla `lote`
--
ALTER TABLE `lote`
  MODIFY `ID_Lote` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=15;

--
-- AUTO_INCREMENT de la tabla `reporte`
--
ALTER TABLE `reporte`
  MODIFY `ID_Reporte` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT de la tabla `rol`
--
ALTER TABLE `rol`
  MODIFY `ID_Rol` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `vacuno`
--
ALTER TABLE `vacuno`
  MODIFY `ID_Vaca` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=15;

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
-- Filtros para la tabla `reporte`
--
ALTER TABLE `reporte`
  ADD CONSTRAINT `reporte_ibfk_1` FOREIGN KEY (`ID_Vaca`) REFERENCES `vacuno` (`ID_Vaca`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Filtros para la tabla `vacuno`
--
ALTER TABLE `vacuno`
  ADD CONSTRAINT `vacuno_ibfk_1` FOREIGN KEY (`ID_Lote`) REFERENCES `lote` (`ID_Lote`) ON UPDATE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
