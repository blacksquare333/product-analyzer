from flask import Flask, request , jsonify, send_from_directory
from flask_cors import CORS
from dotenv import load_dotenv
import os
import requests

load_dotenv()

app = Flask(__name__)
CORS(app)

DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")

@app.route("/")
def index():
    return send_from_directory(".",index.html)
@app.route("/product_analyzer",methods=['POST'])
def generate_product_data_analysis():
    data=request.get_json()

    product_name=data['product_name']

    prompt= f"请根据产品{product_name}分析市场需求量，目标群体以及定价范围"
    response = requests.post(
   "https://api.deepseek.com/v1/chat/completions",
   headers={
       "Authorization":f"Bearer {DEEPSEEK_API_KEY}",    
       "Content-Type": "application/json"
   },

   json={
       "model": "deepseek-chat",
       "messages": [{"role":"user","content":prompt}]
   }
    )

    result=response.json()

    product_data_analysis = result['choices'][0]['message']['content']

    print(result)

    return jsonify({"product_data_analysis":product_data_analysis})

if __name__=="__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0",port=5000,debug=False)