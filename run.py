from matching.matching import Matcher, load_segments
import apsw

DB_FILE = 'results.db'
connection = apsw.Connection(DB_FILE)
cursor = connection.cursor()

def get_next_session():
    # Find next unmatched session row in db
    cur = cursor.execute('SELECT sessionid, proceedingsfile, transcriptionfile ' +
                         'FROM session WHERE matched = 0 LIMIT 1')
    for sessionid, proc_file, asr_file in cur:
        return (sessionid, proc_file, asr_file)
    return None

def run_match(sessionid, proceedings, transcriptions):
    segment_ids = []
    cur = cursor.execute('SELECT segmentid FROM segment '
                         'WHERE sessionid = %d' % sessionid)
    for row in cur:
        segment_ids.append(row[0])

    # Remove scores from possible previous interrupted run
    cursor.execute('DELETE FROM score WHERE segmentid IN (%s)' %
                   ','.join(map(str, segment_ids)))

    print('Loading session %d (%s)' % (sessionid, proceedings))
    matcher = Matcher(proceedings)
    segments = load_segments(transcriptions)

    print('Matching for bokmål...')
    positions = matcher.match(segments)
    matches = matcher.get_matches(positions)

    print('Inserting results')
    for index, match in enumerate(matches):
        cursor.execute('INSERT INTO score VALUES(?,?,?,?,?)',
                       (segment_ids[index], match['ratio'], 'bm',
                        match['corpus_start'], match['corpus_end']))

    print('Matching for nynorsk...')
    positions = matcher.match(segments, bm=False)
    matches = matcher.get_matches(positions, bm=False)

    print('Inserting results')
    for index, match in enumerate(matches):
        cursor.execute('INSERT INTO score VALUES(?,?,?,?,?)',
                       (segment_ids[index], match['ratio'], 'nn',
                        match['corpus_start'], match['corpus_end']))

    # Flag session as matched
    cursor.execute("UPDATE session SET matched=1 WHERE sessionid = %d" % sessionid)

while True:
    session = get_next_session()
    if not session:
        break
    run_match(*session)

connection.close()
