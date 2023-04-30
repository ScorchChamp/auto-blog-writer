import openai
import dotenv
import os
import json
import time

dotenv.load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")


BLOGS = "blogs.json"
STANDARD = "standard.txt"

def getBlogs():
    with open(BLOGS, "r") as f:
        blogs = json.load(f)
    return blogs

def setBlogs(blogs):
    with open(BLOGS, "w") as f:
        json.dump(blogs, f)

def getNewBlog(prompt):
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    return completion.choices[0]['message']['content']

def getStandardPrompt():
    with open(STANDARD, "r") as f:
        prompt = f.read()
    return prompt

def getPrompt():
    prompt = getStandardPrompt()
    blogs = getBlogs()
    titles = [blog["title"] for blog in blogs]
    prompt += "\nCurrently, there are the following titles: " + str(titles)
    return prompt

def parseResult(prompt):
    try: 
        return json.loads(prompt)
    except Exception as e:
        print(e)
        return None

if __name__ == "__main__":
    while True:
        prompt = getPrompt()
        print(prompt)
        newBlog = getNewBlog(prompt)
        result = parseResult(newBlog)
        if result is None:
            print("Failed to parse result")
            continue
        print(result)
        blogs = getBlogs()
        blogs.append(result)
        setBlogs(blogs)
        print("Done!")
        time.sleep(5)
