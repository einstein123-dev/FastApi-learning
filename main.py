from tempfile import template
from fastapi.staticfiles import StaticFiles
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from fastapi import FastAPI,Request,HTTPException,status
# from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from schema import postCreate,postResponse

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
@app.get('/post/{post_id}', include_in_schema=False, name="post_detail")
def post_detail(request:Request, post_id:int):
    for post in posts:
        if post.get("id") == post_id:
            return templates.TemplateResponse(request,
            "post.html",
                                                               {"post":post,"title": post["title"],},
                                                            )
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Page not found")


@app.get('/api/post',include_in_schema=True)
def get_posts():
    return posts

@app.post(
    "/api/posts",
    response_model=postResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_post(post: postCreate):
    new_id = max(p["id"] for p in posts) + 1 if posts else 1
    new_post = {
        "id": new_id,
        "author": post.author,
        "title": post.title,
        "content": post.content,
        "date_posted": "April 23, 2025",
    }
    posts.append(new_post)
    return new_post

@app.get('/api/post/{post_id}',include_in_schema=True,response_model=list[postResponse])
def get_post(post_id:int):
    for post in posts:
        if post.get("id") == post_id:
            return post
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Page not found")


@app.exception_handler(StarletteHTTPException)
def general_http_exception_handler(request: Request, exception: StarletteHTTPException):
    message = (
        exception.detail
        if exception.detail
        else "An error occurred. Please check your request and try again."
    )

    if request.url.path.startswith("/api"):
        return JSONResponse(
            status_code=exception.status_code,
            content={"detail": message},
        )

    return templates.TemplateResponse(
        request,
        "error.html",
        {
            "status_code": exception.status_code,
            "title": exception.status_code,
            "message": message,
        },
        status_code=exception.status_code,
    )


@app.exception_handler(RequestValidationError)
def validation_exception_handler(request: Request, exception: RequestValidationError):
    if request.url.path.startswith("/api"):
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            content={"detail": exception.errors()},
        )

    return templates.TemplateResponse(
        request,
        "error.html",
        {
            "status_code": status.HTTP_422_UNPROCESSABLE_CONTENT,
            "title": status.HTTP_422_UNPROCESSABLE_CONTENT,
            "message": "Invalid request. Please check your input and try again.",
        },
        status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
    )