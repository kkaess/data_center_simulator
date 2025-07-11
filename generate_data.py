import sys
import random
import sqlite3
from UsageModel import UsageModel
from NodeModel import NodeModel

if __name__=="__main__":
    # Pull parameters
    datapoints = int(sys.argv[2])
    timestamp = int(sys.argv[3])
    conn = sqlite3.connect(sys.argv[1])
    cur = conn.cursor()

    # Set up cpu models
    # This could be set up via a config file, but today I'm just hard-coding it.
    linear_model_1 = NodeModel(lambda x : 0.5 + 1.5*x)
    linear_model_2 = NodeModel(lambda x : 1.25 + 0.75*x)
    quadratic_model = NodeModel(lambda x : 0.75 + 1.25*x**2)
    flat_model = NodeModel(lambda x : 2)
    free_energy_model = NodeModel(lambda x : -2*x)

    node_models = [linear_model_1,linear_model_2,quadratic_model,flat_model,free_energy_model]

    # Set up usage models (i.e., cpu frequency distributions
    flat_usage_model = UsageModel(random.random) # Going to use this for all nodes

    # Use the data I created, because flexibility
    nodedata = cur.execute("SELECT * FROM nodes;").fetchall()
    pdudata = cur.execute("SELECT * FROM pdus;").fetchall()

    npdus = len(pdudata) # Kluge, going to assume 1-indexed continuous
    #
    for i in range(datapoints):
        pdu_totals = [0]*npdus
        for node in nodedata:
            usage=flat_usage_model.cast()
            intusage=int(round(usage*100))
            deciamps = int(round(10*node_models[node[1]-1].get_power(usage)))
            QUERY=f"INSERT INTO cpu_measurements VALUES ({timestamp},{node[0]},{intusage});"
            cur.execute(QUERY)
            pdu_totals[node[3]-1]+=deciamps
        conn.commit()
        QUERY=f"INSERT INTO pdu_measurements VALUES"
        for i, pdu_total in enumerate(pdu_totals):
            QUERY+=f" ({timestamp},{i+1},1,{pdu_total}),"
        QUERY=QUERY[:-1]+";"
        cur.execute(QUERY)
        conn.commit()
        timestamp=timestamp+300

    conn.close()
