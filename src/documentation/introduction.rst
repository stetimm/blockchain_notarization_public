.. _introduction:


************
Introduction
************


This is code for notarization of data via the Ethereum blockchain. It accomplishes two very basic tasks:

1. *Notarization*: It let's you notarize a file, by creating a transaction on the blockchain that stores the hash of the file at the time of notarization.
2. *Verification*: It let's you check that a file you have at hand is identical to the one saved in a given notarization transaction on the blockchain.

There are two main examples in this repository. One basic example that allows you to upload and verify files on disk via a primitive command line interaction.
The second example is built around the experimental software package oTree. It is shown how experimental data can be notarized in oTree and how one could verify the raw data with a few lines of code.

The project is currently in a proof-of-concept phase.

To get things running quickly and play around with the functionalities please refer to section :ref:`Quick Start`.

**Important**: Before you can do anything meaningful with this code, you need to get the ``blockchain_config.py`` from me and add it to the *src* directory. This is not tracked as it contains sensible account data.

Motivation
===============

There has been a push towards pre-registration of experiments in order to improve credibility. It has become good scientific practice to preregister experimental protocols, hypotheses and a plan for statistical analysis prior to conducting an experiment.
However, there is no way of proving that the data belonging to an experimental study have not been collected prior to pregistration.
By saving the results of each subject in an experiment directly after they are created on a blockchain, two things can be accomplished:

1. Give non-repudiable proof of the time of creation of the data.
2. Ensure that the data has not been altered.

Further details are outlined in section :ref:`Conceptual Overview`.

My project is a modest attempt to raise the bar for good scientific practices a little bit. At this point, it is only a proof-of-concept. For it to become used more widespread, greater usability must be achieved.
For my purposes, e.g., when running an experiment for my master thesis, I can already use it, though.

Code Structure
===============

As I am not working with real data and don't need to do any data cleaning, I have decided against using pytask. All code resides in the *src* directory.

The code is structured as follows:

    - *notarization_code*: The core modules that achieve notarization and verification.
    - *examples*: Scripts for the two main examples, discussed in :ref:`Quick Start`.
    - *tests*: Tests for all modules in notarization_code.
    - *otree_code*: Code for the oTree example, requires familiarity with oTree.
    - *documentation*: Code to build documentation with sphinx. Note that I host my docu as a github page based on a different branch.
    - *sandbox*: A folder with early attempts, including playing around with a locally hosted chain software, Ganache. Can be completely ignored.

**Important**: In order to be able to run anything meaningful, you need to add the ``blockchain_config.py`` file to the *src* directory. This is not tracked as it contains sensible account data.