from csc.nl import get_nl
import itertools as it
import divisi2

en_nl = get_nl('en')

A = divisi2.network.conceptnet_matrix('en')
concept_axes, axis_weights, feature_axes = A.normalize_all().svd(k=100)
sim = divisi2.reconstruct_similarity(concept_axes, axis_weights, post_normalize=True)

cheese_text = "Cheese is a type of food. It is made from milk. There are many types of cheese. Many things affect the style, texture and flavor of a cheese. These include the origin of the milk, if the milk has been pasteurized, the amount of butterfat, bacteria and mold in the cheese, how the cheese is made and how old the cheese is. For some cheeses, the milk is curdled by adding acids such as vinegar or lemon juice. Most cheeses are acidified by bacteria. This bacteria turns milk sugars into lactic acid. Rennet is then used to finish the curdling. Vegetarian alternatives to rennet can also be used. Most of these are made by fermentation of a fungus called Mucor miehei. Other alternatives us species of the Cynara thistle family. People have been making cheese since before history was written down. It is not known when cheese was first made. It is known that cheese was eaten by the Sumerians in about 4000 BC. Cheese is usually made using milk. The milk of cows, goats, and sheep are most popular. Buffalo, camel and even mare's milk can also be used. Cheese makers usually cook the milk in large pots. They add salt and a substance from the stomach of young cows called rennet. This curdles the cheese and makes it solid. Some makers do not add rennet. They curdle the cheese in other ways. Cheese made in factories is often curdled by using bacteria. Other ingredients are added and the cheese is usually aged for a short time."
cheese_text_list = cheese_text.split('.')


def extract_concepts(sentence):
    return en_nl.extract_concepts(sentence, max_words=1, check_conceptnet=True)


def find_sim_words(word1, word2):
    try:
        similarity = sim.entry_named(word1, word2)
        return similarity
    except KeyError, err:
        print "Key not found: {0}".format(str(err))


def sentence_sim(concepts):
    pairs = list(it.product(*concepts))
    similarity = 0
    for pair in pairs:
        try:
            similarity += find_sim_words(pair[0], pair[1])
        except TypeError:
            pass
    similarity = similarity / len(pairs)
    return similarity


def find_sim_sentences(highlighted, corpus):
    h_concepts = extract_concepts(highlighted)
    for i in range(len(corpus) - 1):
        concepts = []
        sim_amount = 0.0
        c_concepts = extract_concepts(corpus[i])
        concepts.append(h_concepts)
        concepts.append(c_concepts)
        sim_amount = sentence_sim(concepts)
        print "Highlighted sentence: {0}".format(highlighted)
        print "Corpus sentence: {0}".format(corpus[i])
        print "Similarity: {0}".format(sim_amount)


def sim_test():
    highlighted = "Different bacterias can affect cheese"
    find_sim_sentences(highlighted, cheese_text_list)

if __name__ == "__main__":
    sim_test()
