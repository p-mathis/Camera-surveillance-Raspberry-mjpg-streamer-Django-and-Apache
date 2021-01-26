---
title: "pagination.css"
date: 2021-01-24T11:46:27+01:00
draft: false
---

```css
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
```
