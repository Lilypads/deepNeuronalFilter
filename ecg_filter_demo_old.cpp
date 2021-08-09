#include <iostream>
#include <fstream>
#include <string>
#include <stdio.h>
#include <boost/circular_buffer.hpp>
#include <boost/numeric/ublas/matrix.hpp>
#include <boost/numeric/ublas/io.hpp>
#include <Iir.h>
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
#include "dynamicPlots.h"

//#define CVUI_IMPLEMENTATION
//#include "cvui.h"

using namespace std;
constexpr int ESC_key = 27;
//int startTime = time(NULL);

//adding delay line for the noise
double outer_delayLine[outerDelayLineLength] ={0.0};
boost::circular_buffer<double> inner_delayLine(innerDelayLineLength);

// CONSTANTS
//const float fs = 250;
//const int numTrials = 2; //as in open and closed
const int num_subjects = 12;

#ifdef doOuterDelayLine
int num_inputs = outerDelayLineLength;
#else
int num_inputs = 1;
#endif

//NEURAL NETWORK
#ifdef DoDeepLearning
int nNeurons[NLAYERS]={N10, N9, N8, N7, N6, N5, N4, N3, N2, N1, N0};
int* numNeuronsP = nNeurons;
Net* NN = new Net(NLAYERS, numNeuronsP, num_inputs, 0, "");
double w_eta = 0;
double b_eta = 0;
#endif

//FILTERS
Fir1 *outer_filter;
Fir1 *inner_filter;
Fir1 *lms_filter = nullptr;

//SIGNALS
double sample_num, inner_raw_data, outer_raw_data, check_digit;

// GAINS
double outer_gain = 1;
double inner_gain = 1;
#ifdef DoDeepLearning
double remover_gain = 0;
double feedback_gain = 0;
#endif

// FILES
fstream inner_file;
fstream outer_file;
fstream params_file;
fstream lms_file;
fstream lms_remover_file;
fstream laplace_file;
ifstream raw_infile;
void saveParam(){
    params_file << "Gains: "    << "\n"
                << outer_gain << "\n"
                << inner_gain << "\n"
#ifdef DoDeepLearning
                << remover_gain << "\n"
                << feedback_gain << "\n"
                << "Etas: " << "\n"
                << w_eta << "\n"
                << b_eta << "\n"
                << "Network: " << "\n"
                << NLAYERS << "\n"
                << N10 << "\n"
                << N9 << "\n"
                << N8 << "\n"
                << N7 << "\n"
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

#ifdef doOuterPreFilter
    params_file    << "didNoisePreFilter" << "\n"
                   << maxFilterLength << "\n";
#endif
#ifdef doInnerPreFilter
    params_file    << "didSignalPreFilter" << "\n"
                   << maxFilterLength << "\n";
#endif
#ifdef doOuterDelayLine
    params_file    << "didOuterDelayLine" << "\n"
                   << outerDelayLineLength << "\n";
#endif
#ifdef doInnerDelay
    params_file    << "didSignalDelay" << "\n"
                   << innerDelayLineLength << "\n";
#endif
}

void freeMemory(){
//#ifdef DoShowPlots
//    delete plots;
//#endif
#ifdef DoDeepLearning
    delete NN;
#endif
//#ifdef doOuterPreFilter
//    for (auto & i : outer_filter){
//        delete i;
//    }
//#endif
//#ifdef doInnerPreFilter
//    for (auto & i : inner_filter){
//        delete i;
//    }
//#endif
    delete lms_filter;
}

void handleFiles(){
    params_file.close();
#ifdef DoDeepLearnig
    weight_file.close();
    remover_file.close();
    nn_file.close();
#endif
    inner_file.close();
    outer_file.close();
    lms_file.close();
    laplace_file.close();
    lms_remover_file.close();
}

