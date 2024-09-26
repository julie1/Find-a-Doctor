import os
import pandas as pd

import minsearch


DATA_PATH = os.getenv("DATA_PATH", "./data/hip_surgeons.csv")


def load_index(data_path=DATA_PATH):
    df = pd.read_csv(data_path)
    text_fields = df.columns.tolist()
    df.insert(0, 'id', df.index)
    documents = df.to_dict(orient="records")


    index = minsearch.Index(
        text_fields=text_fields,
        keyword_fields=["id"],
    )

    index.fit(documents)
    return index
