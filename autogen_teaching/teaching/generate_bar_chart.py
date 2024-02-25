# filename: generate_bar_chart.py
import matplotlib.pyplot as plt

# Data for application domains and number of papers
domains = [
    "AI-assisted decision-making",
    "User trust in AI",
    "Human-AI collaboration",
    "Human-robot teams",
    "Explainable robots",
    "Model calibration",
    "Trust explanations",
    "HCI",
    "Team cohesion",
    "Anthropomorphic agents"
]

num_papers = [2, 1, 2, 1, 1, 1, 1, 1, 1, 1]

# Create a bar chart
plt.figure(figsize=(12, 6))
plt.bar(domains, num_papers, color='skyblue')
plt.xlabel('Application Domains')
plt.ylabel('Number of Papers')
plt.title('Distribution of Papers Across Application Domains')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()

# Save the bar chart to a file
plt.savefig('papers_distribution.png')

plt.show()