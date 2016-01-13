import string, praw, OAuth2Util, time
from operator import itemgetter



#Variables to Change
subname = 'photoshopbattles' #Subreddit to gather data from
post_to_sub = 'battletalk' #Subreddit to post report to
username = '_korbendallas_'
user_agent = '_korbendallas_ by /u/_korbendallas_ ver 0.1'


#Global Variables
submission_data = [] #Submission_Title, Submission_Author, Submission_Short_Link, Submission_Score, Submission_Short_Link, Submission_Created_Epoch, Submission_Created_GMT
top_submissions = ['Score|Author|Post Title', ':---|:---|:---']
submission_authors = [] #Total_Score, Author, Count
total_submission_count = 0
top_submission_authors = ['Author|Total Score|Submission Count|Submission Average', ':---|:---|:---|:---']
total_submission_authors = 0
    
comment_data = []
top_comments = ['Score|Author|Comment', ':---|:---|:---']
comment_authors = [] #Total_Score, Author, Count
total_comment_count = 0 #Comment_Body, Comment_Author, Comment_Score, Comment_Link, Submission_Title
top_comment_authors = ['Author|Total Score|Comment Count|Comment Average', ':---|:---|:---|:---']
total_comment_authors = 0


    
def Main():    

    #Login
    r = praw.Reddit(user_agent)
    o = OAuth2Util.praw.AuthenticatedReddit.login(r, disable_warning=True)
    sub = r.get_subreddit(subname)

    gather_data(r, sub)
    process_submission_data()
    process_comment_data()
    submit_report(r)


    return


def gather_data(r, sub):

    print 'Gathering Data'

    global submission_data
    global comment_data

    #Gather submissions from the week
    submissions = sub.get_top_from_week(limit=None)

    
    #Go through each submission
    for submission in submissions:

        try:

            #Disregard deleted or removed posts
            if submission.author and submission.banned_by == None:

                submission_data_row = []

                submission_data_row.append(str(submission.title))  #Submission_Title
                submission_data_row.append('/u/' + str(submission.author.name))  #Submission_Author
                submission_data_row.append(str(submission.short_link))  #Submission_Short_Link
                submission_data_row.append(int(submission.score))  #Submission_Score
                submission_data_row.append(str(submission.short_link))  #Submission_Short_Link
                submission_data_row.append(float(submission.created_utc))  #Submission_Created_Epoch
                submission_data_row.append(str(time.strftime('%m/%d/%Y %H:%M:%S', time.gmtime(float(submission.created_utc)))))  #Submission_Created_GMT

                submission_data.append(submission_data_row)
                

                #Get the comments
                submission.replace_more_comments(limit=None, threshold=0)
                comments = praw.helpers.flatten_tree(submission.comments)

                #Disregard submissions with no comments
                if comments:

                    #Go through each comment
                    for comment in comments:

                        try:

                            #Disregard deleted comments
                            if comment.author and comment.banned_by == None:

                                comment_data_row = []

                                comment_data_row.append(string.replace(string.replace(str(comment.body), '\r', ' '), '\n', ' '))  #Comment_Body
                                comment_data_row.append('/u/' + str(comment.author.name))  #Comment_Author
                                comment_data_row.append(int(comment.score))  #Comment_Score
                                comment_data_row.append(str(comment.permalink))  #Comment_Link
                                comment_data_row.append(str(submission.title))  #Submission_Title

                                comment_data.append(comment_data_row)


                        except (Exception) as e:

                            print e.message

        except (Exception) as e:

            print e.message


    return


def process_submission_data():

    print 'Processing Submissions'

    global submission_data
    global top_submissions
    global submission_authors
    global total_submission_count
    global top_submission_authors
    global total_submission_authors
    
    submission_data = reversed(sorted(submission_data, key=itemgetter(3)))
    total_submission_count

    for submission_data_row in submission_data:

        total_submission_count += 1
        
        #Create Top 25 Submission Table
        if len(top_submissions) < 28:
            top_submissions.append(str(submission_data_row[3]) + '|' + submission_data_row[1] + '|[' + submission_data_row[0] + '](' + submission_data_row[2] + ')')
            
        #Compile Top Submission Author Scores
        if submission_authors:
            if submission_data_row[1] in [submission_authors_row[1] for submission_authors_row in submission_authors]:
                submission_authors[[submission_authors_row[1] for submission_authors_row in submission_authors].index(submission_data_row[1])][0] += submission_data_row[3]
                submission_authors[[submission_authors_row[1] for submission_authors_row in submission_authors].index(submission_data_row[1])][2] += 1
            else:
                submission_authors.append([submission_data_row[3], submission_data_row[1], 1])
        else:
            submission_authors.append([submission_data_row[3], submission_data_row[1], 1])

    #Compile Top Submission Author Table
    submission_authors = reversed(sorted(submission_authors, key=itemgetter(0)))

    for submission_author in submission_authors:
        total_submission_authors += 1
        if len(top_submission_authors) < 28:
            top_submission_authors.append(submission_author[1] + '|' + str(submission_author[0]) + '|' + str(submission_author[2]) + '|' + str(float(submission_author[0]) / float(submission_author[2])))
        else:
            break

        
    return


