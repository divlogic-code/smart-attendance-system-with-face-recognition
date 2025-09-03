TIMETABLE = {
    ('Monday', 9): 'DAA',
    ('Monday', 10): 'ECO',
    ('Monday', 11): 'COA',
    ('Monday', 12): 'DM',
    ('Monday', 13): 'DAA LAB',
    ('Monday', 14): 'DAA LAB',
    ('Monday', 15): 'COA LAB',

    ('Tuesday', 9): 'PROJECT LAB',
    ('Tuesday', 10): 'PROJECT LAB',
    ('Tuesday', 11): 'OS',
    ('Tuesday', 12): 'ECO',
    ('Tuesday', 13): 'COA LAB',
    ('Tuesday', 14): 'COA LAB',

    ('Wednesday', 9): 'COA',
    ('Wednesday', 10): 'EVS',
    ('Wednesday', 11): 'OS',
    ('Wednesday', 12): 'ECO',
    ('Wednesday', 13): 'DM',
    ('Wednesday', 14): 'DAA',
    ('Wednesday', 15): 'EVS',

    ('Thursday', 9): 'DAA',
    ('Thursday', 10): 'COA',
    ('Thursday', 11): 'COA LAB',
    ('Thursday', 12): 'COA LAB',
    ('Thursday', 13): 'PROJECT LAB',
    ('Thursday', 14): 'PROJECT LAB',

    ('Friday', 9): 'DAA LAB',
    ('Friday', 10): 'OS LAB',
    ('Friday', 11): 'DM',
    ('Friday', 12): 'OS',
    ('Friday', 13): 'DM',
    ('Friday', 14): 'SPORTS',
    ('Friday', 15): 'OS LAB',
}

def get_current_subject():
    import datetime
    now = datetime.datetime.now()
    day = now.strftime('%A')      
    hour = now.hour               

    return TIMETABLE.get((day, hour))
