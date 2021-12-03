# Deep Neuronal Filter (DNF)
A closed-loop deep neural network (DNN) is used to filter EMG from ECG signals.

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

2) Install openCV library by running:

* For Linux run on terminal:

` sudo apt install libopencv-dev -y `

* For MacOS run on terminal with homebrew package manager https://brew.sh/:

`brew install opencv`

3) Install boost library by running:

* For Linux run on terminal:

` sudo apt-get install libboost-all-dev`

* For MacOS run on terminal with homebrew package manager https://brew.sh/:

`brew install boost`

4) And make sure you have ` cmake ` installed.

## How to compile and run the program:
1) Clone this repository:

` git clone https://github.com/berndporr/deepNeuronalFilter.git` 

2) Navigate to the folder:

`cd deepNeuronalFilter` 

3) execute the shell file:

`./run_all_stat.sh`

 This will create the necessary folders, build the program and the DNF library, and will run the executable.
 
If the executable file does not run and your operating system is a MacOS, you will need to run the following manually on the terminal. Make sure you are in the repository directory before you run.

 `./ecg_filter`

### Conditioning the Signal(ECG+EMG) and Noise(EMGonly) signals:
1) To pre-filter the signals:
    - Use the provided python script `pyFiles/generateFirFilters.py` to generate the `pyFiles/forSignal.dat` and `pyFiles/forNoise.dat` files before running the program.
    - In ` parameters.h ` file make sure that ` doNoisePreFilter ` and ` doSignalPreFilter ` are defined.
    - Insert the max length of filter buffers in the ` parameters.h ` file as the ` #define maxFilterLength ` variable.

### Delays (T):
1) Delay line for the Noise(EMGonly) signal (small Ts in the diagram above):
    - In ` parameters.h ` file make sure that ` doNoiseDelayLine ` is defined
    - In the same file, use ` define noiseDelayLineLength ` to specify the length of the delay line. 
    -  __This defines the number of inputs to the DNF__.
2) Delay the Signal(ECG+EMG) signal (the large T in the diagram):
    - In ` parameters.h ` file make sure that ` doSignalDelay ` is defined
    - In the same file, use ` define signalDelayLineLength ` to specify the duration of the delay
    - __This synchronises the correlation of the signals for optimised learning__
    
### Internal parameters of the network:
* Number of layers and Neurons in DNF:
    - In ` parameters.h ` use ` #define NLAYERS i ` to set the number of layers to `i `
    - Make sure the same number of ` #define Ni x ` are provided to set the number of neurons ` x ` in each layer
    - In ` main.cpp ` change the line ` int nNeurons[NLAYERS]={..., N3, N2, N1}; ` to add or remove ` Ni `

## Final results
The output data will be saved in the `cppData` folder for all recordings.
You can then use the provided python scripts to plot and analyse the final results.


