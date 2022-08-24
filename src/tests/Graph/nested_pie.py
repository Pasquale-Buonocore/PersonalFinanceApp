import matplotlib.pyplot as plt
from matplotlib.cm import get_cmap
import numpy as np
fig, ax = plt.subplots()

size = 0.3
vals = np.array([[60., 32.], [37., 40.], [29., 10.]])

cmap = get_cmap("tab20c")
outer_colors = cmap(np.arange(3)*4)
inner_colors = cmap([1, 2, 5, 6, 9, 10])

labels_inner = ["A", "B", "C", "D", "E", "F"]
labels_outer = ["Slice 1", "Slice 2", "Slice 3"]

# outer slices
ax.pie(vals.sum(axis=1), radius=1, colors=outer_colors,
       wedgeprops=dict(width=size, edgecolor='w'), labels=labels_outer)

# inner slices
ax.pie(vals.flatten(), radius=1-size, colors=inner_colors,
       wedgeprops=dict(width=size, edgecolor='w'), labels=labels_inner, labeldistance=0.7)

ax.set(aspect="equal", title='Pie plot with `ax.pie`')
plt.legend(loc=(-0.3, 0))
plt.show()