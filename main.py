from fastapi import FastAPI, Request
import openai
import base64

app = FastAPI()


openai.api_key = open("API_KEY", "r").read()
count = 0


def generateImgae(prompt):
    response = openai.Image.create(
        prompt=prompt, n=1, response_format="b64_json", size="256x256"
    )

    img = response["data"][0]["b64_json"]
    saveImage(img)
    return response["data"][0]["b64_json"]


def generateVariation(image):
    response = openai.Image.create_variation(
        image=open(image, "rb"), n=1, size="256x256", response_format="b64_json"
    )

    img = response["data"][0]["b64_json"]
    saveImage(img)
    return response["data"][0]["b64_json"]


def saveImage(img):
    global count
    count = count + 1
    decodeData = base64.b64decode((img))
    imgFile = open("image" + str(count) + ".png", "wb")
    imgFile.write(decodeData)
    imgFile.close()

    return "image" + str(count) + ".png"


@app.post("/generate")
async def genetrateImgPost(info: Request):
    req_info = await info.json()
    b64Json = generateImgae(req_info.get("Prompt"))
    return {"Image": b64Json}


@app.post("/variation")
async def genetrateVariationPost(info: Request):
    req_info = await info.json()
    img = saveImage(req_info.get("Image"))
    b64Json = generateVariation(img)
    return {"Image": b64Json}
