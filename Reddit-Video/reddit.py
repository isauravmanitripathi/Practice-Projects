import os # This line imports the os module, which provides a way to interact with the operating system.
import re # This line imports the re module, which provides support for regular expressions in Python.
import praw # This line imports the praw module, which provides a Python interface to the Reddit API.
import markdown_to_text # This line imports a custom module called markdown_to_text, which contains a single function called markdown_to_text(). This function converts a Markdown-formatted string to plaintext.
import time # This line imports the time module, which provides various time-related functions.
from videoscript import VideoScript # This line imports the VideoScript class from the videoscript module. This class represents a script for a video.
import configparser # This line imports the configparser module, which provides a way to read configuration files in the INI file format.

config = configparser.ConfigParser() # This line creates a new ConfigParser object called config. This object provides methods for reading and writing configuration files in the INI file format.
config.read('config.ini') # This line reads the config.ini file and populates the config object with the configuration data.
CLIENT_ID = config["Reddit"]["CLIENT_ID"] # This line retrieves the value of the CLIENT_ID key from the [Reddit] section of the configuration file, and assigns it to the CLIENT_ID variable.
CLIENT_SECRET = config["Reddit"]["CLIENT_SECRET"] # This line retrieves the value of the CLIENT_SECRET key from the [Reddit] section of the configuration file, and assigns it to the CLIENT_SECRET variable.
USER_AGENT = config["Reddit"]["USER_AGENT"] # This line retrieves the value of the USER_AGENT key from the [Reddit] section of the configuration file, and assigns it to the USER_AGENT variable.
SUBREDDIT = config["Reddit"]["SUBREDDIT"] # This line retrieves the value of the SUBREDDIT key from the [Reddit] section of the configuration file, and assigns it to the SUBREDDIT variable.

def getContent(outputDir, postOptionCount) -> VideoScript:
    reddit = __getReddit() # This line calls a private function called __getReddit() to authenticate with the Reddit API and obtain a praw.Reddit instance, which represents a connection to the Reddit API.
    existingPostIds = __getExistingPostIds(outputDir) # This line calls a private function called __getExistingPostIds() to retrieve a list of the existing post IDs of previously processed videos from the outputDir directory.

    now = int(time.time()) # This line records the current time in seconds since the Unix epoch using the time.time() function, and converts it to an integer.
    autoSelect = postOptionCount == 0 # This line sets the autoSelect variable to True if postOptionCount is equal to zero, indicating that the function should automatically select the top post.
    posts = [] # This line creates an empty list called posts to store the selected posts.

    for submission in reddit.subreddit(SUBREDDIT).top(time_filter="day", limit=postOptionCount*3): # This line starts a for loop that iterates over the top posts of the specified subreddit, filtered by posts from the past day (time_filter="day") and limited to postOptionCount*3 posts.
        if (f"{submission.id}.mp4" in existingPostIds or submission.over_18): # This line checks if the current post has already been processed (by checking if its ID is in the existingPostIds list) or if it is marked as NSFW (submission.over_18). If either condition is true, the post is skipped.
            continue
        hoursAgoPosted = (now - submission.created_utc) / 3600 # This line calculates the number of hours since the current post was submitted, and assigns it to the hoursAgoPosted variable.
        print(f"[{len(posts)}] {submission.title}     {submission.score}    {'{:.1f}'.format(hoursAgoPosted)} hours ago") # This line prints the title, score, and age (in hours) of the current post to the console, along with its index in the posts list.
        posts.append(submission) # This line adds the current post to the posts list.
        if (autoSelect or len(posts) >= postOptionCount): # This line checks if `autoSelect` is `True` (indicating that the function should automatically select the top post), or if the number of selected posts is greater than or equal to `postOptionCount`. If either condition is true, the loop is exited.
            break

    if (autoSelect): # This line checks if autoSelect is True.
        return __getContentFromPost(posts[0]) # If autoSelect is True, this line calls a private function called __getContentFromPost() to download and process the content of the top post in the posts list, and returns the resulting VideoScript object.
    else: # If autoSelect is not True, this line executes the following block of code.
        postSelection = int(input("Input: ")) # This line prompts the user to enter an integer value, and assigns the value to the postSelection variable. This value represents the index of the post in the posts list that the user wants to select.
        selectedPost = posts[postSelection] # This line retrieves the post from the posts list at the index specified by the user, and assigns it to the selectedPost variable.
        return __getContentFromPost(selectedPost) # This line calls a private function called __getContentFromPost() to download and process the content of the selected post, and returns the resulting VideoScript object.

