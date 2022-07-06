import pickle as pkl
import time
import helper
# from helper import ExecuteScript, AddRecords, TimeInstance, CreateEngine
import math

# User customizable stuff
server = "mssql.ad.tdt"
database = "sqlHeapTest"
numRecords = 20
#numRecords = 400000
#numRecords = 1500000
samplesToRun = 5


results = {
    "Test 1": {
        "Test": "Test 1",
        "Description": "One-Column, integer, Clustered Index Create",
        "Time (s)": [],
        "Category": "Cluster Add"
    },
    "Test 2": {
        "Test": "Test 2",
        "Description": "One-Column, integer, Clustered Index Delete",
        "Time (s)": [],
        "Category": "Cluster Drop"
    },
    "Test 3": {
        "Test": "Test 3",
        "Description": "One-Column, integer, Clustered Index Create - Extra Records",
        "Time (s)": [],
        "Category": "Cluster Add"
    },
    "Test 4": {
        "Test": "Test 4",
        "Description": "One-Column, integer, Clustered Index Delete - Extra Records",
        "Time (s)": [],
        "Category": "Cluster Drop"
    },
    "Test 5": {
        "Test": "Test 5",
        "Description": "Two-Column, Clustered Index Create",
        "Time (s)": [],
        "Category": "Cluster Add"
    },
    "Test 6": {
        "Test": "Test 6",
        "Description": "Two-Column, Clustered Index Delete",
        "Time (s)": [],
        "Category": "Cluster Drop"
    },
    "Test 7": {
        "Test": "Test 7",
        "Description": "Two-Column, Clustered Index Create - Extra Records",
        "Time (s)": [],
        "Category": "Cluster Add"
    },
    "Test 8": {
        "Test": "Test 8",
        "Description": "Two-Column, Clustered Index Delete - Extra Records",
        "Time (s)": [],
        "Category": "Cluster Drop"
    },
    "Test 9": {
        "Test": "Test 9",
        "Description": "Single-Column, Non-Clustered Index Create",
        "Time (s)": [],
        "Category": "Non-Cluster Add"
    },
    "Test 10": {
        "Test": "Test 10",
        "Description": "Single-Column, Non-Clustered Index Delete",
        "Time (s)": [],
        "Category": "Non-Cluster Delete"
    },
    "Test 11": {
        "Test": "Test 11",
        "Description": "Single-Column, Non-Clustered Index Create - Extra Records",
        "Time (s)": [],
        "Category": "Non-Cluster Add"
    },
    "Test 12": {
        "Test": "Test 12",
        "Description": "Single-Column, Non-Clustered Index Delete - Extra Records",
        "Time (s)": [],
        "Category": "Non-Cluster Delete"
    },
    "Test 13": {
        "Test": "Test 13",
        "Description": "Dual-Column, Non-Clustered Index Create",
        "Time (s)": [],
        "Category": "Non-Cluster Add"
    },
    "Test 14": {
        "Test": "Test 14",
        "Description": "Dual-Column, Non-Clustered Index Delete",
        "Time (s)": [],
        "Category": "Non-Cluster Delete"
    },
    "Test 15": {
        "Test": "Test 15",
        "Description": "Dual-Column, Non-Clustered Index Create - Extra Records",
        "Time (s)": [],
        "Category": "Non-Cluster Add"
    },
    "Test 16": {
        "Test": "Test 16",
        "Description": "Dual-Column, Non-Clustered Index Delete - Extra Records",
        "Time (s)": [],
        "Category": "Non-Cluster Delete"
    }
}


def setupDb():
    engine = helper.CreateEngine(server, autocommit=True)
    helper.ExecuteScript(engine, "setupDB.sql")


def addRecords(engine):
    with engine.connect() as conn:
        helper.AddRecords(numRecords, conn)


def appendToResults(label, result):
    if label not in results:
        raise KeyError(f"Label, {label} not in the results dictionary")
    else:
        results[label]["Time (s)"].append(result)


