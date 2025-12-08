# Without classes - data and functions separate
name = "OpenAI"
model = "gpt-4o-mini"

def generate_response(prompt):
    # Process prompt...
    return response

# With classes - everything bundled together
class OpenAIClient:
    def __init__(self, name, model):
        self.name = name
        self.model = model
    
    def generate_response(self, prompt):
        # Process prompt...
        return response