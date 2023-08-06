
# wer_in_detail

An utility to calculate wer and more (substitute, delete, insert, correct, number of words)

## Install

    pip install wer_in_detail

## Import

    import wer_in_detail
    
## Usage
    
    ground_truth = "hello world"
    hypothesis = "hello duck"

    wer, substitute, delete, insert, correct, num_of_words = wer(ground_truth, hypothesis)
    