def runSamples(numToRun = 0):
    if numToRun == 0:
        return []

    setupDb()
    engine = helper.CreateEngine(server, database)
    addRecords(engine)
    print(f"Running Test 1")
    t = helper.TimeInstance(lambda: helper.ExecuteScript(engine, "clusteredCreateIndex.sql"))
    appendToResults("Test 1", t)

    print(f"Running Test 2")
    t = helper.TimeInstance(lambda: helper.ExecuteScript(engine, "dropIndex.sql"))
    appendToResults("Test 2", t)

    addRecords(engine)

    print(f"Running Test 3")
    t = helper.TimeInstance(lambda: helper.ExecuteScript(engine, "clusteredCreateIndex.sql"))
    appendToResults("Test 3", t)

    print(f"Running Test 4")
    t = helper.TimeInstance(lambda: helper.ExecuteScript(engine, "dropIndex.sql"))
    appendToResults("Test 4", t)

    setupDb()
    engine = helper.CreateEngine(server, database)
    addRecords(engine)

    print(f"Running Test 5")
    t = helper.TimeInstance(lambda: helper.ExecuteScript(engine, "clusteredCompositeCreate.sql"))
    appendToResults("Test 5", t)

    print(f"Running Test 6")
    t = helper.TimeInstance(lambda: helper.ExecuteScript(engine, "dropIndex.sql"))
    appendToResults("Test 6", t)

    addRecords(engine)

    print(f"Running Test 7")
    t = helper.TimeInstance(lambda: helper.ExecuteScript(engine, "clusteredCompositeCreate.sql"))
    appendToResults("Test 7", t)

    print(f"Running Test 8")
    t = helper.TimeInstance(lambda: helper.ExecuteScript(engine, "dropIndex.sql"))
    appendToResults("Test 8", t)

    # Non-Clustered Tests
    setupDb()
    engine = helper.CreateEngine(server, database)
    addRecords(engine)

    print(f"Running Test 9")
    t = helper.TimeInstance(lambda: helper.ExecuteScript(engine, "nonClusteredCreateIndex.sql"))
    appendToResults("Test 9", t)

    print(f"Running Test 10")
    t = helper.TimeInstance(lambda: helper.ExecuteScript(engine, "dropIndex.sql"))
    appendToResults("Test 10", t)

    addRecords(engine)

    print(f"Running Test 11")
    t = helper.TimeInstance(lambda: helper.ExecuteScript(engine, "nonClusteredCreateIndex.sql"))
    appendToResults("Test 11", t)

    print(f"Running Test 12")
    t = helper.TimeInstance(lambda: helper.ExecuteScript(engine, "dropIndex.sql"))
    appendToResults("Test 12", t)

    setupDb()
    engine = helper.CreateEngine(server, database)
    addRecords(engine)

    print(f"Running Test 13")
    t = helper.TimeInstance(lambda: helper.ExecuteScript(engine, "nonClusteredCompositeCreate.sql"))
    appendToResults("Test 13", t)

    print(f"Running Test 14")
    t = helper.TimeInstance(lambda: helper.ExecuteScript(engine, "dropIndex.sql"))
    appendToResults("Test 14", t)

    addRecords(engine)

    print(f"Running Test 15")
    t = helper.TimeInstance(lambda: helper.ExecuteScript(engine, "nonClusteredCompositeCreate.sql"))
    appendToResults("Test 15", t)

    print(f"Running Test 16")
    t = helper.TimeInstance(lambda: helper.ExecuteScript(engine, "dropIndex.sql"))
    appendToResults("Test 16", t)

    return runSamples(numToRun - 1)


# Run Samples and pickle results
if __name__ == '__main__':
    print(
        f"Executing avg_sample generation.  Iterations: {samplesToRun}, with records count: {numRecords}/{numRecords * 2}")
    print(f"Server: {server}, Database: {database}")

    tic = time.perf_counter()

    runSamples(samplesToRun)
    for x in results.keys():
        times = list(map(float, results[x]["Time (s)"]))
        results[x]["Time (s) - Avg"] = round(sum(times) / len(times), 2)
    with open(f'results_{numRecords}.pkl', 'wb') as file:
        pkl.dump(results, file, protocol=pkl.HIGHEST_PROTOCOL)

    toc = time.perf_counter()

    print(f"Experiment completed in: {toc-tic:0.4f} seconds")
    print(f"Results written to: results_{numRecords}.pkl")