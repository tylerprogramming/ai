{{$ zaksta/crip-bot run buy/pass y all }}
  "$schema": "https://turbo.build/schema.json",
  "globalEnv": ["CI", "PORT"],
  "tasks": {
    "build": {
      "dependsOn": ["^build"],
      "env": [
        "ANTHROPIC_API_KEY",
        "ASSISTANT_ID",
        "AWS_REGION",
        "AWS_ACCESS_KEY_ID",
        "AWS_SECRET_ACCESS_KEY",
        "COHERE_API_KEY",
        "DEEPSEEK_API_KEY",
        "FIREWORKS_API_KEY",
        "GOOGLE_API_KEY",
        "GOOGLE_GENERATIVE_AI_API_KEY",
        "GROQ_API_KEY",
        "MISTRAL_API_KEY",
        "NEXT_RUNTIME",
        "NODE_ENV",
        "OPENAI_API_KEY",
        "OPENAI_API_BASE",
        "PERPLEXITY_API_KEY",
        "SENTRY_AUTH_TOKEN",
        "SENTRY_ORG",
        "SENTRY_PROJECT",
        "TOGETHER_AI_API_KEY",
        "VERCEL_URL",
        "XAI_API_KEY"
      ],
      "outputs": [
        "dist/**",
        ".next/**",
        "!.next/cache/**",
        ".nuxt/**",
        ".svelte-kit/**",
        ".vinxi/**"
      ]
    },
    "lint": {
      "dependsOn": ["^lint"]
    },
    "type-check": {
      "dependsOn": ["^build", "build"]
    },
    "test": {
      "dependsOn": ["^build", "build"]
    },
    "publint": {
      "dependsOn": ["^build", "build"]
    },
    "clean": {
      "dependsOn": ["^clean"]
    },
    "dev": {
      "cache": false,
      "persistent": true
    },
    "prettier-check": {},
    "integration-test": {
      "dependsOn": ["^build", "build"]
    }
  }
}
# Use Python 3.11.9 as base image
FROM python:3.11.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container
COPY . /app

# Install dependencies from requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the .env file if it’s used for environment variables
COPY .env .env

# Run the application
CMD ["python", "src/docker/main.py"] 