from flask_blog import celery_down

@celery_down.task
def download_it(content):
    with open('./flask_blog/static/blog.txt', 'w') as f:
        f.write(content)
    return 'blog.txt'