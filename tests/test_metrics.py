import time

import pytest
from tqdm import tqdm

from src.snippyts.metrics import average_token_similarity


def test_performance_average_token_similarity():
    sentences = [
        "Astronomy: The James Webb Space Telescope can detect faint infrared signals from galaxies formed over 13 billion years ago.",
        "Cooking: Searing meat before slow cooking enhances flavor through the Maillard reaction.",
        "Music: Beethoven composed some of his greatest works after losing his hearing.",
        "Psychology: The placebo effect demonstrates how belief alone can trigger real physiological responses.",
        "Linguistics: The Pirahã language of the Amazon is notable for having no fixed words for numbers.",
        "History: The Great Fire of London in 1666 destroyed over 13,000 houses but resulted in surprisingly few deaths.",
        "Mathematics: A prime number is only divisible by 1 and itself, with 2 being the only even prime.",
        "Art: Van Gogh sold only one painting during his lifetime, despite creating over 2,000 artworks.",
        "Technology: Quantum computing leverages the principles of superposition and entanglement to perform complex calculations.",
        "Geography: Lake Baikal in Siberia is the deepest and oldest freshwater lake in the world.",
        "Literature: James Joyce’s Ulysses takes place entirely over the course of a single day in Dublin.",
        "Literature: James Joyce’s Ulysses takes place over the course of a single day.",
        "Physics: According to general relativity, massive objects warp spacetime, creating the effect we perceive as gravity.",
        "Philosophy: Descartes’ famous statement “Cogito, ergo sum” means “I think, therefore I am.”",
        "Philosophy: Descartes’ famous statement means “I think, therefore I am.”",
        "Economics: Inflation erodes the purchasing power of currency over time.",
        "Economics: Inflation erodes the purchasing power of currency.",
        "Film: The 1927 film Metropolis is considered a pioneering work of science fiction cinema.",
        "Film: The 1927 film Metropolis is considered a pioneering work of cinema.",
        "Film: The 1927 film Metropolis is considered a pioneering work of science fiction.",
        "Film: The 1927 film Metropolis is a work of science fiction.",
        "Biology: Mitochondria, often called the 'powerhouse of the cell', produce ATP through cellular respiration.",
        "Law: Habeas corpus is a legal principle that protects against unlawful imprisonment.",
        "Education: Bloom’s Taxonomy categorizes cognitive skills from basic recall to complex evaluation and creation.",
        "Religion: The Eightfold Path in Buddhism outlines practices leading to enlightenment and cessation of suffering.",
        "Sports: The marathon commemorates the legendary run of a Greek soldier from the Battle of Marathon to Athens.",
    ]
    start_time = time.time()
    pbar = tqdm(total=10 * len(sentences) * len(sentences))
    for _ in range(10):
        for i in range(len(sentences)):
            for j in range(len(sentences)):
                pbar.update(1)
                average_token_similarity(sentences[i], sentences[j])
    print("--- %s seconds ---" % (time.time() - start_time))


def test_average_token_similarity():
    tests = [
        (
            "Film: The 1927 film Metropolis is considered a pioneering work of science fiction.",
            "Film: The 1927 film Metropolis is considered a pioneering work of science fiction cinema.",
            0.9375
        ),
        (
            "Film: The 1927 film Metropolis is considered a pioneering work of science fiction.",
            "Film: The 1927 film Metropolis is considered a pioneering work of cinema.", 
            0.9077
        ),
        (
            "Film: The 1927 film Metropolis is considered a pioneering work of science fiction.", 
            "Film: The 1927 film Metropolis is considered a pioneering work of science fiction.", 
            1.0
        ),
        (
            "Film: The 1927 film Metropolis is considered a pioneering work of science fiction.", 
            "Film: The 1927 film Metropolis is a work of science fiction.", 
            0.8667
        ),
        (
            "Film: The 1927 film Metropolis is considered a pioneering work of science fiction.", 
            "Biology: Mitochondria, often called the 'powerhouse of the cell', produce ATP through cellular respiration.", 
            0.3939
        ),
        (
            "Film: The 1927 film Metropolis is considered a pioneering work of science fiction.", 
            "Law: Habeas corpus is a legal principle that protects against unlawful imprisonment.", 
            0.4706
        )
    ]
    for arg0, arg1, sim in tests:
        assert average_token_similarity(arg0, arg1) == sim
        assert average_token_similarity(arg1, arg0) == sim