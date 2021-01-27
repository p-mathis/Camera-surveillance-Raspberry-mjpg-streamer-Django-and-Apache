---
title: "disposition.css"
date: 2021-01-24T11:45:53+01:00
draft: false
---

```css
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
  background-color: #ffdf9f9;
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
  background-color: #fdf9f9);
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
```
