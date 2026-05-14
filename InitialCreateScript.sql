CREATE TABLE IF NOT EXISTS `__EFMigrationsHistory` (
    `MigrationId` varchar(150) CHARACTER SET utf8mb4 NOT NULL,
    `ProductVersion` varchar(32) CHARACTER SET utf8mb4 NOT NULL,
    CONSTRAINT `PK___EFMigrationsHistory` PRIMARY KEY (`MigrationId`)
) CHARACTER SET=utf8mb4;

START TRANSACTION;

ALTER DATABASE CHARACTER SET utf8mb4;

CREATE TABLE `Countries` (
    `CountryID` int NOT NULL AUTO_INCREMENT,
    `CountryName` longtext CHARACTER SET utf8mb4 NULL,
    CONSTRAINT `PK_Countries` PRIMARY KEY (`CountryID`)
) CHARACTER SET=utf8mb4;

CREATE TABLE `Genres` (
    `GenreID` int NOT NULL AUTO_INCREMENT,
    `GenreName` longtext CHARACTER SET utf8mb4 NULL,
    CONSTRAINT `PK_Genres` PRIMARY KEY (`GenreID`)
) CHARACTER SET=utf8mb4;

CREATE TABLE `Users` (
    `Id` int NOT NULL AUTO_INCREMENT,
    `FirstName` longtext CHARACTER SET utf8mb4 NOT NULL,
    `LastName` longtext CHARACTER SET utf8mb4 NOT NULL,
    `Email` longtext CHARACTER SET utf8mb4 NOT NULL,
    `Rank` longtext CHARACTER SET utf8mb4 NOT NULL,
    `RegistrationDate` datetime(6) NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `Password` longtext CHARACTER SET utf8mb4 NOT NULL,
    CONSTRAINT `PK_Users` PRIMARY KEY (`Id`)
) CHARACTER SET=utf8mb4;

CREATE TABLE `Actors` (
    `ActorID` int NOT NULL AUTO_INCREMENT,
    `ActorName` longtext CHARACTER SET utf8mb4 NULL,
    `Biography` longtext CHARACTER SET utf8mb4 NULL,
    `BirthDate` datetime(6) NOT NULL,
    `BirthYear` int NULL,
    `CountryID` int NULL,
    CONSTRAINT `PK_Actors` PRIMARY KEY (`ActorID`),
    CONSTRAINT `FK_Actors_Countries_CountryID` FOREIGN KEY (`CountryID`) REFERENCES `Countries` (`CountryID`) ON DELETE RESTRICT
) CHARACTER SET=utf8mb4;

CREATE TABLE `Directors` (
    `DirectorID` int NOT NULL AUTO_INCREMENT,
    `DirectorName` longtext CHARACTER SET utf8mb4 NULL,
    `Biography` longtext CHARACTER SET utf8mb4 NULL,
    `BirthDate` datetime(6) NOT NULL,
    `BirthYear` int NULL,
    `CountryID` int NULL,
    CONSTRAINT `PK_Directors` PRIMARY KEY (`DirectorID`),
    CONSTRAINT `FK_Directors_Countries_CountryID` FOREIGN KEY (`CountryID`) REFERENCES `Countries` (`CountryID`) ON DELETE RESTRICT
) CHARACTER SET=utf8mb4;

CREATE TABLE `Movies` (
    `MovieID` int NOT NULL AUTO_INCREMENT,
    `Title` varchar(255) CHARACTER SET utf8mb4 NOT NULL,
    `OriginalTitle` varchar(255) CHARACTER SET utf8mb4 NOT NULL,
    `Description` longtext CHARACTER SET utf8mb4 NULL,
    `ReleaseYear` int NOT NULL,
    `Duration` int NOT NULL,
    `Rating` decimal(3,1) NOT NULL,
    `PosterURL` longtext CHARACTER SET utf8mb4 NULL,
    `GenreID` int NOT NULL,
    `DirectorID` int NOT NULL,
    `CreatedAt` datetime(6) NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `UpdatedAt` datetime(6) NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP(6),
    CONSTRAINT `PK_Movies` PRIMARY KEY (`MovieID`),
    CONSTRAINT `FK_Movies_Directors_DirectorID` FOREIGN KEY (`DirectorID`) REFERENCES `Directors` (`DirectorID`) ON DELETE RESTRICT,
    CONSTRAINT `FK_Movies_Genres_GenreID` FOREIGN KEY (`GenreID`) REFERENCES `Genres` (`GenreID`) ON DELETE RESTRICT
) CHARACTER SET=utf8mb4;

CREATE TABLE `Reviews` (
    `ReviewID` int NOT NULL AUTO_INCREMENT,
    `MovieID` int NOT NULL,
    `UserID` int NOT NULL,
    `Rating` int NOT NULL,
    `Text` longtext CHARACTER SET utf8mb4 NOT NULL,
    `PublicationDate` datetime(6) NOT NULL,
    `CreatedAt` datetime(6) NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `UpdatedAt` datetime(6) NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT `PK_Reviews` PRIMARY KEY (`ReviewID`),
    CONSTRAINT `FK_Reviews_Movies_MovieID` FOREIGN KEY (`MovieID`) REFERENCES `Movies` (`MovieID`) ON DELETE CASCADE,
    CONSTRAINT `FK_Reviews_Users_UserID` FOREIGN KEY (`UserID`) REFERENCES `Users` (`Id`) ON DELETE CASCADE
) CHARACTER SET=utf8mb4;

CREATE TABLE `Roles` (
    `RoleID` int NOT NULL AUTO_INCREMENT,
    `MovieID` int NOT NULL,
    `ActorID` int NOT NULL,
    `CharacterName` longtext CHARACTER SET utf8mb4 NULL,
    CONSTRAINT `PK_Roles` PRIMARY KEY (`RoleID`),
    CONSTRAINT `FK_Roles_Actors_ActorID` FOREIGN KEY (`ActorID`) REFERENCES `Actors` (`ActorID`) ON DELETE CASCADE,
    CONSTRAINT `FK_Roles_Movies_MovieID` FOREIGN KEY (`MovieID`) REFERENCES `Movies` (`MovieID`) ON DELETE CASCADE
) CHARACTER SET=utf8mb4;

CREATE INDEX `IX_Actors_CountryID` ON `Actors` (`CountryID`);

CREATE INDEX `IX_Directors_CountryID` ON `Directors` (`CountryID`);

CREATE INDEX `IX_Movies_DirectorID` ON `Movies` (`DirectorID`);

CREATE INDEX `IX_Movies_GenreID` ON `Movies` (`GenreID`);

CREATE INDEX `IX_Reviews_MovieID` ON `Reviews` (`MovieID`);

CREATE INDEX `IX_Reviews_UserID` ON `Reviews` (`UserID`);

CREATE INDEX `IX_Roles_ActorID` ON `Roles` (`ActorID`);

CREATE INDEX `IX_Roles_MovieID` ON `Roles` (`MovieID`);

INSERT INTO `__EFMigrationsHistory` (`MigrationId`, `ProductVersion`)
VALUES ('20250608102225_InitialCreate', '8.0.0');

COMMIT;

