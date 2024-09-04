import google.generativeai as genai

class GenerativeAIChatbot:
    """Class to handle interactions with Google Generative AI chatbot."""

    def __init__(self):
        genai.configure(api_key="AIzaSyAcSoX07ipqpn1xIvL7i1nbhw5esPZvY_s")  # Replace with your actual API key
        self.model = genai.GenerativeModel(
            model_name="gemini-1.5-flash",
            generation_config={
                "temperature": 1,
                "top_p": 0.95,
                "top_k": 64,
                "max_output_tokens": 8192,
                "response_mime_type": "text/plain",
            }
        )
        self.chat_session = self.model.start_chat(
            history=[
                {"role": "user", "parts": ["chatbot name is TechnoClare that provides user help regarding registration process of AYUSH STARTUP"]},
                {"role": "model", "parts": ["## TechnoClare: Your AYUSH Startup Registration Assistant\n\n**Hello! I'm TechnoClare, your friendly guide to navigating the AYUSH Startup registration process.**"]}
            ]
        )

    def get_response(self, message):
        try:
            response = self.chat_session.send_message(message)
            return response.text
        except Exception as e:
            raise RuntimeError(f"Chatbot response error: {str(e)}")
