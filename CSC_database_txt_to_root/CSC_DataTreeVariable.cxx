namespace CSCConvertor {
    
TTree *SparksTree;
    
Char_t chamber[10];
Int_t  layerInt;
Int_t chamberNumber;
Int_t timeYMD;
Char_t timestamp[32];
Float_t amplitude;
Float_t baseline;
Float_t timediff;
Float_t HV;
Float_t Humidity;
    
TDatime *dataTime;
UInt_t dataTimeInt;
    
void buidBranchTree() {
    
    SparksTree = new TTree("SparksTree","data");
    
        SparksTree->Branch("Humidity", &Humidity, "Humidity/F");
        SparksTree->Branch("ChamberNumber", &chamberNumber, "ChamberNumber/I", 10);
        SparksTree->Branch("Layer", &layerInt, "Layer/I");
        SparksTree->Branch("dateTime", &dataTimeInt, "dateTime/I");
        SparksTree->Branch("timeYMD", &timeYMD, "timeYMD/I");
        SparksTree->Branch("Amplitude", &amplitude, "Amplitude/F");
        SparksTree->Branch("Baseline", &baseline, "Baseline/F");
        SparksTree->Branch("Timediff", &timediff, "Timediff/F");
        SparksTree->Branch("HV", &HV, "HV/F");
    
}
}
