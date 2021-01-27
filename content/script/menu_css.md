---
title: "menu.css"
date: 2021-01-24T11:45:42+01:00
draft: false
---

```css
.navbar ul {
  list-style-type: none;
  margin: 0;
  padding: 0;
  overflow: hidden;
  background-color: #8A104D;
}

.navbar li {
  float: left;
}
.navbar li a{
  display: block;
  text-align: center;
  padding: 14px 16px;
  text-decoration: none;
  font-size:18px;
  font-weight: bold;
  color: #bebebe;
  background-color: #8A104D;
  
}

.icon {
  display:none;
}
.icon:hover{
  color : pink;
}

.dropbtn {
  display: inline-block;
  color: green;
  text-align: left;
  padding: 14px 16px;
  text-decoration: none;
}

.navbar li a:hover, .dropdown:hover .dropbtn {
  background-color: #A6A6A6;
  color: white;
}

.dropdown-content {
  display: none;
  position: absolute;
  background-color: #505050;
  min-width: 100px;
  box-shadow: 0px 8px 8px 0px rgba(0,0,0,0.2);
  z-index: 10;
}

.dropdown .dropdown-content a{
  /* color: green; */
  padding: 8px 8px;
  text-decoration: none;
  /* display: block; */
  text-align: left;
}

.dropdown-content a:hover {background-color: blue;}

.dropdown:hover .dropdown-content {
  display: block;
}

.dropdown >a::after{
   content: "▼";
   font-size: 15px;
 }


 @media screen and (max-width: 600px) {
   /* For mobile phones: */
   .navbar li:not(:first-child) {
     display: none;
   }
   .navbar .icon {
     float: right;
     display: block;
   }
 }

 @media screen and (max-width: 600px) {
   .navbar.responsive {position: relative;}
   .navbar.responsive .icon {
     position: absolute;
     right: 0;
     top: 0;
   }
   .navbar.responsive li {
     float: none;
     display: block;
     text-align: left;
   }

 }
```
