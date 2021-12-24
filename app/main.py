from fastapi import FastAPI
#from anc.database import engine
#import anc.models
from app.routers import post, user, auth, vote
from app.anc.config import settings

#from fastapi.middleware.cors import CORSMiddleware
#models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# origins=["https://www.google.com/"]

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=origins,
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )
# For setting direct connection with postgres
#from database import set_connection
# conn = set_connection()
# cur = conn.cursor()

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

@app.get("/")
def get_user():
    return {"message": "Hello World"}

@app.get("/request")
def get_request():
    return {'response': "Someday"}


