#Librerías
import pandas as pd
import numpy as np
from requests import Session
import requests
from credenciales import access_token

class SurveyMonkey:

    def __init__(self,acces_token):
        self.headers = {'Accept':'application/json',
                       'Authorization': f"Bearer {access_token}"
                       }
        self.session = Session()
        self.session.headers.update(self.headers)

    def EndPointSurvey(self):
        endpoint = {'apiurl':"http://api.surveymonkey.com/v3/surveys",
                    'responses':"http://api.surveymonkey.com/v3/surveys/__id__/responses",
                    'details':"http://api.surveymonkey.com/v3/surveys/__id__/details",
                    'rollups':"http://api.surveymonkey.com/v3/surveys/__id__/rollups",
                    'responses_bulk':"http://api.surveymonkey.com/v3/surveys/__id__/responses/bulk",                   
                    }

        return endpoint

    def GetSurveyDetails(self,id):
        url = self.EndPointSurvey()['details'].replace('__id__',str(id))
        r = self.session.get(url)
        data = r.json()

        return data

    def GetRollUpsSurvey(self,id):
        url = self.EndPointSurvey()['rollups'].replace('__id__',str(id))
        r = self.session.get(url)
        data = r.json()

        return data

    def GetResponsesBullk(self,id):
        url = self.EndPointSurvey()['responses_bulk'].replace('__id__',str(id))
        r = self.session.get(url)
        data = r.json()

        return data


    def GetForms(self):
        url = self.EndPointSurvey()['apiurl']
        r = self.session.get(url)

        data = r.json()['data']
        
        formularios = pd.DataFrame(data=[key['title'] for key in data],columns=['titulo'])
        formularios['titulo_interno'] = [key['nickname'] for key in data]
        #formularios['link'] = [key['href'] for key in data]
        formularios['id'] = [key['id'] for key in data]

        formularios = formularios[0:2]
        return formularios
        

    def GetResponse(self,id):
        url = self.EndPointSurvey()['responses'].replace('__id__',str(id))
        r = self.session.get(url)
        data = r.json()['data']

        return data

    def GetNumberResponses(self):

        id_forms = list(self.GetForms()['id'])
        n_responses = []
        for id in id_forms:
            n_response = sm.GetRollUpsSurvey(id)['data'][0]['summary'][0]['answered']
            n_responses.append(n_response)

        formularios = self.GetForms()
        formularios['respuestas'] = n_responses

        return formularios

    def GetResponses(self):

        id_forms = list(self.GetForms()['id'])
        responses = []
        for id in id_forms:
            response = self.GetResponse(id)
            responses.append(response)

        return responses

    def GenerateCSV(self):
        
        data = self.GetNumberResponses()
        return data.to_csv(f'tabla_{len(data)}_formularios.csv')

sm = SurveyMonkey(acces_token=access_token)