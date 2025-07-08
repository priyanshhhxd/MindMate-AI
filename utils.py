from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

tokenizer = AutoTokenizer.from_pretrained("microsoft/DialoGPT-medium")
model = AutoModelForCausalLM.from_pretrained("microsoft/DialoGPT-medium")

def get_ai_response(user_input, chat_history_ids=None):
    # Step 1: Encode input
    input_ids = tokenizer.encode(user_input + tokenizer.eos_token, return_tensors='pt')

    # Step 2: Maintain chat history
    bot_input_ids = torch.cat([chat_history_ids, input_ids], dim=-1) if chat_history_ids is not None else input_ids

    # Step 3: Generate response
    chat_history_ids = model.generate(bot_input_ids, max_length=1000, pad_token_id=tokenizer.eos_token_id)

    # Step 4: Decode the output
    response = tokenizer.decode(chat_history_ids[:, bot_input_ids.shape[-1]:][0], skip_special_tokens=True)

    # Step 5: Clean & check bad responses
    bad_phrases = ["i'm feeling", "i feel", "i am also", "i’m also", "i’m feeling", "i understand because i", "me too"]
    if (
        response.strip().lower() == user_input.strip().lower() or
        response.strip() == "" or
        any(phrase in response.lower() for phrase in bad_phrases)
    ):
        response = "I'm here to support you. Thank you for sharing how you're feeling. Would you like to talk more about it?"

    return response, chat_history_ids