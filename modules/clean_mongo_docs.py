from datetime import datetime

def clean_mongo_docs(docs):
    cleaned = []
    for doc in docs:
        doc["_id"] = str(doc.get("_id", ""))  # Convert ObjectId to string
        for key, value in doc.items():
            if isinstance(value, (list, dict)):
                doc[key] = str(value)
            elif isinstance(value, datetime):
                doc[key] = value.isoformat()
        cleaned.append(doc)
    return cleaned
