All data is saved in directory "C:/Users/user name/AppData/nessuno7/ytcli/"

Programs needed for application:
pipx:
py -m pip install --user pipx (might need )
py -m pipx ensurepath

(Might need conda with ffmpeg:
install miniconda
run: conda install ffmpeg)


To install the package run: pipx install .
To update dependecies, add name of dipendency to dependencies = []
run command: pipx uninstall ytcli
run command: pipx install .

test functioning: ytcli --help

to ensure path add the following path to enivornemtn variables:
C:\Users\"user name"\.local\bin\ytcli.exe


run once before anything else:
ytcli config once

After running make sure the directory "C:/Users/user name/AppData/nessuno7/ytcli/" exists
Copy and paste the MrBeast databse to the databases directory


List of commands:

- change target "name of channel" "tik tok account username (optional)" "tik tok account password (optional)"
        changes the youtube channel and database that you want to use (eg change from MrBeast to Grax)
        name of channel needs the @ (eg @MrBeast) 
- change depth "new depth": how many years old are the videso you want? (eg max 2 years old = depth 2)
- change login "username" "password" (Optional "channel name"): changes username and password for tik tok login just for the curretn youtube channel, unless other channel name is given


- list all : prints name of channels and databases saved
- list videos: print ids and titles of all videso saved in database for the youtube channel
- list posted: lists posted videos from current database
- list not-posted: 
- list db: lists all databases present (each databse contains videos for one channel)

- config once: runs before anything else
-config all: channel_name username password

- run post "id": posts clips only is heatmap is already saved
- run heatmap-post "id": find heatmap then posts clips
- run scrape "depth (optional)": scrapes all info from youtube channels, if depth not defined then runs at default depth
                                to run with scrape: run scrape --depth 3 
- run heatmap "id": just finds the heatmap of a video  
- run heatmap-inter "start id" "end id": finds heatmap for videos with id between the range

- clear clips: delets all saved clips from the clips folder to save space
- clear videos: deletes all saved videos from the videos folder to save space


Error handling:
In case of error when opening chrome, make sure it chromes version is the latest
