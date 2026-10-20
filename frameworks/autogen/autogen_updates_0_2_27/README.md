# Autogen Updates 0 2 27

Shows off the features from the AutoGen 0.2.27 update video, rebuilt on the current API:

- `main.py`: an assistant writes a small web page (HTML, CSS and a JavaScript "Hello!" button) and a code-executor agent saves the files into the `code` folder using `# filename:` comments. The files already in `code/` are sample output from a previous run.
- `dotnet-autogen.cs`: the AutoGen for .NET sample from the video (C#, unchanged).

> **Note:** Updated to AutoGen v0.7. The original video used the older AutoGen 0.2 API, so the code here differs from what's on screen.

## Run it

```bash
pip install -r requirements.txt
# put OPENAI_API_KEY in .env
python main.py
```

> Code the model writes is executed on your machine without a sandbox.
