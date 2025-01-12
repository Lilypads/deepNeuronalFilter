#include <iostream>
#include <fstream>
#include <string>
#include <stdio.h>
#include <boost/circular_buffer.hpp>
#include <boost/numeric/ublas/matrix.hpp>
#include <boost/numeric/ublas/io.hpp>
#include <Fir1.h>
#include <chrono>
#include <string>
#include <ctime>
#include <memory>
#include <numeric>
#include "cldl/Neuron.h"
#include "cldl/Layer.h"
#include "cldl/Net.h"
#include "parameters.h"

using namespace std;

//adding delay line for the noise
double noise_delayLine[noiseDelayLineLength] ={0.0};
boost::circular_buffer<double> signal_delayLine(signalDelayLineLength);

// CONSTANTS
const float fs = 250;
const int num_recordings = 8;//60;//32;//4;//12;  //how many recording to run

#ifdef doNoiseDelayLine
int num_inputs = noiseDelayLineLength;
#else
int num_inputs = 1;
#endif

//NEURAL NETWORK
#ifdef DoDeepLearning
//int nNeurons[NLAYERS]={N0}; //for 1 layer
int nNeurons[NLAYERS]={N6, N5, N4, N3, N2, N1, N0};
//int nNeurons[NLAYERS]={N10, N9, N8, N7, N6, N5, N4, N3, N2, N1, N0}; //for 11 layers
//int nNeurons[NLAYERS]={N14, N13, N12, N11, N10, N9, N8, N7, N6, N5, N4, N3, N2, N1, N0};// for 15 layers
int* numNeuronsP = nNeurons;
Net* NN = new Net(NLAYERS, numNeuronsP, num_inputs, 0, "");
double w_eta = 0;
double b_eta = 0;
#endif

//FILTERS
Fir1 *noise_filter;
Fir1 *signal_filter;
Fir1 *lms_filter = nullptr;

//SIGNALS
double sample_num, signal_raw_data, noise_raw_data, check_digit;

// GAINS
double noise_gain = 1;
double signal_gain = 1;
#ifdef DoDeepLearning
double remover_gain = 0;
double feedback_gain = 0;
#endif

// FILES
fstream signal_file;
fstream noise_file;
fstream params_file;
fstream lms_file;
fstream lms_remover_file;
fstream laplace_file;
ifstream raw_infile;
void saveParam(){
    params_file << "Gains: "    << "\n"
                << noise_gain << "\n"
                << signal_gain << "\n"
#ifdef DoDeepLearning
                << remover_gain << "\n"
                << feedback_gain << "\n"
                << "Etas: " << "\n"
                << w_eta << "\n"
                << b_eta << "\n"
                << "Network: " << "\n"
                << NLAYERS << "\n"
                /*<< N10 << "\n"
                << N9 << "\n"
                << N8 << "\n"		//for more layers parameter save
                << N7 << "\n"*/
                << N6 << "\n"
                << N5 << "\n"
                << N4 << "\n"
                << N3 << "\n"
                << N2 << "\n"
                << N1 << "\n"
                << N0 << "\n"
#endif
                << "LMS" << "\n"
                << LMS_COEFF << "\n"
                << LMS_LEARNING_RATE << "\n";

#ifdef doNoisePreFilter
    params_file    << "didNoisePreFilter" << "\n"
                   << maxFilterLength << "\n";
#endif
#ifdef doSignalPreFilter
    params_file    << "didSignalPreFilter" << "\n"
                   << maxFilterLength << "\n";
#endif
#ifdef doNoiseDelayLine
    params_file    << "didNoiseDelayLine" << "\n"
                   << noiseDelayLineLength << "\n";
#endif
#ifdef doSignalDelay
    params_file    << "didSignalDelay" << "\n"
                   << signalDelayLineLength << "\n";
#endif
}

void freeMemory(){
#ifdef DoDeepLearning
    delete NN;
#endif
    delete lms_filter;
}

void handleFiles(){
    params_file.close();
#ifdef DoDeepLearnig
    weight_file.close();
    remover_file.close();
    nn_file.close();
#endif
    signal_file.close();
    noise_file.close();
    lms_file.close();
    laplace_file.close();
    lms_remover_file.close();
}

