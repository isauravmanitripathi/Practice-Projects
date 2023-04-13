from datetime import datetime # This line imports the datetime class from the datetime module. The datetime class provides various functions and attributes to work with dates and times.
from moviepy.editor import AudioFileClip # This line imports the AudioFileClip class from the moviepy.editor package. The AudioFileClip class is part of the MoviePy library, a powerful video editing library in Python. The AudioFileClip class allows you to create and manipulate audio clips.
import voiceover # This line imports the voiceover module. The module is not part of Python's standard library or any well-known library, so it is likely a custom module that generates voiceovers for video projects.

MAX_WORDS_PER_COMMENT = 100 # This line sets the MAX_WORDS_PER_COMMENT variable to the integer 100. This variable likely defines the maximum number of words allowed per comment when processing Reddit comments for the video project.
MIN_COMMENTS_FOR_FINISH = 4 # This line sets the MIN_COMMENTS_FOR_FINISH variable to the integer 4. This variable likely defines the minimum number of comments required to consider the video project complete.
MIN_DURATION = 20 # This line sets the MIN_DURATION variable to the integer 20. This variable likely defines the minimum duration (in seconds) that a video project should have.
MAX_DURATION = 58 # This line sets the MAX_DURATION variable to the integer 58. This variable likely defines the maximum duration (in seconds) that a video project should have.

