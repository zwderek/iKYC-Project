CREATE TABLE `Customer` (
`customer_id` int NOT NULL,
`name` varchar(50) NOT NULL, # can be nick name 
`welcome_msg` varchar(100) NOT NULL,
`pwd` varchar(20) NOT NULL, 
PRIMARY KEY (`customer_id`));

CREATE TABLE `Login` (
  `login_id` INT NOT NULL,
  `customer_id` INT NOT NULL,
  `login_date` TIME NULL,
  `login_time` DATE NULL,
  PRIMARY KEY (`login_id`));
  
  CREATE TABLE `Profile` (
  `profile_id` INT NOT NULL,
  `customer_id` INT NOT NULL,
  `name` varchar(50) NULL,
  `gender` int NULL,
  `birthday` date NULL,
  `email` varchar(50) NULL,
  `pic` VARCHAR(200) NULL, 
  `is_public` bool NULL, 
  PRIMARY KEY (`profile_id`));

CREATE TABLE `Account` (
`account_id` int NOT NULL,
`customer_id` int NOT NULL,
`type` varchar(10) NOT NULL,
`currency` varchar(3) NOT NULL,
`balance` int NOT NULL, 
PRIMARY KEY (`account_id`));

CREATE TABLE `Transaction` (
`transaction_id` int NOT NULL, 
`account_id` int NOT NULL,
`transaction_date` date NOT NULL,
`transaction_time` time NOT NULL,
`amount` int NOT NULL, 
PRIMARY KEY (`transaction_id`));