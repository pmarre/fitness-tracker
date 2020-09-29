# FitnessTracker - Train with purpose

FitnessTracker can be accessed here: [Live Site](https://fitness-tracker-ms3.herokuapp.com/)

FitnessTracker requires a login, I created a fake account to allow users to play around with the site without having to create a new account. The email is: j.smith@gmail.com and the password is: password123!


## Table of Contents
1. [UX](https://github.com/pmarre/fitness-tracker/blob/master/README.md#user-experience)
   - [User Stories](https://github.com/pmarre/fitness-tracker/blob/master/README.md#user-stories)
   - [Strategy](https://github.com/pmarre/fitness-tracker/blob/master/README.md#strategy)
   - [Scope](https://github.com/pmarre/fitness-tracker/blob/master/README.md#scope)
   - [Structure](https://github.com/pmarre/fitness-tracker/blob/master/README.md#structure)
   - [Wireframes](https://github.com/pmarre/fitness-tracker/blob/master/README.md#wireframes)
2. [Features](https://github.com/pmarre/fitness-tracker/blob/master/README.md#features)
   - [Future Features](https://github.com/pmarre/fitness-tracker/blob/master/README.md#future-features)
3. [Technology Used](https://github.com/pmarre/fitness-tracker/blob/master/README.md#technologies-used)
4. [Testing](https://github.com/pmarre/fitness-tracker/blob/master/README.md#testing)
5. [Database Structure](https://github.com/pmarre/fitness-tracker/blob/master/README.md#database-structure)
6. [Deployment](https://github.com/pmarre/fitness-tracker/blob/master/README.md#deployment)


## User Experience

- The goal of FitnessTracker is to be a simple, responsive site for users to add, manage, and view their workouts on any device. 
- The site should be responsive and work on all browsers
- Clickable items have hover effects to alert the user that they can be clicked
- Inputs use placeholders to clearly describe what needs to be entered by user
- Buttons are clear, so users know they can add, edit, or delete a workout at anytime 

### User Stories

- _"I try to workout almost everyday and want a place where I can quickly input the workout and view it later."_, Completed by allowing the user to create an account on FitnessTracker and add/view any of their workouts on any device
- _"I typically do different forms of working out beyond just runnin and want a place to track all my workouts in one place."_, Completed by allowing users to select from a wide range of different sports/workouts when adding it their dashboard.  
- _"I am new to working out and want a place where I can look back and see how I felt doing the same workout a month ago."_, Completed by allowing users to input notes into their workouts so they can remember how workouts felt at the time. 

### Strategy

My first step in the design process was to decide on my target audience so I could create an appealing decision for the user. While fitness has a large range, my primary target audience is the active athelete training for something specific like a marathon or triathalon. While users new to working out and professional athletes could still successfully use my site, they are not my primary audience. 

Having a broad target audience, I chose a design that was straight to the point. I wanted users to have be able to quickly log in, see their recent workouts, and add new ones. The site becomes a workout journal for people to track progress and continue to grow as athletes.

### Scope

Next, I needed to find what my target audience needed. Many athletes keep workout journals to track previous workouts and jot down quick notes about how they feel. So, I created a solution that would allow these atheletes to create their journal online and access it from anywhere in the world. 

After I came up with the solution, I decided to present it to the user in a very simple way where all information is clearly shown and easily accessible. Unlike a pen a paper though, the user can upload an image from the workout as a fun reminder of what they did.

### Structure

Responsiveness and clarity were my goal for this site. Many athletes use their phones while working out and so I wanted the site to be reflective of that and be able to easily be used from a phone. Also, the purpose of the site is track workouts and I wanted that to remain clear. It is not feature heavy because I don't want to over complicate something that should be simple. 

### Wireframes

<details>
<summary>Dashboard Wireframe</summary>
<br />
   <img alt="Desktop homepage wireframe" src="https://github.com/pmarre/fitness-tracker/blob/master/static/images/ft_dashboard.png">
</details>

<details>
<summary>Login Page Wireframe</summary>
<br />
   <img alt="Desktop homepage wireframe" src="https://github.com/pmarre/fitness-tracker/blob/master/static/images/ft_login.png">
</details>

<details>
<summary>Signup Wireframe</summary>
<br />
   <img alt="Desktop homepage wireframe" src="https://github.com/pmarre/fitness-tracker/blob/master/static/images/ft_signup.png">
</details>

## Features

This project is built with Python, Flask, Jinja, CSS, Bootstrap, and JQuery and uses MongoDB to store user input. I chose to use Bootstrap to keep a nice, clean grid feel to the site. 

Flask is used to quickly build reusable templates that pulls information from MongoDB and allows the user to create, read, update, or delete information that is stored. 

#### More key features:
1. CRUD functionality
   - Users can create, read, update, and delete all workouts and their own profile. 
2. Workout block
   - Users can instantly see workouts they have uploaded laid out in clear blocks. All important information is clearly shown and with buttons to edit/delete that workout
3. Workout counter
   - On the desktop version of the website, users can see a live count of the number of workouts they have completed
4. Login 
   - Users must create a unique login to have access to their dashboard. This allows for multiple users to share one device and creates an added layer of security.

#### Future Features

With fitness tracking, the list of possible features seems endless from graphs showing trends in runnning pace to social interactions here are some of my top features I would like in the future:
1. Social interaction
   - Working out in a group makes working out easier. I would like to add the ability to follow friends, like/comment on their workouts, and join virtual workouts with them
2. Data tracking
   - I would like to add a way to track the trends in the data that users submit. This would allow me to create informative charts to show when the user when they are training too much or too little, or moving faster or slower.
3. Automatic uploads
   - I would like to be able to integrate the website with all the sport watches and phone apps to automaticly upload the users workout to the site.
4. GPS tracking
   - I would like to be able to track where the user workout to give them distance, time, speed, etc and become a one stop shop for working out.

## Technologies Used

- Python - used as the backend language to connect what the user sees and the data they have input
- Flask - framework used to simplify python for faster builds
- Jinja - used for creating templates that dynamically show information found in MongoDB
- MongoDB - database for storing all user input
- HTML5 - used to semantically structure website
- CSS3 - used for styling of HTML
- Javascript - used in conjunction with jQuery to create an interactive user experience
- jQuery - used in conjunction with Javascript to create an interactive user experience
- Bootstrap - used for quick, responsive styling 
- Font Awesome - Used for icons
- Google Fonts - Used for website typography
- Unsplash - used for free stock photos

## Testing

#### Manual Testing:

##### Found Bugs/Errors:

1. Matching names for user uploaded images
   - I resolved this issue by renaming everyfile as it gets uploaded using UUID to generate a unique id for the image to ensure every user gets the images they uploaded
2. Database structure
   - My initial thought was to just add workouts to the users existing document in MongoDB. That seemed to clutter up the database a bit, I created a second collection for workouts alone which takes the user id of the active user making it easy to call the information and declutters the database.
3. Heroku 
   - Heroku created a number of bugs for me to resolve, typically due to my inexperience with using Heroku, but most issues were resolved with rolling back to a previous verison and restarting the process of pushing files over. 
3. Peer review in Code Institute Slack Channel
   - Used the peer review Slack channel to have student/alumni/mentors review the site and give feedback and look for bugs
   - There was one major issue caught:
      - I accidently uploaded my config file to Github exposing all my secret keys and database information. I quickly resolved this and changed all passwords and keys 
4. Mentor review
   - Overall positive feedback from my mentor, Moosa Hassan, but he did suggest adding more sports to the drop down options 
   
#### Device/Browser Testing

1. Used Chrome Dev tools to test the responsiveness of this project on multiple devices
2. Check browser compatibility in Firefox, Chrome, and Safari

## Database Structure

<details>
<summary>Database Structure</summary>
<br />
   <img alt="Db Structure" src="https://github.com/pmarre/fitness-tracker/blob/master/static/images/db_structure.png">
</details>

## Deployment

#### Local Deployment

To create a local copy of this repository, follow these steps:

1. Go to my [repo](https://github.com/pmarre/scratch/)
2. Click the "Clone or Download" button on the top-right of the page
3. Click the copy icon to copy the HTTPS link
4. Open terminal
5. Change the current directory to the location where the cloned directory will be made
6. Type `git clone <cloned URL>` with the cloned URL being the URL you copied in step 3 and run the command

For more information check out GitHub's guide to cloning a repo [here](https://help.github.com/en/github/creating-cloning-and-archiving-repositories/cloning-a-repository).

#### Deploy to Heroku

Detailed instructions for deploying to Heroku can be found [here](https://devcenter.heroku.com/articles/getting-started-with-python?singlepage=true)

