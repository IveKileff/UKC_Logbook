import csv

from datetime import datetime

import plotly.graph_objects as go

from plotly.subplots import make_subplots

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

        # get dates, grades and style for all routes from the file & clean data
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
        if grade[0] in numbers and (
            (style[0:4] == 'Lead' and style[0:6] != 'Lead d') or (
                style[0:5] == 'AltLd' and style[0:7] != 'AltLd d')):
            sport.append(climb)
        elif grade[0] in letters and (
            (style[0:4] == 'Lead' and style[0:6] != 'Lead d') or (
                style[0:5] == 'AltLd' and style[0:7] != 'AltLd d')):
            trad.append(climb)
        # elif grade[0] == 'f':
        #     boulder.append(climb)
        # else:
        #     others.append(climb)
    return sport, trad

def rationalise_trad_grades(climbs):
    for index in range(0, len(climbs)):
        if climbs[index][1][0:2] == 'MS':
            climbs[index][1] = 'S'
        elif climbs[index][1][0:3] == 'MVS':
            climbs[index][1] = 'HS'
        elif climbs[index][1][0:2] == 'HS':
            climbs[index][1] = 'HS'
        elif climbs[index][1][0:3] == 'HVD':
            climbs[index][1] = 'HVD'
        elif climbs[index][1][0:3] == 'HVS':
            climbs[index][1] = 'HVS'
        elif climbs[index][1][0:1] == 'S':
            climbs[index][1] = 'S'
        elif climbs[index][1][0:2] == 'VS':
            climbs[index][1] = 'VS'
        elif climbs[index][1][0:2] == 'E1':
            climbs[index][1] = 'E1'
        elif climbs[index][1][0:2] == 'E2':
            climbs[index][1] = 'E2'
        elif climbs[index][1][0:2] == 'E3':
            climbs[index][1] = 'E3'
        elif climbs[index][1][0:2] == 'E4':
            climbs[index][1] = 'E4'
        elif climbs[index][1][0:2] == 'E5':
            climbs[index][1] = 'E5'
        elif climbs[index][1][0:2] == 'E6':
            climbs[index][1] = 'E6'
        elif climbs[index][1][0:2] == 'E7':
            climbs[index][1] = 'E7'
        elif climbs[index][1][0:2] == 'E8':
            climbs[index][1] = 'E8'
        elif climbs[index][1][0:2] == 'E9':
            climbs[index][1] = 'E9'
        elif climbs[index][1][0:3] == 'E10':
            climbs[index][1] = 'E10'
    return climbs

def find_dates_grades(climb_list):
    '''find out what the dates and grades are for sport climbs'''
    climbs = climb_list[:]
    grades, dates = [], []
    count = 0
    for climb in range(0, len(climbs)):
        date = climbs[count][0]
        dates.append(date)
        grade = climbs[count][1]
        grades.append(grade)
        count += 1
    grade_set = sorted(set(grades))
    date_set = sorted(set(dates))
    return date_set, grade_set

def combine_dates(sport_dates, trad_dates):
    all_dates = sport_dates + trad_dates
    dates = sorted(set(all_dates))
    return dates

def build_summary_dict(dates, grades, climbs):
    '''create a dictionary of lists, each filled with number of climbs climbed 
    at each grade for each date'''
    c_dates = dates[:]
    c_grades = grades[:]
    c_climbs = climbs[:]
    c_grade_dict = {}
    for item in range(0, len(c_grades)):
        c_grade_dict[c_grades[item]] = []

    date_count = 0
    for date in range(0, len(c_dates)):
        for key in c_grade_dict:
            c_grade_dict[key].append(0)
        for climb in range(0, len(c_climbs)):
            if c_climbs[climb][0] == c_dates[date_count]:
                for key in c_grade_dict:
                    if c_climbs[climb][1] == key:
                        c_grade_dict[key][date_count] += 1
        date_count += 1
    return c_grade_dict

def rationalise_summary_dict(climb_summary):
    # print(climb_summary)
    empty_grades = []
    for key, c_list in climb_summary.items():
        total = 0
        for number in range(0, len(c_list)):
            total = total + c_list[number]
        # print(f"{key}: {total}")
        if total == 0:
            empty_grades.append(key)
    while empty_grades:
        key = empty_grades.pop()
        del climb_summary[key]
    return climb_summary

trad_grade_order = ['D', 'VD', 'HVD', 'S', 'HS', 'VS', 'HVS', 'E1', 'E2', 'E3',
'E4', 'E5', 'E6', 'E7', 'E8', 'E9', 'E10']

data = get_data()
sport, trad = categorise_climbs(data)
r_trad = rationalise_trad_grades(trad)
s_dates, s_grades = find_dates_grades(sport)
t_dates, t_grades = find_dates_grades(r_trad)
dates = combine_dates(s_dates, t_dates)
s_grade_dict = build_summary_dict(dates, s_grades, sport)
t_grade_dict_temp = build_summary_dict(dates, trad_grade_order, r_trad)
t_grade_dict = rationalise_summary_dict(t_grade_dict_temp)

# visualise climbs
fig = make_subplots(rows=2, cols=1)

counter = 30
x = dates
for key in s_grade_dict:
    fig.add_trace(go.Bar(x=x, y=s_grade_dict[key], name=key, 
        marker_color = f'rgb(190, {counter}, 30)'), row=2, col=1)
    counter += 30

for key in t_grade_dict:
    fig.add_trace(go.Bar(x=x, y=t_grade_dict[key], name=key), row=1, col=1)

fig.update_layout(barmode='stack', title_text='Clean Trad and Sport Leads')

fig.show()