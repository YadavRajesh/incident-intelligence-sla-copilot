**Current Enterprise Architecture:**

Azure Blob Storage (created)

&#x20;   ├── HistoricalIncidents.csv

&#x20;   ├── historical.index

&#x20;   └── metadata.pkl



Azure Function App (created)

&#x20;   └── Weekly vector refresh



Azure App Service

&#x20;   └── Main AI Copilot API



Azure OpenAI (created)

&#x20;   ├── GPT model

&#x20;   └── Embedding model



\------------------------------------------------------------------------------

**Step 1** --> **Verify Local FastAPI Server Works** (Before cloud deployment, we must verify: the API runs correctly locally.)

&#x20;      -> run this command >>**uvicorn src.api.api:api --reload** (first api is folder name inside src folder, second api is filename api.py, second api is FastAPI object 	  	  variable api = FastAPI()). if you get error running above command run this one instead >>**uvicorn src.api.api:api --reload --port 8010** (meaning we are using port 	  8010, first command was using port 8000 which is a default port and may sometimes being already used.

&#x20;      -> run this url in browser *http://127.0.0.1:8010/docs,* You should now see: Swagger UI with: **POST /analyze-incident** this is the entry point we have defined in our 	  code. **What This Means Architecturally You have successfully converted your AI system into: AI Backend Service instead of: local script execution**

&#x20;      **->** Test the Endpoint, Click: POST /analyze-incident, Then: Try it out, Then paste this JSON:

&#x09;	{

&#x20; "incident\_number": "INC200145",

&#x20; "short\_description": "SAP production order creation failing after deployment",

&#x20; "description": "Users are unable to create sales orders in SAP production environment after the latest transport deployment. Multiple users report order save failures and transaction VA01 timeout errors. Business operations impacted across Order Management team.",

&#x20; "urgency": "1",

&#x20; "state": "Open",

&#x20; "opened\_at": "2026-05-16 08:00:00",

&#x20; "sla\_due": "2026-05-16 12:00:00",

&#x20; "assignment\_group": "SAP Support",

&#x20; "business\_service": "Order Management",

&#x20; "cmdb\_ci": "SAP-PRD-01"

}



**Step 2 --> Prepare Your Project for Cloud Deployment**

\--> run this command in your terminal ***pip freeze > requirements.txt*** (takes all Python packages currently installed inside your active virtual environment 						(venv) along with their exact versions, and writes them into a file called requirements.txt. This file is 						later used by Azure/cloud servers to automatically reinstall the same dependencies so your deployed AI 							workflow runs exactly like your local environment.)



**STEP 3 — Create Startup Command for Azure** 

**-->** Azure App Service needs to know: how to start your FastAPI server.

&#x20;   Your startup command will be: ***uvicorn src.api.api:api --host 0.0.0.0 --port 8010***

&#x20;   Now create a new file **startup.sh** in project root and put this inside:

&#x20;   ***#!/bin/bash***

&#x20;   ***uvicorn src.api.api:api --host 0.0.0.0 --port 8010*** (Azure Linux App Service can directly use this startup script during deployment. This makes 								deployment cleaner and enterprise-friendly.)



**Step 4 → Create Azure App Service for Your AI Workflow on Azure Portal first**

\--> Azure Portal > Home page > Search > App Service > Create > Web App

&#x20;   correctly select:

Existing resource group

Code deployment

Python 3.12

Linux

Central India

Basic B1 plan

Review+Create



**Step 5 -> Configure Deployment from Local VS Code. ZIP DEPLOY from VS Code terminal**

&#x09;In this step we are packaging our entire FastAPI + LangGraph project into a deployable ZIP file and preparing Azure authentication so your local 	code can be uploaded into the Azure Web App you just created. The .zipdeployignore file prevents unnecessary or sensitive files like venv, .env, and 	cache folders from being uploaded, while az login securely connects your local machine to your Azure subscription. After this, Azure will extract 	and run your project directly in the cloud environment.

&#x09;--> First install Azure CLI from *https://learn.microsoft.com/en-us/cli/azure/install-azure-cli-windows?view=azure-cli-latest\&utm\_source=chatgpt.com*

&#x09;--> >>***\& "C:\\Program Files\\Microsoft SDKs\\Azure\\CLI2\\wbin\\az.cmd" login --tenant e3ebb152-fe60-456a-bbb6-bac11e3beb3a --use-device-code***, run this 		command in vs code terminal, this will ask you to login to Microsoft azure.

&#x09;--> Create Deployment ZIP

&#x20;           - >>***Compress-Archive -Path src,data,requirements.txt,startup.sh,build\_index.py -DestinationPath deployment.zip -Force***, run this command which 		will create the deployment.zip folder in project root folder. Now ZIP contains only: source code, vector data, requirements, startup script 		and not the .env file or any other file which contains secret.

&#x20;           - Instead of above command just run the create\_deployment\_zip.py file which handles everything mentioned in above sub step.



**Step 6 -->** **Deploy deployment.zip to Azure Web App**

**-->** ***\& "C:\\Program Files\\Microsoft SDKs\\Azure\\CLI2\\wbin\\az.cmd" webapp deployment source config-zip --resource-group incident-intelligence-sla-copilot --name incident-intelligence-api-rajesh --src deployment.zip***, run the above command in terminal.

&#x20;     --> What this does, Azure will:

&#x09;upload your ZIP

&#x09;extract project files

&#x09;install dependencies from requirements.txt

&#x09;prepare Python runtime

&#x09;host your FastAPI application



**Step 7 --> Startup command.**

\--> Go to Azure Portal > Your Web App > Settings > Configurations > Stack settings, paste this 

&#x20;   ***gunicorn -w 4 -k uvicorn.workers.UvicornWorker src.api.api:api*** under Startup command











Steps to Redeploy

1. Make changes to code.
2. >>Remove-Item deployment.zip, this deleted existing zip folder
3. >>\& "C:\\Program Files\\Microsoft SDKs\\Azure\\CLI2\\wbin\\az.cmd" webapp deployment source config-zip --resource-group incident-intelligence-sla-copilot --name incident-intelligence-api-rajesh --src deployment.zip, this command redeploys code to azure.

