---
title: "general.css"
date: 2021-01-24T11:39:10+01:00
draft: false
---

```css
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
```
