def remember_fact(memory, category, key, value):

    if category not in memory:
        memory[category] = {}

    memory[category][key] = value

    return memory