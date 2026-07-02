"""
Create a sample fake news dataset for testing
This creates a small dataset with fake and real news samples
"""
import pandas as pd
import numpy as np

print("=" * 60)
print("Creating Sample Fake News Dataset")
print("=" * 60)

# Sample news articles (mix of fake and real)
sample_data = [
    {
        "title": "Scientists Discover New Planet in Our Solar System",
        "text": "Astronomers have announced the discovery of a new planet in our solar system. The planet, named X-7, was found using advanced telescope technology. This discovery could change our understanding of the solar system.",
        "label": "REAL"
    },
    {
        "title": "Breaking: Aliens Contact Earth Government",
        "text": "In a shocking development, government officials have confirmed that aliens have made contact with Earth. The aliens are said to be friendly and want to share advanced technology. A press conference is scheduled for next week.",
        "label": "FAKE"
    },
    {
        "title": "New Study Shows Benefits of Exercise",
        "text": "A recent study published in the Journal of Health Sciences shows that regular exercise can significantly improve mental health. The study followed 1000 participants over 5 years and found consistent benefits.",
        "label": "REAL"
    },
    {
        "title": "Celebrity Claims to Have Supernatural Powers",
        "text": "A famous celebrity has revealed they have the ability to read minds and predict the future. Scientists are baffled by this claim. The celebrity plans to demonstrate these powers on live television next month.",
        "label": "FAKE"
    },
    {
        "title": "Climate Change Report Released",
        "text": "The latest climate change report from the United Nations shows that global temperatures are rising faster than previously predicted. Scientists warn that immediate action is needed to prevent catastrophic consequences.",
        "label": "REAL"
    },
    {
        "title": "Secret Government Program Controls Weather",
        "text": "Leaked documents reveal that the government has been controlling the weather for decades using secret technology. Hurricanes, droughts, and floods are all allegedly orchestrated by this program.",
        "label": "FAKE"
    },
    {
        "title": "Technology Company Announces New Product",
        "text": "A major technology company has announced a revolutionary new product that will change how we interact with computers. The product uses artificial intelligence to understand natural language commands.",
        "label": "REAL"
    },
    {
        "title": "Doctors Discover Cure for All Diseases",
        "text": "Medical researchers have found a single cure that works for all diseases including cancer, diabetes, and heart disease. The cure will be available to the public next month. Pharmaceutical companies are trying to suppress this information.",
        "label": "FAKE"
    },
    {
        "title": "Economic Growth Reported This Quarter",
        "text": "The latest economic data shows strong growth in the last quarter. Unemployment rates have decreased and consumer spending is up. Economists are optimistic about the future.",
        "label": "REAL"
    },
    {
        "title": "Ancient Civilization Found Under Ocean",
        "text": "Archaeologists have discovered an ancient civilization that existed 10,000 years ago under the ocean. The civilization had advanced technology that we still don't understand. The government is keeping this discovery secret.",
        "label": "FAKE"
    },
    {
        "title": "New Educational Program Launched",
        "text": "A new educational program has been launched to help students learn coding and computer science. The program is free and available to all students. It includes online courses and hands-on projects.",
        "label": "REAL"
    },
    {
        "title": "Time Travel Machine Invented",
        "text": "A scientist has successfully created a time travel machine and has traveled to the future. The machine can transport people to any point in time. The government has taken control of the technology.",
        "label": "FAKE"
    },
    {
        "title": "Sports Team Wins Championship",
        "text": "In an exciting match, the local sports team won the national championship. Thousands of fans celebrated in the streets. The team's victory marks their third championship in five years.",
        "label": "REAL"
    },
    {
        "title": "Mind Control Technology Revealed",
        "text": "Secret documents show that the government has been using mind control technology on citizens through television and radio signals. This technology can make people think and act in specific ways without their knowledge.",
        "label": "FAKE"
    },
    {
        "title": "New Public Transportation System Opens",
        "text": "The city has opened a new public transportation system that will reduce traffic congestion. The system includes new bus routes and train lines. It is expected to serve thousands of commuters daily.",
        "label": "REAL"
    },
    {
        "title": "World Leaders Are Actually Reptiles",
        "text": "A conspiracy theory claims that world leaders are actually shape-shifting reptiles from another planet. They have been controlling human society for centuries. Evidence includes strange behavior and unusual physical characteristics.",
        "label": "FAKE"
    },
    {
        "title": "Research Shows Benefits of Reading",
        "text": "A new research study demonstrates that reading regularly can improve cognitive function and reduce stress. The study followed participants for two years and found significant improvements in memory and focus.",
        "label": "REAL"
    },
    {
        "title": "Vaccines Contain Microchips",
        "text": "A leaked report reveals that vaccines contain microchips that allow the government to track people. These microchips are invisible and cannot be detected. The purpose is to monitor and control the population.",
        "label": "FAKE"
    },
    {
        "title": "New Renewable Energy Project Announced",
        "text": "A major renewable energy project has been announced that will provide clean electricity to thousands of homes. The project uses solar and wind power. It is expected to reduce carbon emissions significantly.",
        "label": "REAL"
    },
    {
        "title": "Earth is Actually Flat",
        "text": "A group of scientists has proven that the Earth is actually flat, not round. All the evidence for a round Earth has been fabricated by NASA and other organizations. The real shape of Earth has been hidden from the public.",
        "label": "FAKE"
    }
]

# Create DataFrame
df = pd.DataFrame(sample_data)

# Add an index column to match expected format
df.insert(0, 'Unnamed: 0', range(len(df)))

print(f"\nCreated dataset with {len(df)} samples")
print(f"Columns: {list(df.columns)}")
print(f"\nLabel distribution:")
print(df['label'].value_counts())

# Save to CSV
df.to_csv('news.csv', index=False)
print(f"\n✓ Dataset saved to 'news.csv'")
print(f"  File size: {len(pd.read_csv('news.csv').to_csv())} bytes")

print("\n" + "=" * 60)
print("✓ Sample dataset created successfully!")
print("=" * 60)
print("\nNote: This is a small sample dataset for testing.")
print("For production use, download a larger dataset from:")
print("  - Kaggle: https://www.kaggle.com/datasets/clmentbisaillon/fake-and-real-news-dataset")
print("  - Or search for 'fake news dataset' on Kaggle")

