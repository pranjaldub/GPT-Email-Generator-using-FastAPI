# -*- coding: utf-8 -*-
"""FastAPI_Host.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1buWLwIOu82iJbowZRvkDQeJTHF9XRYmS
"""

!pip install fastapi nest-asyncio pyngrok uvicorn
!pip install openai
!pip install -U flask-cors
!pip install flask_jsonpify
!pip install openai
!pip install flask_ngrok
import time
import time
import openai
def set_openai_key(key):
    """Sets OpenAI key."""
    openai.api_key = key

class Example():
    """Stores an input, output pair and formats it to prime the model."""

    def __init__(self, inp, out):
        self.input = inp
        self.output = out

    def get_input(self):
        """Returns the input of the example."""
        return self.input

    def get_output(self):
        """Returns the intended output of the example."""
        return self.output

    def format(self):
        """Formats the input, output pair."""
        return f"input: {self.input}\noutput: {self.output}\n"


class GPT:
    """The main class for a user to interface with the OpenAI API.
    A user can add examples and set parameters of the API request."""

    def __init__(self, engine='davinci',
                 temperature=0.8,
                 max_tokens=500):
        self.examples = []
        self.engine = engine
        self.temperature = temperature
        self.max_tokens = max_tokens

    def add_example(self, ex):
        """Adds an example to the object. Example must be an instance
        of the Example class."""
        assert isinstance(ex, Example), "Please create an Example object."
        self.examples.append(ex.format())

    def get_prime_text(self):
        """Formats all examples to prime the model."""
        return '\n'.join(self.examples) + '\n'

    def get_engine(self):
        """Returns the engine specified for the API."""
        return self.engine

    def get_temperature(self):
        """Returns the temperature specified for the API."""
        return self.temperature

    def get_max_tokens(self):
        """Returns the max tokens specified for the API."""
        return self.max_tokens

    def craft_query(self, prompt):
        """Creates the query for the API request."""
        return self.get_prime_text() + "input: " + prompt + "\n"

    def submit_request(self, prompt):
        """Calls the OpenAI API with the specified parameters."""
        response = openai.Completion.create(engine=self.get_engine(),
                                            prompt=self.craft_query(prompt),
                                            max_tokens=self.get_max_tokens(),
                                            temperature=self.get_temperature(),
                                            top_p=1,
                                            n=1,
                                            stream=False,
                                            stop="\ninput:")
        return response

    def get_top_reply(self, prompt):
        """Obtains the best result as returned by the API."""
        response = self.submit_request(prompt)
        return response['choices'][0]['text']

openai.api_key = "PLACE_YOUR_API_KEY_HERE"
response = openai.Completion.create(engine="davinci", prompt="html is", max_tokens=5)

#train --------------------->
gpt=GPT()
gpt.add_example(Example('Create email with ; receiver:Sam ;sender:Pranjal; new ,customer support representative , pleased , support ,greet ,congratulate ,role', 
                        '''Subject: Meet the new Customer Support Representative
<pre>
Dear team,
<pre>
I am pleased to introduce you to Sam who is starting today as a Customer Support Representative. He will be providing technical support and assistance to our users, making sure they enjoy the best experience with our products.
<pre>
Feel free to greet Sam in person and congratulate him with the new role!
<pre>
Best regards,
Pranjal
Software Engineer'''))




gpt.add_example(Example('Create email with; reciever:Pranjal ;sender:Sam ;previous mail, collaboration , interested , post , UX , dining , experience , industry', 
                        '''Subject: RE: previous mail
<pre>
Hi Pranjal,
<pre>
Following up on my previous email about the collaboration with your website. I’m still interested in writing a guest post about the best UX practices for dining apps. With 10 years of experience in the mobile industry, I have a lot of insights to share with your audience.
<pre>
Please let me know if you’re interested in collaboration!
<pre>
Best,
Sam'''))




gpt.add_example(Example('Create email with;sender:Pranjal ; receiver:none; Do you have student discounts for the Annual Coding Conference? , greetings , discounts , tickets , Annual Coding Conference , price , high , educational discount', 
                        '''Subject: Do you have student discounts for the Annual Coding Conference?
<pre>
Greetings,
<pre>
I would like to ask if you provide student discounts for tickets to the Annual Coding Conference.
<pre>
I’m a full-time student at the University of Texas and I’m very excited about your event, but unfortunately, the ticket price is too high for me. I would appreciate if you could offer me an educational discount.
<pre>
Looking forward to hearing from you!
<pre>
Best,
Pranjal'''))
generate = GPT(engine="davinci",
          temperature=0.8,
          max_tokens=500)




def home(em):
    #det = details.split(';')
    import openai
    #prompt = "Create email with;"+det[1].split(':')[1]+";"+det[2].split(':')[1]+";"+det[3]
    #prompt = 'Create email with;sender:Pranjal ; receiver:none; Do you have student discounts for the Annual Coding Conference? , greetings , discounts , tickets , Annual Coding Conference , price , high , educational discount'
    return gpt.get_top_reply(em)
from fastapi import FastAPI,Request
import nest_asyncio
from pyngrok import ngrok
import uvicorn

app = FastAPI()

@app.get('/{em}')
async def func(em):
    start_time = time.time()
    
    email= home(em)
    #gpt.add_example(Example(st,email))
    elapsed_time = time.time() - start_time
    print(elapsed_time)
    return email

ngrok_tunnel = ngrok.connect(8001)
print('Public URL:', ngrok_tunnel.public_url)
nest_asyncio.apply()
uvicorn.run(app, port=8001)