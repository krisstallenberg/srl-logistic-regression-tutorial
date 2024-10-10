from collections import deque

def find_dependency_path(token_id, sentence, pred_index):
    """
    Extract the shortest dependency path of a token to the predicate.
    
    Return:
        List: a dependency path from token_id to pred_id.

    sentence (list of dict): The sentence object
    token_id (int): The id of the word in the sentence
    pred_id (int): The id of the predicate in the sentence
    """

    # Keep track of visited nodes.
    visited = set()
    # Initialize queue with starting node.
    queue = deque([(token_id, [])])
    # Predicate id is the index of the predicate in the sentence + 1.
    predicate_id = pred_index + 1


    # While there are still nodes to visit.
    while queue:
        # Get the current node and path.
        current_id, path = queue.popleft()

        # If the current node has already been visited, skip it.
        if current_id in visited:
            continue
        visited.add(current_id)

        token = sentence[current_id - 1]
        head_id = int(token['head'])

        # If the current token is the predicate, return the path.
        if current_id == predicate_id:
            return path

        # If the current token is not the head, traverse upwards from dependent to head.
        if head_id != 0 and head_id not in visited:
            queue.append((head_id, path + [f"(up)=={token['dependency_relation']}"]))

        # If the current token is a head, traverse downwards from head to dependent.
        for i, child in enumerate(sentence):
            if int(child['head']) == current_id and (i + 1) not in visited:
                queue.append((i + 1, path + [f"(down)=={child['dependency_relation']}"]))

    # Return empty if no path is found
    return []

def extract_dependency_path(sentence):
    """
    Extract the dependency path of each token to the predicate.
    
    Return:
        List of dependency paths.

    sentence (list of dict): The sentence object
    """
    features = []

    # Find ID of predicate in the sentence
    pred_id = None
    for i, word in enumerate(sentence):
        if word['predicate'] != '_':
            pred_id = i
            break

    # For each word in the sentence, extract its dependency path to the predicate.
    for i, word in enumerate(sentence):
        # If the word is not the predicate, find its dependency path to the predicate.
        if i != pred_id:
            dep_path = find_dependency_path(int(word['id']), sentence, pred_id)
            features.append('=>'.join(dep_path) + ':' if dep_path else '_')
        # If the word is the predicate, add an empty string.
        else:
            features.append('_')

    return features
