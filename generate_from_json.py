import sys
import sqlite3
import json
import random
from pathlib import Path


if __name__=="__main__":

    # Get json file
    with open(sys.argv[1]) as f:
        config_dict = json.load(f)

    # Check that new database is not already in use and create it
    db_filename = config_dict['filename']
    if Path(db_filename).is_file():
        raise ValueError("I refuse to overwrite an existing db file: "+db_filename)
    production_db = sqlite3.connect(db_filename)
    prod_cur = production_db.cursor()

    # Clone structure from template databse
    template_db = sqlite3.connect("protodb.sqlite")
    template_db.backup(production_db)
    template_db.close()

    # Generate PDU Table
    pduspec = config_dict['pduspec']
    if pduspec['type'] == "manual": # I don't have another option yet
        QUERY="INSERT INTO pdus VALUES"
        for i,name in enumerate(pduspec['pdus']):
             ip1 = i+1
             QUERY+=f" ({ip1},\"{name}\"),"
        QUERY=QUERY[:-1]+";"
        prod_cur.execute(QUERY)
        production_db.commit()

    # Generate node types and nodes
    # Kluges and shortcuts aplenty
    # W-T-Fs and "Oh, no!"s galore
    # Syntax errors, I've got twenty
    # But who cares, no big deal, I wrote more!
    types = config_dict['nodespec']['types']
    QUERY="INSERT INTO node_types VALUES"
    for i,name in enumerate(types):
        ip1 = i+1
        QUERY+=f" ({ip1},\"{name}\"),"
    QUERY=QUERY[:-1]+";"
    prod_cur.execute(QUERY)
    production_db.commit()

    pdu_counters = [0]*len(pduspec['pdus'])
    nodecounter=1

    QUERY="INSERT INTO nodes VALUES"
    for nodeset in config_dict['nodespec']['nodesets']:
        n = nodeset['n']

        for i in range(n):
            ip1 = i+1
            if nodeset['naming'] == 'type_seq': #Again, no alternative"
                name=config_dict['nodespec']['types'][nodeset['type']-1]+f"-{ip1}"
            if nodeset['location'] == 'random': #Again, did I give you a choice?"
                pduid=random.randint(1,len(pduspec['pdus']))
                pdu_counters[pduid-1]+=1
                outlet=pdu_counters[pduid-1]
            QUERY+=f" ({nodecounter},{nodeset['type']},\"{name}\",{pduid},{outlet}),"
            nodecounter+=1

    QUERY=QUERY[:-1]+";"
    prod_cur.execute(QUERY)
    production_db.commit()


    production_db.close()
