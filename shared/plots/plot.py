from bokeh.io import curdoc
from bokeh.plotting import figure, output_file, save

class PlotBase:
    def __init__(self, max_width=600, height=300, sizing_mode="fixed", **kwargs) -> None:
        self.max_width = max_width
        self.height = height
        self.sizing_mode = sizing_mode
        self.renderer = kwargs['renderer']
        self.renderer_options = kwargs['renderer_options']
    
    # Prawdopodobnie będzie to do poprawy, na razie poddaję się inwencji twórczej
    def generate_plot(self) -> any:
        p = figure(sizing_mode=self.sizing_mode, max_width=self.max_width, height=self.height)
        return f"{p}.{self.renderer}({self.renderer_options})"

    
test = PlotBase(renderer='scatter', renderer_options='xs')
print(test.generate_plot())

# output_file(filename="shared/plots/index.html", title="Statystyki graczy")

# p = figure(sizing_mode="fixed", max_width=500, height=250)

# save(p)

