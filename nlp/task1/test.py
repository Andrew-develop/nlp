# -*- coding: utf-8 -*-
"""test.py

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1TY4vVB1QX5dcmb0BGraFtNWAnUJ7U4y6
"""

import sys
import torch
import torch.nn.functional as F

if __name__ == '__main__':

    args = sys.argv
    parameters = torch.load(args[1])
    words = open(args[2], 'r', encoding='utf-8').read().splitlines()

    C = parameters['C']
    W1 = parameters['W1']
    b1 = parameters['b1']
    W2 = parameters['W2']
    b2 = parameters['b2']

    chars = sorted(list(set(''.join(words))))
    stoi = {s: i + 1 for i, s in enumerate(chars)}
    stoi['.'] = 0
    itos = {i: s for s, i in stoi.items()}

    X, Y = [], []
    for w in words:
        context = [0] * 3
        for ch in w + '.':
            ix = stoi[ch]
            X.append(context)
            Y.append(ix)
            context = context[1:] + [ix]  # crop and append

    Xte = torch.tensor(X)
    Yte = torch.tensor(Y)

    emb = C[Xte]  # (32, 3, 2)
    h = torch.tanh(emb.view(-1, 30) @ W1 + b1)  # (32, 100)
    logits = h @ W2 + b2  # (32, 27)
    loss = F.cross_entropy(logits, Yte)
    print(f'test loss: {loss}')

    g = torch.Generator().manual_seed(2147483647 + 10)

    for _ in range(20):
        out = []
        context = [0] * 3 # initialize with all ...
        while True:
            emb = C[torch.tensor([context])] # (1,block_size,d)
            h = torch.tanh(emb.view(1, -1) @ W1 + b1)
            logits = h @ W2 + b2
            probs = F.softmax(logits, dim=1)
            ix = torch.multinomial(probs, num_samples=1, generator=g).item()
            context = context[1:] + [ix]
            out.append(ix)
            if ix == 0:
                break

        print(''.join(itos[i] for i in out))