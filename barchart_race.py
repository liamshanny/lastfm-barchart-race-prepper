import csv
from collections import defaultdict
import arrow


def prepare_csv(filename):
    """
    Make sure the header of the csv is the following:
    artist, album, track, date
    artist and date being the actual important ones
    If arrow is failing to parse the date, use excel to format it all to
    YYYY-MM-DD, and remove the 'M/D/YY H:mm' string from lines 19-20
    """
    working_list = []
    all_dates = ['artist']
    with open(filename, 'r') as _filehandler:
        csv_file_reader = csv.DictReader(_filehandler)
        for row in csv_file_reader:
            month = arrow.get(row['date'], 'M/D/YY H:mm').format('MMMM')
            year = arrow.get(row['date'], 'M/D/YY H:mm').format('YYYY')
            row['date'] = year + ' ' + month
            working_list.append(row)
            if row['date'] not in all_dates:
                all_dates.append(row['date'])

    list_with_id = []
    artist_id = 0
    artist_id_hash = defaultdict(int)
    for scrobble in working_list:
        if artist_id_hash.get(scrobble['artist']):
            scrobble['id'] = artist_id_hash[scrobble['artist']]
            list_with_id.append(scrobble)
            continue
        else:
            artist_id += 1
            artist_id_hash[scrobble['artist']] = artist_id
            scrobble['id'] = artist_id
            list_with_id.append(scrobble)

    artist_play_count = defaultdict(int)
    d = defaultdict(dict)
    for row in list_with_id:
        if d[row['artist']].get(row['date']):
            d[row['artist']][row['date']] += 1
        else:
            d[row['artist']][row['date']] = 1

    final_list = []
    for artist in d:
        new_row = {}
        new_row['artist'] = artist
        for date in d[artist]:
            artist_play_count[artist] += d[artist][date]
            new_row[date] = artist_play_count[artist]
        final_list.append(new_row)

    with open(filename + "-processed.csv", 'w') as f:
        w = csv.DictWriter(f, all_dates)
        w.writeheader()
        for each in final_list:
            w.writerow(each)

prepare_csv('lfshammu.csv')
