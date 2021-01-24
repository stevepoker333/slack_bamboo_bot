import requests
from datetime import datetime, timedelta
import re


class Bamboohr:

    def __create_request(self, url, method, payload='', headers='', querystring=''):
        if payload == '':
            response = requests.request(method, url, headers=headers, params=querystring)
        else:
            response = requests.request(method, url, data=payload, headers=headers, params=querystring)
        if response.status_code == 200:
            return response
        else:
            print("Sorry but Bamboohr API not working :(")
            return ''

    def get_emp_profile_by_id(self, emp_id):
        url = "https://api.bamboohr.com/api/gateway.php/vgs/v1/employees/" + emp_id + "/"

        querystring = {"fields": "firstName,lastName,hireDate,department,jobTitle,city,"
                                 "country,location,isPhotoUploaded,status"}

        headers = {
            'accept': "application/json",
            'authorization': "Basic ZTE5YzlkMzE3NTZhNTEzNTEzMjNiZWYxNDc2N2JhOWUxY2NhNjBiODp4"
        }
        response = self.__create_request(url, "GET", headers=headers, querystring=querystring)
        if emp_id != '177':  # my own id (because bambooHR does not return me anything on status check)
            if response.json()['status'] == 'Inactive':
                return None
        return response

    def get_all_emp_profiles(self):
        url = "https://api.bamboohr.com/api/gateway.php/vgs/v1/reports/custom"

        querystring = {"format": "JSON"}

        payload = "{\"fields\":[\"firstName\",\"lastName\",\"hireDate\",\"dateOfBirth\"," \
                  "\"department\",\"location\",\"workEmail\"]}"
        headers = {
            'content-type': "application/json",
            'authorization': "Basic ZTE5YzlkMzE3NTZhNTEzNTEzMjNiZWYxNDc2N2JhOWUxY2NhNjBiODp4"
        }
        response = self.__create_request(url, "POST", payload=payload, headers=headers, querystring=querystring)
        return response

    def get_emp_photo_url(self, emp_id):
        url = "https://api.bamboohr.com/api/gateway.php/vgs/v1/employees/directory"

        headers = {
            'accept': "application/json",
            'authorization': "Basic ZTE5YzlkMzE3NTZhNTEzNTEzMjNiZWYxNDc2N2JhOWUxY2NhNjBiODp4"
        }
        response = self.__create_request(url, "GET", headers=headers)
        response = response.json()
        response_text = str(response['employees'])
        result = re.search(r"id': '{}'".format(emp_id), response_text)
        response_text = re.findall(r"photoUrl': '(\S+)'", response_text[result.start():])
        return response_text[0]

    def check_newbies(self):
        url = "https://api.bamboohr.com/api/gateway.php/vgs/v1/employees/changed"
        since = datetime.today() - timedelta(days=60)
        since = since.strftime('%Y-%m-%d') + 'T12:00:00-02:00'
        querystring = {"since": since, "type": "inserted"}
        headers = {
            'accept': "application/json",
            'authorization': 'Basic ZTE5YzlkMzE3NTZhNTEzNTEzMjNiZWYxNDc2N2JhOWUxY2NhNjBiODp4'
        }
        response = self.__create_request(url, "GET", headers=headers, querystring=querystring).json()
        newbies_list = []
        for i in sorted(response['employees'].keys(), reverse=True):
            employee = self.get_emp_profile_by_id(i).json()
            if employee['hireDate'] == '2019-10-21':  # datetime.today().strftime('%Y-%m-%d'):
                newbies_list.append(i)
        return newbies_list

    def check_hb(self):
        get_list_json = self.get_all_emp_profiles().json()['employees']
        get_list_text = str(get_list_json)
        today = '12-11'   # datetime.today().strftime('%m-%d')
        hb_list = re.findall(r"(\d+)...\S+.\S+.\S+.\S+.\S+.\S+..dateOfBirth....\d+.{}".format(today), get_list_text)
        return hb_list

    def check_anniversary(self):
        get_list_json = self.get_all_emp_profiles().json()['employees']
        get_list_text = str(get_list_json)
        today = '10-24'   # datetime.today().strftime('%m-%d')
        anniversary_list = re.findall(r"(\d+)...\S+.\S+.\S+.\S+.\S+..(\d+).{}\',.\'date".format(today), get_list_text)
        return anniversary_list  # returned list of tuples(id and year) like: [(id, YY), (id, YY), ...]
