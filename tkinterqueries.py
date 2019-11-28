import pickle

with open("queries.pickle", "rb") as fp:
    queries = pickle.load(fp)

print(queries)

with open("queries.pickle", "wb") as fp:
    pickle.dump(queries, fp)