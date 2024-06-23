# mcmc_decryption
Markov Chain Monte Carlo Decryption \
An implementation of MCMC Metropolis algorithm for decrypting text encrypted by an unknown substitution cipher.

### Algorithm
The algorithm works by using a random walk to search for the cipher that was likely used.\
The random walk (Markov Chain) is constructed so that its stationary distribution is the same as the prosterior probability distribution.\
This construction is given by the Metropolis algorithm.\
We then sample likely ciphers, and approximate the plain text!

#### Helpful Resources
https://blog.djnavarro.net/posts/2023-04-12_metropolis-hastings/ \
https://maximilianrohde.com/posts/code-breaking-with-metropolis/ \
https://www.youtube.com/watch?v=U561HGMWjcw
