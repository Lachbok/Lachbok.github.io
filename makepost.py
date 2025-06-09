from datetime import datetime
import os

#process the post and save to /posts folder
with open("post.txt", "r", encoding="utf-8") as file:
    title = file.readline().replace('\n','')
    if not len(title)>0:
        posting = False
    else:
        posting = True
    text = file.read().replace('\n','<br>\n')
now = datetime.now()
formatted = now.strftime("%Y-%m-%d %H:%M:%S")
if posting:
    post = f"<div class='postcontainer'>\n<p class='posttime'>{formatted}</p><p class='posttitle'>{title}</p>\n<p class='posttext'>{text}\n</p>\n</div>\n"
    with open(f"posts/{title}_{formatted.replace(':','-')}.txt".replace(' ','_'), "w", encoding="utf-8") as save:
        save.write(post)

#delete post.txt
with open("post.txt", "w", encoding="utf-8") as file:
    file.write('')
    
#loop through all posts and compile string
folder_path = "posts"
sorted_posts = [] #descending order (newest first)
for filename in os.listdir(folder_path):
    timestamp = ''.join(filename.split('_')[-2:]).replace('-','') #["YEAR-MONTH-DAY","HOUR-MINUTE-SECOND"] -> "YEARMONTHDAYHOURMINUTESECOND"
    if len(sorted_posts)==0:
        sorted_posts.append([timestamp,filename])
        continue
    else: #binary search and place at index
        length = len(sorted_posts)
        upper = length-1
        lower = 0
        while True:
            mid = (upper+lower)//2
            midts = sorted_posts[mid][0]
            if timestamp>midts:
                if mid+1<length and timestamp<sorted_posts[mid+1][0]:
                    #put at index mid+1
                    sorted_posts.insert(mid+1,[timestamp,filename])
                    break
                elif not mid+1<length: #aka mid==len-1
                    #put as very last element
                    sorted_posts.append([timestamp,filename])
                    break
                else:
                    lower = mid+1
                    continue
            elif timestamp<midts:
                if mid-1>-1 and timestamp>sorted_posts[mid-1][0]:
                    #put at index mid-1
                    sorted_posts.insert(mid-1,[timestamp,filename])
                    break
                elif not mid-1>-1: #aka mid==0
                    #put as very first element
                    sorted_posts.insert(0,[timestamp,filename])
                    break
                else:
                    upper = mid
                    continue
            else:
                print("Two posts have same timestamp, probably duplicates.")
                continue

#compile sorted posts into a string
sorted_posts.reverse()
all_posts = ''
for post in sorted_posts:
    full_path = os.path.join(folder_path, post[1])
    with open(full_path, "r", encoding="utf-8") as file:
        all_posts += file.read()

#get the base index
with open("baseindex.html", "r", encoding="utf-8") as file:
    content = file.read()

new = content.replace('$POSTHERE$',all_posts)
with open("index.html", "w", encoding="utf-8") as file:
    file.write(new)

