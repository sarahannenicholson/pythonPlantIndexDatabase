import plotly.express as px
import plotly.graph_objs as go
import pandas as pd
from app import app, db
from app.dbmodels import PlantDatabase
import mysql.connector

df = pd.DataFrame([
    dict(Task=PlantDatabase.query.order_by(PlantDatabase.plant_name).all(), Start='2021-01-20', Finish='2021-02-04'),
])

# create gantt/timeline chart.
fig = px.timeline(df, x_start="Start", x_end="Finish", y="Task")
# shows charts in reversed, so last row of dataframe will show at bottom
fig.update_yaxes(autorange="reversed")

fig.show(df.to_json())

