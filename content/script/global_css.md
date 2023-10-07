/* pour les fontes en fonction du type d'élément */
p {
    font-size: 18px;
    }
  
pre {
    font-size: 18px;
    color: #8A104D;
    }
  
h1 {
    font-size: 44px;
    color: #8A104D;
  
    }
  
.monh1 {
    font-size: 25px;
    color: #8A104D;
    text-align: left;
    }
  
.monh2 {
    font-size:16px;
    color: #8A104D;
    text-align: left;
    font-weight: bold;
  
    }
  
    /* traitement des images : centrer, ajuster... */
.centre-image {
    display: block;
    margin-left: auto;
    margin-right: auto;
  }
  
.imgresponsive {
    width: 100%;
    max-width: 750px;
    height: auto;
  }
.imgLogo {
    width: 150px;
    margin-right: 20px;
  }
.imgSmall {
    width: 100%;
    max-width: 200px;
    height: auto;
  }
  
  
  /* Pour centrer tableau */
  
figcaption {
    font-size: 11px;
    text-align: left;
    vertical-align: bottom;
  }
  
  /* pour des containers selon le texte à disposer */
  
.grid-One {
    display: grid;
    grid-template-columns: 400px;
    grid-gap: 10px;
    /* background-color: #2196F3; */
    padding: 10px; 
  }
.grid-One > div {
    text-align: center;
    font-size: 16px;
    color: #8A104D;
    font-weight: bold;
  }
  
  
.grid-Three {
    display: grid;
    grid-template-columns: 100px 100px 100px;
    grid-gap: 10px;
    padding: 10px;
  }
.grid-Three > div {
    text-align: center;
    font-size: 16px;
    color: #8A104D;
    font-weight: bold;
  }
  
@media screen and (max-width: 600px) {
      /* For mobile phones: */
      .monh1 {
        font-size : 32px;
      }
      .monp {
        font-size : 18px;
      }
    
      p {
        font-size: 11px;
      }
    
      .grid-container {
        display: grid;
        grid-template-columns: 1fr;
        width: 100%;
      }
    }

/* boutons */
.button {
    display: table-cell;
    background-color: #8A104D;
    border: none;
    color: white;
    padding: 12px 12px;
    text-align: center;
    vertical-align: middle;
    text-decoration: none;
    display: inline-block;
    font-size: 15px;
    font-family: var(--main-ft-family);
    margin-bottom: 10px;
    margin-top: 10px;
    margin-left: 100px;
    cursor: pointer;
    width: 200px;
    height: 40px;  
  }
  
  .buttonLigne {
    background-color: #8A104D;
    border: none;
    color: white;
    /* padding: 12px 12px; */
    padding: 6px;
    text-align: center;
    vertical-align: middle;
    text-decoration: none;
    display: inline-block;
    font-size: 15px;
    font-family: var(--main-ft-family);
    margin-bottom: 10px;
    margin-top: 12px;
    margin-left: 8px;
    cursor: pointer;
    width: 200px;
    height: 35px;  
  }

  /* disposition */
  :root {
    --main-bg-color: #f5efe0;
    --main-bg-color2: #4A4A4A;
    --main-bg-color3: #EAEAEA;
  
    --main-ft-family: 'Pacifico';
    --main-ft-size: 16px;
    --main-color: #cd2653;
    --main-color2: #a21e42;
  }
  
  * {
    box-sizing: border-box;
  }
  
  body {
    background-color: #fdf9f9;
  }
  
  .row:after{
    content: "";
    display: table;
    clear: both;
  }
  /* pour avoir deux colonnes (notamment pour les photos doubles) */
  .column2{
    float: left;
    width: 50%;
    padding: 10px;
  }
  
  .grid-container {
    display: grid;
    grid-template-columns: 1fr;
  }
  
  .item_menu {
    grid-row: 1 ;
    grid-column: 1 / 2;
    background-color: #fdf9f9;
  }
  
  .item_header {
    grid-row: 2;
    grid-column: 1 / 2;
    background-color: #fdf9f9;
    padding: 15px;
    text-align: center;
    font-size: 20px;
    font-family: var(--main-ft-family);
  }
  
  .item_main {
    grid-row: 3;
    grid-column: 1 / 2;
    background-color: #fdf9f9;
    font-family: var(--main-ft-family);
  }
  
  .item_footer {
    /* grid-row: 4;
    grid-column: 1 / 2; */
    text-align: left;
    /* background: var(--main-bg-color4); */
    color: #8A104D;
  
    font-size: 14px;
    font-family: var(--main-ft-family);
    /* padding: 40px; */
    vertical-align: middle;
    margin-top: 25px;
    margin-left: 100px;
  }

  /* header footer */
  .header {
    background-color: #8A104D;
    color: var(--main-color);
    padding: 15px;
    text-align: center;
    font-size: 25px;
  }
  
  .footer {
  text-align: left;
  background: var(--main-bg-color);
  color:#8A104D;
  font-size: 12px;
  /* position: fixed; */
  margin-top: 54px;
  margin-left: 100px;
  /* left:80px; */
  bottom:0px;
  height:54px;
  width: 100%;
  }

  /* navigation menu */
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

/* pagination */
.pagination a {
    color: white;
    float: left;
    /* padding: 8px 16px; */
    padding: 5px;
    font-family: var(--main-ft-family);
    text-decoration: none;
    margin-bottom: 8px;
    }
  
  .liActive {
    background-color: #aaa;
  }
  
  
  .spanPage {
    display: block;
    /* padding: 8px 16px; */
    margin-left: 40px;
    margin-top: 40px;
    color:  #8A104D;
   }
  
  .pagination a:hover:not(.active) {
    background-color: gray;
    color:#8A104D;
  }
  
  .pagination li {
    display: inline;
  }
  
  .pagination a:not(active) {
  background-color: #8A104D;
  }
  
  .pagination a:active {
    background-color: #aaa;
  }
