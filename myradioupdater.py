import requests
import json
import sys
import pytz
from jsondb import Jsondb
from datetime import datetime

#class for actually doing myradio stuff
class MyRadioUpdater:
    def __init__(self, api_url, api_key):
        self.api_url = api_url
        self.api_key = api_key
        self.json_db = Jsondb()

    #chatgpt mostly wrote this bit. Just turns a unix time and duration into a nice string. Used for show recommendations
    def unix_to_uk_time(self, unix_time, duration):
        utc_timezone = pytz.utc
        dt_utc = datetime.fromtimestamp(unix_time, tz=utc_timezone)
        uk_timezone = pytz.timezone("Europe/London")
        dt_uk = dt_utc.astimezone(uk_timezone)
        day_of_week = dt_uk.strftime("%A")  
        time_of_day = dt_uk.strftime("%H") 
        duration = int(duration.split(":")[0])
        end_time = int(time_of_day) + duration
        return f"{day_of_week} {time_of_day}:00 - {str(end_time)}:00"

    #similar to the last one and just as AI generated, this one is used for upcoming events
    def convert_to_human_readable(self, datetime_str, end_time):
        dt = datetime.fromisoformat(datetime_str)
        dte = datetime.fromisoformat(end_time)
        dt = dt.astimezone(pytz.timezone('Europe/London'))
        dte = dte.astimezone(pytz.timezone('Europe/London'))
        date_part = dt.strftime("%d %B %Y") 
        start_time = dt.strftime("%H:%M") 
        end_time = dte.strftime("%H:%M")
        human_readable_str = f"{date_part} {start_time} — {end_time}"
        return human_readable_str

    #sorts roles from id and type. Team distinctions are prioritised.
    def getrolecat(self, teamid, roletype):
        if teamid == 1:
            return "Management"
        if teamid in [10,11,20]:
            return "Other Officers"
        if roletype == "h":
            return "Team Heads"
        if roletype == "a":
            return "Team Deputies"

    #gets the current week or shows and filters out jukebox
    def getshows(self, week):
        pool = []
        api_url = self.api_url  + "/timeslot/weekschedule/"+str(week)+"?" + self.api_key
        response = requests.get(api_url)
        upcomingshows = json.loads(response.text)
        days = upcomingshows["payload"]
        shows = []
        for i in days:
            shows = shows + days[i]
        shows = [d for d in shows if d["title"] != "URY Jukebox"]
        for i in shows:
            pool.append({"title": i["title"], "description": i["description"], "time": self.unix_to_uk_time(i["time"], i["duration"]), "art": i["photo"]})
        return pool

    #gets the last n podcasts
    def getpods(self, num):
        pool = []
        api_url = self.api_url + "podcast/allpodcasts?num_results=20&" + self.api_key
        response = requests.get(api_url)
        upcomingshows = json.loads(response.text)
        pods = upcomingshows["payload"]
        for i in pods:
            pool.append({"title": i["title"], "description": i["description"], "time": "Podcast", "art": i["photo"]})
        return pool 

    #Gets the list of open roles. This one is really slow because I didn't want to edit myradio. You could make it much faster by making a new myradio endpoint.
    #If you know how to do that you know why I didn't and if you don't then just trust me.
    def updateRoles(self):
        try:
            #gets all the officer permissions
            api_url = self.api_url + "officer/allofficerpositions?" + self.api_key
            response = requests.get(api_url)
            allroles = json.loads(response.text)
            currentroles = []
            openroles = []
            #filters out all the non-comittee positions and old unused permissions
            for key in allroles["payload"]:
                if key["status"] == "c" and key["type"] in ["h","a"] and key["team"]["status"] == "c":
                    currentroles.append({"id": key["officerid"], "name": key["name"], "type": key["type"], "teamid": key["team"]["teamid"]})
            #loops through all the roles and makes another request for the current roleholders
            for i in currentroles:
                pos = 1
                #some jank stuff to check if the role is for 1 or 2 people
                if "deputy" in i["name"].lower() or i["id"] in [135,39]:
                    pos = 2
                api_url = self.api_url + "officer/" + str(i["id"]) + "/currentholders?" + self.api_key
                response = requests.get(api_url)
                members = json.loads(response.text)
                #checks if any roles available
                incumbants = len(members["payload"])
                if incumbants < pos:
                    openroles.append({"name": i["name"], "teamid": i["teamid"], "category": self.getrolecat(i["teamid"], i["type"])})
                sortedopenroles = sorted(openroles, key=lambda d: d['teamid'])
            self.json_db.set_openroles(json.dumps(sortedopenroles))
            print("Updated list of available roles", file=sys.stderr)
        except:
            print("Error occured updating available roles" , file=sys.stderr)

    def updateRecentShows(self):
        try:
            pool = []
            today = datetime.today()
            week_num = today.isocalendar()[1]
            pool += self.getshows(week_num)
            pool += self.getshows(week_num+1)
            pool += self.getpods(20)
            self.json_db.set_recentshows(json.dumps(pool))
            print("Updated list of suggested shows", file=sys.stderr)
        except:
            print("Error occured updating recommended shows" , file=sys.stderr)

    #just calles the event api
    def updateNextEvent(self):
        try:
            api_url = self.api_url + "event/next?" + self.api_key
            response = requests.get(api_url)
            nextevent = json.loads(response.text)
            tosave = {}
            if len(nextevent["payload"]) > 0:
                event = nextevent["payload"][0]
                tosave =  {"title": event["title"], "time": self.convert_to_human_readable(event["start"], event["end"]), "description": event["description_html"]}
            else:
                tosave = {"title": "No Upcoming Events", "time": "", "description": "We don't have any events scheduled but keep your eye on our Slack for updates!"}
            self.json_db.set_nextevent(json.dumps(tosave))
            print("Updated most recent event", file=sys.stderr)
        except:
            print("Error occured updating next event" , file=sys.stderr)

        