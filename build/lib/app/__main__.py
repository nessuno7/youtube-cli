from .functions.webscraping import youtube_webscraping_functions as ywf
from .functions.data_handlers import database_handler as dh
from .functions import video_editing as ve
from .functions.webscraping import tiktok_uploader as tk
from .functions.data_handlers import create_videos_database as cdb
from .functions.data_handlers import json_handler as jh
from .functions import config
from .functions.data_handlers import channel_database_handler as cdh
import typer
from typing import Optional
import os

app = typer.Typer()


change_app = typer.Typer()
list_app = typer.Typer()
run_app = typer.Typer()
clear_app = typer.Typer()
config_app = typer.Typer()

app.add_typer(change_app, name="change")
app.add_typer(list_app, name="list")
app.add_typer(run_app, name="run")
app.add_typer(clear_app, name="clear")
app.add_typer(config_app, name="config")



# --- change COMMANDS ---
@change_app.command("target")
def change_target(channel_name: str, username: Optional[str] = typer.Option(None, help="username for tiktok channel"), password: Optional[str] = typer.Option(None, help="password for tiktok channel")):
    if channel_name.startswith("@"):
        db_name = channel_name.replace("@", "")
        if not cdh.check_channel_entry_exists(channel_name): #channel entry doesn't exists
            cdh.save_to_channel_database(ch_name=channel_name, username=username, password=password)
            cdb.create_database(name=db_name)
            typer.echo(f"Created new database and entry for channel {channel_name}")

        jh.modify_channel_name(channel_name)
        jh.modify_database_name(db_name)
        if username != None:
            cdh.modify_username(ch_name=channel_name, username=username)
        if password != None:
            cdh.modify_password(ch_name=channel_name, password=password)
        typer.echo(f"Saved {channel_name} as current workiing channel")

    else:
        print("Invalid channel name: must start with @")

@change_app.command("depth")
def set_depth(years: str):
    jh.modify_max_depth_search(years)
    typer.echo(f"Max scraping depth set to {years} years")

@change_app.command("login")
def change_username_password(username: str, password: str, channel_name: Optional[str] = typer.Option(None, help="Name of channel")):
    if channel_name == None:
        channel_name = jh.fetch_channel_name()

    cdh.modify_username(ch_name=channel_name, username=username)
    cdh.modify_password(ch_name=channel_name, password=password)

# --- list COMMANDS ---

@list_app.command("all")
def all_channels_databases():
    cdh.print_channels_and_databases()

@list_app.command("videos")
def all_videos():
    dh.print_all_videos()

@list_app.command("posted")
def which_posted():
    print(f"Listing from {jh.fetch_database_name} database: ")
    dh.print_posted_id(True)

@list_app.command("not-posted")
def which_not_posted():
    print(f"Listing from {jh.fetch_database_name} database: ")
    dh.print_posted_id(False)

@list_app.command("db")
def list_dbs():
    list = os.listdir(config.database_dir)
    for name in list:
        print(name)



# --- config COMMANDS ---
@config_app.command("once")
def create_json():
    config.config_function()
    cdb.create_channels_database()
    jh.save_to_json()

@config_app.command("all")
def create_json(channel_name, username, password):
    cdh.modify_password(ch_name=channel_name, password=password)
    cdh.modify_username(ch_name=channel_name, username=username)
    

# --- db COMMANDS ---               shoudln't need it
#@db_app.command("create")
#def create_db(database_name: str):   
#    jh.modify_database_name(database_name)
#    typer.echo(f"Created new database: {database_name}.db")


# --- run COMMANDS ---
@run_app.command("clip")
def run_post(id: int):
    obtain_heatmap(id=id)
    ve.create_clips(id=id)

@run_app.command("post")
def run_post(id: int):
    ve.create_clips(id=id)
    tk.post_clips(id=id)

@run_app.command("heatmap-post")
def search_and_post(id: int):
    obtain_heatmap(id=id)
    ve.create_clips(id=id)
    tk.post_clips(id=id)

@run_app.command("scrape")
def start_scraping(depth: Optional[int] = typer.Option(None, help="Max number of years to scrape")):
    
    driver = ywf.setup_driver()
    channel_name = jh.fetch_channel_name()
    if channel_name != "":
        typer.echo(f"Starting scraping for {channel_name} with depth={depth}")
        if depth != "":
            jh.fetch_max_depth_search()
            ywf.scroll_down_all_videos(driver=driver, max_depth_search=f"{depth}", channel_name=jh.fetch_channel_name())
            typer.echo("Scraping completed")
        else:
             typer.echo("Scrape failed: no depth")

    else:
        typer.echo("Scrape failed: no channel name")

    driver.quit()
    

@run_app.command("heatmap")
def obtain_heatmap(id: int):
    if dh.fetch_heatmap(id) == "":
        driver = ywf.setup_driver()
        dh.modify_heatmap(id=id, heatmap=ywf.scrape_heatmap(driver=driver, url=dh.fetch_link(id=id)))
        driver.quit()

@run_app.command("heatmap-inter") #recursive/iterator
def obtain_heatmaps(start: int, end: int):
    i = start
    driver = ywf.setup_driver()
    while i in range(start, end):
        if dh.fetch_heatmap(id) == "":
            dh.modify_heatmap(id=i, heatmap=ywf.scrape_heatmap(driver=driver, url=dh.fetch_link(id=i)))
    driver.quit()


# --- clear COMMANDS ---

@clear_app.command("clips")
def clear_clips():
    list = os.listdir(config.clips_dir)
    for clip in list:
        os.remove(config.clips_dir+clip)

@clear_app.command("videos")
def clear_videos():
    list = os.listdir(config.videos_dir)
    for clip in list:
        os.remove(config.videos_dir+clip)

@clear_app.command("dbentry")
def delete_database(channel_name: str):
    cdh.delete_entry(ch_name=channel_name)

@clear_app.command("database")
def delete_database(channel_name: str):
    db_name = channel_name.replace("@", "")
    db_path = db_name+".db"
    os.remove(config.database_dir/db_path)
    cdh.delete_entry(ch_name=channel_name)
    



if __name__ == "__main__":
    app()