int main(int argc, const char *argv[]) {
    //std::srand(1);
for (int k = 0; k < num_subjects; k++) {
    int SUBJECT = k+1;
    cout << "subject: " << SUBJECT << endl;
    //int count = 0;

    //create files for saving the data and parameters
    string sbjct = std::to_string(SUBJECT);
#ifdef DoDeepLearning
    fstream nn_file;
    fstream remover_file;
    fstream weight_file;
#endif

#ifdef DoDeepLearning
    nn_file.open("./cppData/subject" + sbjct + "/fnn_subject" + sbjct + ".tsv", fstream::out);
    remover_file.open("./cppData/subject" + sbjct + "/remover_subject" + sbjct + ".tsv", fstream::out);
    weight_file.open("./cppData/subject" + sbjct + "/lWeights_subject" + sbjct + ".tsv", fstream::out);
#endif
    inner_file.open("./cppData/subject" + sbjct + "/inner_subject" + sbjct + ".tsv", fstream::out);
    outer_file.open("./cppData/subject" + sbjct + "/outer_subject" + sbjct + ".tsv", fstream::out);
    params_file.open("./cppData/subject" + sbjct + "/cppParams_subject" + sbjct + ".tsv", fstream::out);
    lms_file.open("./cppData/subject" + sbjct + "/lmsOutput_subject" + sbjct + ".tsv", fstream::out);
    lms_remover_file.open("./cppData/subject" + sbjct + "/lmsCorrelation_subject" + sbjct + ".tsv", fstream::out);
    laplace_file.open("./cppData/subject" + sbjct + "/laplace_subject" + sbjct + ".tsv", fstream::out);


    if (!params_file) {
        cout << "Unable to create files";
        exit(1); // terminate with error
    }
    if (!nn_file) {
        cout << "Unable to create nn files";
        exit(1); // terminate with error
    }

    raw_infile.open("./SubjectData/Subject" + sbjct + ".tsv");
    
    if (!raw_infile) {
        cout << "Unable to open file";
        exit(1); // terminate with error
    }

#ifdef doOuterPreFilter
    outer_filter = new Fir1("./pyFiles/forOuter.dat");
    outer_filter->reset();
#endif
#ifdef doInnerPreFilter
    inner_filter = new Fir1("./pyFiles/forInner.dat");
    inner_filter->reset();
#endif
//#ifdef doOuterPreFilter
//    int waitOutFilterDelay = maxFilterLength;
//#else
//#ifdef doInnerPreFilter
//    int waitOutFilterDelay = maxFilterLength;
//#else
//    int waitOutFilterDelay = 1;
//#endif
//#endif

    lms_filter = new Fir1(LMS_COEFF);
    lms_filter->setLearningRate(LMS_LEARNING_RATE);

    double corrLMS = 0;
    double lms_output = 0;

        //setting up the neural networks
#ifdef DoDeepLearning
    NN->initNetwork(Neuron::W_RANDOM, Neuron::B_RANDOM, Neuron::Act_Sigmoid);
#endif

while (!raw_infile.eof()) {
        //count += 1;
        //get the data from .tsv files:
        raw_infile >> sample_num >> inner_raw_data >> outer_raw_data >> check_digit;

        // GET ALL GAINS:
#ifdef DoDeepLearning
        inner_gain = 1;
        outer_gain = 1;
        remover_gain = 0.5;
        feedback_gain = 10;
#endif

        //A) INNER ELECTRODE:
        //1) AMPLIFY
        double inner_raw = inner_gain * inner_raw_data;
        //2) FILTERED
#ifdef doInnerPreFilter
        double inner_filtered = inner_filter->filter(inner_raw);
#else
        double inner_filtered = inner_raw;
#endif
        //3) DELAY
#ifdef doInnerDelay
        inner_delayLine.push_back(inner_filtered);
        double inner = inner_delayLine[0];
#else
        double inner = inner_filtered;
#endif

        //B) OUTER ELECTRODE:
        //1) AMPLIFY
        double outer_raw = outer_gain * outer_raw_data;
        //2) FILTERED
#ifdef doOuterPreFilter
        double outer_filtered = outer_filter->filter(outer_raw);
#else
        double outer_filtered = outer_raw;
#endif
        //3) DELAY LINE
        for (int i = outerDelayLineLength-1 ; i > 0; i--){
            outer_delayLine[i] = outer_delayLine[i-1];

        }
        outer_delayLine[0] = outer_filtered;
        double* outer_delayed = &outer_delayLine[0];

        // OUTER INPUT TO NETWORK
#ifdef DoDeepLearning
        NN->setInputs(outer_delayed);
        NN->propInputs();

        // REMOVER OUTPUT FROM NETWORK
        double remover = NN->getOutput(0) * remover_gain;
        double f_nn = (inner - remover) * feedback_gain;

        // FEEDBACK TO THE NETWORK 
        NN->setErrorCoeff(0, 1, 0, 0, 0, 0); //global, back, mid, forward, local, echo error
        NN->setBackwardError(f_nn);
        NN->propErrorBackward();
#endif

        // LEARN
#ifdef DoDeepLearning
        w_eta = 1;
        b_eta = 2;
#endif

#ifdef DoDeepLearning
        NN->setLearningRate(w_eta, b_eta);
        NN->updateWeights();

        // SAVE WEIGHTS
        for (int i = 0; i < NLAYERS; i++) {
            weight_file << NN->getLayerWeightDistance(i) << " ";
        }
        weight_file << NN->getWeightDistance() << "\n";
        NN->snapWeights("cppData", "", SUBJECT);
        double l1 = NN->getLayerWeightDistance(0);
        double l2 = NN->getLayerWeightDistance(1);
        double l3 = NN->getLayerWeightDistance(2);
#endif

        // Do Laplace filter
        double laplace = inner - outer_filtered;

        // Do LMS filter
        corrLMS += lms_filter->filter(outer_filtered);
        lms_output = inner - corrLMS;
        lms_filter->lms_update(lms_output);

        // SAVE SIGNALS INTO FILES
        laplace_file << laplace << endl;
        inner_file << inner << endl;
        outer_file << outer_filtered << endl;
#ifdef DoDeepLearning
        remover_file << remover << endl;
        nn_file << f_nn << endl;
#endif
        lms_file << lms_output << endl;
        lms_remover_file << corrLMS << endl;

/**
 * If the Esc button is pressed on the interactive window the final SNRs are printed on the console and
 * all SNRs and parameters are saved to a file. Also all pointers are deleted to free dynamically allocated memory.
 * Then the files are closed and program returns with 0.
 */
        if (cv::waitKey(20) == ESC_key) {
            saveParam();
#ifdef DoDeepLearning
            NN->snapWeights("cppData", "", SUBJECT);
#endif
            handleFiles();
            freeMemory();
            return 0;
	}

}
saveParam();
    handleFiles();
    raw_infile.close();
    cout << "The program has reached the end of the input file" << endl;

    }
freeMemory();
}