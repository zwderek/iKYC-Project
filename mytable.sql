CREATE TABLE `Customer` (
`customer_id` int NOT NULL,
`name` varchar(50) NOT NULL,
`login_time` time NOT NULL,
`login_date` date NOT NULL,
`welcome_msg` varchar(100) NOT NULL,
`pwd` varchar(20) NOT NULL);

CREATE TABLE `Account` (
`customer_id` int NOT NULL,
`type` varchar(10) NOT NULL,
`currency` varchar(3) NOT NULL,
`account_id` int NOT NULL,
`balance` int NOT NULL );

CREATE TABLE `Transaction` (
`account_id` int NOT NULL,
`transaction_date` date NOT NULL,
`transaction_time` time NOT NULL,
`amount` int NOT NULL);