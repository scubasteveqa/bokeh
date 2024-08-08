import numpy as np
import pandas as pd
import seaborn as sns
from scipy.stats import zscore
from sklearn.preprocessing import MinMaxScaler
from matplotlib import cm

from bokeh.io import curdoc
from bokeh.layouts import column, row
from bokeh.models import ColumnDataSource, Select, Slider
from bokeh.plotting import figure

# Generate a sample dataset using Seaborn
data = sns.load_dataset('penguins').dropna()

# Normalize numerical data using z-score (Scipy) and MinMaxScaler (Scikit-learn)
numerical_cols = ['bill_length_mm', 'bill_depth_mm', 'flipper_length_mm', 'body_mass_g']
data[numerical_cols] = data[numerical_cols].apply(zscore)
scaler = MinMaxScaler()
data[numerical_cols] = scaler.fit_transform(data[numerical_cols])

# Define a colormap from Matplotlib
colormap = cm.get_cmap("viridis")

# Convert the color map to a list of hex colors
data['colors'] = [colormap(val) for val in data['body_mass_g']]
data['colors'] = [f'#{int(r*255):02x}{int(g*255):02x}{int(b*255):02x}' for r, g, b, _ in data['colors']]

# Initialize Bokeh ColumnDataSource
source = ColumnDataSource(data=dict(
    x=data['bill_length_mm'], 
    y=data['bill_depth_mm'],
    colors=data['colors'],
    species=data['species']
))

# Create Bokeh figure
plot = figure(title="Penguins Dataset", x_axis_label='Bill Length (normalized)', 
              y_axis_label='Bill Depth (normalized)', plot_height=600, plot_width=800)

scatter = plot.circle(x='x', y='y', color='colors', size=10, source=source, legend_field='species')
plot.legend.title = 'Species'

# Dropdown for selecting x and y axis data
x_select = Select(title="X-axis Data", value='bill_length_mm', options=numerical_cols)
y_select = Select(title="Y-axis Data", value='bill_depth_mm', options=numerical_cols)

# Slider for controlling marker size
size_slider = Slider(title="Marker Size", start=5, end=20, value=10, step=1)

# Update function
def update(attr, old, new):
    source.data = dict(
        x=data[x_select.value], 
        y=data[y_select.value],
        colors=data['colors'],
        species=data['species']
    )
    plot.xaxis.axis_label = x_select.value.replace("_", " ").title() + " (normalized)"
    plot.yaxis.axis_label = y_select.value.replace("_", " ").title() + " (normalized)"
    scatter.glyph.size = size_slider.value

x_select.on_change('value', update)
y_select.on_change('value', update)
size_slider.on_change('value', update)

# Layout
layout = column(row(x_select, y_select, size_slider), plot)

# Add the layout to the current document
curdoc().add_root(layout)
curdoc().title = "Comprehensive Bokeh App"
