-- phpMyAdmin SQL Dump
-- version 5.2.2
-- https://www.phpmyadmin.net/
--
-- Servidor: localhost:3306
-- Tiempo de generación: 14-07-2026 a las 02:34:31
-- Versión del servidor: 10.4.32-MariaDB
-- Versión de PHP: 8.3.16

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `rosario_cakes`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `clientes`
--

CREATE TABLE `clientes` (
  `id_cliente` int(11) NOT NULL,
  `nombre` varchar(100) NOT NULL,
  `tipo_pago` enum('Efectivo','Tarjeta','Transferencia','Crédito') NOT NULL DEFAULT 'Efectivo',
  `fecha_registro` timestamp NOT NULL DEFAULT current_timestamp(),
  `telefono` varchar(20) DEFAULT NULL,
  `direccion` varchar(255) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `clientes`
--

INSERT INTO `clientes` (`id_cliente`, `nombre`, `tipo_pago`, `fecha_registro`, `telefono`, `direccion`, `email`) VALUES
(1, 'Cliente General', 'Efectivo', '2025-10-24 12:00:00', '809-555-0001', NULL, NULL),
(2, 'María González', 'Tarjeta', '2025-10-24 12:00:00', '809-555-1002', 'Calle Principal #123', 'maria@email.com'),
(3, 'Eventos ABC', 'Crédito', '2025-10-24 12:00:00', '809-555-2003', 'Av. Central #456', 'eventos@abc.com'),
(4, 'Pedro Martínez', 'Transferencia', '2025-10-24 12:00:00', '809-555-3004', NULL, 'pedro@email.com'),
(5, 'Yennifer Carina', 'Efectivo', '2025-10-25 02:23:33', '8296758765', NULL, NULL),
(6, 'Jose Manuel', 'Transferencia', '2025-10-26 04:35:27', '59898485847', NULL, NULL);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `facturas`
--

CREATE TABLE `facturas` (
  `id_factura` int(11) NOT NULL,
  `id_pedido` int(11) NOT NULL,
  `ncf` varchar(20) NOT NULL,
  `monto_total` decimal(10,2) NOT NULL,
  `fecha_emision` timestamp NOT NULL DEFAULT current_timestamp(),
  `estado` enum('Válida','Anulada') DEFAULT 'Válida'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `pagos`
--

CREATE TABLE `pagos` (
  `id_pago` int(11) NOT NULL,
  `id_pedido` int(11) NOT NULL,
  `monto` decimal(10,2) NOT NULL,
  `metodo` enum('Efectivo','Tarjeta','Transferencia','Crédito') NOT NULL,
  `estado` enum('Pendiente','Completado','Cancelado') DEFAULT 'Completado',
  `fecha_pago` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `pasteles`
--

CREATE TABLE `pasteles` (
  `id_pastel` int(11) NOT NULL,
  `nombre` varchar(100) NOT NULL,
  `descripcion` varchar(255) DEFAULT NULL,
  `precio_base` decimal(10,2) NOT NULL,
  `categoria` enum('Cumpleaños','Boda','Celebración','Infantil','Personalizado','Postres') NOT NULL,
  `disponible` tinyint(1) DEFAULT 1,
  `imagen` varchar(255) DEFAULT NULL,
  `fecha_actualizacion` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `pasteles`
--

INSERT INTO `pasteles` (`id_pastel`, `nombre`, `descripcion`, `precio_base`, `categoria`, `disponible`, `imagen`, `fecha_actualizacion`) VALUES
(1, 'Pastel de Chocolate Clásico', 'Delicioso pastel de chocolate con relleno de trufa', 1500.00, 'Cumpleaños', 1, NULL, '2025-10-24 12:00:00'),
(2, 'Tres Leches Tradicional', 'Esponjoso pastel bañado en tres tipos de leche', 1200.00, 'Celebración', 1, NULL, '2025-10-24 12:00:00'),
(3, 'Red Velvet Premium', 'Pastel red velvet con frosting de queso crema', 1800.00, 'Cumpleaños', 1, NULL, '2025-10-24 12:00:00'),
(4, 'Pastel de Boda Elegante', 'Diseño personalizado de múltiples pisos', 5000.00, 'Boda', 1, NULL, '2025-10-24 12:00:00'),
(5, 'Pastel Infantil Temático', 'Diseños personalizados para niños', 2000.00, 'Infantil', 1, NULL, '2025-10-24 12:00:00'),
(6, 'Cheesecake de Fresa', 'Suave cheesecake con cobertura de fresas', 1400.00, 'Postres', 1, NULL, '2025-10-24 12:00:00'),
(7, 'Torta Zanahoria', 'Con nueces y frosting de queso crema', 1300.00, 'Celebración', 1, NULL, '2025-10-24 12:00:00'),
(8, 'Pastel Personalizado', 'Diseño completamente a medida', 2500.00, 'Personalizado', 1, NULL, '2025-10-24 12:00:00'),
(9, 'Tres Leche', NULL, 1500.00, 'Cumpleaños', 1, NULL, '2025-10-26 04:36:49'),
(10, 'Pastel de chocolate con caramelos', NULL, 1300.00, '', 0, NULL, '2025-10-26 04:38:32');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `pedidos`
--

CREATE TABLE `pedidos` (
  `id_pedido` int(11) NOT NULL,
  `id_cliente` int(11) NOT NULL,
  `id_pastel` int(11) NOT NULL,
  `cantidad` int(11) NOT NULL DEFAULT 1,
  `tamaño` enum('Pequeño','Mediano','Grande','Extra Grande') NOT NULL DEFAULT 'Mediano',
  `fecha_pedido` datetime NOT NULL,
  `fecha_entrega` datetime NOT NULL,
  `observaciones` text DEFAULT NULL,
  `estado` enum('Pendiente','En Preparación','Listo','Entregado','Cancelado') DEFAULT 'Pendiente'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `pedidos`
--

INSERT INTO `pedidos` (`id_pedido`, `id_cliente`, `id_pastel`, `cantidad`, `tamaño`, `fecha_pedido`, `fecha_entrega`, `observaciones`, `estado`) VALUES
(1, 6, 9, 1, 'Mediano', '2025-10-26 04:41:02', '2025-10-28 00:00:00', 'Quisiera que sea lo mas ante posible porfavor', 'Pendiente'),
(2, 5, 9, 2, 'Mediano', '2025-10-31 02:03:01', '2025-10-23 00:00:00', 'grhty', 'Pendiente');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `usuarios`
--

CREATE TABLE `usuarios` (
  `id_usuario` int(11) NOT NULL,
  `usuario` varchar(50) NOT NULL,
  `password` varchar(100) NOT NULL,
  `nombre` varchar(100) NOT NULL,
  `rol` enum('admin','vendedor','repostero') NOT NULL DEFAULT 'vendedor',
  `fecha_creacion` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `usuarios`
--

INSERT INTO `usuarios` (`id_usuario`, `usuario`, `password`, `nombre`, `rol`, `fecha_creacion`) VALUES
(1, 'admin', 'admin123', 'Rosario Administrador', 'admin', '2025-10-24 12:00:00'),
(2, 'vendedor', 'vendedor123', 'Vendedor Principal', 'vendedor', '2025-10-24 12:00:00'),
(3, 'repostero', 'repostero123', 'Chef Repostero', 'repostero', '2025-10-24 12:00:00');

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `clientes`
--
ALTER TABLE `clientes`
  ADD PRIMARY KEY (`id_cliente`);

--
-- Indices de la tabla `facturas`
--
ALTER TABLE `facturas`
  ADD PRIMARY KEY (`id_factura`),
  ADD UNIQUE KEY `ncf` (`ncf`),
  ADD KEY `id_pedido` (`id_pedido`);

--
-- Indices de la tabla `pagos`
--
ALTER TABLE `pagos`
  ADD PRIMARY KEY (`id_pago`),
  ADD KEY `id_pedido` (`id_pedido`);

--
-- Indices de la tabla `pasteles`
--
ALTER TABLE `pasteles`
  ADD PRIMARY KEY (`id_pastel`);

--
-- Indices de la tabla `pedidos`
--
ALTER TABLE `pedidos`
  ADD PRIMARY KEY (`id_pedido`),
  ADD KEY `id_cliente` (`id_cliente`),
  ADD KEY `id_pastel` (`id_pastel`);

--
-- Indices de la tabla `usuarios`
--
ALTER TABLE `usuarios`
  ADD PRIMARY KEY (`id_usuario`),
  ADD UNIQUE KEY `usuario` (`usuario`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `clientes`
--
ALTER TABLE `clientes`
  MODIFY `id_cliente` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT de la tabla `facturas`
--
ALTER TABLE `facturas`
  MODIFY `id_factura` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `pagos`
--
ALTER TABLE `pagos`
  MODIFY `id_pago` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `pasteles`
--
ALTER TABLE `pasteles`
  MODIFY `id_pastel` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT de la tabla `pedidos`
--
ALTER TABLE `pedidos`
  MODIFY `id_pedido` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT de la tabla `usuarios`
--
ALTER TABLE `usuarios`
  MODIFY `id_usuario` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `facturas`
--
ALTER TABLE `facturas`
  ADD CONSTRAINT `facturas_ibfk_1` FOREIGN KEY (`id_pedido`) REFERENCES `pedidos` (`id_pedido`);

--
-- Filtros para la tabla `pagos`
--
ALTER TABLE `pagos`
  ADD CONSTRAINT `pagos_ibfk_1` FOREIGN KEY (`id_pedido`) REFERENCES `pedidos` (`id_pedido`);

--
-- Filtros para la tabla `pedidos`
--
ALTER TABLE `pedidos`
  ADD CONSTRAINT `pedidos_ibfk_1` FOREIGN KEY (`id_cliente`) REFERENCES `clientes` (`id_cliente`),
  ADD CONSTRAINT `pedidos_ibfk_2` FOREIGN KEY (`id_pastel`) REFERENCES `pasteles` (`id_pastel`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
