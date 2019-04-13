#!/home1/therevpr/opt/python27/bin/python
import sys
import os
import cgi
import json
import sqlite3
import cgitb
import datetime
import uuid
# enable displaying debug information in html
# cosider commenting this out for deployment
cgitb.enable()

# Open database connection
db = sqlite3.connect('../db/data.db')
db.row_factory = sqlite3.Row
cursor = db.cursor()

if os.environ['REQUEST_METHOD'] == 'PUT':
    print "Content-type: text/plain\n\n"
    try:
        # Parse JSON body
        # This should be a list of commands
        commands = json.load(sys.stdin)

        # Validate individual commands
        if not (isinstance(commands, list)):
            raise Exception('Data is not in list format')
        for cmd in commands:
            # TODO validate fields for each type of action
            if (not ("action" in cmd)):
                raise Exception('"action" missing from a command')
            if (not ("latitude" in cmd)):
                raise Exception('"latitude" missing from a command')
            if (not ("longitude" in cmd)):
                raise Exception('"longitude" missing from a command')
            if (not ("duration" in cmd)):
                raise Exception('"duration" missing from a command')

        # Clear the previous commands from the database
        cursor.execute("DELETE FROM Commands")
        # Insert new commands into the database
        for cmd in commands:
            values = (str(uuid.uuid4()), cmd["action"], cmd["latitude"],
                      cmd["longitude"], cmd["duration"])
            cursor.execute(
                "INSERT INTO Commands (uuid, action, latitude, longitude, duration) VALUES (?, ?, ?, ?, ?)", values)
        # Commit changes
        db.commit()

        print('Commands updated successfully')
    except ValueError:
        print('Error encounted parsing JSON data')
    except Exception, e:
        print('Error encountered: ' + str(e))


if os.environ['REQUEST_METHOD'] == 'DELETE':
    print "Content-type: application/json\n\n"
    try:
        # Parse JSON body
        # This should be a list of commands
        command_uuids = json.load(sys.stdin)

        # Validate individual commands
        if not (isinstance(command_uuids, list)):
            raise Exception('Data is not in array format')
        for uuid in command_uuids:
            if not (isinstance(uuid, basestring)):
                raise Exception('Array element not string')

        # Remove completed commands from the database
        for uuid in command_uuids:
            cursor.execute("DELETE FROM Commands WHERE uuid=?", (uuid,))

        # Commit changes
        db.commit()
        print json.dumps(dict(type="cmdAck", success=True,
                              message="Commands completed successfully"))
    except ValueError:
        print json.dumps(dict(type="cmdAck", success=False,
                              message="JSON could not be decoded"))
    except Exception, e:
        print json.dumps(dict(type="cmdAck", success=False, message=str(e)))

if os.environ['REQUEST_METHOD'] == 'GET':
    print "Content-type: application/json\n\n"
    cursor.execute("SELECT * FROM Commands ORDER BY id ASC")
    commands = cursor.fetchall()
    commands = [dict(row) for row in commands]
    data = dict(type="cmdLst", data=commands)
    print json.dumps(data)

# Close database connection
db.close()
