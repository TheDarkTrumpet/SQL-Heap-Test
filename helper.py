import random
import uuid
import pandas as pd
import itertools
from multiprocessing import Pool
from essential_generators import DocumentGenerator
import time
from sqlalchemy.sql import text
import sqlalchemy as sa


insertedValues = {}
gen = DocumentGenerator()


def generateChunk(arg):
    maxRecords, maxInt = arg
    toInsert = {
        "intColumn": [],
        "md5": [],
        "string": []
    }

    for x in range(maxRecords):
        md = uuid.uuid4().hex
        intValue = random.randint(0, maxInt)
        if intValue in insertedValues:
           continue
        insertedValues[intValue] = None
        randString = gen.gen_sentence()

        toInsert["intColumn"].append(intValue)
        toInsert["md5"].append(md)
        toInsert["string"].append(randString)

    pdToInsert = pd.DataFrame.from_dict(toInsert, orient='columns')
    return pdToInsert


def generateRecords(maxRecords: int):
    numProcesses = 8
    maxInt = maxRecords * 200

    rangeMap = list(itertools.repeat((int(maxRecords / numProcesses), maxInt), numProcesses))
    with Pool(processes=numProcesses) as pool:
        # process_pool = Pool(processes=numProcesses)
        dfs = pool.map(generateChunk, rangeMap)
    pdToInsert = pd.concat(dfs, ignore_index=True, axis=0)

    return pdToInsert


def executeScript(eng: sa.engine.Engine, file: str):
    with eng.connect() as con:
        with open(file) as sql_file:
            sql_command = ''
            # Iterate over all lines in the sql file
            for line in sql_file:
                # Ignore commented lines
                if not line.startswith('--') and line.strip('\n'):
                    # Append line to the command string
                    sql_command += line.strip('\n')

                    # If the command string ends with ';', it is a full statement
                    if sql_command.endswith(';'):
                        # Try to execute statement and commit it
                        try:
                            con.execute(text(sql_command))
                        # Assert in case of error
                        except Exception as e:
                            print(f"Exception raised: {e}")
                        # Finally, clear command string
                        finally:
                            sql_command = ''


def addRecords(maxRecords: int, connection: sa.engine.Connection):
    pdToInsert = generateRecords(maxRecords)
    pdToInsert.to_sql("testTable", con=connection, if_exists='append', chunksize=1000, index=False)
    print(f"Number of records attempted to be inserted: {maxRecords}")


def timeInstance(func):
    tic = time.perf_counter()
    func()
    toc = time.perf_counter()
    duration = f"{toc-tic:0.4f}"
    print(f"Completed in {duration} seconds")
    return duration

