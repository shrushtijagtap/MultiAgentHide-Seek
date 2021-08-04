import pickle

q_table = {}

pickle_s = open("seeker_qtable.pickle","wb")
pickle.dump(q_table, pickle_s)
pickle_s.close()

pickle_h = open("hider_qtable.pickle","wb")
pickle.dump(q_table, pickle_h)
pickle_h.close()