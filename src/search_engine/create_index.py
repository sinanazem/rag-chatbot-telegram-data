def create_index_dict(docs):
    
    index = {}
    for doc in docs:    
        for pos, token in enumerate(doc['text']):
            if token not in index:
                index[token] = {
                'total_freq': 1,
                 'docs': {
                       doc['id']: {
                           'count_of_word': 1,
                           'positions': [pos]
                           }
                    }
                }
            else:
                index[token]['total_freq'] += 1  
                if doc['id'] not in index[token]['docs']:
                    index[token]['docs'][doc['id']] = {}
                    index[token]['docs'][doc['id']]['count_of_word'] = 1
                    index[token]['docs'][doc['id']]['positions'] = [pos]
                else:
                    index[token]['docs'][doc['id']]['count_of_word'] += 1 
                    index[token]['docs'][doc['id']]['positions'].append(pos) 
    
    # create champion lists             
    for word in index:
        champ_list = sorted(index[word]['docs'], key=lambda x: index[word]['docs'][x]['count_of_word'], reverse=True)
        index[word]['champions'] = champ_list[:len(champ_list) // 5]
    return index