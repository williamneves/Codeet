
# import the regex module
import re

# function to print all the hashtags in a text


def extract_hashtags(text):

    # the regular expression
    regex = "#(\w+)"

    # extracting the hashtags
    hashtag_list = re.findall(regex, text)

    # printing the hashtag_list
    print("The hashtags in \"" + text + "\" are :")
    for hashtag in hashtag_list:
        print(hashtag)


text1 = "GeeksforGeeks is a wonderful #website for #ComputerScience"
text2 = "This day is beautiful ! #instagood #photooftheday #cute"
extract_hashtags(text1)
extract_hashtags(text2)
