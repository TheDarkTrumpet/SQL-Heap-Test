import random
import uuid
import pandas as pd
import itertools
from multiprocessing import Pool
from essential_generators import DocumentGenerator

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


