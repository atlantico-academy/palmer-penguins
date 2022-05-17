from operator import index
from .. import project_path
import seaborn as sns


def load():
    df = sns.load_dataset("penguins")
    df.to_csv(
        project_path / 'data' / 'raw' / 'data.csv',
        index=False
    )