from spyre import server
import pandas as pd
import urllib
from datetime import datetime
import os

D = ['Вінницька', 'Волинська', 'Дніпропетровська', 'Донецька', 'Житомирська',
     'Закарпатська', 'Запорізька', 'Івано-Франківська', 'Київська', 'Кіровоградська',
     'Луганська', 'Львівська', 'Миколаївська', 'Одеська', 'Полтавська',
     'Рівненська', 'Сумська', 'Тернопільска', 'Харківська', 'Херсонська',
     'Хмельницька', 'Черкаська', 'Чернівецька', 'Чернігівська', 'Республіка Крим']

def CreateDataFrame(path):
    headers = ['Year', 'Week', 'SMN', 'SMT', 'VCI', 'TCI', 'VHI', 'empty']
    all_files = [i for i in os.listdir(path) if i.endswith('csv')]
    dataFrames = []
    for filename in all_files:
         df = pd.read_csv(fr'{path}\{filename}', header=1, names=headers)
         df = df.drop(df.loc[df['VHI'] == -1].index)
         i = int(filename.split('_')[2].split()[0])
         df['area'] = i

         dataFrames.append(df)
    dataFrame = pd.concat(dataFrames, ignore_index=True)

    dataFrame.pop('empty')
    dataFrame = dataFrame.dropna()
    dataFrame['Year'][(dataFrame['Year'] == '<tt><pre>1982')] = '1982'
    dataFrame['Week'] = dataFrame['Week'].astype(int)
    return dataFrame

class StockExample(server.App):
    title = "Historical Stock Prices"

    inputs = [{"type": 'dropdown',
               "label": 'NOAA data dropdown',
               "options": [{"label": "VCI", "value": "VCI"},
                           {"label": "TCI", "value": "TCI"},
                           {"label": "VHI", "value": "VHI"}],
               "key": 'ticker',
               "action_id": "update_data"},

              {"type": 'dropdown',
               "label": 'Area',
               "options": [{"label": f"{D[i-1]}", "value": f"{i}"}
                           for i in range(1, 26)],
               "key": 'ticker2',
               "action_id": "update_data"},

              {"type": 'text',
               "label": 'Year',
               "value": '1982',
               "key": 'ticker3',
               "action_id": "update_data"},

              {"type": 'text',
               "label": 'week-ranges',
               "value": '1-52',
               "key": 'week_range',
               "action_id": "update_data"}
              ]
    controls = [{"type": "hidden",
                 "id": "update_data"}]

    tabs = ["Table", "Plot"]

    outputs = [{"type": "table",
                "id": "table_id",
                "control_id": "update_data",
                "tab": "Table",
                "on_page_load": True},
               {"type": "plot",
                "id": "plot",
                "control_id": "update_data",
                "tab": "Plot"}]


    def getHTLM(self, params):
        week_range = params["week_range"]
        return week_range

    def getData(self, params):
        ticker = params['ticker']
        area = int(params['ticker2'])
        year = params['ticker3']
        week_range = params['week_range']
        r1, r2 = [int(i) for i in week_range.split('-')]
        df = CreateDataFrame(r'C:\Users\Костянтин\Desktop\pythonProject')
        return df[(df['Year'] == year) & (df['area'] == area) & (df['Week'] >= r1) & (df['Week'] <= r2)][['Year', 'Week', ticker]]

    def getPlot(self, params):
        df = self.getData(params)
        plt_obj = df.plot(x='Week')
        plt_obj.set_xlabel("Week")
        fig = plt_obj.get_figure()
        return fig

app = StockExample()
app.launch(port=9093)


