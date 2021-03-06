# Phy-Net
This repository is a perliminary looks at compressing physics simulations onto neural networks. Similary works can be found in "[Accelerating Eulerian Fluid Simulation With Convolutional Networks](https://arxiv.org/pdf/1607.03597.pdf)" and "[Convolutional Neural Networks for steady Flow Approximation](https://autodeskresearch.com/publications/convolutional-neural-networks-steady-flow-approximation)".


## Diffusion
Compressing an [Implicit Finite Difference Method](https://en.wikipedia.org/wiki/Finite_difference_method) approximation of diffusion.

[![IMAGE ALT TEXT HERE](http://img.youtube.com/vi/N57BvSspLtU/0.jpg)](https://www.youtube.com/watch?v=N57BvSspLtU)

## Lattice Boltzmann Fluid flow
Compressing non-laminar fluid flow around objects. The fluid flow was generated with the open source [palabos library](http://www.palabos.org/). The cpu time for each simulation is approximatly 155 seconds. The approximate time for the neural network is .78 seconds. Total speed up so far is roughly 198 x. The video bellow was not in the training set. The left is true, middle generated, right difference.

[![IMAGE ALT TEXT HERE](http://img.youtube.com/vi/AAQCuJM67RE/0.jpg)](https://www.youtube.com/watch?v=AAQCuJM67RE=54s)

## Network Details
The network is kept all convolutional and uses an [convolutional lstm](https://github.com/loliverhennigh/Convolutional-LSTM-in-Tensorflow). Up sampling using Deconvolution is replased with computationaly effeicent [subpixel convolutions](https://github.com/Tetrachrome/subpixel). Keeping the network convolutional allows the trained model to be used on simulations of different sizes allowing the network to focus on just learning compressed representations of the dynamics.



