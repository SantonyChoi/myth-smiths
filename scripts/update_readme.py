import glob
import os

def update_readme():
    episodes = glob.glob('episodes/*.md')
    episodes.sort()
    with open('README.md', 'w') as readme:
        readme.write("# 웹소설 에피소드 인덱스\n\n")
        for episode in episodes:
            episode_title = os.path.basename(episode).replace('.md', '')
            readme.write(f"- [{episode_title}]({episode})\n")

update_readme()
