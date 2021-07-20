# Deep Neuronal Filter (DNF)
A closed-loop deep neural network (DNN) is used to filter 
the noise from the Delta and Alpha regions of EEG signals.
The EEG signals were obtained from 12 subjects using a 
novel smart 3D printed electrode consisting of a central and a ring electrodes.

## Prerequisites Libraries and packages:
Process might differ depend on your operating system.

1) Install the Fir1 library from _https://github.com/berndporr/fir1_ 

* For Linux run on terminal:

` sudo add-apt-repository ppa:berndporr/dsp `

` sudo apt-get install fir1 ` 

` sudo apt-get install fir1-dev `

* For MacOS run on terminal with homebrew package manager https://brew.sh/:

`brew tap berndporr/dsp`

`brew install fir`

2) Install Iir1 library from _https://github.com/berndporr/iir1_

* For MacOS run on terminal with homebrew package manager https://brew.sh/:

`brew tap berndporr/dsp`

`brew install iir`

3) Install openCV library by running:

* For Linux run on terminal:

` sudo apt install libopencv-dev -y `

* For MacOS run on terminal with homebrew package manager https://brew.sh/:

`brew install opencv`

4) Install boost library by running:

* For Linux run on terminal:

` sudo apt-get install libboost-all-dev`

* For MacOS run on terminal with homebrew package manager https://brew.sh/:

`brew install boost`

5) And make sure you have ` cmake ` installed.

## How to compile and run the program:
1) Clone this repository:

` git clone https://github.com/berndporr/deepNeuronalFilter.git` 

2) Navigate to the folder:

`cd deepNeuronalFilter` 

3) execute the shell file:

`./run_all_stat.sh`

 This will create the necessary folders, build the program and the DNF library, and will run the executable.
 An interactive GUI will appear as below.
 
If the executable file does not run and your operating system is a MacOS, you might need to run the following manually on the terminal. Make sure you are in the repository directory before you run.
 
 `chmod 777 eeg_filter`
 
 `./eeg_filter`
 
 ![Figure 2](./fig2.png)

### Conditioning the Inner and Outer signals:
1) To pre-filter the Inner and Outer signals:
    - Use the provided python script `pyFiles/generateFirFilters.py` to generate the `pyFiles/forInner.dat` and `pyFiles/forOuter.dat` files before running the program.
    - In ` parameters.h ` file make sure that ` doOuterPreFilter ` and ` doInnerPreFilter ` are defined.
    - Insert the max length of filter buffers in the ` parameters.h ` file as the ` #define maxFilterLength ` variable.

### Delays (T):
1) Delay line for the Outer signal (small Ts in the diagram above):
    - In ` parameters.h ` file make sure that ` doOuterDelayLine ` is defined
    - In the same file, use ` define outerDelayLineLength ` to specify the length of the delay line. 
    -  __This defines the number of inputs to the DNF__.
2) Delay the Inner signal (the large T in the diagram):
    - In ` parameters.h ` file make sure that ` doInnerDelay ` is defined
    - In the same file, use ` define innerDelayLineLength ` to specify the duration of the delay
    - __This synchronises the correlation of the signals for optimised learning__
    
### Internal parameters of the network:
1) Number of layers and Neurons in DNF:
    - In ` parameters.h ` use ` #define NLAYERS i ` to set the number of layers to `i `
    - Make sure the same number of ` #define Ni x ` are provided to set the number of neurons ` x ` in each layer
    - In ` main.cpp ` change the line ` int nNeurons[NLAYERS]={..., N3, N2, N1}; ` to add or remove ` Ni `
2) Learning rates:
    - The learning rate for updating the _weights_ and _biases_ are defined in the form of _Eta.10<sup>(power)</sup>_. 
    Use the __Eta__ and __power__ sliders to change the two learning rates.

## Closing the program:
Use the Esc key on the interactive window to close the program safely and avoid corrupted files.

## Final results
The output data will be saved in the `cppData` folder for all subjects.
You can then use the provided python scripts to plot and analyse the final results.



[![DOI](https://zenodo.org/badge/306690603.svg)](https://zenodo.org/badge/latestdoi/306690603)

