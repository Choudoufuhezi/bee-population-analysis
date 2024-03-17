drop table MonitorStation cascade constraints;
drop table Bee cascade constraints;
drop table Detect cascade constraints;
drop table GasConditions cascade constraints;
drop table Influence cascade constraints;
drop table Monitor cascade constraints;
drop table Kill cascade constraints;
drop table RiskFactors cascade constraints;
drop table Parasite cascade constraints;
drop table Pesticide cascade constraints;

CREATE TABLE MonitorStation (
    CentroidLongitude DECIMAL,
    CentroidLatitude DECIMAL,
    Year INTEGER,
    AverageTemperature DECIMAL,
    PRIMARY KEY (CentroidLongitude, CentroidLatitude, Year)
);


CREATE TABLE Bee (
    State VARCHAR(255),
    Year INTEGER,
    MaxColony INTEGER,
    LostColony INTEGER,
    PercentLost DECIMAL,
    Colony INTEGER,
    AddColony INTEGER,
    PercentRenovated DECIMAL,
    PercentLostByDisease DECIMAL,
    PRIMARY KEY (State, Year)
);

CREATE TABLE Detect (
    CentroidLongitude DECIMAL,
    CentroidLatitude DECIMAL,
    StationYear INTEGER,
    BeeState VARCHAR(255),
    BeeYear INTEGER,
    PRIMARY KEY (CentroidLongitude, CentroidLatitude, StationYear, BeeState, BeeYear),
    FOREIGN KEY (BeeState, BeeYear) REFERENCES Bee(State, Year),
    FOREIGN KEY (CentroidLongitude, CentroidLatitude, StationYear) REFERENCES MonitorStation(CentroidLongitude, CentroidLatitude, Year)
);

CREATE TABLE GasConditions (
    Name VARCHAR(255),
    State VARCHAR(255),
    Year INTEGER,
    MeanValue DECIMAL,
    AverageAQI DECIMAL,
    PRIMARY KEY (Name, State, Year)
);

CREATE TABLE Influence (
    GasPollutantsYearAffected INTEGER,
    GasPollutantsStateAffected VARCHAR(255),
    BeeState VARCHAR(255),
    BeeYear INTEGER,
    PRIMARY KEY (GasPollutantsYearAffected, GasPollutantsStateAffected, BeeState, BeeYear, GasPollutantsName),
    FOREIGN KEY (BeeState, BeeYear) REFERENCES Bee(State, Year),
    FOREIGN KEY (GasPollutantsYearAffected, GasPollutantsStateAffected, GasPollutantsName) REFERENCES GasCondition(Year, State, Name)
);

CREATE TABLE RiskFactors (
    State VARCHAR(255),
    Year INTEGER,
    Name VARCHAR(255),
    PRIMARY KEY (State, Year)
);

CREATE TABLE Monitor (
    CentroidLongitude DECIMAL,
    CentroidLatitude DECIMAL,
    StationYear INTEGER,
    RiskFactorsReportedYear INTEGER,
    RiskFactorsReportedState VARCHAR(255),
    PRIMARY KEY (CentroidLongitude, CentroidLatitude, StationYear),
    FOREIGN KEY (RiskFactorsReportedYear, RiskFactorsReportedState) REFERENCES RiskFactors(Year, State),
    FOREIGN KEY (CentroidLongitude, CentroidLatitude, StationYear) REFERENCES MonitorStation(CentroidLongitude, CentroidLatitude, Year)
);


CREATE TABLE Kill (
    BeeState VARCHAR(255),
    BeeYear INTEGER,
    RiskFactorsReportedYear INTEGER,
    RiskFactorsReportedState VARCHAR(255),
    PRIMARY KEY (BeeState, BeeYear, RiskFactorsReportedYear, RiskFactorsReportedState),
    FOREIGN KEY (BeeState, BeeYear) REFERENCES Bee(State, Year),
    FOREIGN KEY (RiskFactorsReportedYear, RiskFactorsReportedState) REFERENCES RiskFactors(Year, State)
);


CREATE TABLE Parasite (
    Year INTEGER,
    State VARCHAR(255),
    PercentAffected DECIMAL,
    PRIMARY KEY (Year, State)
    FOREIGN KEY (Year, State) REFERENCES RiskFactors(Year, State) 
);

CREATE TABLE Pesticide (
    Year INTEGER,
    State VARCHAR(255),
    LowEstimate DECIMAL,
    HighEstimate DECIMAL,
    PRIMARY KEY (Year, State)
	FOREIGN KEY (Year, State) REFERENCES RiskFactors(Year, State)
);


