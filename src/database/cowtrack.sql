-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 04-03-2025 a las 19:18:54
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
  `Contraseña` varchar(255) NOT NULL,
  `ID_Dueño` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `granja`
--

CREATE TABLE `granja` (
  `ID_Granja` int(11) NOT NULL,
  `Dirección` text NOT NULL,
  `Tatuaje` varchar(20) NOT NULL,
  `ID_Dueño` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `lote`
--

CREATE TABLE `lote` (
  `ID_Lote` int(11) NOT NULL,
  `Fecha_Registro` date NOT NULL,
  `ID_Vaca` int(11) NOT NULL,
  `ID_Granja` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

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
  `ID_Fierro` varchar(50) NOT NULL,
  `ID_Lote` int(11) NOT NULL,
  `ID_Arete` varchar(50) NOT NULL,
  `Genero` enum('Macho','Hembra') NOT NULL,
  `Fecha_Nacimiento` date NOT NULL,
  `Raza` varchar(50) NOT NULL,
  `Estado_Salud` enum('Sano','Enfermo') NOT NULL,
  `Observaciones` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

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
  ADD UNIQUE KEY `ID_Dueño` (`ID_Dueño`);

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
  ADD UNIQUE KEY `ID_Granja` (`ID_Granja`);

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
  ADD UNIQUE KEY `ID_Lote` (`ID_Lote`);

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `empleado`
--
ALTER TABLE `empleado`
  ADD CONSTRAINT `empleado_ibfk_1` FOREIGN KEY (`ID_Dueño`) REFERENCES `dueño` (`ID_Dueno`) ON UPDATE CASCADE,
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
