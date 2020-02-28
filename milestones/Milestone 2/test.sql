USE `mydb` ;

Insert into Flight(departure, arrival) Values ('2019-12-25 00:00:00', '2019-12-25 03:00:00');
Insert into Flight(departure, arrival) Values ('2019-12-25 00:03:00', '2019-12-25 05:00:00');
Insert into Flight(departure, arrival) Values ('2019-12-25 00:05:00', '2019-12-25 10:00:00');

Insert into Passenger(name, idFlight) Values ('Jim', 1);
Insert into Passenger(name, idFlight) Values ('Drew', 3);
Insert into Passenger(name, idFlight) Values ('Tim', 2);

Insert into Airport(name, location) Values ('SFO', 'San Francisco');
Insert into Airport(name, location) Values ('OAK', 'Oakland');
Insert into Airport(name, location) Values ('LAX', 'Los Angeles');

Insert into BaggageClaim(name, idAirport) Values ('Section 1 - SFO', 1);
Insert into BaggageClaim(name, idAirport) Values ('Section 2 - SFO', 1);
Insert into BaggageClaim(name, idAirport) Values ('Section 1 - OAK', 2); -- no baggage claim for airport 3

-- Eg: Flight 1, baggageclaim section 1 - sfo, passenger Tim
Insert into Luggage(idFlight, idBaggageClaim, idPassenger) Values (1, 1, 2);
Insert into Luggage(idFlight, idBaggageClaim, idPassenger) Values (2, 3, 1); 
Insert into Luggage(idFlight, idBaggageClaim, idPassenger) Values (3, 2, 3); 

-- Eg: Paul pilots flight 1
Insert into Pilot(name, idFlight) Values ('Paul', 1);
Insert into Pilot(name, idFlight) Values ('Joe', 1);
Insert into Pilot(name, idFlight) Values ('Steve', 2);


Insert into Company(name) Values ('South West Airlines');
Insert into Company(name) Values ('Pacific Airlines');
Insert into Company(name) Values ('American Airlines');

-- Eg: Jim has South West Airline tickets
Insert into Ticket(idCompany, idPassenger) Values (1,1);
Insert into Ticket(idCompany, idPassenger) Values (2,3);
Insert into Ticket(idCompany, idPassenger) Values (3,2);

-- Eg: South West's airplane named Alpha is flight 2
Insert into Airplane(name, idCompany, idFlight) Values ('Alpha', 1, 2); 
Insert into Airplane(name, idCompany, idFlight) Values ('Beta', 3, 3); 
Insert into Airplane(name, idCompany, idFlight) Values ('Charlie', 1, 1);

Insert into Gate(name, idAirplane, idAirport) Values ('Gate A - SFO', 1, 1);
Insert into Gate(name, idAirplane, idAirport) Values ('Gate A - OAK', 2, 2);
Insert into Gate(name, idAirplane, idAirport) Values ('Gate A - LAX', 3, 3);

Insert into Employee(name) Values ('Tan');
Insert into Employee(name) Values ('Apollo');
Insert into Employee(name) Values ('Icarus');

-- Eg: South West employs Paul
Insert into hires(idPilot, idCompany) Values (1,1); 
Insert into hires(idPilot, idCompany) Values (2,2);
Insert into hires(idPilot, idCompany) Values (3,3);

-- Eg: Tan works for SFO
Insert into Employment(idAirport, idEmployee) Values (1,1);
Insert into Employment(idAirport, idEmployee) Values (2,2);
Insert into Employment(idAirport, idEmployee) Values (3,2);
Insert into Employment(idAirport, idEmployee) Values (3,3);

-- Do not delete from Luggage, Ticket, Gate, hires, and Employment since it is not referenced
Delete from Flight Where idFlight = 1;
Delete from Passenger Where idPassenger = 1;
Delete from Airport Where idAirport = 1;
Delete from BaggageClaim Where idBaggageClaim = 1;
Delete from Pilot Where idPilot = 1;
Delete from Company Where idCompany = 1;
Delete from Airplane Where idAirplane = 1;
Delete from Employee Where idEmployee = 1;

-- One to many
Select a.name, g.name From Airport a, Gate g Where a.idAirport = g.idAirport;

-- Many to one
Select p.name, f.idFlight From Passenger p, Flight f Where p.idFlight = f.idFlight;

-- Many to Many
Select * From Employment e;

-- Update one to many
Update Airport SET name='The City' Where name='OAK';

-- Update many to one
Update Passenger SET name='Timmy' Where name='Tim';

-- Update many to many
Update Employment SET idEmployee=2 Where idEmployee=1;






