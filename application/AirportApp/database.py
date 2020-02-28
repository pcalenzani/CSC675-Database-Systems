from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.automap import automap_base


class Database:

    def __init__(self, app):
        """
        This Class will take the project app as a parameter and connect it to the given database.
        The tunneling code is for testing it in local machines, the server itself does not need to tunnel.
        """
        mysql_user = "root"
        mysql_pass = "team7"
        db_port = 3306
        db_name = "mydb"

        app.config['SQLALCHEMY_DATABASE_URI'] = r"mysql://%s:%s@127.0.0.1:%s/%s" % (mysql_user,
                                                                                    mysql_pass,
                                                                                    db_port,
                                                                                    db_name)

        # DB will be used for querying and inserting
        self.DB = SQLAlchemy(app)
        # Base will be used to access tables
        self.Base = automap_base()
        self.Base.prepare(self.DB.engine, reflect=True, schema=db_name)

    def getTable(self, table):
        """
        Function will take table name as string parameter and return the database table

        Following tables are available (case sensitive):
            Airplane
            Airport
            BaggageClaim
            Company
            Employee
            Employment
            Flight
            Gate
            hires
            Luggage
            Passenger
            Pilot
            Ticket

        For attribute name/info, please refer to sql code in the milestone 2 folder
        """
        return self.DB.Table(table, self.DB.MetaData(), autoload=True, autoload_with=self.DB.engine)

    def getFlight(self, flightID):
        """
        Example database query.
        1. Get the table
        2. Query the table via database
        3. Add restrictions

        'idFlight' is the name of the id attribute in the 'Flight' table
        End query with all() to get all entries or first() to get first match.
        """
        Flight = self.getTable('Flight')
        return self.DB.session.query(Flight).filter_by(idFlight=flightID).first()

    """
    Insert functions for Tables:
        Airplane
        Airport
        BaggageClaim
        Company
        Flight
        Gate
        Passenger
        Pilot
    """

    def addAirport(self, name, location):
        Airport = self.getTable('Airport')
        newAirport = Airport.insert().values(name=name,
                                             location=location)
        self.DB.session.execute(newAirport)
        self.DB.session.commit()

    def addFlight(self, departure, arrival):
        Flight = self.getTable('Flight')
        newflight = Flight.insert().values(departure=departure,
                                           arrival=arrival)
        self.DB.session.execute(newflight)
        self.DB.session.commit()

    def addCompany(self, name):
        Company = self.getTable('Company')
        newCompany = Company.insert().values(name=name)
        self.DB.session.execute(newCompany)
        self.DB.session.commit()

    def addAirplane(self, name, idCompany, idFlight):
        Airplane = self.getTable('Airplane')
        newAirplane = Airplane.insert().values(name=name,
                                               idCompany=idCompany,
                                               idFlight=idFlight)
        self.DB.session.execute(newAirplane)
        self.DB.session.commit()

    def addGate(self, name, idAirplane, idAirport):
        Gate = self.getTable('Gate')
        newGate = Gate.insert().values(name=name,
                                               idAirplane=idAirplane,
                                               idAirport=idAirport)
        self.DB.session.execute(newGate)
        self.DB.session.commit()

    def addPilot(self, name, idFlight):
        Pilot = self.getTable('Pilot')
        newPilot = Pilot.insert().values(name=name,
                                               idFlight=idFlight)
        self.DB.session.execute(newPilot)
        self.DB.session.commit()

    def addBaggageClaim(self, name, idAirport):
        BaggageClaim = self.getTable('BaggageClaim')
        newBaggageClaim = BaggageClaim.insert().values(name=name,
                                               idAirport=idAirport)
        self.DB.session.execute(newBaggageClaim)
        self.DB.session.commit()

    def addPassenger(self, name, idFlight):
        Passenger = self.getTable('Passenger')
        newPassenger = Passenger.insert().values(name=name,
                                               idFlight=idFlight)
        self.DB.session.execute(newPassenger)
        self.DB.session.commit()


    # Define classes here to access database

    # FLIGHT TABLE
    # Flight, Airplane, Gate, Pilot, BaggageClaim, Passenger Count

    def getInfo(self, airportID):
        # grab needed tables
        Flight = self.getTable('Flight')
        Airplane = self.getTable('Airplane')
        Gate = self.getTable('Gate')
        Pilot = self.getTable('Pilot')
        BaggageClaim = self.getTable('BaggageClaim')
        Passenger = self.getTable('Passenger')
        list = []

        allFlights = [row[0] for row in self.DB.session.query(Flight.columns.idFlight).distinct()]
        for id in allFlights:

            # grab necessary variables
            retAirplane = self.DB.select([Airplane.columns.name]).where(Airplane.columns.idFlight == id)
            retPilot = self.DB.select([Pilot.columns.name]).where(Pilot.columns.idFlight == id)
            retBag = self.DB.select([BaggageClaim.columns.name]).where(BaggageClaim.columns.idAirport == airportID)
            passCount = [self.DB.session.query(Passenger).filter(Passenger.columns.idFlight == id).count()]

            # execute sql code
            _A = self.DB.session.execute(retAirplane)
            A = [row[0] for row in _A]
            _P = self.DB.session.execute(retPilot)
            P = [row[0] for row in _P]
            _B = self.DB.session.execute(retBag)
            B = [row[0] for row in _B]

            # grab airplane ID for gate
            airplaneIDSQL = self.DB.select([Airplane.columns.idAirplane]).where(Airplane.columns.idFlight == id)
            _airplaneID = self.DB.session.execute(airplaneIDSQL)
            airplaneID = [row[0] for row in _airplaneID]
            if len(airplaneID) == 0:
                G = []
            else:
                retGate = self.DB.select([Gate.columns.name]).where(Gate.columns.idAirplane == airplaneID)
                _G = self.DB.session.execute(retGate)
                G = [row[0] for row in _G]
            list.append((id, A, G, P, B, passCount))
        return list

    # GATE TABLE, gives gate names and associated airplane
    def getGateInfo(self, airportID):
        list = []
        Gate = self.getTable('Gate')
        retGate = self.DB.select([Gate.columns.idGate, Gate.columns.name, Gate.columns.idAirplane]). \
            where(Gate.columns.idAirport == airportID)
        _G = self.DB.session.execute(retGate)
        for value in _G:
            id = value[0]
            name = value[1]
            associatedAirplane = value[2]
            list.append((id, name, associatedAirplane))
        return list

    def getGate(self, gateID):
        Gate = self.getTable('Gate')
        return self.DB.session.query(Gate).filter_by(idGate=gateID).first()

    def getAirplanesinfo(self):
        Airplane = self.getTable('Airplane')
        return self.DB.session.query(Airplane).all()

    def getAirplanes(self, airplaneID):
        Airplane = self.getTable('Airplane')
        return self.DB.session.query(Airplane).filter_by(idAirplane=airplaneID).first()

    # SEARCH PASSENGER
    def getPassenger(self, name):
        Passenger = self.getTable('Passenger')
        search = "%{}%".format(name)
        return self.DB.session.query(Passenger).filter(Passenger.columns.name.like(search)).all()

    # DELETE FLIGHT, based on flight id
    def delFlight(self, idFlight):
        Flight = self.getTable('Flight')
        self.DB.session.execute(Flight.delete().where(Flight.columns.idFlight == idFlight))
        self.DB.session.commit()

    # DELETE PASSENGER, based on passenger id
    def delPassenger(self, idPassenger):
        Passenger = self.getTable('Passenger')
        self.DB.session.execute(Passenger.delete().where(Passenger.columns.idPassenger == idPassenger))
        self.DB.session.commit()
    
    # UPDATE GATE
    def up_gate(self, idGate, idAirplane):
        Gate = self.getTable('Gate')
        self.DB.session.execute(Gate.update().where(Gate.columns.idGate == idGate).values(idAirplane=idAirplane))
        self.DB.session.commit()

    # UPDATE AIRPLANE
    def up_airplane(self, idAirplane, idFlight):
        Airplane = self.getTable('Airplane')
        self.DB.session.execute(Airplane.update().where(Airplane.columns.idAirplane == idAirplane).values(idFlight=idFlight))
        self.DB.session.commit()

    # UPDATE PILOT
    def up_pilot(self, idPilot, idFlight):
        Pilot = self.getTable('Pilot')
        self.DB.session.execute(Pilot.update().where(Pilot.columns.idPilot == idPilot).values(idFlight=idFlight))
        self.DB.session.commit()