class VideoScript: # This line defines the VideoScript class.
    title = "" #  This attribute stores the title of the Reddit post as a string.
    fileName = "" # This attribute stores the filename (without an extension) that will be used for the video file as a string.
    titleSCFile = "" # This attribute stores the filename of the screenshot of the Reddit post's title as a string.
    url = "" # This attribute stores the URL of the Reddit post as a string.
    totalDuration = 0 # This attribute stores the total duration of the video project as an integer. The duration is calculated based on the sum of the durations of the individual comment scenes.
    frames = [] # This attribute is a list that stores instances of comment scenes (e.g., instances of a CommentFrame class or similar). Each scene typically contains information like the comment text, the duration of the scene, and the filename of the screenshot of the comment.

    def __init__(self, url, title, fileId) -> None: # This line defines the constructor of the VideoScript class, which takes three parameters: url (a string representing the URL of the Reddit post), title (a string representing the title of the Reddit post), and fileId (a string representing a unique identifier for the video file).
        self.fileName = f"{datetime.today().strftime('%Y-%m-%d')}-{fileId}" # This line creates a formatted string containing the current date and the fileId parameter. The datetime.today().strftime('%Y-%m-%d') expression formats the current date as a string in the format "YYYY-MM-DD". The formatted string is assigned to the fileName attribute of the VideoScript instance.
        self.url = url # This line assigns the url parameter to the url attribute of the VideoScript instance.
        self.title = title # This line assigns the title parameter to the title attribute of the VideoScript instance.
        self.titleAudioClip = self.__createVoiceOver("title", title) # This line calls the private method __createVoiceOver with the arguments "title" and title. The __createVoiceOver method is not shown in this code snippet, but it likely generates a voiceover audio clip for the given text (the Reddit post's title in this case). The resulting audio clip is assigned to the titleAudioClip attribute of the VideoScript instance.

    def canBeFinished(self) -> bool: # This line defines the canBeFinished method, which takes no parameters other than self. The method returns a boolean value.

        '''
        This line returns a boolean value based on two conditions:
        len(self.frames) > 0: This condition checks whether the frames list of the VideoScript instance has at least one comment scene. It returns True if there is at least one comment scene and False otherwise.
        self.totalDuration > MIN_DURATION: This condition checks whether the total duration of the video project (stored in the totalDuration attribute) is greater than the minimum required duration defined by the MIN_DURATION variable. It returns True if the total duration is greater than the minimum required duration and False otherwise.
        '''
        return (len(self.frames) > 0) and (self.totalDuration > MIN_DURATION)

    def canQuickFinish(self) -> bool: # This line defines the canQuickFinish method, which takes no parameters other than self. The method returns a boolean value.
        '''
        This line returns a boolean value based on two conditions:
len(self.frames) >= MIN_COMMENTS_FOR_FINISH: This condition checks whether the frames list of the VideoScript instance has at least the minimum number of comment scenes required for a quick finish, as defined by the MIN_COMMENTS_FOR_FINISH variable. It returns True if the condition is met and False otherwise.
self.totalDuration > MIN_DURATION: This condition checks whether the total duration of the video project (stored in the totalDuration attribute) is greater than the minimum required duration defined by the MIN_DURATION variable. It returns True if the total duration is greater than the minimum required duration and False otherwise.

        '''
        return (len(self.frames) >= MIN_COMMENTS_FOR_FINISH) and (self.totalDuration > MIN_DURATION)

    def addCommentScene(self, text, commentId) -> None: # This line defines the addCommentScene method, which takes two parameters: text (a string representing the comment text) and commentId (a string representing the comment's unique identifier). The method returns None.
        wordCount = len(text.split()) #  This line splits the text parameter into a list of words and calculates the length of the list (i.e., the number of words in the text). The resulting word count is assigned to the wordCount variable.
        if (wordCount > MAX_WORDS_PER_COMMENT): # This line checks if the word count of the comment text is greater than the maximum allowed word count per comment, defined by the MAX_WORDS_PER_COMMENT variable. If the condition is true, the following line is executed:
            return True # This line returns True, indicating that adding the comment scene has failed due to exceeding the maximum allowed word count.
        frame = ScreenshotScene(text, commentId) # This line creates a new instance of the ScreenshotScene class (or a similar class) with the given text and commentId parameters. The resulting object is assigned to the frame variable.
        frame.audioClip = self.__createVoiceOver(commentId, text) # This line calls the private method __createVoiceOver with the arguments commentId and text. The method likely generates a voiceover audio clip for the given text (the comment text in this case). The resulting audio clip is assigned to the audioClip attribute of the frame object.
        if (frame.audioClip == None): # This line checks if the audioClip attribute of the frame object is None. If the condition is true, the following line is executed:
            return True # This line returns True, indicating that adding the comment scene has failed due to the inability to create the voiceover audio clip.
        self.frames.append(frame) # This line adds the frame object to the frames list of the VideoScript instance, effectively adding the comment scene to the video project.

    def getDuration(self): # This line defines the getDuration method, which takes no parameters other than self.
        return self.totalDuration # This line returns the value stored in the totalDuration attribute of the VideoScript instance, which represents the total duration of the video project.

    def getFileName(self): # This line defines the getFileName method, which takes no parameters other than self.
        return self.fileName # This line returns the value stored in the fileName attribute of the VideoScript instance, which represents the filename (without an extension) that will be used for the video file.

    def __createVoiceOver(self, name, text): #  This line defines the __createVoiceOver method, which takes two parameters: name (a string representing a name that will be used as part of the voiceover file name) and text (a string containing the text that will be used for the voiceover).
        file_path = voiceover.create_voice_over(f"{self.fileName}-{name}", text) # This line calls the create_voice_over function from the voiceover module with the given name and text parameters. The function likely generates a voiceover audio file for the given text and returns its file path. The resulting file path is assigned to the file_path variable.
        audioClip = AudioFileClip(file_path) #  This line creates an AudioFileClip object using the file_path variable. The AudioFileClip class is provided by the moviepy.editor module and represents an audio clip.
        if (self.totalDuration + audioClip.duration > MAX_DURATION): # This line checks if the sum of the current total duration of the video project (stored in the totalDuration attribute) and the duration of the newly created audioClip is greater than the maximum allowed duration, defined by the MAX_DURATION variable. If the condition is true, the following line is executed:
            return None # This line returns None, indicating that creating the voiceover audio clip has failed due to exceeding the maximum allowed duration.
        self.totalDuration += audioClip.duration # This line updates the totalDuration attribute of the VideoScript instance by adding the duration of the audioClip to it.
        return audioClip # This line returns the audioClip object, which represents the voiceover audio clip created for the given text.


class ScreenshotScene: # This line defines the ScreenshotScene class.
    text = "" # This line defines a class attribute named text with a default empty string value. This attribute will store the text of the comment.
    screenShotFile = "" # This line defines a class attribute named screenShotFile with a default empty string value. This attribute will store the file path of the screenshot taken for the comment.
    commentId = "" # This line defines a class attribute named commentId with a default empty string value. This attribute will store the unique identifier of the comment.

    def __init__(self, text, commentId) -> None: # This line defines the constructor method of the ScreenshotScene class, which takes two parameters: text (a string representing the comment text) and commentId (a string representing the comment's unique identifier). The constructor returns None.
        self.text = text # This line assigns the value of the text parameter to the text attribute of the ScreenshotScene instance.
        self.commentId = commentId #This line assigns the value of the commentId parameter to the commentId attribute of the ScreenshotScene instance.