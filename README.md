# Text analysis of scientific articles

## Introduction

This small project is an attempt to take a look at the corellation between the language used in the article and its content. Is it possible to predict the number of citations of an article based on the words used by researchers?

## Short description of tools

Most of the work is done in python 3, Elsevier API is used to mine text. Module [EllsevierMining](./ElsevierMining.py) requires the environmental varibale ELSKEY to be set to the  Elsevier API key.
You can add it to .bashrc or .zshrc by running `echo export ELSKEY='your-API-key' >> ~/.zshrc`