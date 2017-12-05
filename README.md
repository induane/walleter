# walleter

Bitcoin Wallet Checker

This project aims to make checking various wallet operations simple. It ships
a basic file called ``known`` which has some addresses to derive. Otherwise
it can be given as seed value at the command line. It spits out some basic
info on the given address.

It's pretty hacky right now and has a dependency on coinkit which I plan on
removing over time with simple implementations of only tools this project
needs.

Example using the well know 'correct horse battery staple' wallet seed:

```bash
$ walleter -s "correct horse battery staple"
INFO: Opening BlockchainInfo session
INFO: Session open
INFO: Using custom seed: correct horse battery staple
INFO: Wallet found: correct horse battery staple; Received: 15.94334248; Address: 1JwSSubhmg6iPtRjtyqhUYYH7bZg3Lfy1T; Private Key: 5KJvsngHeMpm884wtkJNzQGaCErckhHJBGFsvd3VyK5qMZXj3hS; Balance: 0.00000000
```

You can also use the iterations argument to follow key derivations by feeding
the resulting address back into the next iteration as the seed value for the
next iteration. In the case of the infamous "correct horse battery staple" for
instance, the wallet address "1JwSSubhmg6iPtRjtyqhUYYH7bZg3Lfy1T" was in turn
used as a seed value for another wallet:

```bash
$ walleter -s "correct horse battery staple"
INFO: Opening BlockchainInfo session
INFO: Session open
INFO: Using custom seed: correct horse battery staple
INFO: Wallet found: correct horse battery staple; Received: 15.94334248; Address: 1JwSSubhmg6iPtRjtyqhUYYH7bZg3Lfy1T; Private Key: 5KJvsngHeMpm884wtkJNzQGaCErckhHJBGFsvd3VyK5qMZXj3hS; Balance: 0.00000000
INFO: Wallet found: 1JwSSubhmg6iPtRjtyqhUYYH7bZg3Lfy1T; Received: 0.00006000; Address: 19QBydCuMiY7aRTbkP2tb3KQJUWkTrr5Xi; Private Key: 5JB2t78gAAiDeRf5KRxugTjWcu862yaf44bWL9eVvAUj1ipA1iU; Balance: 0.00000000
```


## Makefile

This project uses a Makefile for various tasks. Some of the available tasks
are listed below.

* `make clean` - Clean build artifacts out of your project
* `make test` - Run Unit Tests (using nose)
* `make sdist` - Build a Python source distribution
* `make rpm` - Build an RPM
* `make docs` - Build the Sphinx documentation
* `make pep8` - Get a pep8 compliance report about your code
* `make` - Equivalent to `make test pep8 docs sdist rpm`
