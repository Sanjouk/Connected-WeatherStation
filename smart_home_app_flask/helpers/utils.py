from datetime import datetime


# Convert MongoDB document fields (_id, datetime) to JSON-serializable formats
def doc_to_json(document):
    if document:
        document['_id'] = str(document['_id'])
        if 'timestamp' in document and isinstance(document['timestamp'], datetime):
            document['timestamp'] = document['timestamp'].isoformat()
        return document
    return None