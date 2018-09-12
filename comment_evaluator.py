#Ivan Vigliante
#ID: 80573300
#CS2302 MW 10:30am - 11:50am Lab 1B
#Professor Aguirre, Diego
#TA Saha, Manoj
#Date of last modification: 09-12-2018
# This program gets the comments from a reddit post and
# recursively analyzes each comment, categorizing them by
# whether they are positive, negative, or neutral comments. 

import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import praw
import time

reddit = praw.Reddit(client_id = 'iRh4lfXV9UHfmw',
                     client_secret = 'RiIrEinG5MNDEt2e3pUYjpS-gXM',
                     user_agent = 'my user agent')

nltk.download('vader_lexicon')
sid = SentimentIntensityAnalyzer()

def get_text_negative_proba(text):
    return sid.polarity_scores(text)['neg']

def get_text_neutral_proba(text):
    return sid.polarity_scores(text)['neu']

def get_text_positive_proba(text):
    return sid.polarity_scores(text)['pos']

def get_submission_comments(url):
    submission = reddit.submission(url=url)
    submission.comments.replace_more()
    
    return submission.comments

def process_comments(comment_forest):
    #if comments list is empty, return
    if len(comment_forest) == 0:
        return [],[],[]

    neg_list, neu_list, pos_list = [], [], []

    #Get comment evaluations
    d = {
        'neu_prob': get_text_neutral_proba(comment_forest[0].body),
        'neg_prob': get_text_negative_proba(comment_forest[0].body),
        'pos_prob': get_text_positive_proba(comment_forest[0].body)
        }
    #Get highest value and store
    max_prob = max(d, key=d.get)
    
    #Append max_prob to its respective list
    
    # If the probability of comment being negative >0.3 also add to list, sentiment
    # analyzer has trouble distinguishing between neutral and negative(or positive) comments
    if max_prob == 'neg_prob' or d['neg_prob']>0.3:
        neg_list.append(comment_forest[0].body)
    
    elif max_prob == 'pos_prob' or d['pos_prob']>0.3:
        pos_list.append(comment_forest[0].body)
    
    else:
        neu_list.append(comment_forest[0].body)
    
    #If there are replies to the current comment, process replies
    if len(comment_forest[0].replies) >= 1:
        temp_neg_list, temp_neu_list, temp_pos_list = process_comments(comment_forest[0].replies)
        neg_list.extend(temp_neg_list), neu_list.extend(temp_neu_list), pos_list.extend(temp_pos_list)
    
    #If there are more same level comments, process the next comments
    if len(comment_forest) > 1:
        temp_neg_list, temp_neu_list, temp_pos_list = process_comments(comment_forest[1:])
        neg_list.extend(temp_neg_list), neu_list.extend(temp_neu_list), pos_list.extend(temp_pos_list)
    
    #Return the response lists once finished
    return neg_list, neu_list, pos_list
    
def main():
    #Gather comments from three posts
    comments_pos_expected = get_submission_comments('https://www.reddit.com/r/MakeupAddiction/comments/9eqlrj/my_everyday_no_makeup_base_with_a_pop_of_color/')
    comments_neg_expected = get_submission_comments('https://www.reddit.com/r/The_Donald/comments/9984v4/just_a_reminder_to_the_snowflakes_trying_to_bring/')
    comments_neu_expected = get_submission_comments('https://www.reddit.com/r/MrRobot/comments/9euji7/no_spoilers_halloween_costume_check/')
    
    #Put comment forests in a list to simplify analyzing and printing
    list_of_comments = [comments_pos_expected, comments_neg_expected, comments_neu_expected]
   
    # for each comment forest, categorize comments into negative, neutral
    # and positive lists and print
    for i in range(len(list_of_comments)):
        start_time = time.time()
        neg_list, neu_list, pos_list = process_comments(list_of_comments[i])
        end_time = (time.time() - start_time)
        
        print('----- Analysis ', i+1, '-----')
        print('Runtime of process_comments() method: %.2f seconds' % end_time)
        print('Comments analyzed: ', len(neg_list) + len(neu_list) + len(pos_list))
        print('Negative comments: ', len(neg_list))
        print('Neutral comments: ', len(neu_list))
        print('Positive comments: ', len(pos_list))
        
        #Gives user the option to print comments by category or move on
        while True:
            prompt = input(' [0]: Continue to next analysis.\n [1]: Print negative comments.\n [2]: Print neutral comments.\n [3]: Print positive comments.\n')
           
            if prompt == '0':
                break
            elif prompt == '1':
                print(neg_list)
            elif prompt == '2':
                print(neu_list)
            elif prompt == '3':
                print(pos_list)
            else:
                print('Command not recognized. Try again.')
            continue
        

main()