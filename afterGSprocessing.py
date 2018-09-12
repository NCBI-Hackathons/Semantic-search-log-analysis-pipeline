from datetime import datetime, timedelta
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import random
from scipy.optimize import basinhopping, differential_evolution

filename = 'logAfterGoldStandard.xlsx'

data = pd.read_excel(filename)
data.index = data.Timestamp
d = data.groupby('SemanticGroup').resample('1H').count()['SemanticGroup'].unstack().T

color_sequence = ['#1f77b4', '#aec7e8', '#ff7f0e', '#ffbb78', '#2ca02c',
                  '#98df8a', '#d62728', '#ff9896', '#9467bd', '#c5b0d5',
                  '#8c564b', '#c49c94', '#e377c2', '#f7b6d2', '#7f7f7f',
                  '#c7c7c7', '#bcbd22', '#dbdb8d', '#17becf', '#9edae5']

fig, ax = plt.subplots(1,1, figsize=(12,12))
# Remove the plot frame lines. They are unnecessary here.
ax.spines['top'].set_visible(False)
ax.spines['bottom'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_visible(False)

# Ensure that the axis ticks only show up on the bottom and left of the plot.
# Ticks on the right and top of the plot are generally unnecessary.
ax.get_xaxis().tick_bottom()
ax.get_yaxis().tick_left()

fig.subplots_adjust(left=.06, right=.75, bottom=.06, top=.94)

out = d.resample('12H').sum()

ax.grid(True, axis='y')
ax.tick_params(axis='both', which='both', bottom=False, top=False,
                labelbottom=True, left=False, right=False, labelleft=True)

# Optimizing label position to avoid overlap

p = list(out.iloc[-1].items())
p.sort(key=lambda x: x[1])

dist = 3
m = -15
step = 0.5
q = []
for k,v in p:
    if np.isnan(v):
        q.append(-1)
    else:
        q.append(v-1)


def conflicts(x):
    x = np.array(x)
    diff = np.diff(x)
    diff = diff[diff < dist].size
    return diff

def improve_placement(q, dist=3, m=-15, step=0.5):
    while conflicts(q) > 0:
        for i in range(len(q) // 2):
            if (q[i+1] - q[i]) < dist:
                if (q[i]-step) > m:
                    q[i] -= step
                q[i+1] += step / 2
            if (q[-i-1] - q[-i-2]) < dist:
                q[-i-1] += step
                q[-i-2] -= step / 2
    return q



q = improve_placement(q, dist=5)
new_positions = {l:v for (l,old_value),v in zip(p,q)}

x_position = out.index[-1] + (out.index[-1] - out.index[0])/50
for i, (label, value) in enumerate(out.iloc[-1].items()):
    ax.plot(out.index, out[label], c=color_sequence[i])
    ax.text(x_position, new_positions[label], label, 
                    fontsize=14, color=color_sequence[i])

    
ax.set_xlabel('Date', size='x-large')
ax.set_ylabel('Search Frequency', size='x-large')
ax.set_title('Searches by Semantic Group', size='x-large')
fig.savefig('searches-by-semantic-group.png', dpi=300)
plt.show()
