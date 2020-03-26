#include <fstream>
#include <iostream>
namespace CSCConvertor {
    
Int_t parseDataTime (char *buff) {
    int y(0), m(0), d(0), c(0), min(0), s(0);
    
    std::string strParse = buff;

    int posDateTime = strParse.find("/");
    if (posDateTime != -1) {
        y = std::atoi(strParse.substr(posDateTime - 4 ,posDateTime).c_str());
        strParse = strParse.substr(posDateTime + 1);
        
        std::cout << "\n year  " << y << ": :" << strParse;

        posDateTime = strParse.find("/");
        
        if (posDateTime != -1)
        m = std::atoi(strParse.substr(posDateTime - 2 ,posDateTime).c_str());
        strParse = strParse.substr(posDateTime + 1);

        posDateTime = strParse.find(" ");

        d = std::atoi(strParse.substr(posDateTime - 2 ,posDateTime).c_str());
        strParse = strParse.substr(posDateTime + 1);

        posDateTime = strParse.find(":");

        c = std::atoi(strParse.substr(posDateTime - 2 ,posDateTime).c_str());
        strParse = strParse.substr(posDateTime + 1);

        posDateTime = strParse.find(":");

        min = std::atoi(strParse.substr(posDateTime - 2 ,posDateTime).c_str());
        strParse = strParse.substr(posDateTime + 1);


        s = std::atoi(strParse.substr(2).c_str());;


        dataTime->Set(y, m, d, c, min, s);
        
    }
    
    return dataTime->Convert();
    
}
    
    Int_t parsetimeMsec (Int_t timeMsec) {
        dataTime->Set(timeMsec);
        return dataTime->GetYear() * 10000 + dataTime->GetMonth() * 100 + dataTime->GetDay();
    }

void buildDataRootTree(std::string basePathcInputFile, std::vector<std::string> vectorPatchfileTxt, TFile *rootFileConvert) {
    dataTime = new TDatime();
    
    for (int i = 0; i < vectorPatchfileTxt.size(); i++) {
        
        if (vectorPatchfileTxt[i].find("finalbase") != -1) {
            
            std::string patchInputFileTxt = basePathcInputFile  + "/" + vectorPatchfileTxt[i];
            std::cout << "\n now parse " << patchInputFileTxt;
            std::ifstream fileTxtData(patchInputFileTxt.c_str());
            
            if (fileTxtData.is_open()) {

                std::string strBuff;
                
                while(getline(fileTxtData, strBuff, '\n')) {

                    std::cout << "\n now parse strBuff +++++++++++ \n " << strBuff;
                    
                    
                    strcpy (chamber, (strBuff.substr(0, strBuff.find("             "))).c_str());
                    
                    //Parse out the chamberNumber
                    chamberNumber = (int)std::atoi((strBuff.substr(2, 3)).c_str());
                    if (chamber[0] == 'C') chamberNumber = -chamberNumber;
                    std::cout << "\n chamberNumber +++++++++++ \n " << chamberNumber;
                    
                    //Parse out the Layer
                    strBuff = (strBuff.substr(strBuff.find("             ") + 13));
                    std::cout << "\n now parse strBuff " << strBuff;
                    layerInt = (int)std::atoi((strBuff.substr(1, strBuff.find("            "))).c_str());
                    
                    //Parse out the Date and Time
                    strBuff = (strBuff.substr(strBuff.find("            ") + 12));
                    strcpy (timestamp, (strBuff.substr(0, strBuff.find("        "))).c_str());
                    dataTimeInt = parseDataTime (timestamp);
                    timeYMD = parsetimeMsec(dataTimeInt);
                    
                    //Parse out the Amplituse
                    strBuff = ("" + strBuff.substr(strBuff.find("        ") + 8));
                    amplitude = (float)std::atof(("" + strBuff.substr(0, strBuff.find("             "))).c_str());

                    //Parse out the Baseline
                    strBuff = ("" + strBuff.substr(strBuff.find("             ") + 13));
                    baseline = (float)std::atof(("" + strBuff.substr(0, strBuff.find("             "))).c_str());

                    //Parse out the Timediff
                    strBuff = ("" + strBuff.substr(strBuff.find("             ") + 13));
                    timediff = (float)std::atof(("" + strBuff.substr(0, strBuff.find("             "))).c_str());
                    
                    //Parse out the HV
                    strBuff = ("" + strBuff.substr(strBuff.find("             ") + 13));
                    HV = (float)std::atof(("" + strBuff.substr(0, strBuff.find("             "))).c_str());
                    
                    //Parse out the Humidity
                    strBuff = ("" + strBuff.substr(strBuff.find("             ") + 13));
                    Humidity = (float)std::atof(("" + strBuff.substr(0, strBuff.find("             "))).c_str());
                    
                        SparksTree->Fill();
                    
                    
                }
                
                fileTxtData.close();
                
            }
            
            
        }
        
    }
    
    delete dataTime;
    
}
}
