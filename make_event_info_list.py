from rdflib import Graph
from pathlib import Path
from tqdm import tqdm
import json
import re
from collections import deque
from pprint import pprint
from time import sleep
from SPARQLWrapper import SPARQLWrapper, JSON


class Database:
    def __init__(self):
        self.sparql = SPARQLWrapper("https://kgrc4si.home.kg:7200/repositories/KGRC4SIv05")
      
    def query(self, sparql_query):
        sleep(0.1)  # 短時間で叩きすぎないよう調整
        self.sparql.setQuery(sparql_query)
        self.sparql.setReturnFormat(JSON)
        return self.sparql.query().convert()["results"]["bindings"]

db = Database()

def get_activities(scene, day):
    scenario = f'{scene}_{day}'
    
    # アクティビティ一覧が書いてあるファイルのパスを構築
    activities_path = f'Dataset/CompleteData/Episodes/{scenario}.json'

    # アクティビティ一覧ファイルからアクティビティ一覧を取り出す
    with open(activities_path, 'r') as activities_file:
        activities_data = json.load(activities_file)
        activities = activities_data["data"]["activities"]

    activities = [a.lower() for a in activities]
    
    return activities

def get_event_info(scene, day):
    event_details = []
    
    activities = get_activities(scene, day)

    for activity in activities:
        activity  = activity.lower()
        sparql_query = f"""
            PREFIX ex: <http://kgrc4si.home.kg/virtualhome2kg/instance/>
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema/>
            PREFIX vh2kg: <http://kgrc4si.home.kg/virtualhome2kg/ontology/>
            PREFIX time: <http://www.w3.org/2006/time#>

            SELECT ?event ?event_number ?action ?event_duration ?object_name ?place_name ?from_name ?to_name WHERE {{
                ex:{activity}_{scene} vh2kg:hasEvent ?event .
                ?event vh2kg:eventNumber ?event_number .
                ?event vh2kg:action ?action .
                ?event vh2kg:time ?time .
                ?time time:numericDuration ?event_duration .

                OPTIONAL {{
                    ?event vh2kg:mainObject ?object .
                    ?object a ?object_name .
                }}

                OPTIONAL {{
                    ?event vh2kg:place ?place .
                    ?place a ?place_name .
                }}

                OPTIONAL {{
                    ?event vh2kg:from ?from .
                    ?from a ?from_name .
                }}

                OPTIONAL {{
                    ?event vh2kg:to ?to .
                    ?to a ?to_name .
                }}

            }} ORDER BY ?event_number
        """


        results = db.query(sparql_query)
        for i, result in enumerate(results):
            event = result['event']['value'].split('/')[-1]
            action = result['action']['value'].split('/')[-1]
            duration = float(result['event_duration']['value'])
            object_name = result.get('object_name', None)
            if object_name != None:
                object_name = object_name['value'].split('/')[-1]
            place_name = result.get('place_name', None)
            if place_name != None:
                place_name = place_name['value'].split('/')[-1]
            from_name = result.get('from_name', None)
            if from_name != None:
                from_name = from_name['value'].split('/')[-1]
            to_name = result.get('to_name', None)
            if to_name != None:
                to_name = to_name['value'].split('/')[-1]

            event_details.append({'event': event, 'action': action, 'duration': duration, 'object': object_name, 'place': place_name, 'from': from_name, 'to': to_name})
        
    return event_details

def main():
    output_dir_path = Path.cwd() / 'event_info'
    output_dir_path.mkdir(exist_ok=True, parents=True)
    
    for scene in [f'scene{i}' for i in range(1, 3)]:
        for day in [f'Day{i}' for i in range(1, 6)]:
            event_details = get_event_info(scene, day)
            output_text_path = output_dir_path / f'{scene}_{day}.csv'
            with open(output_text_path, 'w') as f:
                for i, event_detail in enumerate(event_details):
                    if i == 0:
                        for key in event_detail.keys():
                            f.write(f"{key},")
                        f.write("\n")
                    for value in event_detail.values():
                        f.write(f"{value},")
                    f.write("\n")


if __name__ == '__main__':
    main()
