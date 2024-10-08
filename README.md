# Find-a-Doctor

This repository is a rag application for finding a doctor.
This project was implemented for 
[LLM Zoomcamp](https://github.com/DataTalksClub/llm-zoomcamp) -
a free course about LLMs and RAG.
We will specialize in the current project to hip surgeons and in particular
those who do hip resurfacing. Hip resurfacing (HR), an alternative to total hip replacement (THR), has many 
advantages, especially for physically acive people with hip dysfunction.  Finding a doctor can be tricky
so having available information in an accessible format could be helpful.  Most of the code for this project as well as the format of this README was adapted from Alexey Grigorev's Fitness Assistant project: https://github.com/alexeygrigorev/fitness-assistant

## Project overview

The main criteria for choosing a good HR surgeon are the number of HR surgeries, the success rate, the type of 
HR prosthesis used, and patient reviews.  
Finding names of surgeons, how many HR's they have 
done, whether or not they are recommended by patients, and their locations will be available in this app.
We hope to improve this later with success rate information and more patient reviews.

## Dataset

The dataset used in this project contains information about
hip surgeons, including:

- **orthopedic_surgeon_first_name:** orthopedic surgeon's first name
- **orthopedic_surgeon_surname:** orthopedic surgeon's surname
- **jpg_doctor:** on-line photo link
- **numbers_hr:** number of hip resurfacings done by surgeon
- **adjusted:** date that number of hip resurfacings was adjusted
- **number_thr:** number of total hip replacements by surgeon
- **number_bmhr:** number of Birmingham Mid-Head Resections
- **type_of_hr_prosthesis:** type of hip resurfacing prosthesis
- **type_of_thr_prosthesis:** type of total hip replacement prosthesis
- **operational_technique:** operational technique
- **anesthetic:** anesthetic
- **cement_femur_side:** is prosthesis cemented
- **this_joint_capsule_saved_all:** the joint capsule was completely saved
- **city:** city
- **country:** country
- **patient-reported_positive_outcomes:** patient reported positive outcomes
- **patient-reported_complications:** patient reported complications
- **cut_muscles_is_fixed_again:** muscles cut during surgery repaired
- **complete_opera_report_is_given:** complete surgery report given to patient
- **hr_average_size:** hip resurfacing average size
- **hr_average_location:** posterior, anterior, etc.
- **assesses_x-ray:** assesses x-ray
- **x-ray_at_discharge:** x-ray at discharge
- **two-sided_operation:** both hips done
- **foreign_patient:** foreign patients
- **address:** address
- **street:** street
- **local:** room or suite number
- **postal_code:** postal code
- **phone_normal:** local phone number
- **phone_free_of_charge:** toll free phone number
- **fax:** fax
- **mobile:** mobile phone
- **email:** email address
- **homepage:** homepage url

The dataset was adapted from https://www.resurfacingscan.be/ortopedlistan/drutoml.htm and contains 1032 records. Information from https://www.hipresurfacingsite.com/list-of-doctors.php was also used.  Some inconsistencies and mistakes in the datasets were resolved by hand.

You can find the data in [`Find-a-Doctor/data/hip_surgeons.csv`](Find-a-Doctor/data/hip_surgeons.csv).

## Technologies

- Python 3.12
- Docker and Docker Compose for containerization
- [Minsearch](https://github.com/alexeygrigorev/minsearch) for full-text search
- Flask as the API interface (see [Background](#background) for more information on Flask)
- Grafana for monitoring and PostgreSQL as the backend for it
- OpenAI as an LLM
- conda
- Streamlit for browser interactions with the application

## Preparation

I started by creating a conda environment:
```bash
conda create -n find-a-doctor python=3.12
conda activate find-a-doctor
```
Since we use OpenAI, you need to provide the API key:

1. Install `direnv`. If you use Ubuntu, run `sudo apt install direnv` and then `direnv hook bash >> ~/.bashrc`.
2. Copy `.envrc_template` into `.envrc` and insert your key there.
3. For OpenAI, it's recommended to create a new project and use a separate key.
4. Run `direnv allow` to load the key into your environment.

For dependency management, we use pipenv, so you need to install it:

```bash
pip install pipenv
```

Once installed, you can install the app dependencies:

```bash
pipenv install --dev
```

## Running the application

The following commands are useful if something goes wrong:

To delete all containers including its volumes use:
```bash
docker rm -vf $(docker ps -aq)
```
To delete all the images,
```bash
docker rmi -f $(docker images -aq)
```
Also, 
```bash
docker compose down -v
```
removes volumes declared in the docker-compose file.

If the application fails to start with the following error: Error starting userland proxy: listen tcp4 0.0.0.0:5432: bind: address already in use
```bash
sudo lsof -i :5432
sudo kill -9 $(PID) 
```
will clear the postgres port.

### Database configuration

Before the application starts for the first time, the database
needs to be initialized.

First, run `postgres`:

```bash
docker-compose up postgres
```

Then run the [`db_prep.py`](find-a-doctor/db_prep.py) script:

```bash
pipenv shell
cd Find-a-Doctor
export POSTGRES_HOST=localhost
python db_prep.py
```
If the above produces errors, instead try the following: 
https://www.commandprompt.com/education/how-to-create-a-postgresql-database-in-docker/#:~:text=To%20create%20a%20PostgreSQL%20database%20in%20Docker%2C%20first%2C%20pull%2F,postgres%E2%80%9D%20command
```bash
docker pull postgres
docker run -d --name container_name -p 5432:5432 -e POSTGRES_USER=your_username POSTGRES_PASSWORD=your_password postgres
docker ps #check the container was created and is running
docker exec -it container_name bash #to get a container root command line

psql -h localhost -U your_username #to connect to postgresql
```
```sql
CREATE DATABASE doctor_info;
```
Check that the database was created:
```sql
\l
```
Connect to the database:
```sql
\c doctor_info; 
```
Then repeat the above [`db_prep.py`](find-a-doctor/db_prep.py) script
to initialize the database.

To check the content of the database, use `pgcli` (already
installed with pipenv):

```bash
pipenv run pgcli -h localhost -U your_username -d doctor_info -W
```

You can view the schema using the `\d` command:

```sql
\d conversations;
```

And select from this table:

```sql
select * from conversations;
```

### Running with Docker-Compose

The easiest way to run the application is with `docker-compose`:

```bash
docker-compose up
```
or to run the application in the background:

```bash
docker-compose up -d
```

### Running locally

If you want to run the application locally,
start only postres and grafana:

```bash
docker-compose up postgres grafana
```

If you previously started all applications with
`docker-compose up`, you need to stop the `app`:

```bash
docker-compose stop app
```

Now run the app on your host machine:

```bash
pipenv shell
cd Find-a-Doctor
export POSTGRES_HOST=localhost
python app.py
```

### Running with Docker (without compose)

Sometimes you might want to run the application in
Docker without Docker Compose, e.g., for debugging purposes.

First, prepare the environment by running Docker Compose
as in the previous section.

Next, build the image:

```bash
docker build -t find-a-doctor .
```

And run it:

```bash
docker run -it --rm \
    --network="find-a-doctor_default" \
    --env-file=".env" \
    -e OPENAI_API_KEY=${OPENAI_API_KEY} \
    -e DATA_PATH="Find-a-Doctor/data/hip_surgeons.csv" \
    -p 5000:5000 \
    find-a-doctor
```

### Time configuration

When inserting logs into the database, ensure the timestamps are
correct. Otherwise, they won't be displayed accurately in Grafana.

When you start the application, you will see something like the following in
your logs:

```
Database timezone: Etc/UTC
Database current time (UTC): 2024-10-02 04:41:58.172064+00:00
Database current time (America/Los_Angeles): 2024-10-01 21:41:58.172064-07:00
Python current time: 2024-10-01 21:41:58.172881-07:00
Inserted time (UTC): 2024-10-02 04:41:58.172881+00:00
Inserted time (America/Los_Angeles): 2024-10-01 21:41:58.172881-07:00
Selected time (UTC): 2024-10-02 04:41:58.172881+00:00
Selected time (America/Los_Angeles): 2024-10-01 21:41:58.172881-07:00
```

Make sure the time is correct.

You can change the timezone by replacing `TZ` in `.env`.

On some systems, specifically WSL, the clock in Docker may get
out of sync with the host system. You can check that by running:

```bash
docker run ubuntu date
```
If the time doesn't match yours, you need to sync the clock:

```bash
wsl

sudo apt install ntpdate
sudo ntpdate time.windows.com
```

Note that the time is in UTC.
After that, start the application (and the database) again.


## Using the application

When the application is running, we can start using it.

### CLI

Alexey Grigorev built an interactive CLI application using
[questionary](https://questionary.readthedocs.io/en/stable/).

To start it, run:

```bash
pipenv run python cli.py
```

You can also make it randomly select a question from
[our ground truth dataset](data/ground-truth-retrieval.csv):

```bash
pipenv run python cli.py --random
```
### Streamlit

To use the application on the browser with Streamlit:

```bash
pipenv run streamlit run hip_app.py
```

### Using `requests`

When the application is running, you can use
[requests](https://requests.readthedocs.io/en/latest/)
to send questions—use [test.py](test.py) for testing it:

```bash
pipenv run python test.py
```

It will pick a random question from the ground truth dataset
and send it to the app.

### CURL

You can also use `curl` for interacting with the API:

```bash
URL=http://localhost:5000
QUESTION="How many HR surguries has Dr. Su done?"
DATA='{
    "question": "'${QUESTION}'"
}'

curl -X POST \
    -H "Content-Type: application/json" \
    -d "${DATA}" \
    ${URL}/question
```

You will see something like the following in the response:

```json
{
  "answer": "Dr. Edwin P. Su has performed 2,750 hip resurfacing surgeries (HR).",
  "conversation_id": "50a49856-01ce-4a88-ac0f-d38d4d2ae7bb",
  "question": "How many HR surguries has Dr. Su done?"
}

```

Sending feedback:

```bash
ID="50a49856-01ce-4a88-ac0f-d38d4d2ae7bb"
URL=http://localhost:5000
FEEDBACK_DATA='{
    "conversation_id": "'${ID}'",
    "feedback": 1
}'

curl -X POST \
    -H "Content-Type: application/json" \
    -d "${FEEDBACK_DATA}" \
    ${URL}/feedback
```

After sending it, you'll receive the acknowledgement:

```json
{
    "message": "Feedback received for conversation 50a49856-01ce-4a88-ac0f-d38d4d2ae7bb: 1"
}
```

## Code

The code for the application is in the [`Find-a-Doctor`](Find-a-Doctor/) folder:

- [`app.py`](Find-a-Doctor/app.py) - the Flask API, the main entrypoint to the application
- [`rag.py`](Find-a-Doctor/rag.py) - the main RAG logic for building the retrieving the data and building the prompt
- [`ingest.py`](Find-a-Doctor/ingest.py) - loading the data into the knowledge base
- [`minsearch.py`](Find-a-Doctor/minsearch.py) - an in-memory search engine
- [`db.py`](Find-a-Doctor/db.py) - the logic for logging the requests and responses to postgres
- [`db_prep.py`](Find-a-Doctor/db_prep.py) - the script for initializing the database


We also have some code in the project root directory:

- [`test.py`](test.py) - select a random question for testing
- [`cli.py`](cli.py) - interactive CLI for the app
- [`hip_app.py`](hip_app.py) - Streamlit browser interaction for the app

### Interface

We use Flask for serving the application as an API.

Refer to the ["Using the Application" section](#using-the-application)
for examples on how to interact with the application.

### Ingestion

The ingestion script is in [`ingest.py`](Find-a-Doctor/ingest.py).

Since we use an in-memory database, `minsearch`, as our
knowledge base, we run the ingestion script at the startup
of the application.

It's executed inside [`rag.py`](Find-a-Doctor/rag.py)
when we import it.

## Experiments

For experiments, we use Jupyter notebooks.
They are in the [`notebooks`](notebooks/) folder.

To start Jupyter, run:

```bash
cd notebooks
pipenv run jupyter notebook
```

We have the following notebooks:

- [`rag-test.ipynb`](notebooks/rag-test.ipynb): The RAG flow and evaluating the system.
- [`rag-test-Copy1.ipynb`](notebooks/rag-test-Copy1.ipynb): A copy of the above with different prompt.
- [`evaluation-data-generation.ipynb`](notebooks/evaluation-data-generation.ipynb): Generating the ground truth dataset for retrieval evaluation.
- [`correct_convert_html_to_csv.ipynb`](notebooks/correct_convert_html_to_csv.ipynb): Used to convert raw data to a csv file.
- [`data_prepare.ipynb`](notebooks/data_prepare.ipynb): Used to add another column and clean up data.

### Retrieval evaluation

The basic approach - using `minsearch` without any boosting - gave the following metrics:

- Hit rate: 98%
- MRR: 84%

The improved version (with tuned boosting):

- Hit rate: 98%
- MRR: 95%

The best boosting parameters:

```python
boost = {
        'orthopedic_surgeon_first_name': 0.45,
        'orthopedic_surgeon_surname': 2.87,
        'jpg_doctor': 0.56,
        'numbers_hr': 0.92,
        'adjusted': 1.28,
        'number_thr': 1.23,
        'number_bmhr': 0.96,
        'type_of_hr_prosthesis': 1.66,
        'type_of_thr_prosthesis': 2.72,
        'operational_technique': 2.27,
        'anesthetic': 1.78,
        'cement_femur_side': 2.20,
        'this_joint_capsule_saved_all': 1.23,
        'city': 1.36,
        'country': 1.24,
        'patient-reported_positive_outcomes': 1.26,
        'patient-reported_complications': 2.74,
        'cut_muscles_is_fixed_again': 2.17,
        'complete_opera_report_is_given': 0.06,
        'hr_average_size': 2.13,
        'hr_average_location': 2.57,
        'assesses_x-ray': 0.35,
        'x-ray_at_discharge': 0.66,
        'two-sided_operation': 1.32,
        'foreign_patients': 2.07,
        'address': 0.55,
        'street': 2.71,
        'local': 2.66,
        'postal_code': 0.36,
        'phone_normal': 1.70,
        'phone_free_of_charge': 2.77,
        'fax': 1.36,
        'mobile': 1.77,
        'email': 0.08,
        'homepage': 1.45,
    }

```

### RAG flow evaluation

We used the LLM-as-a-Judge metric to evaluate the quality
of our RAG flow.

For `gpt-4o-mini`, in a sample with 200 records, we had:

- 168 (84%) `RELEVANT`
- 30 (15%) `PARTLY_RELEVANT`
- 2 (1%) `NON_RELEVANT`

We also tested `gpt-4o`, but were unable to complete the evaluation without running out of money.
We were unable to connect to Groq, and we exceeded the number of allowed requests for Hugging Face models.
Money was an object so we went with `gpt-4o-mini`.

Using a second prompt with the LLM as a patient gave the following:

- 163 (81%) `RELEVANT`
- 29 (14%) `PARTLY_RELEVANT`
- 8 (4%) `NON_RELEVANT`

The first prompt does a better job here.

## Monitoring

We use Grafana for monitoring the application. 

It's accessible at [localhost:3000](http://localhost:3000):

- Login: "admin"
- Password: "admin"

### Dashboards


The monitoring dashboard contains several panels:

1. **Last 5 Conversations (Table):** Displays a table showing the five most recent conversations, including details such as the question, answer, relevance, and timestamp. This panel helps monitor recent interactions with users.
2. **+1/-1 (Pie Chart):** A pie chart that visualizes the feedback from users, showing the count of positive (thumbs up) and negative (thumbs down) feedback received. This panel helps track user satisfaction.
3. **Relevancy (Gauge):** A gauge chart representing the relevance of the responses provided during conversations. The chart categorizes relevance and indicates thresholds using different colors to highlight varying levels of response quality.
4. **OpenAI Cost (Time Series):** A time series line chart depicting the cost associated with OpenAI usage over time. This panel helps monitor and analyze the expenditure linked to the AI model's usage.
5. **Tokens (Time Series):** Another time series chart that tracks the number of tokens used in conversations over time. This helps to understand the usage patterns and the volume of data processed.
6. **Model Used (Bar Chart):** A bar chart displaying the count of conversations based on the different models used. This panel provides insights into which AI models are most frequently used.
7. **Response Time (Time Series):** A time series chart showing the response time of conversations over time. This panel is useful for identifying performance issues and ensuring the system's responsiveness.

### Setting up Grafana

All Grafana configurations are in the [`grafana`](grafana/) folder:

- [`init.py`](grafana/init.py) - for initializing the datasource and the dashboard.
- [`dashboard.json`](grafana/dashboard.json) - the actual dashboard (taken from LLM Zoomcamp without changes).

To initialize the dashboard, first ensure Grafana is
running (it starts automatically when you do `docker-compose up`).

Then run:

```bash
pipenv shell

cd grafana

# make sure the POSTGRES_HOST variable is not overwritten 
env | grep POSTGRES_HOST

python init.py
```
Then go to [localhost:3000](http://localhost:3000):

- Login: "admin"
- Password: "admin"

When prompted, keep "admin" as the new password.

If the monitoring dashboard is not connecting to the database, try the following:
```bash
docker network create  find-a-doctor_default #create network to connect to three containers
docker ps #get the names of the three running containers
```
For each running container:
```bash
docker network connect find-a-doctor_default $(container_name)
```
Then, click on the find-a-doctor pipeline and on the left side menu, click on data sources, then PostgresSQL
and change the host from localhost:5432 to find-a-doctor:5432.  The docker-compose file is also modified to include the network.

## Background

Here we provide background on some tech not used in the
course and links for further reading.

### Flask

We use Flask for creating the API interface for our application.
It's a web application framework for Python: we can easily
create an endpoint for asking questions and use web clients
(like `curl` or `requests`) for communicating with it.

In our case, we can send questions to `http://localhost:5000/question`.

For more information, visit the [official Flask documentation](https://flask.palletsprojects.com/).


## Acknowledgements 

I thank Alexey Grigorev for an interesting and informative course as well as the course participants for invaluable help with
various stumbling blocks.

