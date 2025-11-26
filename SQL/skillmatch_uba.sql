- phpMyAdmin SQL Dump
-- version 5.2.1deb3
-- https://www.phpmyadmin.net/
--
-- Servidor: localhost:3306


SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `skillmatch_uba`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `formato`
--

CREATE TABLE `formato` (
  `id_formato` int NOT NULL,
  `nombre` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `formato`
--

INSERT INTO `formato` (`id_formato`, `nombre`) VALUES
(3, 'carpeta comprimida'),
(2, 'imagen'),
(1, 'pdf'),
(4, 'repositorio');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `materias`
--

CREATE TABLE `materias` (
  `id` int NOT NULL,
  `codigo` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `materia` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `materias`
--

INSERT INTO `materias` (`id`, `codigo`, `materia`) VALUES
(244, 'AGR01', 'Sistemas de Coordenadas'),
(245, 'AGR02', 'Sistemas de Representación Orientado a la Agrimensura'),
(246, 'AGR03', 'Dibujo Cartográfico y Topográfico'),
(247, 'AGR04', 'Introducción a la Ingeniería en Agrimensura'),
(248, 'AGR05', 'Instrumental Topográfico'),
(249, 'AGR06', 'Derecho para Agrimensura'),
(250, 'AGR07', 'Elementos de Construcción'),
(251, 'AGR08', 'Métodos Topográficos'),
(252, 'AGR09', 'Cálculo de Compensación'),
(253, 'AGR10', 'Cartografía'),
(254, 'AGR11', 'Geodesia Astronómica y Mediciones Precisas'),
(255, 'AGR12', 'Relevamientos Topográficos'),
(256, 'AGR13', 'Geodesia Geométrica y Satelital'),
(257, 'AGR14', 'Fotogrametría'),
(258, 'AGR15', 'Normativa de Mensura y Propiedad Horizontal'),
(259, 'AGR16', 'Georreferenciación de Trabajos Topográficos y Geodésicos'),
(260, 'AGR17', 'Fotogrametría Digital'),
(261, 'AGR18', 'Aplicación Legal de la Agrimensura'),
(262, 'AGR19', 'Geografía Física y Geología'),
(263, 'AGR20', 'Sistemas de Información Geográfica'),
(264, 'AGR21', 'Catastro'),
(265, 'AGR22', 'Mensuras'),
(266, 'AGR23', 'Teledetección para Agrimensura'),
(267, 'AGR24', 'Información Rural'),
(268, 'AGR25', 'Topografía de Obra'),
(269, 'AGR26', 'Mensuras Aplicadas'),
(270, 'AGR27', 'Valuaciones'),
(271, 'AGR28', 'Tecnologías de Información Geoespacial'),
(272, 'AGR29', 'Planeamiento Urbano e Impacto Social y Ambiental'),
(295, 'ALI01', 'Introducción a la Ingeniería en Alimentos'),
(296, 'ALI02', 'Óptica'),
(297, 'ALI03', 'Fundamentos de Procesos Químicos'),
(298, 'ALI04', 'Laboratorio de Química'),
(299, 'ALI05', 'Química de los compuestos orgánicos'),
(300, 'ALI06', 'Termodinámica de los Procesos'),
(301, 'ALI07', 'Fenómenos de Transporte'),
(302, 'ALI08', 'Modelación Numérica'),
(303, 'ALI09', 'Química Física'),
(304, 'ALI10', 'Química Biológica y de Alimentos'),
(305, 'ALI11', 'Microbiología General y de Alimentos'),
(306, 'ALI12', 'Operaciones Unitarias de Transferencia de Cantidad de Movimiento y Energía'),
(307, 'ALI13', 'Operaciones Unitarias de Transferencia de Materia'),
(308, 'ALI14', 'Fundamentos de la Preservación de Alimentos I (FCEN)'),
(309, 'ALI15', 'Química Analítica Instrumental'),
(310, 'ALI16', 'Laboratorio de Operaciones y Procesos'),
(311, 'ALI17', 'Instalaciones de Plantas de Procesos'),
(312, 'ALI18', 'Fundamentos de la Preservación de Alimentos II (FCEN)'),
(313, 'ALI19', 'Tecnología de Alimentos I (FCEN)'),
(314, 'ALI20', 'Procesamiento de Alimentos en Planta Piloto (FCEN)'),
(315, 'ALI21', 'Dinámica y Control de Procesos de Alimentos'),
(316, 'ALI22', 'Legislación Alimentaria (FFyB)'),
(317, 'ALI23', 'Tecnología de Alimentos II (bimestral)'),
(318, 'ALI24', 'Tecnología de Alimentos III (bimestral)'),
(319, 'ALI25', 'Biotecnología y Reactores para la Industria de Alimentos'),
(320, 'ALI26', 'Gestión del Trabajo y del Ambiente en la Industria Alimentaria'),
(15, 'BIO01', 'Introducción a la Bioingeniería'),
(16, 'BIO02', 'Anatomía e Histología Funcional'),
(17, 'BIO03', 'Algoritmos y Programación'),
(18, 'BIO04', 'Planificación de Proyectos'),
(19, 'BIO05', 'Química de los Compuestos Orgánicos'),
(20, 'BIO06', 'Señales y Sistemas'),
(21, 'BIO07', 'Sistemas Moleculares, Celulares y Tisulares'),
(22, 'BIO08', 'Física de Sólidos y Nuclear'),
(23, 'BIO09', 'Control Automático'),
(24, 'BIO10', 'Análisis de Circuitos'),
(25, 'BIO11', 'Procesos Estocásticos'),
(26, 'BIO12', 'Introducción a los Dispositivos Electrónicos'),
(27, 'BIO13', 'Sistemas Fisiológicos y sus Modelos'),
(28, 'BIO14', 'Introducción a la Mecánica del Continuo'),
(29, 'BIO15', 'Taller de Procesamiento de Señales'),
(30, 'BIO16', 'Circuitos Microelectrónicos'),
(31, 'BIO17', 'Introducción a los Sistemas Embebidos'),
(32, 'BIO18', 'Gestión de Proyectos'),
(33, 'BIO19', 'Introducción a la Biomecánica'),
(34, 'BIO20', 'Instrumentación y Equipamiento para Diagnóstico y Tratamiento'),
(35, 'BIO21', 'Introducción a los Biomateriales'),
(36, 'BIO22', 'Análisis y Procesamiento de Señales en Bioingeniería'),
(37, 'BIO23', 'Imágenes en Bioingeniería'),
(38, 'BIO24', 'Tecnología de Asistencia y Prótesis'),
(39, 'BIO25', 'Ingeniería Clínica y Hospitalaria'),
(170, 'CIV01', 'Introducción a la Ingeniería Civil'),
(171, 'CIV02', 'Estática'),
(172, 'CIV03', 'Introducción al Transporte, la Movilidad y el Urbanismo'),
(173, 'CIV04', 'Resistencia de Materiales'),
(174, 'CIV05', 'Hidráulica General'),
(175, 'CIV06', 'Calor y Termodinámica'),
(176, 'CIV07', 'Análisis Estructural'),
(177, 'CIV08', 'Comportamiento de Materiales'),
(178, 'CIV09', 'Hidráulica Aplicada'),
(179, 'CIV10', 'Mecánica de Suelos y Geología'),
(180, 'CIV11', 'Introducción a la Ciencia de Datos para Ingeniería Civil'),
(181, 'CIV12', 'Diseño Geométrico de Obras Lineales'),
(182, 'CIV13', 'Construcciones Civiles y Arquitectura'),
(183, 'CIV14', 'Topografía y Geodesia'),
(184, 'CIV15', 'Economía y Evaluación de Proyectos de Ingeniería Civil'),
(185, 'CIV16', 'Materiales Viales y Pavimentos I'),
(186, 'CIV17', 'Hidrología Aplicada'),
(187, 'CIV18', 'Hormigón I'),
(188, 'CIV19', 'Sistemas de Transporte Guiado I'),
(189, 'CIV20', 'Puertos y Vías Navegables I'),
(190, 'CIV21', 'Aeropuertos I'),
(191, 'CIV22', 'Ingeniería Sanitaria I'),
(192, 'CIV23', 'Estructuras Metálicas'),
(193, 'CIV24', 'Instalaciones de las Obras Civiles'),
(194, 'CIV25', 'Cimentaciones'),
(195, 'CIV26', 'Hormigón II'),
(196, 'CIV27', 'Gestión Socioambiental de las Obras Civiles'),
(197, 'CIV28', 'Gerenciamiento y Organización de Obras Civiles'),
(1, 'COM01', 'Análisis Matemático II'),
(2, 'COM02', 'Economía y Organización'),
(3, 'COM03', 'Electricidad y Magnetismo'),
(4, 'COM04', 'Electricidad, Magnetismo y Calor'),
(5, 'COM05', 'Física de los Sistemas de Partículas'),
(6, 'COM06', 'Higiene y Seguridad'),
(7, 'COM07', 'Impacto Social, Ambiental y Desarrollo Sustentable'),
(8, 'COM08', 'Introducción a la Ciencia de Datos'),
(9, 'COM09', 'Legislación y Ejercicio Profesional'),
(10, 'COM10', 'Modelación Numérica'),
(11, 'COM11', 'Probabilidad y Estadística'),
(12, 'COM12', 'Química Básica'),
(13, 'COM13', 'Taller de Electrónica'),
(14, 'COM14', 'Álgebra Lineal'),
(130, 'ELE01', 'Introducción a la Ingeniería Electrónica'),
(131, 'ELE02', 'Algoritmos y Programación'),
(132, 'ELE03', 'Introducción a los Dispositivos Electrónicos'),
(133, 'ELE04', 'Sistemas Digitales'),
(134, 'ELE05', 'Señales y Sistemas'),
(135, 'ELE06', 'Análisis de Circuitos'),
(136, 'ELE07', 'Redes de Comunicaciones'),
(137, 'ELE08', 'Planificación de Proyectos'),
(138, 'ELE09', 'Circuitos Microelectrónicos'),
(139, 'ELE10', 'Procesos Estocásticos'),
(140, 'ELE11', 'Control Automático'),
(141, 'ELE12', 'Taller de Sistemas Embebidos'),
(142, 'ELE13', 'Química y Electroquímica'),
(143, 'ELE14', 'Electromagnetismo Aplicado'),
(144, 'ELE15', 'Taller de Automatización y Control'),
(145, 'ELE16', 'Taller de Procesamiento de Señales'),
(146, 'ELE17', 'Dispositivos Semiconductores'),
(147, 'ELE18', 'Taller de Comunicaciones Digitales'),
(148, 'ELE19', 'Taller de Diseño de Circuitos Electrónicos'),
(149, 'ELE20', 'Gestión de Proyectos Electrónicos'),
(60, 'ENE01', 'Introducción a la Ingeniería en Energía Eléctrica'),
(61, 'ENE02', 'Estática y Resistencia de Materiales'),
(62, 'ENE03', 'Física de Sólidos y Nuclear'),
(63, 'ENE04', 'Electrotecnia'),
(64, 'ENE05', 'Análisis Matemático III'),
(65, 'ENE06', 'Campos Electromagnéticos'),
(66, 'ENE07', 'Circuitos y Sistemas de Control'),
(67, 'ENE08', 'Medidas Eléctricas'),
(68, 'ENE09', 'Termodinámica / Mecánica de Fluidos y Máquinas'),
(69, 'ENE10', 'Máquinas Eléctricas I'),
(70, 'ENE11', 'Tecnología de Materiales Eléctricos'),
(71, 'ENE12', 'Diagnósticos Eléctricos y Ensayos'),
(72, 'ENE13', 'Máquinas Eléctricas II'),
(73, 'ENE14', 'Mecánica Aplicada'),
(74, 'ENE15', 'Instalaciones de Baja Tensión y Luminotecnia'),
(75, 'ENE16', 'Sistemas Eléctricos de Potencia'),
(76, 'ENE17', 'Conversión Estática de la Energía Eléctrica'),
(77, 'ENE18', 'Economía de la Energía Eléctrica'),
(78, 'ENE19', 'Transmisión y Distribución de la Energía Eléctrica'),
(79, 'ENE20', 'Generación de Energía Eléctrica'),
(80, 'ENE21', 'Protecciones Eléctricas y Equipos de Maniobra'),
(273, 'IND01', 'Principios de Ingeniería Industrial'),
(274, 'IND02', 'Estática y Resistencia de Materiales'),
(275, 'IND03', 'Organización y Dirección Empresaria'),
(276, 'IND04', 'Probabilidad'),
(277, 'IND05', 'Economía'),
(278, 'IND06', 'Materiales y Aplicaciones I'),
(279, 'IND07', 'Transformación de la Energía'),
(280, 'IND08', 'Desarrollo Económico'),
(281, 'IND09', 'Estadística Aplicada'),
(282, 'IND10', 'Gestión Integral de la Cadena de Valor'),
(283, 'IND11', 'Electrotecnia, Máquinas e Instalaciones Eléctricas'),
(284, 'IND12', 'Investigación Operativa'),
(285, 'IND13', 'Sistemas Contables y Gestión de Costos'),
(286, 'IND14', 'Industrias Digitales'),
(287, 'IND15', 'Ingeniería Ambiental, Sustentabilidad y Cuidado del Planeta'),
(288, 'IND16', 'Ingeniería Económica'),
(289, 'IND17', 'Equipos y Sistemas para Automatización Industrial'),
(290, 'IND18', 'Industrias Químicas'),
(291, 'IND19', 'Transformación de Materiales'),
(292, 'IND20', 'Higiene y Seguridad'),
(293, 'IND21', 'Industrias Extractivas'),
(294, 'IND22', 'Proyecto Industrial'),
(40, 'INF01', 'Fundamentos de Programación'),
(41, 'INF02', 'Introducción al Desarrollo de Software'),
(42, 'INF03', 'Organización del Computador'),
(43, 'INF04', 'Algoritmos y Estructuras de Datos'),
(44, 'INF05', 'Teoría de Algoritmos'),
(45, 'INF06', 'Sistemas Operativos'),
(46, 'INF07', 'Paradigmas de Programación'),
(47, 'INF08', 'Base de Datos'),
(48, 'INF09', 'Taller de Programación'),
(49, 'INF10', 'Ingeniería de Software I'),
(50, 'INF11', 'Ciencia de Datos'),
(51, 'INF12', 'Gestión del Desarrollo de Sistemas Informáticos'),
(52, 'INF13', 'Programación Concurrente'),
(53, 'INF14', 'Redes'),
(54, 'INF15', 'Física para Informática'),
(55, 'INF16', 'Empresas de Base Tecnológica I'),
(56, 'INF17', 'Ingeniería de Software II'),
(57, 'INF18', 'Sistemas Distribuidos I'),
(58, 'INF19', 'Taller de Seguridad Informática'),
(59, 'INF20', 'Empresas de Base Tecnológica II'),
(221, 'LAS01', 'Álgebra II'),
(222, 'LAS02', 'Algoritmos y Programación I'),
(223, 'LAS03', 'Matemática Discreta'),
(224, 'LAS04', 'Organización del Computador'),
(225, 'LAS05', 'Algoritmos y Programación II'),
(226, 'LAS06', 'Probabilidad y Estadística B'),
(227, 'LAS07', 'Estructuras y Procesos Organizacionales'),
(228, 'LAS08', 'Organización de Datos'),
(229, 'LAS09', 'Algoritmos y Programación III'),
(230, 'LAS10', 'Economía de las Organizaciones'),
(231, 'LAS11', 'Sistemas Operativos'),
(232, 'LAS12', 'Métodos y Modelos en la Ingeniería de Software I'),
(233, 'LAS13', 'Taller de Programación'),
(234, 'LAS14', 'Modelos y Optimización I'),
(235, 'LAS15', 'Métodos y Modelos en la Ingeniería de Software II'),
(236, 'LAS16', 'Base de Datos'),
(237, 'LAS17', 'Administración de las Organizaciones'),
(238, 'LAS18', 'Modelos y Optimización II'),
(239, 'LAS19', 'Administración y Control de Proyectos Informáticos I'),
(240, 'LAS20', 'Diseño, Operación y Gestión de Servicios Informáticos'),
(241, 'LAS21', 'Redes y Aplicaciones Distribuidas'),
(242, 'LAS22', 'Legislación y Ejercicio Profesional en Sistemas e Informática'),
(243, 'LAS23', 'Estándares de Calidad y Modelos de Referencia'),
(81, 'MEC01', 'Introducción a la Ingeniería Mecánica'),
(82, 'MEC02', 'Conocimiento de Materiales Metálicos'),
(83, 'MEC03', 'Diseño Mecánico'),
(84, 'MEC04', 'Mecánica Clásica del Cuerpo Rígido'),
(85, 'MEC05', 'Mecanismos'),
(86, 'MEC06', 'Introducción a la Mecánica del Sólido Deformable'),
(87, 'MEC07', 'Termodinámica'),
(88, 'MEC08', 'Análisis Matemático III'),
(89, 'MEC09', 'Conocimiento de Materiales No Metálicos'),
(90, 'MEC10', 'Ensayos Industriales'),
(91, 'MEC11', 'Electrotecnia General'),
(92, 'MEC12', 'Taller de Manufactura Mecánica'),
(93, 'MEC13', 'Mecánica de Fluidos'),
(94, 'MEC14', 'Proyecto de Instrumentación'),
(95, 'MEC15', 'Máquinas Térmicas'),
(96, 'MEC16', 'Tecnología Mecánica'),
(97, 'MEC17', 'Sistemas de Almacenamiento, Transferencia de Calor y Masa y sus Instalaciones'),
(98, 'MEC18', 'Daño y Fractura de Elementos Mecánicos'),
(99, 'MEC19', 'Máquinas Eléctricas'),
(100, 'MEC20', 'Sistemas de Control y Automatización'),
(101, 'MEC21', 'Turbomáquinas'),
(102, 'MEC22', 'Proyecto de Instalaciones Industriales'),
(103, 'MEC23', 'Elementos de Máquinas'),
(104, 'MEC24', 'Mantenimiento y Calidad'),
(105, 'NAV01', 'Óptica'),
(106, 'NAV02', 'Introducción a la Ingeniería Naval'),
(107, 'NAV03', 'Medios de Representación'),
(108, 'NAV04', 'Estática'),
(109, 'NAV05', 'Dibujo Naval y Mecánico'),
(110, 'NAV06', 'Resistencia de Materiales'),
(111, 'NAV07', 'Termodinámica'),
(112, 'NAV08', 'Conocimiento de Materiales'),
(113, 'NAV09', 'Electrotecnia'),
(114, 'NAV10', 'Máquinas e Instalaciones Eléctricas'),
(115, 'NAV11', 'Estabilidad del Buque'),
(116, 'NAV12', 'Mecánica de Fluidos'),
(117, 'NAV13', 'Teoría de Estructuras'),
(118, 'NAV14', 'Diseño de Estructuras de Buques'),
(119, 'NAV15', 'Sistemas Auxiliares Navales'),
(120, 'NAV16', 'Mecanismos y Elementos de Máquinas'),
(121, 'NAV17', 'Resistencia y Propulsión de Buques'),
(122, 'NAV18', 'Sistemas Inherentes a la Operación del Buque'),
(123, 'NAV19', 'Tecnología de Astilleros'),
(124, 'NAV20', 'Análisis Estructural de Buques'),
(125, 'NAV21', 'Mecánica Clásica del Cuerpo Rígido'),
(126, 'NAV22', 'Plantas Propulsoras'),
(127, 'NAV23', 'Proyecto de Buques Mercantes'),
(128, 'NAV24', 'Prácticas en Astilleros'),
(129, 'NAV25', 'Dinámica de Estructuras de Buques'),
(198, 'PET01', 'Introducción a la Ingeniería en Petróleo'),
(199, 'PET02', 'Geología General'),
(200, 'PET03', 'Fluidodinámica de los Hidrocarburos'),
(201, 'PET04', 'Química de los Hidrocarburos'),
(202, 'PET05', 'Geofísica'),
(203, 'PET06', 'Termodinámica de los Hidrocarburos'),
(204, 'PET07', 'Electrotecnia, Máquinas e Instalaciones Eléctricas'),
(205, 'PET08', 'Estática y Resistencia de Materiales'),
(206, 'PET09', 'Geología de los Hidrocarburos'),
(207, 'PET10', 'Propiedades de la Roca y los Fluidos de Reservorios'),
(208, 'PET11', 'Ingeniería de Reservorios'),
(209, 'PET12', 'Perforación e Intervención de Pozos I'),
(210, 'PET13', 'Procesamiento de Hidrocarburos en Yacimiento'),
(211, 'PET14', 'Sustentabilidad de Proyectos de Hidrocarburos'),
(212, 'PET15', 'Interpretación de Registro de Pozos'),
(213, 'PET16', 'Perforación e Intervención de Pozos II'),
(214, 'PET17', 'Producción de Hidrocarburos'),
(215, 'PET18', 'Proyecto de Instalaciones de Superficie'),
(216, 'PET19', 'Estimulación de Formaciones'),
(217, 'PET20', 'Ingeniería de Reservorios No Convencionales'),
(218, 'PET21', 'Recuperación Secundaria y Asistida de Petróleo'),
(219, 'PET22', 'Industrialización de los Hidrocarburos'),
(220, 'PET23', 'Transporte y Distribución de Hidrocarburos'),
(150, 'QUI01', 'Química General'),
(151, 'QUI02', 'Introducción a Ingeniería Química'),
(152, 'QUI03', 'Química Inorgánica'),
(153, 'QUI04', 'Fundamentos de Procesos Químicos'),
(154, 'QUI05', 'Óptica'),
(155, 'QUI06', 'Termodinámica de los Procesos'),
(156, 'QUI07', 'Química Orgánica'),
(157, 'QUI08', 'Fenómenos de Transporte'),
(158, 'QUI09', 'Operaciones Unitarias de Transferencia de Cantidad de Movimiento y Energía'),
(159, 'QUI10', 'Química Física'),
(160, 'QUI11', 'Química Analítica Instrumental'),
(161, 'QUI12', 'Laboratorio de Operaciones y Procesos'),
(162, 'QUI13', 'Operaciones Unitarias de Transferencia de Materia'),
(163, 'QUI14', 'Instalaciones de Plantas de Procesos'),
(164, 'QUI15', 'Diseño de Reactores'),
(165, 'QUI16', 'Dinámica y Control de Procesos'),
(166, 'QUI17', 'Evaluación de Proyectos de Plantas Químicas'),
(167, 'QUI18', 'Ingeniería de Bioprocesos'),
(168, 'QUI19', 'Diseño de Procesos'),
(169, 'QUI20', 'Emisiones de Contaminantes Químicos y Biológicos');

-- --------------------------------------------------------


--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `formato`
--
ALTER TABLE `formato`
  ADD PRIMARY KEY (`id_formato`),
  ADD UNIQUE KEY `nombre` (`nombre`);

--
-- Indices de la tabla `materias`
--
ALTER TABLE `materias`
  ADD PRIMARY KEY (`codigo`);




--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `formato`
--
ALTER TABLE `formato`
  MODIFY `id_formato` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;



