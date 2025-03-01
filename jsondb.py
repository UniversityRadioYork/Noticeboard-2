from pathlib import Path
import json
import io
import sys

#This is the database for the app. its just a json file. Its fine we only store a few hundred lines of text. Probably fine. eh.
class Jsondb:
    def __init__(self):
        project = Path("/opt/notice.json")
        if project.is_file() == False:
            print("Database json did not exists, creating new db", file=sys.stderr)
            with open("/opt/notice.json", 'w') as file:
                file.write("{}") 
            data = self.get_data()
            data["brokenlabel"] = "Something Broken?"
            data["brokenhtml"] = "<h4>Report all faults on #studio-faults channel on Slack!!</h4>\n<p>And if you need help with anything else don't be scared to ask in our #ask-a-question slack channel</p>"
            data["joinlabel"] = "Join our Slack!"
            data["joinhtml"] = "<h2>Go to ury.slack.com</h2>"
            data["listenlabel"] = "More ways to Listen"
            data["listenhtml"] = "<h4>Tune in on 88.3 FM, Online at ury.org.uk or on digital radio!</h4>\n<p>We've also got all our old stuff at mixcloud.com/URY1350</p>"
            data["extralabel"] = ""
            data["extrahtml"] = ""
            data["welfarelabel"] = "Struggling with wellbeing or need a chat?"
            data["welfarehtml"] = "<p>We're here for you! email welfare@ury.org.uk, go to ury.org.uk/welfare or reach out to one of our welfare officers</p>"
            data["bannerlabel"] = "Get Involved!"
            data["meetinglabel"] = "Meeting Times"
            data["meetinghtml"] = "<p>Station Meetings Monday at 7PM, in V/N/123a.</p>\n<p>Production Meetings Monday at 8PM, in V/N/123a.</p>"
            data["committeehtml"] = "<h1>Join our Committee</h1>\n<p>To run for a role just send an email to ury@yorksu.org</p>"
            data["showlabel"] = "Your Next Listen?"
            data["refresh"] = "0"
            data["openroles"] = "{}"
            data["nextevent"] = "{}"
            data["recentshows"] = "[]"
            self.save_data(data)

    def get_data(self):
        with open("/opt/notice.json", 'r') as file:
            data = json.load(file)
            return data

    def save_data(self, data):
        with open("/opt/notice.json", 'w') as file:
            json.dump(data, file)

    def set_userdata(self, brokenlabel, brokenhtml, joinlabel, joinhtml, listenlabel, listenhtml, extralabel, extrahtml, welfarelabel, welfarehtml, bannerlabel, meetinglabel, meetinghtml, committeehtml, showlabel, refresh):
        data = self.get_data()
        data["brokenlabel"] = brokenlabel
        data["brokenhtml"] = brokenhtml
        data["joinlabel"] = joinlabel
        data["joinhtml"] = joinhtml
        data["listenlabel"] = listenlabel
        data["listenhtml"] = listenhtml
        data["extralabel"] = extralabel
        data["extrahtml"] = extrahtml
        data["welfarelabel"] = welfarelabel
        data["welfarehtml"] = welfarehtml
        data["bannerlabel"] = bannerlabel
        data["meetinglabel"] = meetinglabel
        data["meetinghtml"] = meetinghtml
        data["committeehtml"] = committeehtml
        data["showlabel"] = showlabel
        data["refresh"] = refresh
        self.save_data(data)

    def set_openroles(self, openroles):
        data = self.get_data()
        data["openroles"] = openroles
        self.save_data(data)

    def set_recentshows(self, recentshows):
        data = self.get_data()
        data["recentshows"] = recentshows
        self.save_data(data)

    def set_nextevent(self, nextevent):
        data = self.get_data()
        data["nextevent"] = nextevent
        self.save_data(data)

    def get_openroles(self):
        data = self.get_data()
        return data["openroles"]

    def get_recentshows(self):
        data = self.get_data()
        return data["recentshows"]

    def get_nextevent(self):
        data = self.get_data()
        return data["nextevent"]

    def get_brokenlabel(self):
        data = self.get_data()
        return data["brokenlabel"]

    def get_brokenhtml(self):
        data = self.get_data()
        return data["brokenhtml"]

    def get_joinlabel(self):
        data = self.get_data()
        return data["joinlabel"]

    def get_joinhtml(self):
        data = self.get_data()
        return data["joinhtml"]

    def get_listenlabel(self):
        data = self.get_data()
        return data["listenlabel"]

    def get_listenhtml(self):
        data = self.get_data()
        return data["listenhtml"]

    def get_extralabel(self):
        data = self.get_data()
        return data["extralabel"]

    def get_extrahtml(self):
        data = self.get_data()
        return data["extrahtml"]

    def get_welfarelabel(self):
        data = self.get_data()
        return data["welfarelabel"]

    def get_welfarehtml(self):
        data = self.get_data()
        return data["welfarehtml"]

    def get_bannerlabel(self):
        data = self.get_data()
        return data["bannerlabel"]

    def get_meetinglabel(self):
        data = self.get_data()
        return data["meetinglabel"]

    def get_meetinghtml(self):
        data = self.get_data()
        return data["meetinghtml"]

    def get_committeehtml(self):
        data = self.get_data()
        return data["committeehtml"]

    def get_showlabel(self):
        data = self.get_data()
        return data["showlabel"]

    def get_refresh(self):
        data = self.get_data()
        return data["refresh"]