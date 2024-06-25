import openai

class GPTController:
    def __init__(self, api_key, trigger_words, gpt_model):
        self.api_key = api_key
        self.trigger_words = trigger_words
        self.gpt_model = gpt_model
        self.client = openai.OpenAI(api_key=api_key)

    def check_triggers(self, text):
        for word in self.trigger_words:
            if word in text:
                return True
        return False

    def paraphrase_text(self, text, prompt):
        max_token = 250 if len(text) >= 250 else len(text)
        response = self.client.chat.completions.create(
            model=self.gpt_model,
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": f"{prompt} : {text[: 3000] if len(text) > 3000 else text}"}
            ],
            max_tokens= max_token
        )
        answer = "\n".join(filter(lambda x : x, [item.message.content for item in response.choices]))
        print(answer, max_token)
        return answer
    
    def modify_text_list(self, text_list, prompt):
        result = []
        for text in text_list:
            new_text = self.paraphrase_text(text, prompt)
            result.append(new_text)
        return result




