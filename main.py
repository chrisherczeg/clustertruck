#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
import json
import urllib2
import jinja2
from datetime import datetime
from markupsafe import Markup

jinja_environment = jinja2.Environment(loader=jinja2.FileSystemLoader('templates'))

class MainHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template('clustertruck.html')
        locations = self.clustertruck_API()
        weather_indy = self.weather_API_Indy(locations)
        weather_bloom = self.weather_API_Bloomington(locations)
        indy_weather = self.dictionary_weather(weather_indy)
        bloom_weather =self.dictionary_weather(weather_bloom)
        months = self.dictionary_month(self.weather_API_Indy(locations))
        date = self.dictionary_date(self.weather_API_Indy(locations))
        monday_bloom = (self.get_number(bloom_weather, date, months, 'Monday')) / 17.00 * 100
        tuesday_bloom = (self.get_number(bloom_weather, date, months, 'Tuesday')) / 17.00 *100
        wednesday_bloom= (self.get_number(bloom_weather, date, months, 'Wednesday')) / 17.00 *100
        thursday_bloom = (self.get_number(bloom_weather, date, months, 'Thursday')) / 17.00 *100
        friday_bloom = (self.get_number(bloom_weather, date, months, 'Friday')) / 17.00 *100
        saturday_bloom = (self.get_number(bloom_weather, date, months, 'Saturday'))/17.00 *100
        sunday_bloom = (self.get_number(bloom_weather, date, months, 'Sunday'))/17.00 *100


        monday_indy = (self.get_number(indy_weather, date, months, 'Monday'))/17.00 *100
        tuesday_indy = (self.get_number(indy_weather, date, months, 'Tuesday'))/17.00 *100
        wednesday_indy = (self.get_number(indy_weather, date, months, 'Wednesday'))/17.00*100
        thursday_indy = (self.get_number(indy_weather, date, months, 'Thursday'))/17.00*100
        friday_indy = (self.get_number(indy_weather, date, months, 'Friday'))/17.00*100
        saturday_indy = (self.get_number(indy_weather, date, months, 'Saturday'))/17.00*100
        sunday_indy = (self.get_number(indy_weather, date, months, 'Sunday'))/17.00*100


        variables = {

        'Monday': Markup('<dd class="percentage percentage-%i"><span class="text">Monday</span></dd>'%((round(monday_bloom)))),
        'Tuesday': Markup('<dd class="percentage percentage-%i"><span class="text">Tuesday</span></dd>'%(round(tuesday_bloom))),
        'Wednesday': Markup('<dd class="percentage percentage-%i"><span class="text">Wednesday</span></dd>'% (round(wednesday_bloom))),
        'Thursday':Markup('<dd class="percentage percentage-%i"><span class="text">Thursday</span></dd>' %(round(thursday_bloom))),
        'Friday': Markup('<dd class="percentage percentage-%i"><span class="text">Friday</span></dd>'%(round(friday_bloom))),
        'Saturday': Markup('<dd class="percentage percentage-%i"><span class="text">Saturday</span></dd>' %(round(saturday_bloom))),
        'Sunday': Markup('<dd class="percentage percentage-%i"><span class="text">Sunday</span></dd>' %(round(sunday_bloom))),
        'MondayIndy': Markup('<dd class="percentage percentage-%i"><span class="text">Monday</span></dd>' % ((round(monday_indy)))),
        'TuesdayIndy': Markup('<dd class="percentage percentage-%i"><span class="text">Tuesday</span></dd>' % (round(tuesday_indy))),
        'WednesdayIndy': Markup('<dd class="percentage percentage-%i"><span class="text">Wednesday</span></dd>' % (round(wednesday_indy))),
        'ThursdayIndy': Markup('<dd class="percentage percentage-%i"><span class="text">Thursday</span></dd>' % (round(thursday_indy))),
        'FridayIndy': Markup('<dd class="percentage percentage-%i"><span class="text">Friday</span></dd>' % (round(friday_indy))),
        'SaturdayIndy': Markup('<dd class="percentage percentage-%i"><span class="text">Saturday</span></dd>' % (round(saturday_indy))),
        'SundayIndy': Markup('<dd class="percentage percentage-%i"><span class="text">Sunday</span></dd>' % (round(sunday_indy)))
         }

        self.response.write(template.render(variables))

    def clustertruck_API(self):
        url_Cluster_Truck = 'https://api.staging.clustertruck.com/api/kitchens'
        json_obj = urllib2.urlopen(url_Cluster_Truck)
        json_dictionary = json.load(json_obj)
        location_coordinates = {}
        for location in json_dictionary:
            location_coordinates[location['name']] = location['location']

        return location_coordinates
    #[[{u'Downtown Indy': {u'lat': 39.7776023, u'lng': -86.1555877}}], [{u'Bloomington': {u'lat': 39.17093690000001, u'lng': -86.500373}}]]
