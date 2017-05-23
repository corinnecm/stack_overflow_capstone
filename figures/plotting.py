import matplotlib.pyplot as pyplot
import pandas as pd
import numpy as np
from pandas.plotting import scatter_plot

plt.switch_backend('pdf')

df = pd.concat([finder.X_train, finder.y_train], axis=1)

sm = scatter_matrix(df.sample(1000), alpha=0.3, figsize=(10, 10),
                    diagonal='kde')

[s.xaxis.label.set_rotation(45) for s in sm.reshape(-1)]
[s.yaxis.label.set_rotation(0) for s in sm.reshape(-1)]

[s.get_yaxis().set_label_coords(-0.3, 0.5) for s in sm.reshape(-1)]

[s.set_xticks(()) for s in sm.reshape(-1)]
[s.set_yticks(()) for s in sm.reshape(-1)]

fig = sm[0, 0].get_figure()

fig.savefig('file_name.png')
