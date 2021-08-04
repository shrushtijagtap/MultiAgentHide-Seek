import pickle
pickle_in = open("hider_qtable.pickle","rb")
qtable = pickle.load(pickle_in)
print(qtable)