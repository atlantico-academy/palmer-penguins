from invoke import task
from src.data import raw



@task
def load(c):
    raw.load()
    print("Dados carregados!")