##need weather
    def weather_API_Bloomington(self,locations):
        lat = locations['Downtown Indy']['lat']
        long = locations['Downtown Indy']['lng']
        api_key = '5f1b8f64f5b3a41ab8aa24daf5f5d886'
        url_weather = 'http://api.openweathermap.org/data/2.5/forecast?lat=%s&lon=%s&appid=%s' %(lat,long,api_key)
        json_obj = urllib2.urlopen(url_weather)
        json_dictionary = json.load(json_obj)
        return json_dictionary

    def weather_API_Indy(self, locations):
        lat =  locations['Bloomington']['lat']
        long = locations['Bloomington']['lng']
        api_key = '5f1b8f64f5b3a41ab8aa24daf5f5d886'
        url_weather = 'http://api.openweathermap.org/data/2.5/forecast?lat=%s&lon=%s&appid=%s' % (lat, long, api_key)
        json_obj = urllib2.urlopen(url_weather)
        json_dictionary = json.load(json_obj)
        return json_dictionary

    def dictionary_weather(self, dictionary):
        weather = {'Monday': 'null', 'Tuesday': 'null', 'Wednesday': 'null', 'Thursday': 'null', 'Friday': 'null',
                   'Saturday': 'null', 'Sunday': 'null'}

        for i in dictionary['list']:
            ep = i['dt']
            date = str(datetime.fromtimestamp(ep))
            real_time = date[11:]
            if real_time == '11:00:00':
                weather[str(datetime.fromtimestamp(ep).strftime("%A"))] = str(i['weather'][0]['main'])

        return weather
    def dictionary_date(self, dictionary):
        day = {'Monday': 'null', 'Tuesday': 'null', 'Wednesday': 'null', 'Thursday': 'null', 'Friday': 'null',
                   'Saturday': 'null', 'Sunday': 'null'}

        for i in dictionary['list']:
            ep = i['dt']
            date = date = str(datetime.fromtimestamp(ep))
            real_day = date[8:10]
            day[str(datetime.fromtimestamp(ep).strftime("%A"))] = str(real_day)
        return day

    def dictionary_month(self, dictionary):
        day = {'Monday': 'null', 'Tuesday': 'null', 'Wednesday': 'null', 'Thursday': 'null', 'Friday': 'null',
                   'Saturday': 'null', 'Sunday': 'null'}

        for i in dictionary['list']:
            ep = i['dt']
            date = date = str(datetime.fromtimestamp(ep))
            real_month= date[5:7]
            day[str(datetime.fromtimestamp(ep).strftime("%A"))] = str(real_month)
        return day

    def get_number(self, dictionary_weather, dictionary_date,dictionary_month, day):
        number = 0
        if day == 'Monday':
            number+=1
        elif day == 'Tuesday':
            number+=2
        elif day == 'Wedsnesday':
            number+=3
        elif day == 'Thursday':
            number+=4
        elif day == 'Friday':
            number+=5
        elif day == 'Saturday':
            number+=3
        else:
            number+=3

        if dictionary_date[day] == '30':
            if dictionary_month[day] == '04' or dictionary_month[day] == '06' or dictionary_month[day] == '09'or dictionary_month[day] == '11':
                number += 5
        elif dictionary_date[str(day)] == '31':
            if dictionary_month[day] == '01' or dictionary_month[day] == '03' or dictionary_month[day] == '05' or dictionary_month[day] == '07' or dictionary_month[day] == '08' or dictionary_month[day] == '10' or dictionary_month[day] == '12':
                number+=5
        elif dictionary_date[day] == '28':
            if dictionary_month[day] == '02':
                number +=5

        if dictionary_weather[day] == 'Clouds':
            number+=-2
        elif dictionary_weather[day] == 'Rain':
            number+=4
        elif dictionary_weather[day] == 'Snow':
            number+=5
        elif dictionary_weather[day] == 'Clear':
            number +=-2
        else:
            number+=-2
        if number < 0:
            number = 0

        return number

app = webapp2.WSGIApplication([
    ('/', MainHandler)
], debug=True)
