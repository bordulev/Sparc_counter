#ifndef __CINT__
#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <bitset>

#include <TFile.h>
#include <TNtuple.h>
#include <TH2.h>
#include <TProfile.h>
#include <TCanvas.h>
#include <TFrame.h>
#include <TROOT.h>
#include <TSystem.h>
#include <TRandom3.h>
#include <TBenchmark.h>
#include <TInterpreter.h>
#include <TApplication.h>
#include <TString.h>
#include <TBits.h>

#include <TNamed.h>
#include <TArrayI.h>
#include <TColor.h>
#include <TStyle.h>
#include <TF1.h>
#include <TGraph.h>
#include <TTree.h>

#include "CSC_ParseFilesConvertor.cxx"

TROOT root("",""); // static TROOT object

int main(int argc, char** argv)
#else
TFile* hsimple(Int_t get=0)
#endif
{
    CSCConvertor::convertTxtToRoot();
    
    return 1;
#ifdef __CINT__
    return hfile;
#else
    return 0;
#endif
}
