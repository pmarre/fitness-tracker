# FitnessTracker - Train with purpose

FitnessTracker can be accessed here: [Live Site](https://fitness-tracker-ms3.herokuapp.com/)


## Table of Contents
1. UX
   - [User Stories]()
   - [Strategy]()
   - [Scope]()
   - [Structure]()
2. Features
3. Tech Used
4. Testing
5. Database Structure
6. Deployment


## User Experience
- The goal of FitnessTracker is to be a simple, responsive site for users to add, manage, and view their workouts on any device. 
- The site should be responsive and work on all browsers
- Clickable items have hover effects to alert the user that they can be clicked
- Inputs use placeholders to clearly describe what needs to be entered by user
- Buttons are clear, so users know they can add, edit, or delete a workout at anytime 

### User Stories
- _"I try to workout almost everyday and want a place where I can quickly input the workout and view it later."_, Completed by allowing the user to create an account on FitnessTracker and add/view any of their workouts on any device


## Bugs 
 - Login Page Error Message:
   - When a user logins in I want a message to be displayed if there email or password is incorrect
   - Running into issues with retrieving the login success param from url_for and using it as a arg in login() 
