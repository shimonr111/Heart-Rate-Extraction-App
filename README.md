# Heart Rate Extraction Application

## Overview
Welcome to Heart Rate Extraction Application, a client-server desktop application developed in Python for extracting heart rates from patients using recorded or live video. The application features a user-friendly UI to manage patient and user data, stored efficiently in JSON data files. The heart rate extraction process involves a sophisticated pipeline, outlined below.

## Pipeline for Heart Rate Extraction
1. Receiving video input
2. Locating the ROI which is the forhead using Haar Casced classifier
3. Addressing the green color channel from the ROI
4. Perform FFT on this values on the extracted data from section 3
5. Locate peaks in a particular frequency band, often between 0.75 Hz and 4 Hz, within the converted frequency domain using bandpass filter
6. Counting the peaks within the given time and frequency ranges (time range of 15-30 seconds)
7. Calculation of the pulse-The algorithm should determine the patient heart rate based on the recognized peaks
   
## References
Our development process and pipeline for extracting the pulse were influenced and guided by valuable insights from the following articles:

1.	Bush, I. (2016). Measuring Heart Rate from Video. Stanford Computer Science.
2.	Hill, B. L., Liu, X., McDuff, D. (2021). Beat-to-Beat Cardiac Pulse Rate Measurement From Video. University of California, Los Angeles.
3.	Lee, Y. C., Syakura, A., Khalil, M. A., Wu, C. H., Ding, Y. F., Wang, C. W. (September 2020). A real-time camera-based adaptive breathing monitoring system.
4.	Molinaro, N., Schena, E., Silvestri, S., Bonotti, F., Aguzzi, D., Viola, E., Buccolini, F., Massaroni, C. (February 2022). Contactless Vital Signs Monitoring From Videos Recorded With Digital Cameras: An Overview.
5.	Viola, P., Jones, M. (2001). Rapid Object Detection using a Boosted Cascade of Simple Features. Mitsubishi Electric Research Labs, Compaq CRL.
6.	Chen, X., Cheng, J., Song, R., Liu, Y., Ward, R., Wang, Z. J. (October 2019). Video-Based Heart Rate Measurement: Recent Advances and Future Prospects.
