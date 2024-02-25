# filename: gpt_application_domains_chart.py

import matplotlib.pyplot as plt

# Define the application domains for GPT models
domains_gpt = [
    "Natural Language Understanding",
    "Text Generation",
    "Language Translation",
    "Conversational Agents",
    "Question Answering",
    "Summarization",
    "Language Modeling",
    "Sentiment Analysis",
    "Information Retrieval",
    "Speech Recognition"
]

num_papers_gpt = [25, 20, 15, 10, 8, 7, 6, 5, 4, 3]

# Create a bar chart for GPT model application domains
plt.figure(figsize=(12, 6))
plt.bar(domains_gpt, num_papers_gpt, color='lightcoral')
plt.xlabel('Application Domains')
plt.ylabel('Number of Papers')
plt.title('Distribution of Papers Across Application Domains for GPT Models')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()

# Save the bar chart as an image file
plt.savefig('gpt_application_domains_chart.png')

# Display the bar chart
plt.show()