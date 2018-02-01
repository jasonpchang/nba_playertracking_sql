############################################
# load_movement_mod.py
#    add nba player movement data
###########################################


#################################
# imports
#################################
import json
import urllib



##################################
# initialize tables in database
##################################
def movement_init(hdb):
  # game details:
  # game id, game date, visiting team id, home team id
  comm = """CREATE TABLE games (game_id INTEGER, date INTEGER, home_id INTEGER, visit_id INTEGER, UNIQUE(game_id))"""
  hdb.execute(comm)

  # team details
  # team id, team name
  comm = """CREATE TABLE teams (team_id INTEGER, team_name TEXT, team_abbr TEXT, UNIQUE(team_id))"""
  hdb.execute(comm)

  # player details
  # player id, player first, player last, jersey, team_id
  comm = """CREATE TABLE players (player_id INTEGER, player_first TEXT, player_last TEXT, position TEXT, jersey INTEGER, team_id INTEGER, UNIQUE(player_id,team_id))"""
  hdb.execute(comm)

  # movements
  # game_id, event_id, period, game time, shot clock time, team_id, player_id, locx, locy, locz
  comm = """CREATE TABLE movements (game_id INTEGER, event_id INTEGER, period INTEGER, game_time REAL, shot_time REAL, team_id INTEGER, player_id INTEGER, player_x REAL, player_y REAL, player_z REAL, UNIQUE(game_id,event_id,player_id))"""
  hdb.execute(comm)



