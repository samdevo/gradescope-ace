import click
from src.browserbot import submit_assignment


@click.group()
def main():
    pass


@main.command()
@click.option("-u", "--url", "url", required=True)
def submit(url):
    """
    Submits the current repository to the specified url
    """
    click.echo(url)
    submit_assignment(url)




