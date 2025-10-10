#functions for videoediting there
#the tiktok_uploader will get the videos from here
import yt_dlp
from .data_handlers import database_handler as dh
from moviepy import VideoFileClip #, mirror_x
import os
from .config import clips_dir, videos_dir

def is_video_already_downloaded(filename):
    files = os.listdir(videos_dir)
    if filename in files:
        return True
    else:
        return False
    

def is_clip_already_downloaded(filename):
    files = os.listdir(clips_dir)
    if filename in files:
        return True
    else:
        return False


def download_youtube_video(link, id):  
    if is_video_already_downloaded(f"full_video_{id}.mp4") == False:
        ydl_opts = {
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/mp4',
            'merge_output_format': 'mp4',
            'outtmpl': f'{videos_dir}/full_video_{id}.%(ext)s',
        }

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([link])
            print(f'Video with id {id} downloaded successfully!')
            return f'{videos_dir}/full_video_{id}.mp4'
        except:
            print(f"Failed to download video with id {id}")
            return ""
        
    return f'{videos_dir}/full_video_{id}.mp4'


def list_to_float(list):
    s = ''.join(list)
    return float(s)


def extract_heatmap_datapoints(heatmap):
    h_list = list(heatmap)
    c_count = 0
    i = 0
    comma_index = 0

    return_list = []

    for x in h_list:
        if x == "C":
            c_count = 0
        
        if  x == ",":
            c_count = c_count + 1

            if c_count == 3: #found the data point
                comma_index = i
                first_n_i = i
                while h_list[first_n_i] != " ":
                    first_n_i = first_n_i -1
                first_n_i = first_n_i+1

                x_value_list = []

                while first_n_i < comma_index:
                    x_value_list.append(h_list[first_n_i])
                    first_n_i = first_n_i + 1

                x_value = round((list_to_float(x_value_list)-5)/1000, 2)
                
                y_value_list = []
                comma_index = comma_index + 1
                while comma_index < len(h_list) and h_list[comma_index] != " ":
                    y_value_list.append(h_list[comma_index])
                    comma_index = comma_index+1

                y_value = round((100-list_to_float(y_value_list))/100, 2)

                return_list.append((x_value, y_value))

        i = i+1
    
    return_list.pop(0)

    return return_list

def get_3_best_moments(heatmap):
    heatmap_list = extract_heatmap_datapoints(heatmap=heatmap)
    
    print(heatmap_list)

    i1 = int(len(heatmap_list)/3)
    i2 = int(len(heatmap_list)*2/3)
    i3 = len(heatmap_list)
    i = 0
    max1 = heatmap_list[0]
    max2 = heatmap_list[i1]
    max3 = heatmap_list[i2]
    while i < i1:
        point = heatmap_list[i]
        if point[1] > max1 [1]:
            max1 = point
        i = i+1
    while i <i2:
        point = heatmap_list[i]
        if point[1] > max2 [1]:
            max2 = point
        i = i+1
    while i <i3:
        point = heatmap_list[i]
        if point[1] > max3 [1]:
            max3 = point
        i = i+1
    
    print(max1)
    print(max2)
    print(max3)

    return [max1, max2, max3]


def save_clips(highlights, path, id):
    highlight_counter = 0
    video = VideoFileClip(path)
    
    duration = video.duration
        
    duration = int(duration)
    dh.modify_duration(id=id, duration=duration) 

    print(duration)   

    for highlight in highlights:
        highlight_counter = highlight_counter + 1
        time1 = int(duration*highlight[1])

        if time1 <60:
            time0 = 0
        else:
            time0 = time1-60
        diff = duration - time1
        if diff > 120:
            time2 = time1 + 60
            time3 =  time1 +120
        elif diff > 90:
            time2 = time1 + 60
            time3 = time1 + diff 
        else:
            time2 = time1 + int(diff/2)
            time3 = time1 + diff

        print(time0)
        print(time1)
        print(time2)
        print(time3)

        

        if is_clip_already_downloaded(f"clip_{highlight_counter}_1_videoid_{id}.mp4") == False and (time1-time0)>10:
            clip1 = video.subclipped(time0, time1)
            clip1.write_videofile(f"{clips_dir}/clip_{highlight_counter}_1_videoid_{id}.mp4")
        if is_clip_already_downloaded(f"clip_{highlight_counter}_2_videoid_{id}.mp4") == False and (time2-time1)>10:
            clip2 = video.subclipped(time1, time2)
            clip2.write_videofile(f"{clips_dir}/clip_{highlight_counter}_2_videoid_{id}.mp4")
        if is_clip_already_downloaded(f"clip_{highlight_counter}_3_videoid_{id}.mp4") == False and (time3-time2)>1:
            clip3 = video.subclipped(time2, time3)
            clip3.write_videofile(f"{clips_dir}/clip_{highlight_counter}_3_videoid_{id}.mp4")
    


def create_clips(id):
    
    link = dh.fetch_link(id=id)
    heatmap = dh.fetch_heatmap(id=id)
    #clip = dh.fetch_clip(id=id) check if clip is already made

    if heatmap != "":
        path = download_youtube_video(link=link, id=id)
        print(path)
        if path != "":
            highlights = get_3_best_moments(heatmap=heatmap)
            save_clips(highlights=highlights, path=path, id=id)
    else:
        print(f"Video with id {id} has no heatmap")
            




    

