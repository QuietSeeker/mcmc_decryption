import re
import string
import random
import requests
from collections import Counter
import math
import enchant

english_dict = enchant.Dict("en_GB")


def generate_cipher():
    alphabet = list(string.ascii_lowercase)
    random.shuffle(alphabet)
    return "".join(alphabet)


def encode_text(text, cipher):
    mapping = str.maketrans(string.ascii_lowercase, cipher)
    return text.translate(mapping)


def decode_text(ciphertext, cipher):
    mapping = str.maketrans(cipher, string.ascii_lowercase)
    return ciphertext.translate(mapping)


book_url = "https://www.gutenberg.org/cache/epub/1661/pg1661.txt"


def get_book_text(url):
    response = requests.get(url)
    return response.text


def clean_text(text):
    # Remove all non-alphabetical characters except spaces
    text = re.sub(r"[^a-zA-Z\s]", "", text)

    # Remove all accent characters
    text = re.sub(
        r"[àáâãäåæçèéêëìíîïðñòóôõöøùúûüýþÿÀÁÂÃÄÅÆÇÈÉÊËÌÍÎÏÐÑÒÓÔÕÖØÙÚÛÜÝÞß]", "", text
    )

    # Convert all letters to lowercase
    text = text.lower()

    return text


def n_grams(text, n):
    for i in range(len(text) - n + 1):
        s = ""
        for t in range(n):
            s += text[i + t]
        yield s


def calc_n_gram_probs(text, n):
    n_gram_counts = Counter(n_grams(text, n))
    n_gram_probs = {k: v / n_gram_counts.total() for k, v in n_gram_counts.items()}
    return n_gram_probs


def get_n_gram_prob(n_gram, n_gram_probs):
    if n_gram in n_gram_probs:
        return n_gram_probs[n_gram]
    else:
        return 1 / len(n_gram_probs)


def log_score_similarity(candidate, n_gram_probs, n):
    lscore = 0

    for n_gram in n_grams(candidate, n):
        prob = get_n_gram_prob(n_gram, n_gram_probs)
        lscore += math.log(prob)

    return lscore


cipher = generate_cipher()

book_text = get_book_text(book_url)
book_text = clean_text(book_text)

n = 2
n_gram_probs = calc_n_gram_probs(book_text, n)
# print(n_gram_probs)
# sorted_probs = sorted(n_gram_probs.items(), key=lambda item: item[1])
# print(sorted_probs)


def perform_transpositions(string, repeat):
    string = list(string)
    for _ in range(repeat):
        i, j = random.sample(range(len(string)), 2)
        string[i], string[j] = string[j], string[i]

    return "".join(string)


print("Markov Chain Monte Carlo method for decrypting substitution ciphertext\n")

plaintext = "to be or not to be that is the question whether tis nobler in the mind to suffer the slings and arrows of outrageous fortune or to take arms against a sea of troubles"

# plaintext = "What you see and what you hear depends a great deal on where you are standing. It also depends on what sort of person you are."

plaintext = clean_text(" " + plaintext + " ")

# Generate a random cipher to be the true cipher
true_cipher = generate_cipher()

# Encode the plaintext
ciphered_text = encode_text(plaintext, true_cipher)
print(f"(Target) Plaintext: {plaintext}\n")
print(f"Ciphertext: {ciphered_text}\n")
input("Press ENTER to start")


# Metropolis MCMC algorithm
iterations = 500000

# Generate the initial cipher
current_cipher = generate_cipher()

# A counter to count accepted ciphers
accepted_cipher_count = 0

for _ in range(iterations):
    # Propose a new cipher
    proposed_cipher = perform_transpositions(
        current_cipher, 2
    )  # Repeating transpositions can get us to more ciphers (similar effect to changing variance of Normal dist)

    proposed_decoding = decode_text(ciphered_text, proposed_cipher)
    current_decoding = decode_text(ciphered_text, current_cipher)

    # Log-likelihood of the decoded text from the proposed cipher
    log_proposed_likelihood = log_score_similarity(proposed_decoding, n_gram_probs, n)

    # Log-likelihood of the decoded text from the current cipher
    log_current_likelihood = log_score_similarity(current_decoding, n_gram_probs, n)

    # Acceptance probability of the proposal, defined by the Metropolis algorithm
    # (Log subtraction is division)
    acceptance_probability = min(
        1, math.exp(log_proposed_likelihood - log_current_likelihood)
    )

    accept = random.random() < acceptance_probability

    if accept:
        current_cipher = proposed_cipher

        # Print the text as decoded by the current cipher
        print(f"Acceptance {accepted_cipher_count}: {proposed_decoding}")

        # Increment the counter so that we can keep track of acceptances
        # This is just for printing the output
        accepted_cipher_count += 1
