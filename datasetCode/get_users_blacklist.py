import matplotlib.pyplot as plt
import plotly.plotly as py
from load_jsons import *
import collections

createBlacklist = True

data = load("../../datasets/instaBarcelona/json_toy/")
print "Number of jsons: " + str(len(data))

# Plot num of publications of top  users
users = {}
for k, v in data.iteritems():
    if v['owner']['id'] not in users:
        users[v['owner']['id']] = 1
    else:
        users[v['owner']['id']] = users[v['owner']['id']] + 1

print "Number of users: " + str(len(users))
print "User with max publications has:  " + str(max(users.values()))

topX = 100
user_publis_sorted = users.values()
user_publis_sorted.sort(reverse=True)
x = range(topX)
width = 1/1.5
plt.bar(x, user_publis_sorted[0:topX], width, color="blue")
plt.title("Num of posts of top authors")
plt.show()
print "Done"

if createBlacklist:
    # Create a blacklist of users: That will be users having more than X publications (100)
    print "Creating users black list"
    users_blacklist = open("../../datasets/instaBarcelona/users_blacklist.txt","w")
    posts_TH = 5 #Will discard users having more than 100 publications, they are probably spam
    blacklisted = 0
    for user, num in users.iteritems():
        if num > posts_TH:
            blacklisted += 1
            users_blacklist.write(str(user) + '\n')
    print "Num of blacklisted users: " + str(blacklisted)


# Plot num of likes
likes_tens = {}
likes_hundreds = {}

for k, v in data.iteritems():
    likes_ten = round(v['likes']['count'] / 10)
    if likes_ten not in likes_tens:
        likes_tens[likes_ten] = 1
    else:
        likes_tens[likes_ten] = likes_tens[likes_ten] + 1


print "Number of different likes values (ten): " + str(len(likes_tens))
print "Publication with max likes has (ten):  " + str(max(likes_tens.values()))

topX = 10

likes_tens_ordered = collections.OrderedDict(sorted(likes_tens.items()))

if len(likes_tens_ordered.values()) < topX:
    print "Not enought likes to print tens"
else:
    likes_publis_sorted = likes_tens_ordered.values()
    likes_publis_sorted.sort(reverse=True)
    my_xticks = ['0-5', '5-15', '15-25', '25-35','35-45', '45-55', '55-65', '75-85', '85-95','95-105']
    x = range(topX)
    plt.xticks(x, my_xticks)
    width = 1/1.5
    plt.bar(x, likes_publis_sorted[0:topX], width, color="blue")
    plt.title("Likes of top posts (tens)")
    plt.show()


print "Done"
