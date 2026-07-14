-- phpMyAdmin SQL Dump
-- Cleaned for deployment: demo data replaces real user records
--
-- Database: `braintumor`
--

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

-- --------------------------------------------------------

--
-- Table structure for table `tbladmin`
--

CREATE TABLE `tbladmin` (
  `id` int(11) NOT NULL,
  `email` varchar(100) DEFAULT NULL,
  `password` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- NOTE: Change this admin password after import.
-- Generate a new bcrypt hash locally and run:
-- UPDATE tbladmin SET password = 'your_new_hash' WHERE email = 'admin@example.com';
--
INSERT INTO `tbladmin` (`id`, `email`, `password`) VALUES
(1, 'admin123@example.com', 'PASTE_YOUR_OWN_GENERATED_HASH_HERE');

-- --------------------------------------------------------

--
-- Table structure for table `tblfaq`
--

CREATE TABLE `tblfaq` (
  `id` int(11) NOT NULL,
  `question` text DEFAULT NULL,
  `answer` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

INSERT INTO `tblfaq` (`id`, `question`, `answer`) VALUES
(3, 'What is a brain tumor?', 'A brain tumor is an abnormal growth of cells inside the brain that can affect normal brain functions.'),
(4, 'How does this system detect brain tumors?', 'The system analyzes uploaded MRI scan images using a trained deep learning model to predict whether a tumor is present.'),
(5, 'Which technology is used for detection?', 'The project uses Artificial Intelligence and Deep Learning techniques such as CNN (Convolutional Neural Network).'),
(6, 'What type of images are supported?', 'The system mainly supports MRI brain scan images.'),
(7, 'Can this system replace doctors?', 'No. The system is only an assisting tool for early detection and analysis. Final diagnosis must always be done by medical professionals.'),
(8, 'Is the prediction result 100% accurate?', 'No AI system is 100% accurate. Accuracy depends on dataset quality, training process, and image clarity.'),
(9, 'What happens after uploading an image?', 'The image is preprocessed, analyzed by the model, and then the prediction result is displayed.'),
(10, 'Which algorithm is used in the project?', 'CNN (Convolutional Neural Network) is commonly used for image classification tasks in medical imaging.');

-- --------------------------------------------------------

--
-- Table structure for table `tblhealthtips`
--

CREATE TABLE `tblhealthtips` (
  `id` int(11) NOT NULL,
  `title` varchar(200) DEFAULT NULL,
  `description` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

INSERT INTO `tblhealthtips` (`id`, `title`, `description`) VALUES
(3, 'Maintain a Healthy Diet', 'Eat nutritious foods rich in vitamins, fruits, vegetables, and proteins to support brain health.'),
(4, 'Exercise Regularly', 'Physical activity improves blood circulation and supports healthy brain function.'),
(5, 'Avoid Smoking and Alcohol', 'Excessive smoking and alcohol consumption may increase health risks.'),
(6, 'Get Regular Medical Checkups', 'Early diagnosis helps in better treatment and prevention of serious conditions.'),
(7, 'Manage Stress', 'Practice meditation, yoga, or relaxation techniques to reduce mental stress.');

-- --------------------------------------------------------

--
-- Table structure for table `tblusers`
--

CREATE TABLE `tblusers` (
  `id` int(11) NOT NULL,
  `username` varchar(100) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `mobile` varchar(15) DEFAULT NULL,
  `password` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Left empty intentionally — register new accounts after deployment.

--
-- Indexes for dumped tables
--

ALTER TABLE `tbladmin`
  ADD PRIMARY KEY (`id`);

ALTER TABLE `tblfaq`
  ADD PRIMARY KEY (`id`);

ALTER TABLE `tblhealthtips`
  ADD PRIMARY KEY (`id`);

ALTER TABLE `tblusers`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

ALTER TABLE `tbladmin`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

ALTER TABLE `tblfaq`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=12;

ALTER TABLE `tblhealthtips`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

ALTER TABLE `tblusers`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=1;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;