def getContentFromId(outputDir, submissionId) -> VideoScript: #  This line defines the function getContentFromId, which takes two parameters: outputDir and submissionId. The return type of this function is VideoScript.
    reddit = __getReddit() # This line calls a private function __getReddit(), which presumably returns an authenticated Reddit API instance, and assigns it to the variable reddit.
    existingPostIds = __getExistingPostIds(outputDir) # This line calls another private function __getExistingPostIds(outputDir), passing the outputDir as an argument. This function likely returns a list of existing post IDs that have been previously processed, which is then assigned to the variable existingPostIds.
    
    if (submissionId in existingPostIds): #  This line checks if the given submissionId is already in the list of existingPostIds.
        print("Video already exists!") # If the submission ID exists in the list, this line prints a message indicating that the video already exists.
        exit() # This line exits the program if the video already exists, preventing further processing.
    try: # This line starts a try-except block to handle potential errors.
        submission = reddit.submission(submissionId) # Within the try block, this line retrieves the Reddit submission object with the given submissionId using the authenticated Reddit API instance.
    except: #  If an exception occurs (e.g., the submission is not found), the code execution moves to the except block.
        print(f"Submission with id '{submissionId}' not found!") # This line prints an error message indicating that the submission with the specified ID was not found.
        exit() #  This line exits the program if the submission was not found, preventing further processing.
    return __getContentFromPost(submission) # This line calls a private function __getContentFromPost(submission) and returns its result. The function likely processes the Reddit submission and returns a VideoScript object containing the extracted content.

def __getReddit(): # This line defines the private function __getReddit(), which takes no arguments.
    return praw.Reddit( # This line starts the return statement, creating a new instance of the praw.Reddit class.
        client_id=CLIENT_ID, # This line sets the client_id parameter for the praw.Reddit class. CLIENT_ID is a constant that holds the unique identifier of your registered Reddit application.
        client_secret=CLIENT_SECRET, # This line sets the client_secret parameter for the praw.Reddit class. CLIENT_SECRET is a constant that holds the secret key of your registered Reddit application.
        user_agent=USER_AGENT # This line sets the user_agent parameter for the praw.Reddit class. USER_AGENT is a constant that holds a user agent string, which should provide information about your application and should follow Reddit's user agent guidelines.
    ) # This line closes the praw.Reddit constructor.

'''
In summary, the __getReddit() function creates a new instance of the praw.Reddit class using the specified CLIENT_ID, CLIENT_SECRET, and USER_AGENT. This instance represents a connection to the Reddit API and is used to make requests to retrieve and process Reddit data.
'''


def __getContentFromPost(submission) -> VideoScript: # This line defines the private function __getContentFromPost, which takes a single parameter submission. The return type of this function is VideoScript.
    content = VideoScript(submission.url, submission.title, submission.id) # This line initializes a new VideoScript object using the submission's URL, title, and ID, and assigns it to the variable content.
    print(f"Creating video for post: {submission.title}") # This line prints a message indicating that a video is being created for the given post, displaying the post's title.
    print(f"Url: {submission.url}") # This line prints the URL of the submission.

    failedAttempts = 0 # This line initializes a variable failedAttempts with the value 0, which will be used to count the number of failed attempts to add comment scenes.
    for comment in submission.comments: #  This line starts a loop that iterates over each comment in the submission's comments.
        if(content.addCommentScene(markdown_to_text.markdown_to_text(comment.body), comment.id)): # This line calls the addCommentScene method of the content object, passing the comment's body after converting it from markdown to text and the comment's ID. If the addCommentScene method returns True, it means that the comment scene could not be added, so the code enters the if block.
            failedAttempts += 1 # If the previous line returns True, this line increments the failedAttempts counter by 1.
        if (content.canQuickFinish() or (failedAttempts > 2 and content.canBeFinished())): # This line checks if any of the following conditions are met: the content object can be quickly finished, or there have been more than two failed attempts and the content object can be finished. If either condition is met, the code enters the if block.
            break #  If the conditions in the previous line are met, this line breaks out of the loop, stopping the iteration over the comments.
    return content # This line returns the content object, which is an instance of the VideoScript class containing the processed submission data.

def __getExistingPostIds(outputDir):
    files = os.listdir(outputDir)
    # I'm sure anyone knowledgeable on python hates this. I had some weird 
    # issues and frankly didn't care to troubleshoot. It works though...
    files = [f for f in files if os.path.isfile(outputDir+'/'+f)]
    return [re.sub(r'.*?-', '', file) for file in files]
