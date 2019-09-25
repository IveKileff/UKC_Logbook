import csv

from datetime import datetime

import plotly.graph_objects as go

from plotly.subplots import make_subplots

class BuildData:
    '''A class that visualises the grades of the User's Lead Climbs'''

    def __init__(self, filename):
        '''initialise attributes'''
        self.filename = filename
        self.data, self.sport, self.trad, self.dates  = [], [], [], []
        self.s_grade_dict, self.t_grade_dict = {}, {}

    def run_program(self):
        self.get_data()
        self.categorise_climbs()
        self.rationalise_trad_grades()
        self.build_visuals()
        self.visualise_climbs()

    def get_data(self):
        '''open the logbook file and set variables based on file structure'''
        with open(self.filename) as f:
            reader = csv.reader(f)
            header_row = next(reader)
            for index, header in enumerate(header_row):
                if header == 'Date':
                    date_index = index
                elif header == 'Grade':
                    grade_index = index
                elif header == 'Style':
                    style_index = index

            # get dates, grades & style for all routes from file & clean data
            for row in reader:
                date = datetime.strptime(row[date_index][3:], '%b/%y')
                grade = row[grade_index].replace("*", "").strip()
                style = row[style_index]
                row_data = [date, grade, style]
                self.data.append(row_data)
            self.data.sort()
           
    def categorise_climbs(self):
        '''categorise climbs using Style, and extract only Lead climbs'''
        numbers = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
        letters = ['D', 'E', 'H', 'M', 'S', 'V']
        data = self.data[:]     
        # made a copy of this list in case I want to extend the program later
        while data:
            climb = data.pop()
            grade = climb[1]
            style = climb[2] 
            if grade[0] in numbers and (
                (style[0:4] == 'Lead' and style[0:6] != 'Lead d') or (
                    style[0:5] == 'AltLd' and style[0:7] != 'AltLd d')):
                self.sport.append(climb)
            elif grade[0] in letters and (
                (style[0:4] == 'Lead' and style[0:6] != 'Lead d') or (
                    style[0:5] == 'AltLd' and style[0:7] != 'AltLd d')):
                self.trad.append(climb)

    def rationalise_trad_grades(self):
        for index in range(0, len(self.trad)):
            if self.trad[index][1][0:2] == 'MS':
                self.trad[index][1] = 'S'
            elif self.trad[index][1][0:3] == 'MVS':
                self.trad[index][1] = 'HS'
            elif self.trad[index][1][0:2] == 'HS':
                self.trad[index][1] = 'HS'
            elif self.trad[index][1][0:3] == 'HVD':
                self.trad[index][1] = 'HVD'
            elif self.trad[index][1][0:3] == 'HVS':
                self.trad[index][1] = 'HVS'
            elif self.trad[index][1][0:1] == 'S':
                self.trad[index][1] = 'S'
            elif self.trad[index][1][0:2] == 'VS':
                self.trad[index][1] = 'VS'
            elif self.trad[index][1][0:2] == 'E1':
                self.trad[index][1] = 'E1'
            elif self.trad[index][1][0:2] == 'E2':
                self.trad[index][1] = 'E2'
            elif self.trad[index][1][0:2] == 'E3':
                self.trad[index][1] = 'E3'
            elif self.trad[index][1][0:2] == 'E4':
                self.trad[index][1] = 'E4'
            elif self.trad[index][1][0:2] == 'E5':
                self.trad[index][1] = 'E5'
            elif self.trad[index][1][0:2] == 'E6':
                self.trad[index][1] = 'E6'
            elif self.trad[index][1][0:2] == 'E7':
                self.trad[index][1] = 'E7'
            elif self.trad[index][1][0:2] == 'E8':
                self.trad[index][1] = 'E8'
            elif self.trad[index][1][0:2] == 'E9':
                self.trad[index][1] = 'E9'
            elif self.trad[index][1][0:3] == 'E10':
                self.trad[index][1] = 'E10'

    def build_visuals(self):
        '''engineer data to enable visualisation'''
        trad_grade_order = ['D', 'VD', 'HVD', 'S', 'HS', 'VS', 'HVS', 'E1', 
        'E2', 'E3', 'E4', 'E5', 'E6', 'E7', 'E8', 'E9', 'E10']
        s_dates, s_grades = self._find_dates_grades(self.sport)
        t_dates, t_grades = self._find_dates_grades(self.trad)
        all_dates = s_dates + t_dates
        self.dates = sorted(set(all_dates))
        self.s_grade_dict = self._build_summary_dict(self.dates, s_grades, 
            self.sport)
        t_grade_dict_temp = self._build_summary_dict(self.dates, 
            trad_grade_order, self.trad)
        self.t_grade_dict = self._rationalise_summary_dict(t_grade_dict_temp)

    def _find_dates_grades(self, climb_list):
        '''find out what the dates and grades are for sport climbs'''
        grades, dates = [], []
        count = 0
        for climb in range(0, len(climb_list)):
            date = climb_list[count][0]
            dates.append(date)
            grade = climb_list[count][1]
            grades.append(grade)
            count += 1
        grade_set = sorted(set(grades))
        date_set = sorted(set(dates))
        return date_set, grade_set

    def _build_summary_dict(self, dates, grades, climbs):
        '''create a dictionary of lists, each filled with number of climbs 
        climbed at each grade for each date'''
        c_grade_dict = {}
        for item in range(0, len(grades)):
            c_grade_dict[grades[item]] = []

        date_count = 0
        for date in range(0, len(dates)):
            for key in c_grade_dict:
                c_grade_dict[key].append(0)
            for climb in range(0, len(climbs)):
                if climbs[climb][0] == dates[date_count]:
                    for key in c_grade_dict:
                        if climbs[climb][1] == key:
                            c_grade_dict[key][date_count] += 1
            date_count += 1
        return c_grade_dict

    def _rationalise_summary_dict(self, climb_summary):
        '''remove grades that haven't been climbed from the dictionary'''
        empty_grades = []
        for key, c_list in climb_summary.items():
            total = 0
            for number in range(0, len(c_list)):
                total = total + c_list[number]
            if total == 0:
                empty_grades.append(key)
        while empty_grades:
            key = empty_grades.pop()
            del climb_summary[key]
        return climb_summary

    def visualise_climbs(self):
        '''visualise climbs'''
        fig = make_subplots(rows=2, cols=1)
        counter = 30
        x = self.dates
        for key in self.s_grade_dict:
            fig.add_trace(go.Bar(x=x, y=self.s_grade_dict[key], name=key, 
                marker_color = f'rgb(190, {counter}, 30)'), row=2, col=1)
            counter += 30
        for key in self.t_grade_dict:
            fig.add_trace(go.Bar(x=x, y=self.t_grade_dict[key], name=key), 
                row=1, col=1)
        fig.update_layout(barmode='stack', 
            title_text='Clean Trad and Sport Leads')
        fig.show()
