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
    with open(f"posts/{title}-{formatted.replace(':','-')}.txt".replace(' ','_'), "w", encoding="utf-8") as save:
        save.write(post)

#delete post.txt
with open("post.txt", "w", encoding="utf-8") as file:
    file.write('')
    
#loop through all posts and compile string
all_posts = ''
folder_path = "posts"
for filename in os.listdir(folder_path):
    full_path = os.path.join(folder_path, filename)
    with open(full_path, "r", encoding="utf-8") as file:
        all_posts += file.read()

#get the base index
with open("baseindex.html", "r", encoding="utf-8") as file:
    content = file.read()

#pos = len(content)-19
#new = '\n'+content[:pos]+post+content[pos:]+'\n'
new = content.replace('###',all_posts)
with open("index.html", "w", encoding="utf-8") as file:
    file.write(new)

