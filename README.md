# optohawk
Your Hawk eye for surveillance  🦅
 
## Inspiration 💡
Imagine this - it’s a dark night in the pandemic, streets are empty and thieves and robbers are all around. There might be a break-in — wait, what was that? As per reports, the amount of home robberies and thefts has increased to a striking 𝟔𝟓% post-lockdown. Every time, due to lack of proper evidence, these robbers run away!

*We mainly tend to focus on what's gonna happen while we forget what is happening right now.* Don't worry, we got your back 😉

## What it does 🤔
Introducing 𝐎𝐩𝐭𝐨𝐇𝐚𝐰𝐤 - An artificially intelligent home police that detects robbery and break-ins. We detect the robber’s age, gender and create a face close-up while informing you and the proper authorities about this incident. Our generated Tensorflow Model showed an accuracy of 93.28% during testing. Our system can work in dark conditions since training was done in mostly dark videos and also infrared ones. We also are determining the current mood of the person in the frame. Our solution is extremely cheap and the entire app can be deployed in a setup of only $25.

## How we built it 👨‍🔧
𝐎𝐩𝐭𝐨𝐇𝐚𝐰𝐤 is crafted with ❤️. It's primarily built on Python. We are leveraging Tensorflow for the stream feed processing on R-pi and then processing it via our custom summarizer model running on python. Moreover, the camera module is directly integrated on R-pi and can be accessed via a static Access point, which can be accessed from anywhere around the world! All of the models are trained on Colab & can be run directly on the Colab. 

We also used two research papers [R1](https://patents.google.com/patent/US20190379873A1/en?q=background+segmentation&oq=background+segmentation) & [R2](https://patents.google.com/patent/US9215467B2/en?q=background+segmentation+video&oq=background+segmentation+video) for understanding how to properly perform semantic segmentation from a live feed & also for content-aware frame cropping.

## Challenges we ran into 😫
Initially, we were facing some issues while training the model on our system, including underfitting errors as we had to reduce the dataset parameters to optimize it so that it can run seamlessly on low end devices. Also, it was a bit difficult for us to collaborate in a virtual setting but we somehow managed to finish the project on time.

## Accomplishments that we're proud of 😊
We are proud of finishing the project on time which seemed like a tough task initially but happily were also able to add most of the features that we envisioned for the app during ideation.

## What we learned 😬
A lot of things, both summed up in technical & non-technical sides. Also not to mention, we enhanced our googling and Stackoverflow searching skill during the hackathon 😆

## What's next for Optohawk 🚀
We just really want this project to create a real impact while fixing the loopholes of existing security system! Still, we would love to make it more scalable & cross-platform so that the user interaction increases & we can help reduce robbery & ill-actions together :)

Crafted with ❤️ for BC Hacks 2.0 
