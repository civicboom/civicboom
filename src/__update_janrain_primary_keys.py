import os
import json

from civicboom.lib.services.janrain import janrain
import psycopg2

conn = psycopg2.connect("host=dbw.civicboom.com dbname=civicboom user=civicboom pass=Eev3fair")
cur = conn.cursor()

# -- Variables --

apiKey = '2f93094487a2e2af9f60725670e8cbd5bdc9fe8a'

janrain_mappings_filename = 'janrain_idents.json'


# -- Subs --

def get_username_from_id(id):
    """
    Placeholder for code to looking username from id
    """
    return cur.execute("SELECT id FROM member WHERE id_num=%s;", (int(id), )).fetchone()[0]


# -- Main --

if os.path.exists(janrain_mappings_filename):
    print "Loading %s" % janrain_mappings_filename
    mappings = json.loads(open(janrain_mappings_filename, 'r').read())
else:
    print "Loading from Janrain"
    mappings = janrain('all_mappings',apiKey=apiKey)['mappings']   # Get all ident mappings from janrain
    file(janrain_mappings_filename, "w").write(json.dumps(mappings)) # Backup idents, just in case

# Remap old primary key 'id' to new primary key 'username'
for id, identifiers in mappings.iteritems():
    username = get_username_from_id(id)
    print "remaping %s to %s" % (id, username)
    for identifier in identifiers:
        #janrain('map',  identifier=identifier, primaryKey=username, apiKey=apiKey) # By default will overwrite existing identifiers so we dont need to explicity call unmap
        pass

