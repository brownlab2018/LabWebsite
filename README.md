# The Brown STM Lab | Website Code

This website is the central hub for every STM image our lab has ever acquired regardless of its quality. It is our intention to maintain full transparency with how our data is collected and processed, with that being said every image seen here is automatically generated from the raw data found in the orginial RHK .sm4 file.

In order for the image to be viewable the raw data automatically undergoes a plane subtract to generate the “_ps.png” image and an x-offset filter, which is a high-pass filter in the fast-scan direction, to generate the “_xo.png” image.

This website was developed using Django 3.1.4 to handle the bulk of the functionality, Heroku to host the site, and Amazon AWS S3 as a third-party file storage system.

A huge amount of credit goes to **S. Alex Kandel** from the University of Notre Dame, this website was modeled after the **The Kandel Group Image Gallery**. The ability to parse data from the .sm4 file format would not be possible without the code from Alex Kandel, the read_sm4 function was only slightly modified to work with a newer version of Python and Django.
