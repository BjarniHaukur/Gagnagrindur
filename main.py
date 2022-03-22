import time
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from DataFrames import *


def get_keys(n):
    arr = np.arange(1, n+1)
    np.random.shuffle(arr)
    return arr

def equal_access_rates(n, m):
    access = np.array([i for i in range(1, n+1) for _ in range(m)])
    np.random.shuffle(access)
    return access

def zipf_distribution(n, distribution):
    zipf = np.random.zipf(a=distribution, size=n)
    access = np.array([(i+1) for i in range(n) for _ in range(zipf[i])])
    np.random.shuffle(access)
    return access

def my_print(costs):
    if len(costs[0]) <= 10:
        print(costs)
    else:
        print("Last 10 entries: ", costs[0][-10:], costs[1][-10:])

def measure_and_insert(keys, values, df: DataFrame):
    then = time.time()
    for k, v in zip(keys, values):
        df.insert(k, v)

    return time.time() - then

def measure_search(access, df: DataFrame):
    then = time.time()
    for a in access:
        _ = df.search(a)

    return time.time() - then


def test(n, m, generator):
    # Insert
    keys = get_keys(n)
    if n <= 26:
        values = [chr(i-1+ord('A')) for i in keys]
    else:
        values = get_keys(n)

    # Initialize
    bt = BinaryTree()
    tt = Treap(max_range=10**6)
    ll = LinkedList()

    # Search for these keys
    access = generator(n, m)

    bt_time = (measure_and_insert(keys, values, bt), measure_search(access, bt))
    tt_time = (measure_and_insert(keys, values, tt), measure_search(access, tt))
    ll_time = (measure_and_insert(keys, values, ll), measure_search(access, ll))

    bt_op = bt.get_average_costs()
    tt_op = tt.get_average_costs()
    ll_op = ll.get_average_costs()
    
    return list(zip(bt_op, tt_op, ll_op)), list(zip(bt_time, tt_time, ll_time))

def run_and_plot(n_range, ma, generator, name, extra="", stepsize=10):
    x_range = np.arange(stepsize, n_range+1, step=stepsize)
    iop_hist = []
    sop_hist = []
    itime_hist = []
    stime_hist = []
    for n in x_range:        
        ops, time = test(n, ma, generator)
        iop_hist.append(ops[0])
        sop_hist.append(ops[1])
        itime_hist.append(time[0])
        stime_hist.append(time[1])
    
    # data = pd.DataFrame(index=x_range, data=list(zip(iop_hist, sop_hist, itime_hist, stime_hist)),
    #                     columns=["insert_operations", "search_operations", "insert_time", "search_time"])


    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2)
    fig.suptitle(name+extra)
    labels = ["BinaryTree", "Treap", "LinkedList"]
    for i in range(len(labels)):
        ax1.plot(x_range, [x[i] for x in iop_hist])
        ax2.plot(x_range, [x[i] for x in sop_hist])
        ax3.plot(x_range, [x[i] for x in itime_hist])
        ax4.plot(x_range, [x[i] for x in stime_hist], label=labels[i])

    ax1.title.set_text("Insert cost")
    ax2.title.set_text("Search cost")
    fig.supxlabel("Number of keys")
    ax1.set(ylabel="Average number of operation")
    ax3.set(ylabel="Time(s)")
    ax4.legend(loc="upper left")
    plt.savefig("myndir/" + name+extra)


if __name__ == '__main__':
    for n in [200, 600]:
        for m in [1, 25, 50, 75, 100]:
            run_and_plot(n, m, equal_access_rates, "Equal Access Rates", f" n={n}, m={m}")
        for a in [2, 4]:
            run_and_plot(n, a, zipf_distribution, "Zipf Distribution", f" n={n}, a={a}")
    