##################################
# add movement information
##################################
def movement_add_info(hdb,date1,date2,prompt):
  # initialize variables
  opts = [1,2]

  # if database is empty
  ddict = {}
  query = """SELECT min(date) FROM games"""
  hdb.execute(query)
  val = hdb.fetchone()[0]
  if val==None:
    year = str(date1)[:4]
    val = int('00%s%s%s00001' %(year[0],year[2],year[3]))
    gid_start = val
    date_end  = date2
  else:
    # grab existing dates and associated game ids in database
    query = """SELECT date,game_id FROM games"""
    for output in hdb.execute(query):
      date = output[0]
      gid  = int(output[1])
      if date in ddict:
        ddict[date].append(gid)
      else:
        ddict[date] = []
        ddict[date].append(gid)
    dbmin = min(ddict)
    dbmax = max(ddict)

    # if both dates are less than the minimum date
    if (date2 < dbmin):
      # start from first game of that year
      year = str(date1)[:4]
      val = int('00%s%s%s00001' %(year[0],year[2],year[3]))
      gid_start = val
      date_end = date2
    # if both dates are greater than the maximum date
    elif (date1 > dbmax):
      # start at game+1 in database
      val = int(max(ddict[dbmax]))+1
      gid_start = val
      date_end = date2
    # else find lastest game_id given date
    else:
      # initialize some sort of game_id
      year = str(date1)[:4]
      val = int('00%s%s%s00001' %(year[0],year[2],year[3]))
      # find latest game_id possible given start date
      for ddate in sorted(ddict):
        if ddate <= date1:
          gid = int(max(ddict[ddate]))
          if (gid > val):
	        # INDENT ADDED HERE TO GET IT TO WORK
            val = gid+1
      gid_start = val
      date_end = date2

  # set initial game count
  gcount = gid_start
  # loop until end date reached
  while True:
    # check if game exists
    try:
      url = 'http://stats.nba.com/stats/locations_getmoments/?eventid=1&gameid=%s' %(str(gcount).zfill(10))
      jsonurl = urllib.urlopen(url)
      pdict = json.loads(jsonurl.read())
    except:
      year = str(date2)[:4]
      gcount = int('00%s%s%s00001' %(year[0],year[2],year[3]))
      url = 'http://stats.nba.com/stats/locations_getmoments/?eventid=1&gameid=%s' %(str(gcount).zfill(10))
      jsonurl = urllib.urlopen(url)
      pdict = json.loads(jsonurl.read())
      
    # check game date and whether to keep going
    gdate = int(pdict['gamedate'].replace('-',''))
    flag = False
    # check if game id already in dictionary
    for dgame in ddict.values():
      if gcount in dgame:
        gcount += 1
        flag = True
        break
    if flag is True:
      continue
    # skip if game number is too early
    if gdate<date1:
      gcount += 1
      continue
    # if past end date, then break out
    if (gdate > date_end):
      break
    # check statement
    print "Adding game: %s" %(gcount)

    # fill in game info
    gid = int(pdict['gameid'])
    hid = pdict['home']['teamid']
    vid = pdict['visitor']['teamid']
    info   = (gid,gdate,hid,vid)
    insert = """INSERT OR IGNORE INTO games VALUES (?,?,?,?)"""
    hdb.execute(insert,info)

    # fill in team info
    hname = pdict['home']['name']
    habbr = pdict['home']['abbreviation']
    info   = (hid,hname,habbr)
    insert = """INSERT OR IGNORE INTO teams VALUES (?,?,?)"""
    hdb.execute(insert,info)
    vname = pdict['visitor']['name']
    vabbr = pdict['visitor']['abbreviation']
    info   = (vid,vname,vabbr)
    insert = """INSERT OR IGNORE INTO teams VALUES (?,?,?)"""
    hdb.execute(insert,info)

    # fill in player info
    # home team
    for players in pdict['home']['players']:
      pid     = players['playerid']
      pfirst  = players['firstname']
      plast   = players['lastname']
      ppos    = players['position']
      pjersey = players['jersey']
      info   = (pid,pfirst,plast,ppos,pjersey,hid)
      insert = """INSERT OR IGNORE INTO players VALUES (?,?,?,?,?,?)"""
      hdb.execute(insert,info)
    # visting team
    for players in pdict['visitor']['players']:
      pid     = players['playerid']
      pfirst  = players['firstname']
      plast   = players['lastname']
      ppos    = players['position']
      pjersey = players['jersey']
      info   = (pid,pfirst,plast,ppos,pjersey,vid)
      insert = """INSERT OR IGNORE INTO players VALUES (?,?,?,?,?,?)"""
      hdb.execute(insert,info)

    ### CHECKPOINT 1 ###
    #for row in hdb.execute('SELECT * FROM players ORDER BY player_last'):
    #  print row

    # set event parameters
    gap = 20
    gapcount = 0
    ecount = 1

    # loop over events until large gap in event id
    while gapcount<gap:
      try:
        url = 'http://stats.nba.com/stats/locations_getmoments/?eventid=%s&gameid=%s' %(ecount,str(gcount).zfill(10))
        jsonurl = urllib.urlopen(url)
        pdict = json.loads(jsonurl.read())
      except:
        gapcount += 1
        ecount   += 1
        continue
      # check for malfunctions
      if ('moments' not in pdict):
        ecount   += 1
        continue
      # checkpoint statement
      print "Adding event: %s" %(ecount)

      # fill in play info
      molen = len(pdict['moments'])
      for step in range(molen):
        movement = pdict['moments'][step]
        # ignore if not 11 entries
        nobj = len(movement[5])
        if (nobj != 11):
          continue
        # event info
        eid      = movement[1]
        # game info
        period   = movement[0]
        gtime    = movement[2]
        stime    = movement[3]
        # ball info
        ballx    = movement[5][0][2]
        bally    = movement[5][0][3]
        ballz    = movement[5][0][4]
        info     = (gid,eid,period,gtime,stime,-1,-1,ballx,bally,ballz)
        insert   = """INSERT OR IGNORE INTO movements VALUES (?,?,?,?,?,?,?,?,?,?)"""
        hdb.execute(insert,info)
        # player info
        nplayers = len(movement[5])-1
        for player in range(1,nplayers+1):
          tid     = movement[5][player][0]
          pid     = movement[5][player][1]
          playerx = movement[5][player][2]
          playery = movement[5][player][3]
          playerz = movement[5][player][4]
          info    = (gid,eid,period,gtime,stime,tid,pid,playerx,playery,playerz)
          insert  = """INSERT OR IGNORE INTO movements VALUES (?,?,?,?,?,?,?,?,?,?)"""
          hdb.execute(insert,info)
      # update event count and reset gap counts
      gapcount = 0
      ecount += 1


    # update game count
    print "Completed game %s" %(gcount)
    gcount += 1
    if (prompt is True):
      # prompt for whether to continue
      print "==================================="
      print "Would you like to add next game:"
      print "  (01) Yes"
      print "  (02) No"
      print "==================================="
      opt = int(raw_input('Select option: '))
      while (opt not in opts):
        opt = int(raw_input('Choose option that exists: '))
      print "==================================="
      if (opt==2):
        break
