from logbook_5_build_data import BuildData

filename = 'ukc_logbook.csv'
climbs = BuildData(filename)
climbs.get_data()
climbs.categorise_climbs()
climbs.rationalise_trad_grades()
climbs.build_visuals()
climbs.visualise_climbs()
