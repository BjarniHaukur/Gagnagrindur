import numpy as np
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


def test(n, m, generator, verbose=False):
    # Insert
    keys = get_keys(n)
    if n <= 26:
        values = [chr(i-1+ord('A')) for i in keys]
    else:
        values = get_keys(n)

    bt = BinaryTree()
    tt = Treap(max_range=10**6)
    ll = LinkedList()
    for i in range(n):
        bt.insert(keys[i], values[i])
        tt.insert(keys[i], values[i])
        ll.insert(keys[i], values[i])

    # Search
    access = generator(n, m)
    
    for a in access:
        _ = bt.search(a)
        _ = tt.search(a)
        _ = ll.search(a)

    bt_avg = bt.get_average_costs()
    tt_avg = tt.get_average_costs()
    ll_avg = ll.get_average_costs()

    if verbose:
        print("Insert cost | search cost\n")
        print("Binary Tree")
        my_print(bt.get_costs())
        print("Average cost", bt_avg, "\n")

        print("Treap")
        my_print(tt.get_costs())
        print("Average cost", tt_avg, "\n")

        print("Linked List (move to front)")
        my_print(ll.get_costs())
        print("Average cost", ll_avg, "\n")
    
    return [x for x in zip(bt_avg, tt_avg, ll_avg)]

def run_and_plot(n_range, ma, generator, name, extra="", stepsize=10, verbose=False):
    x_range = np.arange(stepsize, n_range+1, step=stepsize)
    insert_hist = []
    search_hist = []
    if verbose: print("\nTest for ", name+extra)
    for n in x_range:        
        y = test(n, ma, generator, verbose)
        insert_hist.append(y[0])
        search_hist.append(y[1])
    
    fig, (ax1, ax2) = plt.subplots(1, 2)
    fig.suptitle(name+extra)
    labels = ["BinaryTree", "Treap", "LinkedList"]
    for i in range(3):
        ax1.plot(x_range, [x[i] for x in insert_hist], label=labels[i])
        ax2.plot(x_range, [x[i] for x in search_hist])

    ax1.title.set_text("Insert cost")
    ax2.title.set_text("Search cost")
    fig.supxlabel("Number of keys")
    fig.supylabel("Average number of operations")
    fig.legend(loc="center right")
    plt.savefig(name+extra)


if __name__ == '__main__':
    n = 200
    m = 2
    a = 2
    run_and_plot(n, m, equal_access_rates, "Equal Access Rates")
    run_and_plot(n, a, zipf_distribution, "Zipf Distribution", f" a={a}")
    