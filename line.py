# line.py
# Authors - Jonika Rathi, Shubhang Seth
# This is the program utility used to plot the payback period graph for solar investment vs electric utility charges
# This file is imported by main.py

# This program uses matplotlib to plot the graph and save it
import matplotlib.pyplot as plt


# This function is used to plot the graph of cost vs savings
# It takes a parameter for federal incentives which is used to further increase savings
def plot(cost, savings, fed_incentive):
    # Let's plot for 20 years
    t = [i for i in range(21)]

    # We get the saving(or depreciated value) for the solar investment per year.
    annual_saving = abs(savings/len(t))

    # Subsequently keep decreasing the depreciated cost per year
    y_savings = [savings - (i * annual_saving) for i in t]
    # And add the electric utility cost per year
    y_cost = [cost * i for i in t]

    # plot the data
    fig = plt.figure()
    ax = fig.add_subplot()
    ax.plot(t, y_cost, color='tab:blue', label='Electric Utility Charges')
    ax.plot(t, y_savings, color='tab:orange', label='Depreciated Solar Investment')

    # # set the limits
    ax.set_xlim([0, len(t)])
    ax.set_ylim([0, savings])

    # Intersection point
    # The point where your electric charges go beyond your solar depreciated cost is when it starts turning into savings
    # Also called payback period
    xi = savings / (annual_saving + cost)
    yi = savings - annual_saving * xi
    # print(xi, yi)
    plt.axvline(xi, color='gray', linewidth='1', linestyle='--', marker='.', label='Payback Period')
    plt.scatter(xi, yi, color='black')

    # Let's see the effects of incentive
    savings = savings * (1 - fed_incentive/100)
    annual_saving = abs(savings / len(t))
    y_savings = [savings - (i * annual_saving) for i in t]
    ax.plot(t, y_savings, color='tab:red', label='Solar Investment with Federal Incentive', linestyle='--')

    ax.set_title('Payback Period')
    plt.xlabel('Number of years')
    plt.ylabel('Cost (in $)')

    # display the plot
    plt.legend(loc="upper right")
    # plt.show()
    fig.savefig('payback.png', dpi=fig.dpi)
    return 'payback.png', xi


# This is for testing purpose only
if __name__ == '__main__':
    plot(1200, 10000, 20.0)
