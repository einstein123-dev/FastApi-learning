from tempfile import template
from fastapi.staticfiles import StaticFiles

from fastapi import FastAPI,Request,HTTPException,status
# from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

app = FastAPI()
app.mount("/static",StaticFiles(directory="static"),name = "static")

templates = Jinja2Templates(directory="templates")

posts: list[dict] = [
    {
        "id": 1,
        "author": "Corey Schafer",
        "title": "FastAPI is Awesome",
        "content": "This framework is really easy to use and super fast.",
        "date_posted": "April 20, 2025",
    },
    {
        "id": 2,
        "author": "Jane Doe",
        "title": "Python is Great for Web Development",
        "content": "Python is a great language for web development, and FastAPI makes it even better.",
        "date_posted": "April 21, 2025",
    },
    {
        "id": 3,
        "author": "John Smith",
        "title": "Understanding REST APIs",
        "content": "REST APIs allow different systems to communicate over HTTP using standard methods.",
        "date_posted": "April 22, 2025",
    },
    {
        "id": 4,
        "author": "Alice Johnson",
        "title": "Getting Started with Databases",
        "content": "Databases store and organize data so it can be easily retrieved and managed.",
        "date_posted": "April 23, 2025",
    },
    {
        "id": 5,
        "author": "Bob Williams",
        "title": "Why Learn Backend Development",
        "content": "Backend development powers the logic behind every web application you use.",
        "date_posted": "April 24, 2025",
    },
]

@app.get('/', include_in_schema=False, name="home")
@app.get('/post',include_in_schema=False, name="post")
def home(request:Request):
    # return f"<h1>{posts[0]["title"]}</h1> <p>{posts[0]["content"]}</p>"
    # return ({"message":"hello world"})
    return templates.TemplateResponse(request,
                                      "home.html",
                                      {"posts":posts,"title":"Home"}
                                      )

@app.get('/api/post',include_in_schema=True)
def get_posts():
    return posts

@app.get('/api/post/{post_id}',include_in_schema=True)
def get_post(post_id:int):
    for post in posts:
        if post.get("id") == post_id:
            return post
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Page not found")
        