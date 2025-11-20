-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: localhost
-- Generation Time: Dec 11, 2024 at 07:47 PM
-- Server version: 10.4.28-MariaDB
-- PHP Version: 8.0.28

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `flying_schema`
--

-- --------------------------------------------------------

--
-- Table structure for table `Airline`
--

CREATE TABLE `Airline` (
  `airline_name` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `Airline`
--

INSERT INTO `Airline` (`airline_name`) VALUES
('JetBlue');

-- --------------------------------------------------------

--
-- Table structure for table `Airplane`
--

CREATE TABLE `Airplane` (
  `airplane_id` int(11) NOT NULL,
  `airline_name` char(100) DEFAULT NULL,
  `manufacturer` char(100) DEFAULT NULL,
  `model_number` char(50) DEFAULT NULL,
  `manufacture_date` date DEFAULT NULL,
  `num_seats` int(11) DEFAULT NULL,
  `age` int(11) GENERATED ALWAYS AS (timestampdiff(YEAR,`manufacture_date`,curdate())) VIRTUAL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `Airplane`
--

INSERT INTO `Airplane` (`airplane_id`, `airline_name`, `manufacturer`, `model_number`, `manufacture_date`, `num_seats`) VALUES
(1, 'JetBlue', 'Boeing', 'B-101', '2013-05-02', 4),
(2, 'JetBlue', 'Airbus', 'A-101', '2011-05-02', 4),
(3, 'JetBlue', 'Boeing', 'B-101', '2015-05-02', 50);

-- --------------------------------------------------------

--
-- Table structure for table `Airport`
--

CREATE TABLE `Airport` (
  `airport_code` char(4) NOT NULL,
  `airport_name` varchar(100) DEFAULT NULL,
  `city` varchar(100) DEFAULT NULL,
  `country` varchar(100) DEFAULT NULL,
  `num_terminals` int(11) DEFAULT NULL,
  `type` char(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `Airport`
--

INSERT INTO `Airport` (`airport_code`, `airport_name`, `city`, `country`, `num_terminals`, `type`) VALUES
('BEI', 'BEI', 'Beijing', 'China', 2, 'Both'),
('BOS', 'BOS', 'Boston', 'USA', 2, 'Both'),
('HKA', 'HKA', 'Hong Kong', 'China', 2, 'Both'),
('JFK', 'JFK', 'NYC', 'USA', 4, 'Both'),
('LAX', 'LAX', 'Los Angeles', 'USA', 2, 'Both'),
('PVG', 'PVG', 'Shanghai', 'China', 2, 'Both'),
('SFO', 'SFO', 'San Francisco', 'USA', 2, 'Both'),
('SHEN', 'SHEN', 'Shenzen', 'China', 2, 'Both');

-- --------------------------------------------------------

--
-- Table structure for table `Customer`
--

CREATE TABLE `Customer` (
  `email` char(50) NOT NULL,
  `passport_country` char(50) DEFAULT NULL,
  `first_name` char(50) DEFAULT NULL,
  `last_name` char(50) DEFAULT NULL,
  `password` char(50) DEFAULT NULL,
  `dob` date DEFAULT NULL,
  `address` char(200) DEFAULT NULL,
  `passport_num` int(11) DEFAULT NULL,
  `passport_exp_date` date DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `Customer`
--

INSERT INTO `Customer` (`email`, `passport_country`, `first_name`, `last_name`, `password`, `dob`, `address`, `passport_num`, `passport_exp_date`) VALUES
('testcustomer@nyu.edu', 'USA', 'Jon', 'Snow', '1234', '1999-12-19', '1555 Jay St Brooklyn, NY', 54321, '2025-12-24'),
('user1@nyu.edu', 'USA', 'Alice', 'Bob', '1234', '1999-11-19', '5405 Jay St Brooklyn, NY', 54322, '2025-12-25'),
('user2@nyu.edu', 'USA', 'Cathy', 'Wood', '1234', '1999-10-19', '1702 Jay St Brooklyn, NY', 54323, '2025-10-24'),
('user3@nyu.edu', 'USA', 'Trudy', 'Jones', '1234', '1999-09-19', '1890 Jay St Brooklyn, NY', 54324, '2025-09-24');

-- --------------------------------------------------------

--
-- Table structure for table `Flight`
--

CREATE TABLE `Flight` (
  `flight_num` int(11) NOT NULL,
  `airline_name` char(100) DEFAULT NULL,
  `airplane_id` int(11) DEFAULT NULL,
  `airport_code` char(4) DEFAULT NULL,
  `arrival` datetime DEFAULT NULL,
  `departure` datetime DEFAULT NULL,
  `base_price` decimal(10,2) DEFAULT NULL,
  `arrival_airport_code` char(4) DEFAULT NULL,
  `Status` varchar(50) DEFAULT 'On Time'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `Flight`
--

INSERT INTO `Flight` (`flight_num`, `airline_name`, `airplane_id`, `airport_code`, `arrival`, `departure`, `base_price`, `arrival_airport_code`, `Status`) VALUES
(102, 'JetBlue', 3, 'SFO', '2024-09-20 13:25:25', '2024-09-20 16:50:25', 300.00, 'LAX', 'On Time'),
(104, 'JetBlue', 3, 'PVG', '2024-10-04 13:25:25', '2024-10-04 16:50:25', 300.00, 'BEI', 'On Time'),
(106, 'JetBlue', 3, 'SFO', '2024-08-04 13:25:25', '2024-08-04 16:50:25', 350.00, 'LAX', 'Delayed'),
(134, 'JetBlue', 3, 'JFK', '2023-12-15 13:25:25', '2023-12-15 16:50:25', 300.00, 'BOS', 'delayed'),
(206, 'JetBlue', 2, 'SFO', '2025-02-04 13:25:25', '2025-02-04 16:50:25', 400.00, 'LAX', 'On time'),
(207, 'JetBlue', 2, 'LAX', '2025-03-04 13:25:25', '2025-03-04 16:50:25', 300.00, 'SFO', 'On time'),
(296, 'JetBlue', 1, 'PVG', '2024-12-30 13:25:25', '2024-12-30 16:50:25', 3000.00, 'SFO', 'On time'),
(715, 'JetBlue', 1, 'PVG', '2024-09-28 13:25:25', '2024-09-28 16:50:25', 500.00, 'BEI', 'Delayed'),
(839, 'JetBlue', 3, 'SHEN', '2023-12-26 13:25:25', '2023-12-26 16:50:25', 300.00, 'BEI', 'On time');

-- --------------------------------------------------------

--
-- Table structure for table `Maitenance`
--

CREATE TABLE `Maitenance` (
  `airplane_id` int(11) DEFAULT NULL,
  `start_date_time` datetime DEFAULT NULL,
  `end_date_time` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `Maitenance`
--

INSERT INTO `Maitenance` (`airplane_id`, `start_date_time`, `end_date_time`) VALUES
(1, '2025-01-27 13:25:25', '2025-01-29 07:25:25'),
(2, '2025-01-27 13:25:25', '2025-01-29 07:25:25');

-- --------------------------------------------------------

--
-- Table structure for table `Purchase`
--

CREATE TABLE `Purchase` (
  `purchase_id` int(11) NOT NULL,
  `ticket_id` int(11) DEFAULT NULL,
  `purchase_date_time` datetime DEFAULT NULL,
  `card_info` char(50) DEFAULT NULL,
  `card_exp` char(50) DEFAULT NULL,
  `card_type` char(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `Purchase`
--

INSERT INTO `Purchase` (`purchase_id`, `ticket_id`, `purchase_date_time`, `card_info`, `card_exp`, `card_type`) VALUES
(1, 1, '2024-08-17 11:55:55', '1111222233334444', '03/2025', 'credit'),
(2, 2, '2024-08-16 11:55:55', '1111222233335555', '03/2025', 'credit'),
(3, 3, '2024-09-14 11:55:55', '1111222233335555', '03/2025', 'credit'),
(4, 4, '2024-08-21 11:55:55', '11112222333355555', '03/2024', 'credit'),
(5, 5, '2024-09-28 11:55:55', '1111222233334444', '03/2024', 'credit'),
(6, 6, '2024-08-02 11:55:55', '1111222233334444', '03/2024', 'credit'),
(7, 7, '2024-07-23 11:55:55', '1111222233335555', '03/2024', 'credit'),
(8, 8, '2023-12-23 11:55:55', '1111222233335555', '03/2024', 'credit'),
(9, 9, '2024-07-14 11:55:55', '1111222233335555', '03/2024', 'credit'),
(11, 11, '2023-10-23 11:55:55', '1111222233335555', '03/2024', 'credit'),
(12, 12, '2024-05-02 11:55:55', '1111222233334444', '03/2024', 'credit'),
(14, 14, '2024-11-20 11:55:55', '11112222333355555', '03/2024', 'credit'),
(15, 15, '2024-11-21 11:55:55', '1111222233335555', '03/2024', 'credit'),
(16, 16, '2024-09-19 11:55:55', '1111222233335555', '03/2024', 'credit'),
(17, 17, '2024-08-15 11:55:55', '1111222233335555', '03/2024', 'credit'),
(18, 18, '2024-09-25 11:55:55', '1111222233334444', '03/2024', 'credit'),
(19, 19, '2024-11-22 11:55:55', '1111222233334444', '03/2024', 'credit'),
(20, 20, '2023-12-17 11:55:55', '1111222233334444', '03/2024', 'credit');

-- --------------------------------------------------------

--
-- Table structure for table `Staff`
--

CREATE TABLE `Staff` (
  `username` char(100) NOT NULL,
  `airline_name` char(100) DEFAULT NULL,
  `first_name` char(100) DEFAULT NULL,
  `last_name` char(100) DEFAULT NULL,
  `dob` date DEFAULT NULL,
  `password` char(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `Staff`
--

INSERT INTO `Staff` (`username`, `airline_name`, `first_name`, `last_name`, `dob`, `password`) VALUES
('admin', 'JetBlue', 'Roe', 'Jones', '1978-05-25', 'abcd');

-- --------------------------------------------------------

--
-- Table structure for table `StaffEmails`
--

CREATE TABLE `StaffEmails` (
  `id` int(11) NOT NULL,
  `username` varchar(50) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `StaffEmails`
--

INSERT INTO `StaffEmails` (`id`, `username`, `email`) VALUES
(1, 'admin', 'staff1@nyu.edu'),
(2, 'admin', 'staff2@nyu.edu');

-- --------------------------------------------------------

--
-- Table structure for table `StaffPhoneNumbers`
--

CREATE TABLE `StaffPhoneNumbers` (
  `id` int(11) NOT NULL,
  `username` varchar(50) DEFAULT NULL,
  `phone_number` bigint(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `StaffPhoneNumbers`
--

INSERT INTO `StaffPhoneNumbers` (`id`, `username`, `phone_number`) VALUES
(1, 'admin', 11122223333),
(2, 'admin', 44455556666);

-- --------------------------------------------------------

--
-- Table structure for table `Ticket`
--

CREATE TABLE `Ticket` (
  `ticket_id` int(11) NOT NULL,
  `email` char(100) DEFAULT NULL,
  `flight_num` int(11) DEFAULT NULL,
  `rating` int(11) DEFAULT NULL,
  `comments` char(200) DEFAULT NULL,
  `calc_price` decimal(10,2) DEFAULT NULL,
  `first_name` char(50) DEFAULT NULL,
  `last_name` char(50) DEFAULT NULL,
  `dob` date DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `Ticket`
--

INSERT INTO `Ticket` (`ticket_id`, `email`, `flight_num`, `rating`, `comments`, `calc_price`, `first_name`, `last_name`, `dob`) VALUES
(1, 'testcustomer@nyu.edu', 102, 4, 'Very Comfortable', 300.00, 'Jon', 'Snow', '1999-12-19'),
(2, 'user1@nyu.edu', 102, 5, 'Relaxing, check-in and onboarding very\r\nprofessional', 300.00, 'Alice', 'Bob', '1999-11-19'),
(3, 'user2@nyu.edu', 102, 3, 'Satisfied and will use the same flight\r\nagain', 300.00, 'Cathy', 'Wood', '1999-10-19'),
(4, 'user1@nyu.edu', 104, 5, 'Comfortable journey and Professional', 300.00, 'Alice', 'Bob', '1999-11-19'),
(5, 'testcustomer@nyu.edu', 104, 1, 'Customer Care services are not\r\ngood', 300.00, 'Jon', 'Snow', '1999-12-19'),
(6, 'testcustomer@nyu.edu', 106, NULL, NULL, 350.00, 'Jon', 'Snow', '1999-12-19'),
(7, 'user3@nyu.edu', 106, NULL, NULL, 350.00, 'Trudy', 'Jones', '1999-09-19'),
(8, 'user3@nyu.edu', 839, NULL, NULL, 300.00, 'Trudy', 'Jones', '1999-09-19'),
(9, 'user3@nyu.edu', 102, NULL, NULL, 300.00, 'Trudy', 'Jones', '1999-09-19'),
(11, 'user3@nyu.edu', 134, NULL, NULL, 300.00, 'Trudy', 'Jones', '1999-09-19'),
(12, 'testcustomer@nyu.edu', 715, NULL, NULL, 500.00, 'Jon', 'Snow', '1999-12-19'),
(14, 'user3@nyu.edu', 206, NULL, NULL, 400.00, 'Trudy', 'Jones', '1999-09-19'),
(15, 'user1@nyu.edu', 206, NULL, NULL, 400.00, 'Alice', 'Bob', '1999-11-19'),
(16, 'user2@nyu.edu', 206, NULL, NULL, 400.00, 'Cathy', 'Wood', '1999-10-19'),
(17, 'user1@nyu.edu', 207, NULL, NULL, 300.00, 'Alice', 'Bob', '1999-11-19'),
(18, 'testcustomer@nyu.edu', 207, NULL, NULL, 300.00, 'Jon', 'Snow', '1999-12-19'),
(19, 'user1@nyu.edu', 296, NULL, NULL, 3000.00, 'Alice', 'Bob', '1999-11-19'),
(20, 'testcustomer@nyu.edu', 296, NULL, NULL, 3000.00, 'Jon', 'Snow', '1999-12-19');

-- --------------------------------------------------------

--
-- Table structure for table `UserPhoneNumbers`
--

CREATE TABLE `UserPhoneNumbers` (
  `id` int(11) NOT NULL,
  `email` varchar(100) DEFAULT NULL,
  `phone_number` bigint(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `UserPhoneNumbers`
--

INSERT INTO `UserPhoneNumbers` (`id`, `email`, `phone_number`) VALUES
(1, 'testcustomer@nyu.edu', 12343214321),
(2, 'user1@nyu.edu', 12343224322),
(3, 'user2@nyu.edu', 12343234323),
(4, 'user3@nyu.edu', 12343244324);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `Airline`
--
ALTER TABLE `Airline`
  ADD PRIMARY KEY (`airline_name`);

--
-- Indexes for table `Airplane`
--
ALTER TABLE `Airplane`
  ADD PRIMARY KEY (`airplane_id`),
  ADD KEY `airline_name` (`airline_name`);

--
-- Indexes for table `Airport`
--
ALTER TABLE `Airport`
  ADD PRIMARY KEY (`airport_code`);

--
-- Indexes for table `Customer`
--
ALTER TABLE `Customer`
  ADD PRIMARY KEY (`email`);

--
-- Indexes for table `Flight`
--
ALTER TABLE `Flight`
  ADD PRIMARY KEY (`flight_num`),
  ADD KEY `airline_name` (`airline_name`),
  ADD KEY `airplane_id` (`airplane_id`),
  ADD KEY `airport_code` (`airport_code`);

--
-- Indexes for table `Maitenance`
--
ALTER TABLE `Maitenance`
  ADD KEY `airplane_id` (`airplane_id`);

--
-- Indexes for table `Purchase`
--
ALTER TABLE `Purchase`
  ADD PRIMARY KEY (`purchase_id`),
  ADD KEY `ticket_id` (`ticket_id`);

--
-- Indexes for table `Staff`
--
ALTER TABLE `Staff`
  ADD PRIMARY KEY (`username`),
  ADD KEY `airline_name` (`airline_name`);

--
-- Indexes for table `StaffEmails`
--
ALTER TABLE `StaffEmails`
  ADD PRIMARY KEY (`id`),
  ADD KEY `username` (`username`);

--
-- Indexes for table `StaffPhoneNumbers`
--
ALTER TABLE `StaffPhoneNumbers`
  ADD PRIMARY KEY (`id`),
  ADD KEY `username` (`username`);

--
-- Indexes for table `Ticket`
--
ALTER TABLE `Ticket`
  ADD PRIMARY KEY (`ticket_id`),
  ADD KEY `email` (`email`);

--
-- Indexes for table `UserPhoneNumbers`
--
ALTER TABLE `UserPhoneNumbers`
  ADD PRIMARY KEY (`id`),
  ADD KEY `email` (`email`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `StaffEmails`
--
ALTER TABLE `StaffEmails`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT for table `StaffPhoneNumbers`
--
ALTER TABLE `StaffPhoneNumbers`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- AUTO_INCREMENT for table `UserPhoneNumbers`
--
ALTER TABLE `UserPhoneNumbers`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `Airplane`
--
ALTER TABLE `Airplane`
  ADD CONSTRAINT `airplane_ibfk_1` FOREIGN KEY (`airline_name`) REFERENCES `Airline` (`airline_name`);

--
-- Constraints for table `Flight`
--
ALTER TABLE `Flight`
  ADD CONSTRAINT `flight_ibfk_1` FOREIGN KEY (`airline_name`) REFERENCES `Airline` (`airline_name`),
  ADD CONSTRAINT `flight_ibfk_2` FOREIGN KEY (`airplane_id`) REFERENCES `Airplane` (`airplane_id`),
  ADD CONSTRAINT `flight_ibfk_3` FOREIGN KEY (`airport_code`) REFERENCES `Airport` (`airport_code`);

--
-- Constraints for table `Maitenance`
--
ALTER TABLE `Maitenance`
  ADD CONSTRAINT `maitenance_ibfk_1` FOREIGN KEY (`airplane_id`) REFERENCES `Airplane` (`airplane_id`);

--
-- Constraints for table `Purchase`
--
ALTER TABLE `Purchase`
  ADD CONSTRAINT `purchase_ibfk_1` FOREIGN KEY (`ticket_id`) REFERENCES `Ticket` (`ticket_id`);

--
-- Constraints for table `Staff`
--
ALTER TABLE `Staff`
  ADD CONSTRAINT `staff_ibfk_1` FOREIGN KEY (`airline_name`) REFERENCES `Airline` (`airline_name`);

--
-- Constraints for table `StaffEmails`
--
ALTER TABLE `StaffEmails`
  ADD CONSTRAINT `staffemails_ibfk_1` FOREIGN KEY (`username`) REFERENCES `Staff` (`username`);

--
-- Constraints for table `StaffPhoneNumbers`
--
ALTER TABLE `StaffPhoneNumbers`
  ADD CONSTRAINT `staffphonenumbers_ibfk_1` FOREIGN KEY (`username`) REFERENCES `Staff` (`username`);

--
-- Constraints for table `Ticket`
--
ALTER TABLE `Ticket`
  ADD CONSTRAINT `ticket_ibfk_1` FOREIGN KEY (`email`) REFERENCES `Customer` (`email`);

--
-- Constraints for table `UserPhoneNumbers`
--
ALTER TABLE `UserPhoneNumbers`
  ADD CONSTRAINT `userphonenumbers_ibfk_1` FOREIGN KEY (`email`) REFERENCES `Customer` (`email`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
