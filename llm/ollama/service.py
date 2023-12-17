import llm.ollama.client as oc

def list_model_names():
    models = oc.models()
    return [model.get("name") for model in models]

def get_system_prompt(name):
    data = oc.show(name)
    default_system_prompt = "You are an AI assistant. Help the user as much as you can."
    if data:
        return data.get("system", default_system_prompt)
    return default_system_prompt