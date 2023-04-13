from moviepy.editor import * #  This imports everything from the moviepy.editor library. MoviePy is a Python library used for video editing: cutting, concatenations, title insertions, video compositing, etc. In this project, it will be used to create the YouTube Shorts video.

import reddit, screenshot, time, subprocess, random, configparser, sys, math
'''
import reddit: This imports a custom module called reddit. This module likely contains functions and classes related to interacting with the Reddit API and fetching data from it.
import screenshot: This imports another custom module called screenshot. This module might be responsible for taking screenshots of specific content, like Reddit posts or comments.
import time: The time module provides various functions to work with time values, like waiting for a certain amount of time or getting the current time. It might be used for managing time intervals between tasks in the project.
import subprocess: The subprocess module allows you to spawn new processes, connect to their input/output/error pipes, and obtain their return codes. It might be used in this project to run external commands or scripts for video processing.
import random: The random module is used to generate random numbers. It might be used in this project to add randomness to the video creation process or to select random Reddit posts.
import configparser: The configparser module is used for working with configuration files. It's a way to read and write data from and to configuration files, allowing you to store settings externally from your script.
import sys: The sys module provides access to some variables used or maintained by the interpreter and to functions that interact with the interpreter. It might be used for various system-related tasks, like managing command-line arguments or exiting the script.
'''

from os import listdir # This imports the listdir function from the os module, which is used to list all files in a specified directory.
from os.path import isfile, join # This imports the isfile and join functions from the os.path module. isfile is used to check if a given path is a regular file, while join is used to join one or more pathname components into a single pathname string. These functions are often used for file and directory operations.

