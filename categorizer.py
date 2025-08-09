from transformers import pipeline
import math

clf = pipeline(
    "zero-shot-classification",
    model="facebook/bart-large-mnli",
    device=-1  # CPU mode
)

# batch processing
def categorize_batch(texts, labels, batch_size=8): # batch size small for ram
    results = []
    texts = list(texts)
    total_batches = math.ceil(len(texts) / batch_size)

    for i in range(total_batches):
        batch = texts[i * batch_size : (i + 1) * batch_size]
        print(f"Processing batch {i+1}/{total_batches}...")
        batch_results = clf(batch, labels, multi_label=False)
        results.extend(batch_results)

    return results
