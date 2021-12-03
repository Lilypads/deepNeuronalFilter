//
// Created by sama on 25/06/19.
// Edited by lily on 9/08/21.
//
#ifndef ECGFILTER_PARAMETERS_H
#define ECGFILTER_PARAMETERS_H

#define LMS_COEFF (int)(250)
#define LMS_LEARNING_RATE 0.00001

#define DoShowPlots

#define maxFilterLength 250

// NOISE:
#define doNoisePreFilter
#define doNoiseDelayLine
#define noiseDelayLineLength 45 //59

// SIGNAL:
#define doSignalPreFilter
#define doSignalDelay
#define signalDelayLineLength 45 //59

//NN specifications
#define DoDeepLearning
#define NLAYERS 7 //original 11
//#define N14 20 //14
//#define N13 20 //13
//#define N12 20 //12
//#define N11 20 //11
/*#define N10 20//29 //10
#define N9 20//23 //9
#define N8 20//19 //8
#define N7 20//17 //7*/
#define N6 39//13 //6
#define N5 27//11 //5
#define N4 13//7 //4
#define N3 7//5 //3
#define N2 5//3 //2
#define N1 3//2 //1
#define N0 1 //this has to always be 1


#endif //ECGFILTER_PARAMETERS_H