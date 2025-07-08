from langchain.prompts import PromptTemplate
from langchain.llms import OpenAI
from langchain.chains import LLMChain
from langchain.callbacks import get_openai_callback
from langchain.chat_models import ChatOpenAI
from flask import Flask,render_template,jsonify,request

app=Flask(__name__)


Template="""You are an experienced financial advisor and stock market analyst with over 20 years of expertise.

The user will ask you any question about stocks, investing, or the stock market in general.

User's Question: {question}

Your task is:

1. If the question is about a specific company's stock, then:
    - Identify the company the user is referring to.
    - Gather and present the following data about the company in a well-decorated structured text format, as shown below:

📊 Company Analysis: Company Name

🔹Company Name:
Company Name

🔹 Current Stock Price:
💲 Current Stock Price (USD or INR)

🔹 52-Week High / Low:
🔼 High: 52-Week High  
🔽 Low: 52-Week Low

🔹 P/E Ratio:
📈 P/E Ratio

🔹 Market Capitalization:
💰 Market Cap

🔹 Recent Financial Performance:
Recent Financial Performance

---

⚠️ Key Risks:

1. Risk 1  
2. Risk 2

---\n

✅ Key Strengths:

1. Strength 1  
2. Strength 2

---

 📌 Recommendation:  
Invest / Hold / Avoid

💡 Reasoning:  
Detailed numerical justification for the recommendation

---

💬 If the user has any further questions or needs detailed sector-wise recommendations, encourage them to ask.

---

2. If the question is a **general query about the stock market** (e.g. definitions, best sectors, how investing works), then:
    - Provide your answer in a **clear, structured, and professional decorated text format** under:

### 📚 General Stock Market Answer:

your explanation here

---

If you cannot identify the user's intent, ask them to rephrase politely and clearly.
"""

prompt_template=PromptTemplate(
    input_variables=["question"],
    template=Template
)

import os,dotenv
key=os.getenv("OPEN_API_KEY")

llm=ChatOpenAI(api_key=key,model="gpt-3.5-turbo",temperature=0.5) 
quiz_chain=LLMChain(llm=llm,prompt=prompt_template,output_key="answer",verbose=True)

@app.route("/")
def index():
    return render_template('chat.html')

@app.route("/get",methods=["GET","POST"])
def chat():
    msg=request.form["msg"]
    input=msg
    print(input)
    result=quiz_chain.run(input)
    print("Response:",result)
    return str(result)

if __name__=='__main__':
    port = int(os.environ.get("PORT", 5000))  # Use Render's PORT or fallback to 5000 locally
    app.run(host="0.0.0.0", port=port)