def createVideo():
    config = configparser.ConfigParser() # This line imports the configparser module and creates an instance of the ConfigParser class called config. The ConfigParser class is a class for working with configuration files in INI format.
    config.read('config.ini') # This line reads the configuration file config.ini using the read() method of the ConfigParser object created in the previous line.
    outputDir = config["General"]["OutputDirectory"] # This line retrieves the value of the OutputDirectory key from the [General] section of the configuration file, and assigns it to the variable outputDir.

    startTime = time.time() # This line retrieves the current time in seconds since the epoch (January 1, 1970), using the time.time() method, and assigns it to the variable startTime.

    # Get script from reddit
    # If a post id is listed, use that. Otherwise query top posts
    if (len(sys.argv) == 2): # This line is an if statement that checks whether the length of the sys.argv list (which contains command line arguments) is equal to 2. If it is, the code inside the if block will be executed; otherwise, the code inside the else block will be executed.
        script = reddit.getContentFromId(outputDir, sys.argv[1]) # This line calls the getContentFromId() method of a reddit object with two arguments: outputDir, which is a directory where output files will be saved, and sys.argv[1], which is the second command line argument (assuming there are two arguments). This method retrieves the content of a Reddit post with the specified ID and returns a Script object, which is assigned to the script variable.
    else:
        postOptionCount = int(config["Reddit"]["NumberOfPostsToSelectFrom"]) # This line retrieves the value of the NumberOfPostsToSelectFrom key from the [Reddit] section of the configuration file, and converts it to an integer using the int() function. The integer value is assigned to the variable postOptionCount.
        script = reddit.getContent(outputDir, postOptionCount) # This line calls the getContent() method of a reddit object with two arguments: outputDir, which is a directory where output files will be saved, and postOptionCount, which is the number of top posts to query from Reddit. This method retrieves the content of the top posts from Reddit and returns a Script object, which is assigned to the script variable.
    fileName = script.getFileName() # This line calls the getFileName() method of the script object, which returns a filename based on the Reddit post title and the current date and time. The filename is assigned to the fileName variable.

    # Create screenshots
    screenshot.getPostScreenshots(fileName, script) # This line calls the getPostScreenshots() method of a screenshot object with two arguments: fileName, which is the filename of the Reddit post, and script, which is the Script object containing the content of the Reddit post. This method creates screenshots of the Reddit post and saves them to the output directory specified in the configuration file.

    # Setup background clip
    bgDir = config["General"]["BackgroundDirectory"] # This line retrieves the value of the BackgroundDirectory key from the [General] section of the configuration file, and assigns it to the variable bgDir.
    bgPrefix = config["General"]["BackgroundFilePrefix"] # This line retrieves the value of the BackgroundFilePrefix key from the [General] section of the configuration file, and assigns it to the variable bgPrefix.
    bgFiles = [f for f in listdir(bgDir) if isfile(join(bgDir, f))] # This line uses the listdir() and isfile() functions from the os module to get a list of all the files in the bgDir directory that are files (i.e., not directories). The list comprehension creates a list of filenames by iterating over the list of files and selecting only those that are files.
    bgCount = len(bgFiles) # This line gets the length of the bgFiles list (i.e., the number of files in the bgDir directory that are files) and assigns it to the variable bgCount.
    bgIndex = random.randint(0, bgCount-1) # This line generates a random integer between 0 and bgCount-1 (inclusive) using the randint() function from the random module, and assigns it to the variable bgIndex.

    '''
    This line creates a VideoFileClip object by specifying the filename of a random background video and a duration. The filename is constructed using an f-string that concatenates bgDir, bgPrefix, bgIndex, and .mp4. The audio argument is set to False to indicate that the video should not include audio. The subclip() method is called to create a new VideoFileClip object that contains only the first script.getDuration() seconds of the video. This new object is assigned to the variable backgroundVideo.
    '''
    backgroundVideo = VideoFileClip(
        filename=f"{bgDir}/{bgPrefix}{bgIndex}.mp4", 
        audio=False).subclip(0, script.getDuration())
    w, h = backgroundVideo.size # This line retrieves the width and height of the backgroundVideo clip using its size attribute and assigns them to the variables w and h, respectively.

    def __createClip(screenShotFile, audioClip, marginSize): # This line defines a new function called __createClip that takes three arguments: screenShotFile, which is the filename of a screenshot image; audioClip, which is an AudioFileClip object representing the audio for the video clip; and marginSize, which is the size of the margin to be added around the screenshot image.

        '''
        This line creates an ImageClip object from the screenshot image file specified in the screenShotFile argument, with a duration equal to the duration of the audioClip argument. The set_position() method is called to set the position of the image in the center of the video frame.
        '''
        imageClip = ImageClip(
            screenShotFile,
            duration=audioClip.duration
            ).set_position(("center", "center"))
        imageClip = imageClip.resize(width=(w-marginSize)) # This line resizes the imageClip object by calling its resize() method with a width argument equal to the width of the background video (w) minus the marginSize argument. The height is automatically adjusted to maintain the aspect ratio of the image.
        videoClip = imageClip.set_audio(audioClip) # This line sets the audio for the imageClip object by calling its set_audio() method with the audioClip argument. The resulting object is assigned to the videoClip variable.
        videoClip.fps = 1 # This line sets the frame rate of the videoClip object to 1 frame per second, since each frame will represent one second of audio.
        return videoClip # This line returns the videoClip object created by the function.

    # Create video clips
    print("Editing clips together...") # This line prints the message "Editing clips together..." to the console, indicating that the video clips are being edited together.
    clips = [] # This line creates an empty list called clips, which will be used to store the video clips that are created.
    marginSize = int(config["Video"]["MarginSize"]) # This line retrieves the value of the MarginSize key from the [Video] section of the configuration file, converts it to an integer using the int() function, and assigns it to the variable marginSize.
    clips.append(__createClip(script.titleSCFile, script.titleAudioClip, marginSize)) # This line creates a new video clip using the __createClip() function and the title screenshot image and audio clip from the script object, with the specified marginSize. The resulting clip is added to the clips list using its append() method.
    for comment in script.frames: # This line starts a for loop that iterates over each Comment object in the frames list of the script object.
        clips.append(__createClip(comment.screenShotFile, comment.audioClip, marginSize)) # This line creates a new video clip using the __createClip() function and the screenshot image and audio clip from the current Comment object in the loop, with the specified marginSize. The resulting clip is added to the clips list using its append() method.

    # Merge clips into single track
    '''
    This line concatenates all the video clips in the clips list using the concatenate_videoclips() function from the moviepy.video.compositing.concatenate module. This function takes a list of VideoClip objects and returns a new VideoClip object that is the concatenation of all the input clips. The resulting clip is assigned to the contentOverlay variable.
The set_position(("center", "center")) method is called on the contentOverlay object to set its position in the center of the video frame. This method takes a tuple with two strings as an argument, where the first string specifies the horizontal position (either "left", "center", or "right") and the second string specifies the vertical position (either "top", "center", or "bottom"). In this case, both strings are set to "center" to position the video clip in the center of the frame both horizontally and vertically.
    '''
    contentOverlay = concatenate_videoclips(clips).set_position(("center", "center"))

    # Compose background/foreground

    '''
    This line creates a new CompositeVideoClip object called final using the CompositeVideoClip() function from the moviepy.video.compositing.CompositeVideoClip module. The clips argument is set to a list containing two VideoClip objects: backgroundVideo and contentOverlay. The size argument is set to the size of the backgroundVideo clip. This function creates a new VideoClip object that is a composite of the two input clips, with the contentOverlay clip overlaid on top of the backgroundVideo clip.
    This line sets the audio for the final clip to the audio from the contentOverlay clip, by calling its set_audio() method with the audio attribute of the contentOverlay clip.
    '''
    final = CompositeVideoClip(
        clips=[backgroundVideo, contentOverlay], 
        size=backgroundVideo.size).set_audio(contentOverlay.audio)
    final.duration = script.getDuration() # This line sets the duration of the final clip to the duration of the script object (i.e., the length of the audio clip associated with the script).
    final.set_fps(backgroundVideo.fps) # This line sets the frame rate of the final clip to the frame rate of the backgroundVideo clip, by calling its set_fps() method with the fps attribute of the backgroundVideo clip. This ensures that the frame rate of the composite clip matches the frame rate of the background video.

    # Write output to file
    print("Rendering final video...") # This line prints the message "Rendering final video..." to the console, indicating that the final video is being rendered.
    bitrate = config["Video"]["Bitrate"] # This line retrieves the value of the Bitrate key from the [Video] section of the configuration file, and assigns it to the variable bitrate.
    threads = config["Video"]["Threads"] # This line retrieves the value of the Threads key from the [Video] section of the configuration file, and assigns it to the variable threads.
    outputFile = f"{outputDir}/{fileName}.mp4" # This line constructs the output filename for the final video by concatenating the outputDir variable, which contains the output directory specified in the configuration file, with the fileName variable, which contains the filename of the script, and the ".mp4" file extension. The resulting string is assigned to the variable outputFile.

    '''
    This line writes the final clip to a video file using the write_videofile() method. The outputFile argument specifies the filename of the output file. The codec argument specifies the video codec to be used (in this case, MPEG-4). The threads argument specifies the number of threads to use for encoding the video. The bitrate argument specifies the target bitrate for the output video.
    '''
    final.write_videofile(
        outputFile, 
        codec = 'mpeg4',
        threads = threads, 
        bitrate = bitrate
    )
    print(f"Video completed in {time.time() - startTime}") # This line prints the message "Video completed in [elapsed time]" to the console, where [elapsed time] is the difference between the current time and the startTime variable, which was set earlier in the script. This message indicates that the video rendering process is complete and reports the elapsed time.

    # Preview in VLC for approval before uploading
    if (config["General"].getboolean("PreviewBeforeUpload")): # This line checks if the PreviewBeforeUpload key in the [General] section of the configuration file is set to True. If it is, the video will be played back for review before continuing with the upload process.
        vlcPath = config["General"]["VLCPath"] # This line retrieves the value of the VLCPath key from the [General] section of the configuration file, which specifies the path to the VLC media player executable.
        p = subprocess.Popen([vlcPath, outputFile]) # This line creates a new subprocess using the Popen() function from the subprocess module. The first argument is a list containing two elements: vlcPath, which is the path to the VLC media player executable, and outputFile, which is the path to the output video file. This will launch the VLC media player and play back the video file.
        print("Waiting for video review. Type anything to continue") # This line prints the message "Waiting for video review. Type anything to continue" to the console, indicating that the program is waiting for user input to continue.
        wait = input() # This line waits for user input from the console. Once the user has typed anything and pressed enter, the program will continue.

    print("Video is ready to upload!") # This line prints the message "Video is ready to upload!" to the console, indicating that the final video has been successfully created and is ready to be uploaded.
    print(f"Title: {script.title}  File: {outputFile}") # This line prints the title of the script and the filename of the output video file to the console, indicating the details of the final video.
    endTime = time.time() # This line records the current time as endTime using the time.time() function from the time module.
    print(f"Total time: {endTime - startTime}") # This line calculates the total time taken to create the final video by subtracting the startTime value from the endTime value, and prints the result to the console.

if __name__ == "__main__":
    createVideo()

    '''
    This is a conditional statement that checks whether the script is being run as the main program. If the script is being run as the main program, the createVideo() function is called to create the final video.

The __name__ variable is a built-in Python variable that holds the name of the current module. When a Python script is executed, its __name__ variable is set to "__main__" to indicate that it is the main program being run.

By using this conditional statement, the createVideo() function will only be executed if the script is being run as the main program. If the script is being imported as a module into another Python script, the createVideo() function will not be executed automatically.
    '''