int main(int argc, const char *argv[]) {
    //std::srand(1);
for (int k = 0; k < num_recordings; k++) {
    int RECORDING = k+1;
    cout << "recording: " << RECORDING << endl;
    int count = 0;

    //create files for saving the data and parameters
    string rcrdng = std::to_string(RECORDING);
#ifdef DoDeepLearning
    fstream nn_file;
    fstream remover_file;
    fstream weight_file;
#endif

#ifdef DoDeepLearning
    nn_file.open("./cppData/recording" + rcrdng + "/fnn_recording" + rcrdng + ".tsv", fstream::out);
    remover_file.open("./cppData/recording" + rcrdng + "/remover_recording" + rcrdng + ".tsv", fstream::out);
    weight_file.open("./cppData/recording" + rcrdng + "/lWeights_recording" + rcrdng + ".tsv", fstream::out);
#endif
    signal_file.open("./cppData/recording" + rcrdng + "/signal_recording" + rcrdng + ".tsv", fstream::out);
    noise_file.open("./cppData/recording" + rcrdng + "/noise_recording" + rcrdng + ".tsv", fstream::out);
    params_file.open("./cppData/recording" + rcrdng + "/cppParams_recording" + rcrdng + ".tsv", fstream::out);
    lms_file.open("./cppData/recording" + rcrdng + "/lmsOutput_recording" + rcrdng + ".tsv", fstream::out);
    lms_remover_file.open("./cppData/recording" + rcrdng + "/lmsCorrelation_recording" + rcrdng + ".tsv", fstream::out);
    laplace_file.open("./cppData/recording" + rcrdng + "/laplace_recording" + rcrdng + ".tsv", fstream::out);

    if (!params_file) {
        cout << "Unable to create files";
        exit(1); // terminate with error
    }
    if (!nn_file) {
        cout << "Unable to create nn files";
        exit(1); // terminate with error
    }

    raw_infile.open("./RecordingData/Recording" + rcrdng + ".tsv"); //load data
    
    if (!raw_infile) {
        cout << "Unable to open file";
        exit(1); // terminate with error
    }

#ifdef doNoisePreFilter
    noise_filter = new Fir1("./pyFiles/forNoise.dat");
    noise_filter->reset();
#endif
#ifdef doSignalPreFilter
    signal_filter = new Fir1("./pyFiles/forSignal.dat");
    signal_filter->reset();
#endif
#ifdef doNoisePreFilter
    int waitOutFilterDelay = maxFilterLength;
#else
#ifdef doSignalPreFilter
    int waitOutFilterDelay = maxFilterLength;
#else
    int waitOutFilterDelay = 1;
#endif
#endif

    lms_filter = new Fir1(LMS_COEFF);
    lms_filter->setLearningRate(LMS_LEARNING_RATE);

    double corrLMS = 0;
    double lms_output = 0;

        //setting up the neural networks
#ifdef DoDeepLearning
    NN->initNetwork(Neuron::W_RANDOM, Neuron::B_NONE, Neuron::Act_Sigmoid);
#endif

while (!raw_infile.eof()) {
        count += 1;
        //get the data from .tsv files:
        raw_infile >> sample_num >> signal_raw_data >> noise_raw_data >> check_digit;

        // GET ALL GAINS:
#ifdef DoDeepLearning
        signal_gain = 10000;
        noise_gain = 100;
        remover_gain = 100;
        feedback_gain = 100;
#endif

        //A) SIGNAL ELECTRODE:
        //1) AMPLIFY
        double signal_raw = signal_gain * signal_raw_data;
        //2) FILTERED
#ifdef doSignalPreFilter
        double signal_filtered = signal_filter->filter(signal_raw);
#else
        double signal_filtered = signal_raw;
#endif
        //3) DELAY
#ifdef doSignalDelay
        signal_delayLine.push_back(signal_filtered);
        double signal = signal_delayLine[0];
#else
        double signal = signal_filtered;
#endif

        //B) NOISE ELECTRODE:
        //1) AMPLIFY
        double noise_raw = noise_gain * noise_raw_data;

        //2) FILTERED
#ifdef doNoisePreFilter
        double noise_filtered = noise_filter->filter(noise_raw);
#else
        double noise_filtered = noise_raw;

#endif
        //3) DELAY LINE
        for (int i = noiseDelayLineLength-1 ; i > 0; i--){
            noise_delayLine[i] = noise_delayLine[i-1];

        }

        noise_delayLine[0] = noise_filtered;
        double* noise_delayed = &noise_delayLine[0];

        // NOISE INPUT TO NETWORK
#ifdef DoDeepLearning
        NN->setInputs(noise_delayed);
        NN->propInputs();

        // REMOVER OUTPUT FROM NETWORK
        double remover = NN->getOutput(0) * remover_gain;
        double f_nn = (signal - remover) * feedback_gain;

	/*if(remover != 0){
        	cout << "Not zero remover here!" << sample_num << ": "<< f_nn;
	}*/

        // FEEDBACK TO THE NETWORK 
        NN->setErrorCoeff(0, 1, 0, 0, 0, 0); //global, back, mid, forward, local, echo error
        NN->setBackwardError(f_nn);
        NN->propErrorBackward();
#endif

        // LEARN
#ifdef DoDeepLearning
	if(count == waitOutFilterDelay + noiseDelayLineLength + 1){
		w_eta = 0.01;
       	b_eta = 0;
	}
#endif


#ifdef DoDeepLearning
        NN->setLearningRate(w_eta, b_eta);
	if(count > waitOutFilterDelay + noiseDelayLineLength){
		NN->updateWeights(); //puts in neuron 
	}
        

        // SAVE WEIGHTS
        for (int i = 0; i < NLAYERS; i++) {
            weight_file << NN->getLayerWeightDistance(i) << " ";

        }
        weight_file << NN->getWeightDistance() << "\n";
        NN->snapWeights("cppData", "", RECORDING);
        //double l1 = NN->getLayerWeightDistance(0);
        //double l2 = NN->getLayerWeightDistance(1);
        //double l3 = NN->getLayerWeightDistance(2);

	/*if(NN->getWeightDistance() != 0){
        	cout << "Not zero weight here!" << sample_num << ": "<< NN->getWeightDistance();
	 	}*/

#endif

        // Do Laplace filter
        double laplace = signal - noise_filtered;

        // Do LMS filter
        corrLMS += lms_filter->filter(noise_filtered);
        lms_output = signal - corrLMS;
        lms_filter->lms_update(lms_output);

        // SAVE SIGNALS INTO FILES
        laplace_file << laplace << endl;
        signal_file << signal << endl;
        noise_file << noise_filtered << endl;
#ifdef DoDeepLearning
        remover_file << remover << endl;
        nn_file << f_nn << endl;
#endif
        lms_file << lms_output << endl;
        lms_remover_file << corrLMS << endl;

}
saveParam();
    handleFiles();
    raw_infile.close();
    cout << "The program has reached the end of the input file" << endl;

    }
freeMemory();
}