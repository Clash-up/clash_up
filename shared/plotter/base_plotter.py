import pandas as pd
from pydantic import BaseModel


class BasePlotter:
    def __init__(self, provider: str):
        self.provider = provider

    def convert_data_to_dataframe(self, data_source: BaseModel) -> pd.DataFrame:
        self.data_source = data_source
        return pd.DataFrame([self.data_source.model_dump()])