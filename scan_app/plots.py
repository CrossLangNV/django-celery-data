import plotly.express as px
from plotly.offline import plot

class BarChart:

    def __init__(self, data = None):
        # should be a pandas DataFrame
        self._data = data

    def plot(self):
        # data_belgium = px.data.gapminder().query("country == 'Belgium'")
        fig = px.bar(self._data, x='File', y='Line count')
        plot_div = plot(fig, output_type='div', filename='files-line-count')
        return plot_div

    def init_data(self, dir):
        pass