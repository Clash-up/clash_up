import pandas as pd
from bokeh.io import curdoc
from bokeh.plotting import figure, output_file, save

from shared.pyd_models import PlayerRead, WarEntryRead
from shared.plotter.base_plotter import BasePlotter

# TODO: Dokończyć rysowanie wykresu
class BokehPlotter(BasePlotter('bokeh')):
    def __init__(self, data_source: PlayerRead | WarEntryRead,  max_width=600, height=300, sizing_mode="fixed", **kwargs) -> None:
        self.data_frame = self.convert_data_to_dataframe(data_source)
        self.max_width = max_width
        self.height = height
        self.sizing_mode = sizing_mode
        self.render = kwargs['render']
        self.render_options = kwargs['render_options']
    

test = BokehPlotter()
test.get_data()


