#!/home1/therevpr/opt/python27/bin/python
import sys
import os
import cgi
import json
import sqlite3
import cgitb
import datetime
# enable displaying debug information in html
# cosider commenting this out for deployment
cgitb.enable()

# Open database connection
db = sqlite3.connect('../db/data.db')
db.row_factory = sqlite3.Row
cursor = db.cursor()

# prepare headers of response
print "Content-type: application/json\n\n"

# To be used by the spab or other vessels...
if os.environ['REQUEST_METHOD'] == 'POST':
    try:
        # Parse JSON body
        data = json.load(sys.stdin)

        # Verify all the expected fields are present
        # timestamp
        if (not ("sourceId" in data)):
            raise Exception('sourceId missing from data')
        if (not ("timestamp" in data)):
            raise Exception('timestamp missing from data')
        # position
        if (not ("latitude" in data)) or (not ("longitude" in data)):
            raise Exception('latitude missing from data')
        # temperature
        if (not ("temperature" in data)):
            raise Exception('temperature missing from data')
        # salinity
        if (not ("salinity" in data)):
            raise Exception('salinity missing from data')

        # Process data
        # Parse timestamp
        # timestamp = data["timestamp"] #/100000  # + 1420070400
        # dateTime = datetime.datetime.fromtimestamp(timestamp)
        # dateString = dateTime.strftime('%Y-%m-%d %H:%M:%S')

        # Store data in database
        values = (data["sourceId"], data["timestamp"], data["latitude"],
                  data["longitude"], data["temperature"], data["salinity"])
        cursor.execute(
            "INSERT INTO Samples (sourceId, timestamp, latitude, longitude, temperature, salinity) VALUES (?, ?, ?, ?, ?, ?)", values)
        db.commit()
        print json.dumps(dict(type="telemAck", success=True,
                              message="Inserted successfully"))
    except ValueError:
        print json.dumps(dict(type="telemAck", success=False,
                              message="JSON could not be decoded"))
    except Exception, e:
        print json.dumps(dict(type="telemAck", success=False,
                              message=str(e)))

if os.environ['REQUEST_METHOD'] == 'GET':
    fromTimestamp = 0  # Default value
    params = cgi.FieldStorage()
    if ("fromTimestamp" in params):
        fromTimestamp = int(params.getvalue("fromTimestamp"))
    cursor.execute("SELECT * FROM samples WHERE timestamp > ? ORDER BY timestamp DESC",
                   (fromTimestamp,))
    data = cursor.fetchall()
    data = [dict(row) for row in data]
    print json.dumps(data)

# Close database connection
db.close()
