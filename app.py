# Imported the necessary libraries and modules
from fastapi import FastAPI, Request
import uvicorn
from uvicorn import Server
from chatgpt import answer
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()                         # FastAPI instance
origins = ["http://localhost:3001"]     # Defined the allowed origins for CORS
app.on_event("startup")              # startup event to add the secret header
    
async def startup_event():  
    server = Server(app, host="localhost", port=8000)
    server.config.before_server_start.append(server.config.headers.append(["X-Secret-Header","abcd"])) #custom header before server start

# A home route that returns a message
@app.get("/")
def home():
    return "Hi from Aishwarya"   # Returning a simple greeting message

# Configure CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins = ["*"],
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"],
)

# Defining a route for handling user queries and providing responses
@app.get("/api/response")
async def get_response(message: str, request: Request):
     response =  answer(message)  # Get response from the answer function
     if(len(response)!=0):
        print (response)          # Print the response for debugging
        return response           # Return the response to the user
     else: 
        return "Oops! Something went wrong"

# Run the uvicorn server
if __name__ == "__main__":
    uvicorn.run("app:app",port = 8000,reload=True)  