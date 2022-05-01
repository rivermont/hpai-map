# 2022 HPAI Map

This project is an interactive map of avian influenza reports from the 2022 outbreak, intended as a supplement for [this NPR article](https://www.npr.org/2022/04/06/1091061758/bird-flu-outbreak).
It uses the [LeafletJS](https://leafletjs.com) library to visualize data from the United States Department of Agriculture (USDA).
Two datasets are shown: reports from wild birds and reports from captive flocks.

A Python script downloads the data and processes it to produce GeoJSON files containing the counties where avian flu was reported.
The script combines the USDA data with GeoJSON files from the Census Bureau.
Every morning at 1am EST the script runs to pull the latest reports from USDA, which typically posts 3-5 new reports each day.
It's theoretically possible to do all the data processing in JS in the browser, but that would be much slower for the user.

### Future improvements
In the future it would be nice to implement the following features:
* Toggle between displaying number of reports and number of birds
* Display popup with all information when both layers are visible
* Dynamic timeline
* Mobile support

