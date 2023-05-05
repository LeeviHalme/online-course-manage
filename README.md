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

- [x] Automatic CI/CD to a production DigitalOcean droplet running Ubuntu using docker-compose
- [x] Authentication
  - [x] Ability to login using username (possibly email) and password
  - [x] Ability to register as a teacher or as a student
    - [x] Add validation to user input
- [ ] Courses
  - [ ] Student-user features
    - [x] View all courses
    - [x] View courses you've enrolled in
    - [ ] View a specific course
      - [x] View course material (text-based) (could implement markup support)
      - [ ] Course assignments  
        - [x] View course assignments
        - [ ] Answer to exercise questions
      - [x] Enroll using invite code
      - [ ] View course summary
        - [ ] View statistics
        - [ ] View total awarded points
        - [ ] Unenroll from the course
  - [ ] Teacher-user features
    - [x] View all courses
    - [ ] Delete a specific course
    - [x] Add new course
    - [ ] View a specific course
      - [ ] View statistics
      - [ ] View enrolled students
      - [ ] View specific student's awarded points
    - [ ] Edit course
      - [ ] Change/edit course material
      - [ ] Change/edit assignments
        - [ ] Add new assignment
        - [ ] Delete an assignment 
      - [x] View and reset invite code
      - [x] Edit course details

# Local Setup

### Requirements

- [Docker](https://www.docker.com/) version **20.10.21** or greater

### Setup

```shell
git clone https://github.com/LeeviHalme/online-course-manager.git
```
```shell
cd online-course-manager
```
```shell
docker-compose up --build
```

### Endpoints
- Adminer SQL explorer: [localhost:8080](http://localhost:8080)
- Flask app (OnlineCourseManager): [localhost:5000](http://localhost:5000)

# Production setup

```shell
docker-compose -f docker-compose.prod.yml up -d --build
```

# License

MIT <3