def process_comment_data():

    print 'Processing Comments'

    global comment_data
    global top_comments
    global comment_authors
    global total_comment_count
    global top_comment_authors
    global total_comment_authors
    
    comment_data = reversed(sorted(comment_data, key=itemgetter(2)))

    for comment_data_row in comment_data:

        total_comment_count += 1

        #Create Top 25 Comments Table
        if len(top_comments) < 28:
            top_comments.append(str(comment_data_row[2]) + '|' + comment_data_row[1] + '|[' + comment_data_row[4] + '](' + comment_data_row[3] + '?context=1000)')

        #Compile Top Comment Author Scores
        if comment_authors:
            if comment_data_row[1] in [comment_authors_row[1] for comment_authors_row in comment_authors]:
                comment_authors[[comment_authors_row[1] for comment_authors_row in comment_authors].index(comment_data_row[1])][0] += comment_data_row[2]
                comment_authors[[comment_authors_row[1] for comment_authors_row in comment_authors].index(comment_data_row[1])][2] += 1
            else:
                comment_authors.append([comment_data_row[2], comment_data_row[1], 1])
        else:
            comment_authors.append([comment_data_row[2], comment_data_row[1], 1])

    #Compile Top Comment Author Table
    comment_authors = reversed(sorted(comment_authors, key=itemgetter(0)))

    for comment_author in comment_authors:
        total_comment_authors += 1
        if len(top_comment_authors) < 28:
            top_comment_authors.append(comment_author[1] + '|' + str(comment_author[0]) + '|' + str(comment_author[2]) + '|' + str(float(comment_author[0]) / float(comment_author[2])))


    return
    

def submit_report(r):

    print 'Compiling and Submitting Report'

    global subname
    global post_to_sub

    global submission_data
    global top_submissions
    global submission_authors
    global total_submission_count
    global top_submission_authors
    global total_submission_authors

    global comment_data
    global top_comments
    global comment_authors
    global total_comment_count
    global top_comment_authors
    global total_comment_authors


    report_text = ['#Weekly Report for /r/' + subname]
    report_text.append('---')

    report_text.append('---')
    report_text.append('#Submissions')
    report_text.append('---')
    
    report_text.append('---')
    report_text.append('Total Submissions: ' + str(total_submission_count))
    report_text.append('Total Submission Authors: ' + str(total_submission_authors))
    report_text.append('---')

    report_text.append('###Top 25 Submissions')
    report_text.append('\r\n'.join(top_submissions))
    report_text.append('---')

    report_text.append('###Top 25 Submitters')
    report_text.append('\r\n'.join(top_submission_authors))
    report_text.append('---')


    report_text.append('---')
    report_text.append('#Comments')
    report_text.append('---')
    
    report_text.append('---')
    report_text.append('Total Comments: ' + str(total_comment_count))
    report_text.append('Total Comment Authors: ' + str(total_comment_authors))
    report_text.append('---')
    
    report_text.append('###Top 25 Comments')
    report_text.append('\r\n'.join(top_comments))
    report_text.append('---')

    report_text.append('###Top 25 Commenters')
    report_text.append('\r\n'.join(top_comment_authors))
    report_text.append('---')
    
    
    report_text.append('---')
    report_text.append('^(created by /u/_korbendallas_)')
    report_text.append('---')


    #Submit Report
    post_title = 'Weekly Report for /r/' + subname + ' - ' + str(time.strftime('%A, %B %d, %Y', time.gmtime(float(submission.created_utc))))
    r.submit(post_to_sub, post_title, text='\r\n\r\n'.join(report_text))
    
            
    return




Main()



