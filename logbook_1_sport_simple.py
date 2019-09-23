import csv

from datetime import datetime

import plotly.graph_objects as go

# open the file and set variables based on structure
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
        date = row[date_index]
        grade = row[grade_index].replace("*", "").strip()
        style = row[style_index]
        row_data = [date, grade, style]
        data.append(row_data)

    # categorise climbs using Style to distinguish them, 
    # only extracting Lead climbs
    sport, boulder, trad, others = [], [], [], []
    numbers = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
    letters = ['D', 'E', 'H', 'M', 'S', 'V']
    while data:
        climb = data.pop()
        grade = climb[1]
        style = climb[2] 
        if grade[0] in numbers and style[0:4] == 'Lead':
            sport.append(climb)
        elif grade[0] == 'f':
            boulder.append(climb)
        elif grade[0] in letters and style[0:4] == 'Lead':
            trad.append(climb)
        else:
            others.append(climb)

    # find out what the dates and grades are
    sport_climbs = sport[:]
    grades, v_dates = [], []
    count = 0
    for climb in range(0, len(sport_climbs)):
        date = sport_climbs[count][0]
        v_dates.append(date)
        grade = sport_climbs[count][1]
        grades.append(grade)
        count += 1
    grade_set = sorted(set(grades))
    date_set = list(set(v_dates))
    print(grade_set)
    print(f"number of dates: {len(date_set)}")

    # make lists for a subset of grades
    five_a, five_b, five_c, six_a, six_a_plus = [], [], [], [], []
    
    date_count = 0
    for date in range(0, len(date_set)):
        five_a.append(0)
        five_b.append(0)
        five_c.append(0)
        six_a.append(0)
        for climb in range(0, len(sport_climbs)):
            if sport_climbs[climb][0] == date_set[date_count]:
                if sport_climbs[climb][1] == '5a':
                    sum_so_far = five_a[date_count]
                    five_a[date_count] = sum_so_far + 1
                elif sport_climbs[climb][1] == '5b':
                    sum_so_far = five_b[date_count]
                    five_b[date_count] = sum_so_far + 1
                elif sport_climbs[climb][1] == '5c':
                    sum_so_far = five_c[date_count]
                    five_c[date_count] = sum_so_far + 1
                elif sport_climbs[climb][1] == '6a':
                    sum_so_far = six_a[date_count]
                    six_a[date_count] = sum_so_far + 1
        date_count += 1
    print(date_set)
    print(five_a)
    print(five_b)
    print(five_c)
    print(six_a)

    # # visualise sport climbs
    x = date_set
    y = five_a
    fig = go.Figure(go.Bar(x =x, y=y, name='5a'))
    fig.add_trace(go.Bar(x=x, y=five_b, name='5b'))
    fig.add_trace(go.Bar(x=x, y=five_c, name='5c'))
    fig.add_trace(go.Bar(x=x, y=six_a, name='6a'))
    fig.update_layout(barmode='stack')
    fig.show()

