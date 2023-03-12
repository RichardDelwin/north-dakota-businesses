# Data Collection

I am Richard Delwin Myloth, and I have successfully completed the task outlined in the document available at https://gist.github.com/jvani/57200744e1567f33041130840326d488

My submission consists of 5 files, namely:

1.  **main.py**: This file contains the code to run the Scrapy crawler for fetching data from the web app. After retrieving the required data, it executes a function call to plot_graph.py for plotting the graph.
2.  **plot_graph.py**: This file contains the code to plot the graph based on the data obtained from main.py.
3. **businesses_data.json**: This file stores the data collected by the crawler during the data retrieval process.
4. **businesses_graph.png**: This file is the output of plot_graph.py and displays the graph plotted using the data collected by the crawler.
5. **requirements.txt**: This file lists the libraries I used during the development of the project.
6. **README.md**: This file contains the necessary information related to the project, such as installation instructions and usage details.

# Some choices made

1. I have made some choices while completing the task, which I believe are important to highlight. For instance, while querying the web app with the two filters (**company name starts with X and is active**), I have observed that it returns some records where the first letter isn't X. So I did not rely on the API to return the correct results, and I have only retained those records whose name does in fact start with X. As a result, there are **173** such businesses.

Example:

![Alt text](readme_images\Businesses_that_don't_start_with_X.png?raw=true "Example")



2. I have listed my sources (such as StackOverflow, etc.) apart from the official documentation of Scrapy, matplotlib, Networkx at the beginning of each python script.

# Usage instructions

### 1. Creating a virtual environment:
1.  `git clone` 
2.  `cd repo`
3.  `pip install virtualenv`  (if you don't already have virtualenv installed)
4.  `virtualenv venv`  to create your new environment.
5.  `venv/Scripts/activate`  to enter the virtual environment
6.  `pip install -r requirements.txt`  to install the requirements in the current environment

### 2. Obtaining businesses data and plotting the graph
 1. `python main.py`  to obtain data, generate the data file (businesses_data.json), and plot the graph (businesses.png) (The entire process takes around 3.5 minutes).

Note:| `python plot_graph` can also be executed if plot_graph is to be executed independently.


<br>

Thank you for considering me. I appreciate the time and effort you have taken to review my application. I'm looking forward to hearing from you.

**Thank you!**