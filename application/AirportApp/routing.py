from flask import render_template, url_for, redirect, request

try:
    from .database import Database
except ModuleNotFoundError:
    from database import Database


# This function will be called by init on server start up and establish all routes

def Routing(app):
    # Page routing can pass data into html pages from the database
    # Example: db.getFlight(flightID) will return the flight entry of the given flight id
    db = Database(app)

    # Every web page needs a routing like the one below for home
    # These routes can pass variables into the function below
    @app.route('/')
    def index():
        # Variables and functions can be passed into html files to use
        return render_template('coverpage.html',
                               title='Oakland Airport')

    # Page after entering through index/welcome page
    @app.route('/home')
    def homepage():
        return render_template('home.html', title='Oakland Airport Home Page')

    # Page to display all info on flights
    @app.route('/flight')
    def flights():
        # Flight, Gate, Airplane, Pilot, BaggageClaim, Passenger Count
        Flightcolumns = db.getInfo('1')
        return render_template('flight.html',
                               title='Airport Monitor',
                               columns=Flightcolumns
                               )

    # Page will contain form to add a flight
    @app.route('/addflight', methods=["GET", "POST"])
    def addflight():
        if request.method == "POST":
            departure_time = request.form['departure']
            arrival_time = request.form['arrival']

            db.addFlight(departure_time, arrival_time)
            # Add the Flight based on the info here
            # Have to input in the database
            return redirect(url_for('flights'))
        else:
            return render_template('addflight.html')

    # Page will delete a specified flight
    # NOTE: This feature will probably be built into flight page and not need its own
    @app.route('/deleteFlight/<int:fid>')
    def deleteFlights(fid):
        db.delFlight(fid)
        return redirect(url_for('flights'))

    # Page will search for passengers and display them
    # Empty searches will get all passengers
    @app.route('/passenger', methods=["GET", "POST"])
    def passengers():
        if request.method == "POST":
            name = request.form['name']
            passengerResults = db.getPassenger(name)
            return render_template('passenger.html',
                                   title='Check Passengers',
                                   results=passengerResults)
        else:
            return render_template('passenger.html', title='Check Passengers')

    # Page will delete specified passenger
    @app.route('/deletePassenger/<int:pid>')
    def deletePassengers(pid):
        db.delPassenger(pid)
        return redirect(url_for('passengers'))

    # Page will display all gates
    @app.route('/gate')
    def gate():
        gate = db.getGateInfo('1')
        return render_template('gate.html', title='Gate Info',
                               columns=gate)

    # Page will update gate info
    # NOTE: This feature will probably be built into gate page and not need its own
    @app.route('/gateupdate/<int:gid>', methods=["GET", "POST"])
    def gateupdate(gid):
        if request.method == "POST":
            flight = request.form['airplane']
            db.up_gate(gid, flight)
            return redirect(url_for('gate'))
        else:
            gate = db.getGate(gid)
            return render_template('gateUpdate.html', gid=gid,
                                   gatevalue=gate.name, airplane=gate.idAirplane)

    @app.route('/airplane')
    def airplane():
        airplanes = db.getAirplanesinfo()
        return render_template('airplane.html', title='Airplane Info', airplanes=airplanes)

    # Page will update airplane info
    @app.route('/airplaneUpdate/<int:apid>', methods=["GET", "POST"])
    def airplaneUpdate(apid):
        if request.method == "POST":
            updatedFlightID = request.form['flightId']
            db.up_airplane(apid, updatedFlightID)
            return redirect(url_for('airplane'))
        else:
            airplanes = db.getAirplanes(apid)
            return render_template('airplaneUpdate.html',
                                   title='Update Airplane',
                                   apid=apid,
                                   airplanename=airplanes.name,
                                   airplaneflight=airplanes.idFlight)

    # General FAQ/about page for our project
    @app.route('/support')
    def support():
        return render_template('support.html', title='Support')


