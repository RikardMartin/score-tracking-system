# Zero-sum game scores tracking app
A streamlit based web app for registering and following up the results of zero sum games. It can be adapted and used for tracking similar stuff as well. Originally developed for tracking ping pong stats at our company by me, Richard Martin.

## installing and running it locally
The app is written in Python with the [streamlit](http://streamlit.io) library. I suggest you create a virutal environment fist, e.g. a [conda environment](docs.conda.io/en/latest)

Activate your conda environment and install streamlit
```(bash)
conda activate <my-env>
pip install streamlit
```
You will also need some more packages which are specified in `requirements.txt`.

When you have installed streamlit, navigate your terminal to the folder where this `README.md`-file is located and type
```(bash)
streamlit run main.py
```
This will start up your webserver locally. When it is running you will receive a link in the terminal. Ctrl-click that link to open the app in a browser.

## Developiong the app
The code is written entirely in Python by using the streamlit library. Information about these can be found here:
* [Streamlit](https://streamlit.io/)
* [Python](https://www.python.org/)


## Deploying to Azure
The app can be packages in a Docker container for a smooth was of deploying it online or ditributing it. Here is a way of containerizing the app and publishing it to a container registry on Azure. For this to work you will need:
1. [Install Azure CLI](https://learn.microsoft.com/en-us/cli/azure/install-azure-cli)
2. [A container registry on Azure](https://learn.microsoft.com/en-us/azure/container-registry/container-registry-get-started-portal?tabs=azure-cli)
3. Access to the above resources.

Then you can buld and deploy your app online by running the following command in a terminal located in the project folder. Not that you might need to run `az login` every once in a while.
```(bash)
az acr build --registry <container-registry-name> --resource-group <resource-group-name> --image <image-name> .
```
