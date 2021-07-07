.. _Conceptual Overview:

**********
Conceptual Overview
**********


In the following, I briefly outline the approach I chose to achieve notarization of data via a `blockchain <https://en.wikipedia.org/wiki/Blockchain>`_.


General Principle
===============
I principle, I only exploit the fact that a blockchain is distributed record-keeping system. Something that is saved in a transaction on a blockchain cannot be changed anymore and is publicly accessible to anyone.
To achieve notarization, I simply save the `hash checksum <https://en.wikipedia.org/wiki/Hash_function>`_ (more precisely, the `SHA256 checksum <https://en.wikipedia.org/wiki/SHA-2#Comparison_of_SHA_functions>`_) of a file or piece of data in a transaction on a blockchain.
"Saving in a transaction" in this context means that I save a string as the "input_data" (comparable to the reference field in a wire transfer) of a transaction.

Anyone who receives this file or piece of data and knows which transaction on the blockchain to look up can verify that the file has not been changed since its hash was placed on the blockchain.
To do so, that person just needs to calculate the hash checksum of the file at hand and compare it to the on checksum saved as "input_data" in the transaction on the blockchain.
Any transaction on the blockchain has a timestamp, if the two checksums match the file has not been altered since placed on the blockchain.

The transaction that is sent is a simple one: it is just over 0 ETH from one account back to itself. The only thing that matters is the string saved as "input_data".

Of course, one could argue that it would be possible to change data before saving the hash on the blockchain. For this reason it is crucial to ensure that the notarization of the data takes place automatically right after the data is created.
For example, when collecting data with oTree, notarization should be built-in the code so that the experimenter has no chance to alter data before it is notarized.

Details on (the Connection to) the Ethereum Network
===============
The general principle outlined above applies to any blockchain. For this specific exemplary implementation I chose to use the `Ethereum blockchain <https://en.wikipedia.org/wiki/Ethereum>`_.
There are several things to take care of. I need to have an account and connect to the Ethereum network. Further, the account I use needs to have sufficient balance to pay for the transaction fees necessary to process (mine) it.

For the purposes of this proof-of-concept implementation, I simply use an account on a test network, which, in principle, functions exactly like the actual main network, but does not require actual money.
For a live implementation, switching to the main network should be considered. This can easily be achieved with the code I provide, only a few things need to be changed.
The test network I use is the Ropsten ETH test network. For more details see `here <https://www.2key.network/blog-posts/what-is-ropsten-eth-and-how-can-i-get-some>`_.
The fact that I use an account on the Ropsten test network allows me to (relatively) unproblematically share the data to access the account. This allows anyone interested in reviewing my code to run things without having to set up their own account.

To connect to the (Ropsten) Ethereum network, I use the free service provider `infura <https://infura.io>`_ which provides a simple API to access Ethereum networks.
I have an account with infura that provides me with a URL to connect to the Ethereum network. You will notice that the URL is used in this repository referenced by ``INFURA_URL``.

To write code to execute stuff on the Ethereum blockchain I employ the python package `Web3.py <https://web3py.readthedocs.io/en/stable/>`_.

*Setting up your own accounts*
If you are interested in setting up your own accounts to try out things, I recommend creating an ETH wallet with `metamask <https://metamask.io>`_. With metamask, you have accounts on the Ethereum main net and on several test networks.
To get Ropsten ETH you can simply use the `Ropsten Faucet <https://faucet.ropsten.be>`_.
You can also create an account on `infura <https://infura.io>`_  to generate your own URL to connect to ETH networks. The interface is straightforward.


Within oTree
===============

`oTree <https://www.otree.org/>`_ is an open-source framework with which (among other things) economic experiments can be run. To include the notarization functionalities I developed into oTree I do the following:

1. I save the decisions a player made on a session level as ``participant.vars``.
2. For the player class, I add methods to create a string with information that can be hashed.
3. I also add a method on the player level that calls the functions for notarization to save the hashed string on the blockchain.
4. By adding a method ``before_next_page(self)`` on the last page before the results page of the experiment, I trigger the notarization.

The result of this is that for each player, I have a transaction hash saved that is generated after all input is complete.
This transaction hash can then be used for verification. For a more detailed example, see section :ref:`oTree Example - Walkthrough`.