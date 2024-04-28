![production ci](https://github.com/LeeviHalme/online-course-manager/actions/workflows/prod-cicd.yml/badge.svg)

# Description
E-Course management platform. Organise online courses efficiently with automatic assignment checking, student/teacher user control and self-enrolment.

This project was made for **TKT20011 Intermediate Studies Project: Database Application**-course organised by University of Helsinki in the fourth period of 2023.

### Peer Reviewers

The app is hosted at: [https://online-course-manager.leevihal.me/](https://online-course-manager.leevihal.me/)

# Development Plan
This bullet-point list fill list out all features for this application and is kept up-to-date throughout the course.

## Tasks
- [x] Setup Github Repo
- [x] Connect project to Labtools
- [x] Provide a roadmap and feature list for this project
- [x] Provide app building instructions for peer reviewers

## Features

Ticked = Completed & Live in Production

- [x] Automatic CI/CD to a production DigitalOcean droplet running Ubuntu using docker-compose **Completed**
- [x] Authentication **Completed**
  - [x] Ability to login using username (possibly email) and password
  - [x] Ability to register as a teacher or as a student
    - [x] Add validation to user input
- [ ] Courses
  - [x] Student-user features **Completed**
    - [x] View all courses
    - [x] View courses you've enrolled in
    - [x] View a specific course
      - [x] View course material (text-based) (could implement markup support)
      - [x] Course assignments  
        - [x] View course assignments
        - [x] Answer to exercise questions
      - [x] Enroll using invite code
      - [x] View course summary
        - [x] View statistics
        - [x] View total awarded points
        - [x] Unenroll from the course
  - [ ] Teacher-user features
    - [x] View all courses
    - [ ] Delete a specific course
    - [x] Add new course
    - [ ] View a specific course
      - [ ] View statistics
      - [x] View enrolled students
      - [x] View specific student's awarded points
    - [x] Edit course
      - [x] Add course material
      - [x] Add assignments
      - [x] View and reset invite code
      - [x] Edit course details

# Local Setup

### Requirements

- [Docker](https://www.docker.com/) version **20.10.21** or greater

### Setup

1. Clone the repository
```bash
git clone https://github.com/LeeviHalme/online-course-manager.git
```
```bash
cd online-course-manager
```

2. Setup environment

```bash
mv .env.sample .env
```

- After renaming the example env file, fill in the values according to your configuration!

3. Starting the compose-project

```bash
docker-compose up --build
```

### Endpoints
- Adminer SQL explorer: [localhost:8080](http://localhost:8080)
- Flask app (OnlineCourseManager): [localhost:5000](http://localhost:5000)

# Production setup

```shell
docker-compose -f docker-compose.prod.yml up -d --build
```

## Docker setup

If you want, you can build and run the Flask app as a seperate image. To do this, first build the image bu running:

```bash
docker build -f Dockerfiles/Flask.Dockerfile . -t online-course-manager
```

*NOTE: In order to use the production version, change the file name from Flask.Dockerfile to Flask.Prod.Dockerfile*

After building the image, you can start it up in a container by runnning:

```bash
docker run -d -p 5000:5000 online-course-manager
```

*NOTE: This will expose the Flask app in port 5000*

# License

MIT <3
