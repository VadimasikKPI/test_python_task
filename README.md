# Overview:
This project aims to develop a service for working with a dataset provided in a .csv file. The service will allow users to filter and export data based on specified criteria. The project will be containerized using Docker for easy deployment and management.

# Repository:
The project repository is hosted on GitLab. You can access it here.

# Getting Started:
To run the project locally, follow these steps:

1.Clone the repository to your local machine:

Copy code 
```bash 
git clone https://github.com/VadimasikKPI/test_python_task
```
2.Navigate to the project directory:

Copy code 
```bash 
cd <project-directory>
```
Ensure you have Docker installed on your machine.

3.Build the Docker images using Docker Compose:

Copy code 
```bash 
docker-compose build
```

4.Start the Docker containers:

Copy code 
```bash 
docker-compose up
```

# Once the containers are up and running, you can access the service at http://localhost:5000.

# Usage:
The service provides the following endpoints:

/filter: Filter data based on specified criteria such as category, gender, date of birth, age, and age range.
/export: Export filtered data in CSV format.
API Documentation:
The Swagger UI is available at http://localhost:5000/swagger. It provides detailed documentation of the available endpoints and their usage.

# Endpoints:

# GET /filter: Filter data based on specified criteria.

# Parameters:
## category: Filter by category.
## gender: Filter by gender.
## dateBirth: Filter by Date of Birth.
## age: Filter by age.
## age_range: Filter by age range (e.g., 25 - 30 years).
## Responses:
### 200: Filtered data.
### 500: Server error
# GET /export: Export filtered data in CSV format.

## Parameters: Same as /filter.
## Responses:
### 200: Exported CSV data.
### 500: Server error

# Additional Information:

-The project uses Python Flask for the backend and PostgreSQL as the database.
-Data is read from the provided .csv dataset and stored in the database.
-Third-party libraries are not used, ensuring simplicity and transparency.
-The service is containerized using Docker, providing easy deployment and scalability.