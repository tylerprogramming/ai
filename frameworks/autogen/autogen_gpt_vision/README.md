# Autogen Gpt Vision

An image-explainer agent that looks at pictures from the web and answers questions about them (find Waldo, identify dog breeds, describe game characters). Images are downloaded and sent to the vision-capable model as a `MultiModalMessage`.

Updated to AutoGen v0.7 (the new `autogen_agentchat` API).

## Run it

```bash
pip install -r requirements.txt
echo "OPENAI_API_KEY=sk-..." > .env
python autogen_vision.py
```

Uncomment Example 2 or 3 in `autogen_vision.py` to try the other images.
