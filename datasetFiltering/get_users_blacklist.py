import matplotlib.pyplot as plt
import plotly.plotly as py
from load_jsons import *
import collections

posts_TH = 50  # Will discard users having more than this publications, they are probably spam
createBlacklist = True

data = load("../../../ssd2/instaBarcelona/json/")
print "Number of jsons: " + str(len(data))

# Plot num of publications of top  users
users = {}
for k, v in data.iteritems():
    if v['owner']['id'] not in users:
        users[v['owner']['id']] = 1
    else:
        users[v['owner']['id']] = users[v['owner']['id']] + 1

print "Number of authors: " + str(len(users))
print "User with max publications has:  " + str(max(users.values()))

topX = 10000
user_publis_sorted = users.values()
user_publis_sorted.sort(reverse=True)
x = range(topX)
width = 1/1.5
plt.ylim([0,2000])
plt.bar(x, user_publis_sorted[0:topX], width, color="brown")
# plt.title("Number of posts of top" + str(topX) + "authors")
plt.show()

if createBlacklist:
    # Create a blacklist of users: That will be users having more than X publications (100)
    print "Creating users black list"
    users_blacklist = open("../../../ssd2/instaBarcelona/users_blacklist" + str(posts_TH) + ".txt","w")
    blacklisted = 0
    for user, num in users.iteritems():
        if num > posts_TH:
            blacklisted += 1
            users_blacklist.write(str(user) + '\n')
    print "Num of blacklisted users: " + str(blacklisted)


# Plot num of likes
# likes_tens = {}
# likes_hundreds = {}
#
# for k, v in data.iteritems():
#     likes_ten = round(v['likes']['count'] / 10)
#     if likes_ten not in likes_tens:
#         likes_tens[likes_ten] = 1
#     else:
#         likes_tens[likes_ten] = likes_tens[likes_ten] + 1
#
#
# print "Number of different likes values (ten): " + str(len(likes_tens))
# print "Publication with max likes has (ten):  " + str(max(likes_tens.values()))
#
# topX = 10
#
# likes_tens_ordered = collections.OrderedDict(sorted(likes_tens.items()))
#
# if len(likes_tens_ordered.values()) < topX:
#     print "Not enought likes to print tens"
# else:
#     likes_publis_sorted = likes_tens_ordered.values()
#     likes_publis_sorted.sort(reverse=True)
#     my_xticks = ['0-5', '5-15', '15-25', '25-35','35-45', '45-55', '55-65', '75-85', '85-95','95-105']
#     x = range(topX)
#     plt.xticks(x, my_xticks)
#     width = 1/1.5
#     plt.bar(x, likes_publis_sorted[0:topX], width, color="blue")
#     plt.title("Likes of top posts (tens)")
#     plt.show()


print "Done"

