# Python (V2 Model) Based Azure Function
This POC aims to do the following:
-	Creation of a python (v2 model) based azure function which will work in local as well as in azure environment
-	This function will be triggered through azure event-hub trigger - whenever any data is published to azure event-hub. For running in local, azure event-hub emulator has been used.
-	The function will also publish the data to azure blob storage. For running in local, azurite has been used.
-	Creation of a http trigger-based helper azure function as well – it will publish the data into the azure event-hub. This function will be used for testing the main function.

### Pre-requisites
-	In local, everything is done in WSL environment. So, windows subsystem for Linux (WSL) installation is must.
-	Docker Engine is installed in WSL
-	Dotnet is installed in WSL
sudo apt-get install -y dotnet-sdk-9.0
-	Python version >=3.10 is installed
-	VSCode (as IDE) is available
-	Azure Functions Core Tools is installed in WSL (https://learn.microsoft.com/en-us/azure/azure-functions/functions-run-local?tabs=windows%2Cisolated-process%2Cnode-v4%2Cpython-v2%2Chttp-trigger%2Ccontainer-apps&pivots=programming-language-python )
-	Azure EventHub emulator (https://github.com/Azure/azure-event-hubs-emulator-installer) and azurite (for azure storage emulator) should be available. 

### Steps
For step by step instructions, please take a look at teh following PDF file: 
https://github.com/gsbuddy87/MyPFunctionApp/blob/master/azure_function_guide.pdf

#### Note
Azure documentation has been used for the reference. 
