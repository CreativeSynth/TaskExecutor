import openai
import os
import time
openai.api_key = os.getenv('OPENAI_API_KEY')
messages = [ {"role": "system", "content": 
			"You are a intelligent assistant."} ] 
while True: 
	message = input("User : ")
	start_time = time.time()
	if message: 
		messages.append( 
			{"role": "user", "content": message}, 
		) 
		chat = openai.chat.completions.create( 
			model="gpt-3.5-turbo", messages=messages 
		) 
	reply = chat.choices[0].message.content
	end_time = time.time()
	print(f"ChatGPT: {reply} \t (응답시간 {end_time-start_time})s") 
	messages.append({"role": "assistant", "content": reply}) 
