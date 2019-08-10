# auth-playground

A repo for testing out the google sign in logic with Flask and Python3

## Getting Started

These instructions will get you a copy of the project up and running on your local machine.

### Prerequisites

##### To run the VM, you must have the following:
* [VirtualBox](https://www.virtualbox.org/wiki/Downloads)
* [Vagrant](https://www.vagrantup.com/)
* Python3 is installed on the Vagrant VM

For more information on the base setup, visit the [Udacity VM Setup](https://github.com/udacity/fullstack-nanodegree-vm)

##### A project created in your Google Dev console. 
0. The Dev Console can be found [here](https://console.developers.google.com)
1. Create a project
2. Go to your credentials. The root link is [here](https://console.developers.google.com/apis/credentials)
3. Click "Create credentials", then "OAuth client ID"
4. Select "Web Application"
5. Give the credentials a name (such as "google-auth-playground-creds")
6. Under "Authorized JavaScript origins", add "http://localhost:5000" and hit Enter
7. Under "Authorized redirect URIs", add "http://localhost:5000/oauthcallback" and hit Enter
8. Click the "Create" button
9. You are done with this step, move on to "Running the VM" section.

##### A project created in your Facebook Developers console.
0. The Facebook Dev console can be found [here](https://developers.facebook.com)
1. Create a project
2. Go to your FB Dev Console Dashboard, scroll down to the **My Products** section
3. Under the **Facebook Login** product, click **"Settings"**
4. Under **"Valid OAuth Redirect URIs"**, enter a valid URI if applicable (not needed for localhost testing)

### Running the VM

To run the VM you must do the following:
1. Obtain a copy of the vagrant setup repository from: [Repo Zip](https://github.com/udacity/fullstack-nanodegree-vm/archive/master.zip)
2. Unzip the master.zip file into a chosen directory
3. Obtain a copy of this repository from [here](https://github.com/Justin-Tadlock/auth-playground/archive/master.zip) 
4. Unzip the content into the Vagrant's repository directory under "{repoLocation}/vagrant/auth-playground"
5. Open a command prompt/PowerShell/terminal window inside the vagrant directory
6. Run the following commands
```
vagrant init
vagrant up
vagrant ssh
```
7. Once the vagrant VM is running, navigate to the **auth-playground** app directory
``` 
cd /vagrant/auth-playground 
```

### Setting up the VM to run the web server

##### In order for the application to work, you must install the appropriate modules on your vagrant VM:
```sudo pip3 install --upgrade -r requirements.txt```
or
```sudo sh ./get-prereqs.sh ```

##### You will need to download the credentials json file from your Google Dev Console
1. Go to your Google Dev Console Credentials section [here](https://console.developers.google.com/apis/credentials)
2. Go to the credentials you created in the Pre-Req section, on the far right click the **DOWN** arrow to download the credentials in json format
3. Go to the location the file was downloaded, rename the file "client_secrets.json"
4. Copy-paste the "client_secrets.json" file into your **auth-playground** app directory.
5. You are done with this step

##### You will need to create the credentials json file for your Facebook Dev Console
0. Create a **fb_client_secrets.json** file within your **auth-playground** app directory 
1. Next, go to your Facebook Dev Console 
2. On the left-hand nav pane, click **Settings** > **Basic**
3. Open your **fb_client_secrets.json** file 
4. Add your **App ID** and your **App Secret** to the file following this format:
The content should look like this:
{
    "web": {
        "app_id": "Your App ID",
        "app_secret": "Your App Secret"
    }
}

5. Save the file and you're done with this step

##### You will also require a "secret_key.txt" file to be made and have some text inside it.
1. In your google-auth-playground app directory create a "secret_key.txt" file.
2. Open the file and type some text
3. Save the file and close the file.
4. You are done with this step

##### To run the web app run this command in your vagrant ssh terminal window:
``` python3 ./start-app.py ```

### Reviewing Web App Functionality
Once the web app is running, open your browser and navigate to 
``` http://localhost:5000 ```

Click the "Sign in" button with the Google icon and review the functionality.


## Built With

* [Python](https://www.python.org/downloads/) - Python is a programming language that lets you work quickly and integrate systems more effectively
* [Flask](https://palletsprojects.com/p/flask/) - A lightweight WSGI web application framework.
* HTML
* CSS

## Authors

* **[Justin-Tadlock](https://github.com/Justin-Tadlock)** - *Initial work*

## Acknowledgments

* [Udacity VM Setup](https://github.com/udacity/fullstack-nanodegree-vm) - for the initial setup of the Vagrant VM.
* [Integrating Google Sign-In into your web app](https://developers.google.com/identity/sign-in/web/sign-in) - The tutorial used for building this playground.


