# Boolean-Retrieval-Model

## Introduction
Information need has to be translated into a Boolean expression which most users find awkward.
The Boolean queries formulated by the users are most often too simplistic.
The Boolean model imposes a binary criterion for deciding relevance.
The question of how to extend the Boolean model to accomodate partial matching and a ranking has attracted considerable attention in the past.

## Objective
I have created Inverted index and positional indexfor a set of collection to facilitate Boolean Model of IR. 
Inverted files and Positional files are the primary data structure to support the efficient determination of which documents contain specified terms and at which proximity. 

## Datasets
Dataset is a collection of Trump Speeches (File name: Trump Speeches 56 files) for
implementing inverted index and positional index. A single file contains a single speech from All
of Trump's Speeches from June 2015 to November 9, 2016.

## Some Definitions
Word – A delimited string of characters as itappears in the text.
Term – A “normalized” word (case, morphology, spelling etc); an equivalence class of words.
Token – An instance of a word or term occurring in a document.
Type – The same as a term in most cases: an equivalence class of tokens.

## Tokenization
Tokenization process decide when to emit atoken.
Input: “Friends, Romans and Countrymen” - > Output: Tokens :Friends, Romans, Countrymen
