import socket
from http.server import BaseHTTPRequestHandler, HTTPServer
import time
import json
import gspread
from threading import Timer
import sched
from oauth2client.service_account import ServiceAccountCredentials
import datetime

# General setup code for the server was inspired by: https://gist.github.com/bradmontgomery/2219997

hostName = "192.168.0.8"
hostPort = 80 

# use creds to create a client to interact with the Google Drive API
scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
client = gspread.authorize(creds)

# Opening the sheet
sheet = client.open("IOT DATA")
worksheet = sheet.get_worksheet(0)

rowIndexDevice1 = 1
rowIndexDevice2 = 2


class MyServer(BaseHTTPRequestHandler):

# Handling POST requests
    def do_POST(self):
        print( "incomming http: ", self.path )

        content_length = int(self.headers['Content-Length']) #  Gets the size of data
        post_data = self.rfile.read(content_length) #  Gets the data itself

        self.send_response(200) # Response 200 means no problems
        self.end_headers()
        self.wfile.write(b"1") # Sends a simple response 

        data = json.loads(post_data)

        timeAndDate = str(datetime.datetime.now())

        global rowIndexDevice1
        global rowIndexDevice2

        accumulatedAcceleration = data["x"] * data["y"] * data["z"] # calculates the total change in acceleration
        absoluteAcceleration = abs(accumulatedAcceleration) # calculates the absolute value of the acceleration

        if data["ID"]=="1":
            rowIndexDevice1 +=1
            worksheet.update_cell(rowIndexDevice1,1,timeAndDate)
            worksheet.update_cell(rowIndexDevice1,2, data["x"]) # insert the x axis acceleration
            worksheet.update_cell(rowIndexDevice1,3, data["y"]) # insert the y axis acceleration
            worksheet.update_cell(rowIndexDevice1,4, data["z"]) # insert the z axis acceleration
            worksheet.update_cell(rowIndexDevice1,5, absoluteAcceleration) # insert the absolute value of total acceleration  
        if data["ID"]=="2":
            rowIndexDevice2 +=1
            worksheet.update_cell(rowIndexDevice2,7,timeAndDate)
            worksheet.update_cell(rowIndexDevice2,8, data["temp"])

myServer = HTTPServer((hostName, hostPort), MyServer)
print(time.asctime(), "Server Started - %s:%s" % (hostName, hostPort))

try:
    myServer.serve_forever()
except KeyboardInterrupt:
    pass

myServer.server_close()
print(time.asctime(), "Server Stopped - %s:%s" % (hostName, hostPort))

