import glob
import apsw
import json
import sys

connection = apsw.Connection(sys.argv[1])
cursor = connection.cursor()

cursor.execute("DROP TABLE IF EXISTS session")
cursor.execute("DROP TABLE IF EXISTS segment")
cursor.execute("DROP TABLE IF EXISTS score")

cursor.execute("""
CREATE TABLE session(
  sessionid         INTEGER PRIMARY KEY,
  proceedingsfile   TEXT,
  transcriptionfile TEXT
)""")

cursor.execute("""
CREATE TABLE segment(
  segmentid     INTEGER PRIMARY KEY, -- unique segment id
  sessionid     INT,                 -- same as in session table
  segmentindex  INT,                 -- segment index in session
  audiofilename TEXT,
  duration      REAL
)""")

cursor.execute("""
CREATE TABLE score(
  segmentid INT,
  run       INT,
  score     REAL,
  language  TEXT
)""")

proceedings = glob.glob('data/proceedings/*.txt')
segments = glob.glob('data/transcriptions/json/*.json')

sessionid = 0
for proc in proceedings:
    date = proc.split('/')[-1][:10]
    segs = [ s for s in segments if date in s ]
    if len(segs) != 1:
        print("Error with ", proc)
    print("saving session %s..." % date)

    c = cursor.execute("INSERT INTO session(sessionid, proceedingsfile, transcriptionfile) VALUES(?,?,?)",
                       (sessionid, proc, segs[0]))
    sessionid += 1

    segmentindex = 0
    with open(segs[0]) as f:
        for l in f:
            data = json.loads(l)
            cursor.execute("INSERT INTO segment(sessionid, segmentindex, audiofilename, duration) VALUES(?,?,?,?)",
                           (sessionid, segmentindex, data['file'], data['duration']))
            segmentindex += 1
    print("\t%d segments saved" % segmentindex)

connection.close()
