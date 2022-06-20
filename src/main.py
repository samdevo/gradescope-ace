import click
from browserbot import submit_assignment, init_session, send_submit


@click.group()
def main():
    pass


@main.command()
@click.option("-u", "--url", "url", required=True)
def submit(url):
    """
    Submits the current repository to the specified url
    """
    send_submit(url)


@main.command()
def init():
    """
    Creates a gradescope browser session for user to sign in
    """
    init_session()


if __name__ == '__main__':
    main()




