from apiclient.discovery import build

DEVELOPER_KEY = <DeveloperKey>
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

def fetch_AllVideos_by_Channel(channelToSearch,OutputFilename):
    youtube = build(YOUTUBE_API_SERVICE_NAME,YOUTUBE_API_VERSION,developerKey=DEVELOPER_KEY)
    MyListOfVideos=youtube.playlistItems().list(part="snippet",playlistId="<ChannelID>",maxResults="50").execute()
    nextPageToken = MyListOfVideos.get('nextPageToken')
    while ('nextPageToken' in MyListOfVideos):
        nextPage = youtube.playlistItems().list(part="snippet",playlistId=channelToSearch,maxResults="50",pageToken=nextPageToken).execute()
        MyListOfVideos['items'] = MyListOfVideos['items'] + nextPage['items']
        if 'nextPageToken' not in nextPage:
            MyListOfVideos.pop('nextPageToken', None)
        else:
            nextPageToken = nextPage['nextPageToken']
            print ("\n\n")
    for MyVideo in MyListOfVideos["items"]:
        myVideoTitle=MyVideo["snippet"]["title"]
        myVideoId=MyVideo["snippet"]["resourceId"]["videoId"]
        myStat = youtube.videos().list(part="statistics",id=myVideoId).execute()
        myVideoDesc = MyVideo["snippet"]["description"]
        myVideoDt = MyVideo["snippet"]["publishedAt"]
        myVideoCt = myStat.get('items')[0]['statistics']

        print(myVideoCt['viewCount'])
        print (myVideoTitle + "#" + myVideoDesc)
        with open(OutputFilename, "a",encoding="utf-8") as file_object:
            file_object.write(myVideoTitle + "-" + myVideoCt['viewCount'] + "-" + myVideoId + "-" + myVideoDt + "\n")
    return (MyListOfVideos)


    
if __name__ == "__main__":
            fetch_AllVideos_by_Channel("<ChannelID>","FileName.txt")
