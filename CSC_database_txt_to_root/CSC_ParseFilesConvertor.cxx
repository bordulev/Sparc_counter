#include <stdio.h>
#include <fstream>
#include <iostream>
#include <string>

#include <sys/types.h>
#include <dirent.h>

#include "CSC_DataTreeVariable.cxx"
#include "CSC_BuildRootConst.cxx"


namespace CSCConvertor {
    
    //Where to find the txt database file
    std::string inputPathConvert = "/afs/cern.ch/user/i/ibordule/prod/Sparkcounter/output/database_txt";
    //Where to store the root file
    std::string outputPathConvert = "/afs/cern.ch/user/i/ibordule/prod/Sparkcounter/output/database_root";
    
    std::vector<std::string> insideNameTxtFile;
    std::vector<std::string> insideFolders;

void findInsideTXTandFolder(std::string pathFolder) {
    
    insideNameTxtFile.clear();
    
    DIR *dp;
    struct dirent *ep;
    
        dp = opendir (pathFolder.c_str());
        if (dp != NULL) {
            ep = readdir (dp);
            while (ep) {
                std::string fileName = ep->d_name;
                if (fileName.find(".txt") != -1 && fileName.find(".zip") == -1) {
                    insideNameTxtFile.push_back(fileName);
                } else if (fileName.find(".") == -1) {
                    insideFolders.push_back(pathFolder + "/" + fileName);
                }
                ep = readdir (dp);
            }
            (void) closedir (dp);
        }
}




void convertTxtToRoot() {
    
    TFile *rootFileConvert;
    gROOT->ProcessLine("#include <vector>");
    
    insideFolders.clear();
    

    //parentDir
    
    std::string rootpath = outputPathConvert + "/CSC_Sparks.root";
    rootFileConvert = new TFile(rootpath.c_str(), "RECREATE");
    
    buidBranchTree();
    
    std::string pathFolder = inputPathConvert;
    insideFolders.push_back(pathFolder);
    
    for (int i = 0; i < insideFolders.size(); i++) {
        findInsideTXTandFolder(insideFolders[i]);
        buildDataRootTree(insideFolders[i], insideNameTxtFile, rootFileConvert);
    }
    
    rootFileConvert->Write();
    rootFileConvert->Print();
    
    
    delete SparksTree;
    rootFileConvert->Close();
    delete rootFileConvert;
}

void buildLocalDB(std::string input,std::string output) {
    inputPathConvert = input;
    outputPathConvert = output;
    
    convertTxtToRoot();
}
}
