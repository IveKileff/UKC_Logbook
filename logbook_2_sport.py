import csv

from datetime import datetime

import plotly.graph_objects as go

def get_data():
    '''open the logbook file and set variables based on file structure'''
    filename = 'ukc_logbook.csv'
    with open(filename) as f:
        reader = csv.reader(f)
        header_row = next(reader)
        for index, header in enumerate(header_row):
            if header == 'Date':
                date_index = index
            elif header == 'Grade':
                grade_index = index
            elif header == 'Style':
                style_index = index

        # get dates, grades and style for all routes from the file
        data = []
        for row in reader:
            date = datetime.strptime(row[date_index][3:], '%b/%y')
            grade = row[grade_index].replace("*", "").strip()
            style = row[style_index]
            row_data = [date, grade, style]
            data.append(row_data)
        data.sort()
        return data

def categorise_climbs(data):
    '''categorise climbs using Style, and extract only Lead climbs'''
    sport, boulder, trad, others = [], [], [], []
    numbers = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
    letters = ['D', 'E', 'H', 'M', 'S', 'V']
    while data:
        climb = data.pop()
        grade = climb[1]
        style = climb[2] 
        if grade[0] in numbers and style[0:4] == 'Lead':
            sport.append(climb)
        elif grade[0] in letters and style[0:4] == 'Lead':
            trad.append(climb)
        # elif grade[0] == 'f':
        #     boulder.append(climb)
        else:
            others.append(climb)
    return sport, trad

def find_dates_grades(subtable):
    '''find out what the dates and grades are for sport climbs'''
    sport_climbs = subtable[:]
    grades, dates = [], []
    count = 0
    for climb in range(0, len(sport_climbs)):
        date = sport_climbs[count][0]
        dates.append(date)
        grade = sport_climbs[count][1]
        grades.append(grade)
        count += 1
    grade_set = sorted(set(grades))
    date_set = sorted(set(dates))
    return date_set, grade_set

def build_summary_dict(dates, grades, climbs):
    '''create a dictionary of lists, each filled with number of climbs climbed 
    at each grade for each date'''
    s_dates = dates[:]
    s_grades = grades[:]
    sport = climbs[:]
    s_grade_dict = {}
    for item in range(0, len(s_grades)):
        s_grade_dict[s_grades[item]] = []

    date_count = 0
    for date in range(0, len(s_dates)):
        for key in s_grade_dict:
            s_grade_dict[key].append(0)
        for climb in range(0, len(sport)):
            if sport[climb][0] == s_dates[date_count]:
                for key in s_grade_dict:
                    if sport[climb][1] == key:
                        s_grade_dict[key][date_count] += 1
        date_count += 1
    return s_grade_dict

data = get_data()
sport, trad = categorise_climbs(data)
s_dates, s_grades = find_dates_grades(sport)
t_dates, t_grades = find_dates_grades(trad)
s_grade_dict = build_summary_dict(s_dates, s_grades, sport)

# visualise sport climbs
counter = 30
x = s_dates
y = s_grade_dict['3a']
fig = go.Figure(go.Bar(x =x, y=y, name='3a', marker_color = 'rgb(130, 0, 130)'))
for key in s_grade_dict:
    if key == '3a':
        continue
    fig.add_trace(go.Bar(x=x, y=s_grade_dict[key], name=key, 
        marker_color = f'rgb(130, {counter}, 130)'))
    counter += 30
    # fig.add_trace(go.Bar(x=x, y=s_grade_dict['4c'], name='4c', 
    #     marker_color = 'rgb(130, 60, 130)'))
    # fig.add_trace(go.Bar(x=x, y=s_grade_dict['5a'], name='5a', 
    #     marker_color = 'rgb(130, 90, 130)'))
    # fig.add_trace(go.Bar(x=x, y=s_grade_dict['5b'], name='5b', 
    #     marker_color = 'rgb(130, 120, 130)'))
    # fig.add_trace(go.Bar(x=x, y=s_grade_dict['5c'], name='5c', 
    #     marker_color = 'rgb(130, 150, 130)'))
    # fig.add_trace(go.Bar(x=x, y=s_grade_dict['6a'], name='6a', 
    #     marker_color = 'rgb(130, 180, 130)'))
    # fig.add_trace(go.Bar(x=x, y=s_grade_dict['6a+'], name='6a+', 
    #     marker_color = 'rgb(130, 210, 130)'))
fig.update_layout(barmode='stack', title_text='Sport Routes')
fig.show()