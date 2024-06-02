# Priority Task Script – Tableau Server
Interacting with Tableau Server through a Python RPA script since no API is available.  

## 1 Scope
Change the priority tasks (extract refreshes).

## 2 How it works
We exploit the Python library Selenium to map a few clicks in each extract refresh content page.

## 3 Extracting priority tasks information
Before starting with the Python script, we need to extract the information about the priority tasks in the Postgres metadata of Tableau Server through an SQL code.
