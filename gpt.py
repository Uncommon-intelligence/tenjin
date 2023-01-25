import openai

class GPT3:
    def __init__(self):
        pass
        # openai.api_key = self.api_key

    def _format_prompt(self, query, contexts):
        text = "context: \n"
        for context in contexts:
            text += context + "\n"

        text += "\nquery:\n"
        text += query + "\n"
        text += "\noutput:\n"

        return text 


    def query(self, query, contexts, max_tokens=500, temperature=0, top_p=1, frequency_penalty=0.0, presence_penalty=0.0):
        prompt = self._format_prompt(query, contexts)

        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=self._format_prompt(query, contexts),
            max_tokens=max_tokens,
            temperature=temperature,
        )

        return response