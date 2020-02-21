## Libraries

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from bokeh.io import curdoc
from bokeh.io import output_file, show
from bokeh.plotting import figure
from bokeh.models import CategoricalColorMapper, HoverTool, ColumnDataSource, Slider, NumeralTickFormatter
from bokeh.layouts import row, column, widgetbox
#from bokeh.palettes import Spectral6
from bokeh.models.widgets import Panel, Tabs


# Import data
time_df = pd.read_csv("time_df.csv", parse_dates= ['launch_date_mid_month'])
df_condensed = pd.read_csv("df_condensed.csv",index_col=0)
results = pd.read_csv("results.csv", index_col=0)


# Define source datasets

source1 = ColumnDataSource(data={
    'x': time_df.launch_date_mid_month,
    'y': time_df.obs_count,
    'z': time_df.success_rate
})

source2 = ColumnDataSource(data={
    'x': df_condensed.loc[2018].goal_usd_log,
    'y': df_condensed.loc[2018].comb_model_output,
    'sector': df_condensed.loc[2018].subcategory
})

source3 = ColumnDataSource(data={
    'x': results.loc[2018].midpoint_prob,
    'y': results.loc[2018].success_rate,
    'count': results.loc[2018].obs_count
})


# Define update functions

def update_plot2(attr, old, new):
    yr = slider.value
    new_data={
    'x': df_condensed.loc[yr].goal_usd_log,
    'y': df_condensed.loc[yr].comb_model_output,      
    }    
    source2.data = new_data


def update_plot3(attr, old, new):
    yr = slider.value
    new_data={
    'x': results.loc[yr].midpoint_prob,
    'y': results.loc[yr].success_rate,
    'count': results.loc[yr].obs_count        
    }    
    source3.data = new_data



slider = Slider(start = 2009, end=2018, value= 2018, step=1, title='Year')
slider.on_change('value', update_plot2)
slider.on_change('value', update_plot3)


# Time series charts tab

p1 = figure(title = "Projects counts over time", plot_width=1200, x_axis_type='datetime',
		y_axis_label = "Monthly project count")
p1.line(x='x', y = 'y', source=source1, color = 'blue')


p2 = figure(title = "Project success rate over time", plot_width=1200, x_axis_type='datetime',
		y_axis_label = "Monthly project success rate")
p2.line(x='x', y = 'z', source=source1, color = 'red')
p2.yaxis.formatter = NumeralTickFormatter(format='0 %')


# Model factors tab

p3 = figure(y_range=(0,1), plot_width=600, tools = 'pan,box_zoom,hover', 
		x_axis_label = "Project goal in USD (logged)", 
		y_axis_label = "Modelled success rate", 
		title="How size interacts with predicted likelihood to success")
p3.diamond(x='x', y='y', source=source2, size=2)
p3.yaxis.formatter = NumeralTickFormatter(format='0 %')




# Model results tab

p4 = figure(x_range=(0,1), y_range=(0,1), plot_width=600, tools = 'pan,box_zoom,hover', 
		x_axis_label = "Modelled success likelihood band", 
		y_axis_label = "Actual success rate", 
		title="Predictions vs actual success probabilities")
p4.diamond(x='x', y='y', source=source3, size=10)
p4.xaxis.formatter = NumeralTickFormatter(format='0 %')
p4.yaxis.formatter = NumeralTickFormatter(format='0 %')


p5 = figure(x_range=(0,1), plot_width=600, tools = 'pan,box_zoom', 
		x_axis_label = "Modelled success likelihood band", 
		y_axis_label = "Project count", 
		title="Distribution by prediction bucket")
p5.vbar(x='x', top = 'count', source=source3, width=0.09, color = 'orange')
p5.xaxis.formatter = NumeralTickFormatter(format='0 %')




tab1 = Panel(child = column(p1,p2), title="Trends over time")
tab2 = Panel(child = row([widgetbox(slider),p3]), title="Project timeline")
tab3 = Panel(child = row([widgetbox(slider),p4,p5]), title="Results: model predictions vs actuals")

tabs = Tabs(tabs = [tab1,tab2,tab3])

curdoc().add_root(tabs)
#curdoc().add_root(layout)
curdoc().title = "Kickstarter - Technology project predictions"